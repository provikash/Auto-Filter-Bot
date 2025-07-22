import logging
import re
import base64
from struct import pack
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError, OperationFailure 
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URL, SECOND_DATABASE_URL, DATABASE_NAME, COLLECTION_NAME, MAX_BTN

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name',)
        collection_name = COLLECTION_NAME

# Second database (optional)
SecondMedia = None
if SECOND_DATABASE_URL:
    second_client = AsyncIOMotorClient(SECOND_DATABASE_URL)
    second_db = second_client[DATABASE_NAME]
    second_instance = Instance.from_db(second_db)

    @second_instance.register
    class SecondMediaCls(Document):
        file_id = fields.StrField(attribute='_id')
        file_name = fields.StrField(required=True)
        file_size = fields.IntField(required=True)
        caption = fields.StrField(allow_none=True)
        class Meta:
             indexes = ('$file_name', )
             collection_name = COLLECTION_NAME
    SecondMedia = SecondMediaCls

def _clean_text(s):
    """Remove usernames and extra symbols for consistency."""
    return re.sub(r"@\w+|(_|\-|\.|\+)", " ", str(s or ''))

def _create_regex(query):
    """Build regex for filenames matching."""
    query = str(query or '').strip()
    if not query:
        return re.compile('.', re.IGNORECASE)
    if ' ' not in query:
        pattern = r'(\b|[\.\+\-_])' + re.escape(query) + r'(\b|[\.\+\-_])'
    else:
        pattern = re.escape(query).replace('\\ ', r'.*[\s\.\+\-_]')
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error:
        return re.compile('.', re.IGNORECASE)

async def save_file(media):
    """Save file to main DB, fallback to second DB on OperationFailure."""
    file_id = unpack_new_file_id(media.file_id)
    file_name = _clean_text(getattr(media, 'file_name', ''))
    file_caption = _clean_text(getattr(media, 'caption', ''))
    try:
        doc = Media(file_id=file_id, file_name=file_name, file_size=media.file_size, caption=file_caption)
    except ValidationError:
        logging.error(f'Saving Error - {file_name}')
        return 'err'
    try:
        await doc.commit()
        logging.info(f'Saved - {file_name}')
        return 'suc'
    except DuplicateKeyError:
        logging.debug(f'Already Saved - {file_name}')
        return 'dup'
    except OperationFailure:
        if SecondMedia:
            try:
                sec_doc = SecondMedia(file_id=file_id, file_name=file_name, file_size=media.file_size, caption=file_caption)
                await sec_doc.commit()
                logging.info(f'Saved to 2nd db - {file_name}')
                return 'suc'
            except DuplicateKeyError:
                logging.debug(f'Already in 2nd db - {file_name}')
                return 'dup'
    return 'err'

async def get_search_results(query, max_results=MAX_BTN, offset=0, lang=None):
    regex = _create_regex(query)
    filter_ = {'file_name': regex}
    # First db search
    results = [doc async for doc in Media.find(filter_)]
    # Second db search if set
    if SecondMedia:
        results += [doc async for doc in SecondMedia.find(filter_)]
    # Filter language if requested
    if lang:
        lang_files = [f for f in results if lang in f.file_name.lower()]
        total = len(lang_files)
        files = lang_files[offset:offset+max_results]
    else:
        total = len(results)
        files = results[offset:offset+max_results]
    next_offset = (offset + max_results) if (offset + max_results) < total else ''
    return files, next_offset, total

async def delete_files(query):
    regex = _create_regex(query)
    filter_ = {'file_name': regex}
    total = await Media.count_documents(filter_)
    return total, Media.find(filter_)

async def get_file_details(query):
    """Get first file matching the file_id."""
    filter_ = {'file_id': query}
    return await Media.find(filter_).to_list(length=1)

def encode_file_id(s: bytes) -> str:
    r, n = b"", 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")

def unpack_new_file_id(new_file_id):
    decoded = FileId.decode(new_file_id)
    return encode_file_id(pack("<iiqq", int(decoded.file_type), decoded.dc_id, decoded.media_id, decoded.access_hash))
    
