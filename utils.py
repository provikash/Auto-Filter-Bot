from pyrogram.errors import UserNotParticipant, FloodWait
from info import LONG_IMDB_DESCRIPTION, TIME_ZONE
from imdb import Cinemagoer
import asyncio
from pyrogram.types import InlineKeyboardButton
from pyrogram import enums
from datetime import datetime
from database.users_chats_db import db
from shortzy import Shortzy
import requests
import re
import pytz

imdb = Cinemagoer()

class temp:
    START_TIME = 0
    BANNED_USERS = set()
    BANNED_CHATS = set()
    ME = None
    CANCEL = False
    U_NAME = None
    B_NAME = None
    SETTINGS = {}
    VERIFICATIONS = {}
    FILES = {}
    USERS_CANCEL = False
    GROUPS_CANCEL = False
    BOT = None
    PREMIUM = {}

async def is_subscribed(bot, query, channels):
    """
    Check if user is subscribed to given channels.
    Returns list of InlineKeyboardButton join buttons for channels user is NOT member of.
    """
    buttons = []
    for channel_id in channels:
        try:
            chat = await bot.get_chat(int(channel_id))
            await bot.get_chat_member(channel_id, query.from_user.id)
        except UserNotParticipant:
            invite_link = getattr(chat, 'invite_link', None)
            if invite_link:
                buttons.append([InlineKeyboardButton(f'Join {chat.title}', url=invite_link)])
        except Exception:
            pass
    return buttons

def upload_to_gofile(file_path):
    """
    Upload a file to GoFile and return download page link or None on failure.
    """
    url = "https://store1.gofile.io/uploadFile"
    try:
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        data = response.json()
        if response.status_code == 200 and data.get("status") == "ok":
            return data["data"]["downloadPage"]
    except Exception:
        pass
    return None

async def get_poster(query, bulk=False, id=False, file=None):
    """
    Get movie poster and metadata from IMDb API.
    bulk: if True, returns search results list instead of single movie info
    id: if True, treat query as IMDb id
    """
    def list_to_str(k):
        if not k:
            return "N/A"
        if isinstance(k, str):
            return k
        return ', '.join(str(x) for x in k)

    if not id:
        query = query.strip().lower()
        title = query
        year = None

        # Extract year from query or file name
        year_match = re.findall(r'[1-2]\d{3}$', query)
        if year_match:
            year = year_match[0]
            title = query.replace(year, '').strip()
        elif file:
            year_match2 = re.findall(r'[1-2]\d{3}', file)
            if year_match2:
                year = year_match2[0]

        search_results = imdb.search_movie(title, results=10)
        if not search_results:
            return None

        if year:
            filtered = [m for m in search_results if str(m.get('year')) == str(year)]
            filtered = filtered or search_results
        else:
            filtered = search_results

        filtered = [m for m in filtered if m.get('kind') in ['movie', 'tv series']] or filtered

        if bulk:
            return filtered

        imdb_id = filtered[0].movieID
    else:
        imdb_id = query

    movie = imdb.get_movie(imdb_id)

    date = movie.get("original air date") or movie.get("year") or "N/A"
    if not LONG_IMDB_DESCRIPTION:
        plot = movie.get('plot', [])
        plot = plot[0] if plot else ""
    else:
        plot = movie.get('plot outline', "")

    if plot and len(plot) > 800:
        plot = plot[:800] + "..."

    return {
        'title': movie.get('title'),
        'votes': movie.get('votes'),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get('box office'),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_str(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_str(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer": list_to_str(movie.get("writer")),
        "producer": list_to_str(movie.get("producer")),
        "composer": list_to_str(movie.get("composer")),
        "cinematographer": list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_str(movie.get("genres")),
        'poster': movie.get('full-size cover url'),
        'plot': plot,
        'rating': str(movie.get("rating")),
        'url': f'https://www.imdb.com/title/tt{imdb_id}'
    }

async def is_check_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except Exception:
        return False

async def get_verify_status(user_id):
    verify = temp.VERIFICATIONS.get(user_id)
    if verify is None:
        verify = await db.get_verify_status(user_id)
        temp.VERIFICATIONS[user_id] = verify
    return verify

async def update_verify_status(user_id, verify_token="", is_verified=False, link="", expire_time=0):
    current = await get_verify_status(user_id)
    current.update({
        'verify_token': verify_token,
        'is_verified': is_verified,
        'link': link,
        'expire_time': expire_time
    })
    temp.VERIFICATIONS[user_id] = current
    await db.update_verify_status(user_id, current)

async def broadcast_messages(user_id, message, pin):
    try:
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, pin)
    except Exception:
        await db.delete_user(int(user_id))
        return "Error"

async def groups_broadcast_messages(chat_id, message, pin):
    try:
        m = await message.copy(chat_id=chat_id)
        if pin:
            try:
                await m.pin()
            except Exception:
                pass
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await groups_broadcast_messages(chat_id, message, pin)
    except Exception:
        await db.delete_chat(chat_id)
        return "Error"

async def get_settings(group_id):
    settings = temp.SETTINGS.get(group_id)
    if settings is None:
        settings = await db.get_settings(group_id)
        temp.SETTINGS[group_id] = settings
    return settings

async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value
    temp.SETTINGS[group_id] = current
    await db.update_settings(group_id, current)

def get_size(size):
    """
    Convert bytes to human-readable string (e.g. 1.23 MB)
    """
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024 and i < len(units)-1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"

def list_to_str(l):
    """
    Convert list-like to comma-separated string or 'N/A' if empty or None.
    """
    if not l:
        return "N/A"
    if isinstance(l, str):
        return l
    return ', '.join(str(i) for i in l)

async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    return await shortzy.convert(link)

def get_readable_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for name, count in periods:
        if seconds >= count:
            value, seconds = divmod(seconds, count)
            result += f'{int(value)}{name}'
    return result

def get_wish():
    now_hour = datetime.now(TIME_ZONE).hour
    if now_hour < 12:
        return "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 🌞"
    elif now_hour < 18:
        return "ɢᴏᴏᴅ ᴀꜰᴛᴇʀɴᴏᴏɴ 🌗"
    else:
        return "ɢᴏᴏᴅ ᴇᴠᴇɴɪɴɢ 🌘"

async def get_seconds(time_string):
    """
    Parses a time string like '10min' or '1hour' and converts to seconds.
    """
    match = re.match(r'(\d+)([a-zA-Z]+)', time_string.strip())
    if not match:
        return 0

    value, unit = int(match.group(1)), match.group(2).lower()
    units_map = {
        's': 1,
        'sec': 1,
        'second': 1,
        'seconds':1,
        'min': 60,
        'minute': 60,
        'minutes': 60,
        'hour': 3600,
        'hours': 3600,
        'day': 86400,
        'days': 86400,
        'month': 2592000,  # 30 days
        'months': 2592000,
        'year': 31536000,
        'years': 31536000
    }
    return value * units_map.get(unit, 0)
            
