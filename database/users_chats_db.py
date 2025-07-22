from motor.motor_asyncio import AsyncIOMotorClient
from info import (
    TIME_ZONE, ADMINS, DATABASE_NAME, DATABASE_URL, FORCE_SUB_CHANNELS, IMDB_TEMPLATE,
    WELCOME_TEXT, LINK_MODE, TUTORIAL, SHORTLINK_URL, SHORTLINK_API, SHORTLINK, FILE_CAPTION,
    IMDB, WELCOME, SPELL_CHECK, PROTECT_CONTENT, AUTO_FILTER, AUTO_DELETE, IS_STREAM, VERIFY_EXPIRE
)
import datetime

client = AsyncIOMotorClient(DATABASE_URL)
mydb = client[DATABASE_NAME]

class Database:
    default_settings = {
        'auto_filter': AUTO_FILTER,
        'file_secure': PROTECT_CONTENT,
        'imdb': IMDB,
        'spell_check': SPELL_CHECK,
        'auto_delete': AUTO_DELETE,
        'welcome': WELCOME,
        'welcome_text': WELCOME_TEXT,
        'template': IMDB_TEMPLATE,
        'caption': FILE_CAPTION,
        'url': SHORTLINK_URL,
        'api': SHORTLINK_API,
        'shortlink': SHORTLINK,
        'tutorial': TUTORIAL,
        'links': LINK_MODE,
        'fsub': FORCE_SUB_CHANNELS,
        'is_stream': IS_STREAM
    }

    default_verify = {
        'is_verified': False,
        'verified_time': 0,
        'verify_token': "",
        'link': "",
        'expire_time': 0
    }
    
    def __init__(self):
        self.col = mydb.Users
        self.grp = mydb.Groups
        self.prm_users = mydb.Premium_Users

    @staticmethod
    def new_user(id, name):
        return dict(
            id=id,
            name=name,
            ban_status={'is_banned': False, 'ban_reason': ''},
            verify_status=Database.default_verify.copy()
        )

    @staticmethod
    def new_group(id, title):
        return dict(
            id=id,
            title=title,
            chat_status={'is_disabled': False, 'reason': ''},
            settings=Database.default_settings.copy()
        )
    
    async def add_user(self, id, name):
        await self.col.insert_one(self.new_user(id, name))
    
    async def is_user_exist(self, id):
        return bool(await self.col.find_one({'id': int(id)}))
    
    async def total_users_count(self):
        return await self.col.count_documents({})
    
    async def remove_ban(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'ban_status': {'is_banned': False, 'ban_reason': ''}}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'ban_status': {'is_banned': True, 'ban_reason': ban_reason}}})

    async def get_ban_status(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', {'is_banned': False, 'ban_reason': ''}) if user else {'is_banned': False, 'ban_reason': ''}

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def delete_chat(self, grp_id):
        await self.grp.delete_many({'id': int(grp_id)})

    async def get_banned(self):
        chats_cursor = self.grp.find({'chat_status.is_disabled': True})
        users_cursor = self.col.find({'ban_status.is_banned': True})
        b_chats = [chat['id'] async for chat in chats_cursor]
        b_users = [user['id'] async for user in users_cursor]
        return b_users, b_chats
    
    async def add_chat(self, chat_id, title):
        await self.grp.insert_one(self.new_group(chat_id, title))

    async def get_chat(self, chat_id):
        chat = await self.grp.find_one({'id': int(chat_id)})
        return chat.get('chat_status') if chat else False
    
    async def re_enable_chat(self, chat_id):
        await self.grp.update_one({'id': int(chat_id)}, {'$set': {'chat_status': {'is_disabled': False, 'reason': ""}}})
        
    async def update_settings(self, chat_id, settings):
        await self.grp.update_one({'id': int(chat_id)}, {'$set': {'settings': settings}})
    
    async def get_settings(self, chat_id):
        chat = await self.grp.find_one({'id': int(chat_id)})
        return chat.get('settings', self.default_settings) if chat else self.default_settings.copy()
    
    async def disable_chat(self, chat_id, reason="No Reason"):
        await self.grp.update_one({'id': int(chat_id)}, {'$set': {'chat_status': {'is_disabled': True, 'reason': reason}}})

    async def get_verify_status(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        info = user.get('verify_status', self.default_verify.copy()) if user else self.default_verify.copy()
        # Ensure always have 'expire_time'
        if not info.get('expire_time'):
            expire = info.get('verified_time', 0)
            try:  # If stored as int
                expire = int(expire)
            except Exception:
                expire = 0
            info['expire_time'] = expire + VERIFY_EXPIRE
        return info
        
    async def update_verify_status(self, user_id, verify):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'verify_status': verify}})
    
    async def total_chat_count(self):
        return await self.grp.count_documents({})
    
    async def get_all_chats(self):
        return self.grp.find({})
    
    async def get_db_size(self):
        stats = await mydb.command("dbstats")
        return stats['dataSize']
   
    async def get_all_chats_count(self):  # Redundant with total_chat_count, kept for compatibility
        return await self.grp.count_documents({})
        
db = Database()
        
