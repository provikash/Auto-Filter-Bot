import math
import secrets
import mimetypes
from info import BIN_CHANNEL
from utils import temp
from aiohttp import web
from web.utils.custom_dl import TGCustomYield, chunk_size, offset_fix
from web.utils.render_template import media_watch

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(
        text='<h1 align="center"><a href="https://t.me/HA_Bots"><b>HA Bots</b></a></h1>',
        content_type='text/html'
    )

@routes.get("/watch/{message_id}")
async def watch_handler(request):
    try:
        message_id = int(request.match_info['message_id'])
        html = await media_watch(message_id)
    except Exception:
        html = "<h1>Something went wrong</h1>"
    return web.Response(text=html, content_type='text/html')

@routes.get("/download/{message_id}")
async def download_handler(request):
    try:
        message_id = int(request.match_info['message_id'])
        return await media_download(request, message_id)
    except Exception:
        return web.Response(text="<h1>Something went wrong</h1>", content_type='text/html')

async def media_download(request, message_id: int):
    try:
        # Get Telegram media message and properties
        media_msg = await temp.BOT.get_messages(BIN_CHANNEL, message_id)
        file_props = await TGCustomYield().generate_file_properties(media_msg)
        file_size = file_props.file_size
        file_name = file_props.file_name or f"{secrets.token_hex(2)}.jpeg"
        mime_type = file_props.mime_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        # Determine requested range for partial download support
        range_header = request.headers.get('Range')
        if range_header:
            from_bytes, _, until_bytes = range_header.replace('bytes=', '').partition('-')
            from_bytes = int(from_bytes) if from_bytes else 0
            until_bytes = int(until_bytes) if until_bytes else file_size - 1
        else:
            from_bytes = getattr(request.http_range, 'start', 0)
            until_bytes = getattr(request.http_range, 'stop', None)
            until_bytes = until_bytes if until_bytes is not None else file_size - 1

        req_length = until_bytes - from_bytes + 1
        new_chunk_size = await chunk_size(req_length)
        offset = await offset_fix(from_bytes, new_chunk_size)
        first_part_cut = from_bytes - offset
        last_part_cut = (until_bytes % new_chunk_size) + 1
        part_count = math.ceil(req_length / new_chunk_size)

        body = TGCustomYield().yield_file(
            media_msg, offset, first_part_cut, last_part_cut, part_count, new_chunk_size
        )

        status = 206 if range_header else 200
        headers = {
            "Content-Type": mime_type,
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        }
        # Add Content-Length for full downloads
        if status == 200:
            headers["Content-Length"] = str(file_size)

        return web.Response(status=status, body=body, headers=headers)

    except Exception:
        return web.Response(text="<h1>Something went wrong</h1>", content_type='text/html')
        
