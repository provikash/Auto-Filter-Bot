class script(object):

    START_TXT = (
        "<b>ʜᴇʏ {}, <i>{}</i>\n\n"
        "ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴡɪᴛʜ ʟɪɴᴋ sʜᴏʀᴛᴇɴᴇʀ ʙᴏᴛ. ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴀꜱ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴡɪᴛʜ ʟɪɴᴋ sʜᴏʀᴛᴇɴᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ... "
        "ɪᴛ'ꜱ ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇʀᴇ ᴍᴏᴠɪᴇꜱ ᴡɪᴛʜ ʏᴏᴜʀ ʟɪɴᴋ ꜱʜᴏʀᴛᴇɴᴇʀ... ♻️</b>"
    )

    MY_ABOUT_TXT = (
        "★ Server: <a href=https://www.heroku.com>Heroku</a>\n"
        "★ Database: <a href=https://www.mongodb.com>MongoDB</a>\n"
        "★ Language: <a href=https://www.python.org>Python</a>\n"
        "★ Library: <a href=https://pyrogram.org>Pyrogram</a>"
    )

    MY_OWNER_TXT = (
        "★ Name: Bots\n"
        "★ Username:\n"
        "★ Country:"
    )

    STATUS_TXT = (
        "🗂 Total Files: <code>{}</code>\n"
        "👤 Total Users: <code>{}</code>\n"
        "👥 Total Chats: <code>{}</code>\n"
        "✨ Used Storage: <code>{}</code>\n"
        "🗳 Free Storage: <code>{}</code>\n"
        "🚀 Bot Uptime: <code>{}</code>"
    )

    NEW_GROUP_TXT = (
        "#NewGroup\n"
        "Title - {}\n"
        "ID - <code>{}</code>\n"
        "Username - {}\n"
        "Total - <code>{}</code>"
    )

    NEW_USER_TXT = (
        "#NewUser\n"
        "★ Name: {}\n"
        "★ ID: <code>{}</code>"
    )

    NOT_FILE_TXT = (
        "👋 Hello {},\n\n"
        "I can't find the <b>{}</b> in my database! 🥲\n\n"
        "👉 Google Search and check your spelling is correct.\n"
        "👉 Please read the Instructions to get better results.\n"
        "👉 Or not been released yet."
    )
    
    EARN_TXT = (
        "<b>ʜᴏᴡ ᴛᴏ ᴇᴀʀɴ ꜰʀᴏᴍ ᴛʜɪs ʙᴏᴛ\n\n"
        "➥ ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴇᴀʀɴ ᴍᴏɴᴇʏ ʙʏ ᴜsɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n\n"
        "» sᴛᴇᴘ 1:- ғɪʀsᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴ.\n\n"
        "» sᴛᴇᴘ 2:- ᴍᴀᴋᴇ ᴀᴄᴄᴏᴜɴᴛ ᴏɴ <a href=https://telegram.me/how_to_download_channel/14>mdisklink.link</a>"
        " [ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴜsᴇ ᴏᴛʜᴇʀ sʜᴏʀᴛɴᴇʀ ᴡᴇʙsɪᴛᴇ ]\n\n"
        "» sᴛᴇᴘ 3:- ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ɢɪᴠᴇɴ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ.\n\n"
        "➥ ᴛʜɪꜱ ʙᴏᴛ ɪs ꜰʀᴇᴇ ꜰᴏʀ ᴀʟʟ, ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ғᴏʀ ꜰʀᴇᴇ ᴏꜰ ᴄᴏꜱᴛ.</b>"
    )

    HOW_TXT = (
        "<b>ʜᴏᴡ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴏᴡɴ sʜᴏʀᴛɴᴇʀ ‼️\n\n"
        "➥ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴏᴡɴ sʜᴏʀᴛɴᴇʀ ᴛʜᴇɴ ᴊᴜsᴛ sᴇɴᴅ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴇᴛᴀɪʟs ɪɴ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n\n"
        "➥ ғᴏʀᴍᴀᴛ ↓↓↓\n\n"
        "<code>/set_shortlink sʜᴏʀᴛɴᴇʀ sɪᴛᴇ sʜᴏʀᴛɴᴇʀ ᴀᴘɪ</code>\n\n"
        "➥ ᴇxᴀᴍᴘʟᴇ ↓↓↓\n\n"
        "<code>/set_shortlink mdisklink.link 5843c3cc645f5077b2200a2c77e0344879880b3e</code>\n\n"
        "➥ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜɪᴄʜ sʜᴏʀᴛᴇɴᴇʀ ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛʜᴇɴ sᴇɴᴅ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ /get_shortlink\n\n"
        "📝 ɴᴏᴛᴇ:- ʏᴏᴜ sʜᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ɪɴ ɢʀᴏᴜᴘ. "
        "sᴇɴᴅ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜᴏᴜᴛ ʙᴇɪɴɢ ᴀɴ ᴀɴᴏɴʏᴍᴜs ᴀᴅᴍɪɴ.</b>"
    )

    IMDB_TEMPLATE = (
        "✅ I Found: <code>{query}</code>\n\n"
        "🏷 Title: <a href={url}>{title}</a>\n"
        "🎭 Genres: {genres}\n"
        "📆 Year: <a href={url}/releaseinfo>{year}</a>\n"
        "🌟 Rating: <a href={url}/ratings>{rating} / 10</a>\n"
        "☀️ Languages: {languages}\n"
        "📀 RunTime: {runtime} Minutes\n\n"
        "🗣 Requested by: {message.from_user.mention}"
    )

    FILE_CAPTION = (
        "<i>{file_name}</i>\n\n"
        "🚫 ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴄʟᴏsᴇ ʙᴜᴛᴛᴏɴ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴇɴ ᴛʜᴇ ᴍᴏᴠɪᴇ 🚫"
    )

    WELCOME_TEXT = "👋 Hello {mention}, Welcome to {title} group! 💞"

    HELP_TXT = "<b>Note - <spoiler>Try each command without any argument to see more details 😹</spoiler></b>"

    ADMIN_COMMAND_TXT = (
        "<b>Here is bot admin commands 👇\n\n"
        "/index_channels - to check how many index channel id added\n"
        "/stats - to get bot status\n"
        "/delete - to delete files using query\n"
        "/delete_all - to delete all indexed file\n"
        "/broadcast - to send message to all bot users\n"
        "/grp_broadcast - to send message to all groups\n"
        "/pin_broadcast - to send message as pin to all bot users.\n"
        "/pin_grp_broadcast - to send message as pin to all groups.\n"
        "/restart - to restart bot\n"
        "/leave - to leave your bot from particular group\n"
        "/unban_grp - to enable group\n"
        "/ban_grp - to disable group\n"
        "/ban_user - to ban a users from bot\n"
        "/unban_user - to unban a users from bot\n"
        "/users - to get all users details\n"
        "/chats - to get all groups\n"
        "/invite_link - to generate invite link\n"
        "/index - to index bot accessible channels</b>"
    )

    USER_COMMAND_TXT = (
        "<b>Here is bot user commands 👇\n\n"
        "/start - to check bot alive or not\n"
        "/gofile - upload file to gofile.io\n"
        "/settings - to change group settings as your wish\n"
        "/set_template - to set custom imdb template\n"
        "/set_caption - to set custom bot files caption\n"
        "/set_shortlink - group admin can set custom shortlink\n"
        "/get_custom_settings - to get your group settings details\n"
        "/set_welcome - to set custom new joined users welcome message for group\n"
        "/set_tutorial - to set custom tutorial link in result page button\n"
        "/id - to check group or channel id\n"
        "/set_fsub - to set force subscribe channels\n"
        "/remove_fsub - to remove all force subscribe channel</b>"
    )
    
