import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, Photo, Document
from .database import collection
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo
import telegraph

# Add Movie to database
@Client.on_message(filters.chat(ADMINS) & filters.media)
async def web_db(c: Client, m: Message):
    if m.media:
        message = m.caption

        # Save the image file locally
        file_path = await c.download_media(m)

        id = collection.insert_one(
            {"caption": message.html,
             "title": message.splitlines()[0],
             "image_path": file_path}
        )

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Delete", callback_data=f"delete#{id.inserted_id}")]
            ]
        )

        txt = await m.reply("Added Successfully", reply_markup=reply_markup)

    else:
        txt = await m.reply("Something went wrong")

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await m.delete()
        await txt.delete()

            
