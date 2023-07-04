from translation import *
from pyrogram import Client, filters
from plugins.groups import group_send_handler
from plugins.database import collection
from pymongo import TEXT
from config import START_MSG, HOWTO, OWNER_USERNAME, GROUP, BOT_USERNAME, FILEBOT, START_PIC
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)

@Client.on_message(filters.command('start'))
async def start_message(c,m):
    collection.create_index([("title" , TEXT),("caption", TEXT)],name="movie_index")
    if len(m.command) == 1:
        return await m.reply_photo(f"{START_PIC}",
            caption=START_MSG,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('❤ Movie group', url='https://t.me/Filmy_Fundas')
                    ], 
                    [
                        InlineKeyboardButton("𝙼𝚘𝚟𝚒𝚎 𝙲𝚑𝚊𝚗𝚗𝚊𝚕", url="https://t.me/one_file"),
                        InlineKeyboardButton("ɢʀᴏᴜᴘ", url=f'https://t.me/{GROUP}')
                    ]
                ]
            )
        )
    else:
        return await group_send_handler(c,m)
