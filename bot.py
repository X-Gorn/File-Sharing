import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
TRACK_CHANNEL = int(os.environ['TRACK_CHANNEL'])
OWNER_ID = os.environ['OWNER_ID']

#Button
START_BUTTONS=[
    [
        InlineKeyboardButton('Source', url='https://github.com/X-Gorn/File-Sharing'),
        InlineKeyboardButton('Project Channel', url='https://t.me/xTeamBots'),
    ],
    [InlineKeyboardButton('Author', url="https://t.me/xgorn")],
]

# Running bot
xbot = Client('File-Sharing', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start & Get file
@xbot.on_message(filters.command('start') & filters.private)
async def _startfile(bot, update):
    if update.text == '/start':
        await update.reply_text(f"I'm File-Sharing!\nYou can share any telegram files and get the sharing link using this bot!\n\n/help for more details...", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))
        return
    up = await bot.get_messages(update.from_user.id, update.message_id)
    if len(update.command) != 2:
        return
    code = update.command[1]
    if '-' in code:
        unique_id, msg_id = code.split('-')
        if not msg_id.isdigit():
            return
        check = await bot.get_messages(TRACK_CHANNEL, int(msg_id))
        if check.empty:
            return
        if check.video:
            unique_idx = check.video.file_unique_id
        elif check.photo:
            unique_idx = check.photo.file_unique_id
        elif check.audio:
            unique_idx = check.audio.file_unique_id
        elif check.document:
            unique_idx = check.document.file_unique_id
        elif check.sticker:
            unique_idx = check.sticker.file_unique_id
        elif check.animation:
            unique_idx = check.animation.file_unique_id
        elif check.voice:
            unique_idx = check.voice.file_unique_id
        elif check.video_note:
            unique_idx = check.video_note.file_unique_id
        if unique_id != unique_idx.lower():
            return
        await check.copy(update.from_user.id)   
    else:
        return


# Help msg
@xbot.on_message(filters.command('help') & filters.private)
async def _help(bot, update):
    await update.reply_text("Supported file types:\n\n- Video\n- Audio\n- Photo\n- Document\n- Sticker\n- GIF\n- Voice note\n- Video note\n\n If bot didn't respond, contact @xgorn", True)


# Store file
@xbot.on_message(filters.media & filters.private)
async def _main(bot, update):
    if OWNER_ID == 'all':
        pass
    elif int(OWNER_ID) == update.from_user.id:
        pass
    else:
        return
    copied = await update.copy(TRACK_CHANNEL)
    if copied.video:
        unique_idx = copied.video.file_unique_id
        msg_id = copied.message_id
    elif copied.photo:
        unique_idx = copied.photo.file_unique_id
        msg_id = copied.message_id
    elif copied.audio:
        unique_idx = copied.audio.file_unique_id
        msg_id = copied.message_id
    elif copied.document:
        unique_idx = copied.document.file_unique_id
        msg_id = copied.message_id
    elif copied.sticker:
        unique_idx = copied.sticker.file_unique_id
        msg_id = copied.message_id
    elif copied.animation:
        unique_idx = copied.animation.file_unique_id
        msg_id = copied.message_id
    elif copied.voice:
        unique_idx = copied.voice.file_unique_id
        msg_id = copied.message_id
    elif copied.video_note:
        unique_id = copied.video_note.file_unique_id
        msg_id = copied.message_id
    else:
        await copied.delete()
        return
    me = await bot.get_me()
    await update.reply_text(
        'Here is Your Sharing Link:', 
        True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Sharing Link', url=f'https://t.me/{me.username}?start={unique_idx.lower()}-{str(msg_id)}')]
        ]) 
    )


xbot.run()
