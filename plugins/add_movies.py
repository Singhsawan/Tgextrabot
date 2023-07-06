
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import collection
from config import *
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import pymongo
from config import INDEXCHANNEL_ID

# Add Movie to database
@@Client.on_message(filters.chat(ADMINS + INDEXCHANNEL_ID) & filters.media)
async def web_db(c: Client, m: Message):
    if m.media:
        message = m.caption

        id = collection.insert_one(
            {"caption": message.html,
                'title': message.splitlines()[0]}
        )

        reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Delete", callback_data=f"delete#{id.inserted_id }")],
        ])

        txt = await m.reply('Added Successfully', reply_markup=reply_markup)

    else:
        txt = await m.reply('Something went wrong')
        
    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await m.delete()
        await txt.delete()


