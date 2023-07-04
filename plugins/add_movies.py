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
        media = m.media

        # Upload image to Telegraph and get the URL
        if isinstance(media, Photo):
            image_path = await c.download_media(media)
            telegraph_url = await c.create_telegraph_page(title='Image', content=[telegraph.File.from_path(image_path)])
        elif isinstance(media, Document):
            image_path = await c.download_media(media)
            telegraph_url = await c.create_telegraph_page(title='Document', content=[telegraph.File.from_path(image_path)])
        else:
            telegraph_url = None

        id = collection.insert_one({
            "caption": message.html,
            "title": message.splitlines()[0],
            "image_url": telegraph_url.url if telegraph_url else None
        })

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Delete", callback_data=f"delete#{id.inserted_id}")]
        ])

        txt = await m.reply('Added Successfully', reply_markup=reply_markup)
    else:
        txt = await m.reply('Something went wrong')

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await m.delete()
        await txt.delete()
            
