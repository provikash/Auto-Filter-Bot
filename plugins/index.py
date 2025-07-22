import re
import time
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from info import ADMINS, INDEX_EXTENSIONS
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp, get_readable_time

lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^index#'))
async def index_files(bot, query):
    _, ident, chat_id, lst_msg_id, skip = query.data.split("#")
    if ident == 'yes':
        msg = query.message
        await msg.edit("Starting Indexing...")
        try:
            chat_id = int(chat_id)
        except:
            pass
        await index_files_to_db(int(lst_msg_id), chat_id, msg, bot, int(skip))
    elif ident == 'cancel':
        temp.CANCEL = True
        await query.message.edit("Trying to cancel Indexing...")

@Client.on_message(filters.command('index') & filters.private & filters.user(ADMINS))
async def send_for_index(bot, message):
    if lock.locked():
        return await message.reply('Wait until previous process complete.')

    i = await message.reply("Forward last message or send last message link.")
    msg = await bot.listen(chat_id=message.chat.id, user_id=message.from_user.id)
    await i.delete()

    last_msg_id = None
    chat_id = None

    if msg.text and msg.text.startswith("https://t.me"):
        try:
            msg_link = msg.text.strip("/").split("/")
            last_msg_id = int(msg_link[-1])
            chat_id = msg_link[-2]
            if chat_id.lstrip('-').isdigit():
                chat_id = int(f"-100{chat_id.lstrip('-100')}")
        except Exception as e:
            return await message.reply('Invalid message link!')
    elif msg.forward_from_chat and msg.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = msg.forward_from_message_id
        chat_id = msg.forward_from_chat.id
    else:
        return await message.reply('This is not a forwarded message or valid link.')

    try:
        chat = await bot.get_chat(chat_id)
    except Exception as e:
        return await message.reply(f'Errors - {e}')

    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply("I can index only channels.")  

    s = await message.reply("Send skip message number.")  
    msg2 = await bot.listen(chat_id=message.chat.id, user_id=message.from_user.id)  
    await s.delete()  
    try:  
        skip = int(msg2.text)  
    except:  
        return await message.reply("Number is invalid.")  

    buttons = [
        [InlineKeyboardButton('YES', callback_data=f'index#yes#{chat_id}#{last_msg_id}#{skip}')],
        [InlineKeyboardButton('CLOSE', callback_data='close_data')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(
        f'Do you want to index <b>{chat.title}</b> channel?\nTotal Messages: <code>{last_msg_id}</code>',
        reply_markup=reply_markup
    )

async def index_files_to_db(lst_msg_id, chat_id, msg, bot, skip):
    start_time = time.time()
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    current = skip

    async with lock:
        try:
            async for message in bot.iter_messages(chat_id, lst_msg_id, offset_id=skip):
                time_taken = get_readable_time(time.time() - start_time)

                if temp.CANCEL:
                    temp.CANCEL = False
                    await msg.edit(
                        f"Successfully Cancelled!\nCompleted in {time_taken}\n\n"
                        f"Saved <code>{total_files}</code> files to Database!\n"
                        f"Duplicate Files Skipped: <code>{duplicate}</code>\n"
                        f"Deleted Messages Skipped: <code>{deleted}</code>\n"
                        f"Non-Media messages skipped: <code>{no_media + unsupported}</code>\n"
                        f"Unsupported Media: <code>{unsupported}</code>\n"
                        f"Errors Occurred: <code>{errors}</code>"
                    )
                    return

                current += 1

                if current % 30 == 0:
                    btn = [[InlineKeyboardButton('CANCEL', callback_data=f'index#cancel#{chat_id}#{lst_msg_id}#{skip}')]]
                    try:
                        await msg.edit_text(
                            text=(
                                f"Total messages received: <code>{current}</code>\n"
                                f"Total messages saved: <code>{total_files}</code>\n"
                                f"Duplicate Files Skipped: <code>{duplicate}</code>\n"
                                f"Deleted Messages Skipped: <code>{deleted}</code>\n"
                                f"Non-Media messages skipped: <code>{no_media + unsupported}</code>\n"
                                f"Unsupported Media: <code>{unsupported}</code>\n"
                                f"Errors Occurred: <code>{errors}</code>"
                            ),
                            reply_markup=InlineKeyboardMarkup(btn)
                        )
                    except FloodWait as e:
                        await asyncio.sleep(e.value)

                if getattr(message, 'empty', False):
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue

                media = getattr(message, message.media.value, None)
                if not media or not (str(getattr(media, 'file_name', '')).lower()).endswith(tuple(INDEX_EXTENSIONS)):
                    unsupported += 1
                    continue

                # Add original caption before saving
                setattr(media, 'caption', message.caption or '')

                sts = await save_file(media)
                if sts == 'suc':
                    total_files += 1
                elif sts == 'dup':
                    duplicate += 1
                elif sts == 'err':
                    errors += 1
        except Exception as e:
            await msg.reply(f'Index canceled due to Error - {e}')
        else:
            time_taken = get_readable_time(time.time() - start_time)
            await msg.edit(
                f'Successfully saved <code>{total_files}</code> to Database!\n'
                f'Completed in {time_taken}\n\n'
                f'Duplicate Files Skipped: <code>{duplicate}</code>\n'
                f'Deleted Messages Skipped: <code>{deleted}</code>\n'
                f'Non-Media messages skipped: <code>{no_media + unsupported}</code>\n'
                f'Unsupported Media: <code>{unsupported}</code>\n'
                f'Errors Occurred: <code>{errors}</code>'
            )
            
