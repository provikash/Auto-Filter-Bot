import os
import time
import asyncio
import uvloop

from pyrogram import Client, types
from pyrogram.errors import FloodWait
from aiohttp import web
from typing import Union, Optional, AsyncGenerator

from web import web_app
from info import (LOG_CHANNEL, API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL, 
                  ADMINS, SECOND_DATABASE_URL, DATABASE_URL)
from utils import temp, get_readable_time

from database.users_chats_db import db
from database.ia_filterdb import Media
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uvloop.install()


class Bot(Client):
    def __init__(self):
        super().__init__(
            name='Auto_Filter_Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )

    async def start(self):
        try:
            await super().start()
        except FloodWait as e:
            delay = e.value
            print(f"Warning - Flood Wait Occurred, Wait For: {get_readable_time(delay)}")
            await asyncio.sleep(delay)
            print("Info - Now Ready For Deploying!")

        temp.START_TIME = time.time()

        # Load banned users and chats into temp
        temp.BANNED_USERS, temp.BANNED_CHATS = await db.get_banned()

        # Verify DB connection(s)
        client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Info - Successfully connected to DATABASE_URL")
        except Exception:
            print("Error - Make sure DATABASE_URL is correct, exiting now")
            exit()

        if SECOND_DATABASE_URL:
            client2 = MongoClient(SECOND_DATABASE_URL, server_api=ServerApi('1'))
            try:
                client2.admin.command('ping')
                print("Info - Successfully connected to SECOND_DATABASE_URL")
            except Exception:
                print("Error - Make sure SECOND_DATABASE_URL is correct, exiting now")
                exit()

        # Handle bot restart notification
        if os.path.exists('restart.txt'):
            with open("restart.txt") as file:
                chat_id, msg_id = map(int, file.read().split())
            try:
                await self.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Restarted Successfully!')
            except Exception:
                pass
            os.remove('restart.txt')

        temp.BOT = self

        # Ensure indexes in Media collection
        await Media.ensure_indexes()

        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name

        print(f"{me.first_name} is started now 🤗")

        # Start aiohttp web app
        app_runner = web.AppRunner(web_app)
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()

        # Send startup messages
        try:
            await self.send_message(LOG_CHANNEL, f"<b>{me.mention} Restarted! 🤖</b>")
        except Exception:
            print("Error - Make sure bot admin in LOG_CHANNEL, exiting now")
            exit()

        try:
            test_msg = await self.send_message(BIN_CHANNEL, "Test")
            await test_msg.delete()
        except Exception:
            print("Error - Make sure bot admin in BIN_CHANNEL, exiting now")
            exit()

        for admin in ADMINS:
            try:
                await self.send_message(admin, "<b>✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ</b>")
            except Exception:
                print(f"Info - Admin ({admin}) not started this bot yet")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped! Bye...")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0
    ) -> Optional[AsyncGenerator[types.Message, None]]:
        """
        Iterates through messages in a chat from offset to limit sequentially.
        """
        current = offset
        while current < limit:
            chunk_size = min(200, limit - current)
            # +1 because range end is exclusive and to include last message
            message_ids = list(range(current, current + chunk_size))
            messages = await self.get_messages(chat_id, message_ids)
            for message in messages:
                yield message
                current += 1


if __name__ == "__main__":
    app = Bot()
    app.run()
    
