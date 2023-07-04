import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
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
        if isinstance(media, pyrogram.types.Photo):
            image_path = await c.download_media(media)
            telegraph_url = await c.create_telegraph_page(title='Image', content=[Image(image_path)])
        elif isinstance(media, pyrogram.types.Document):
            image_path = await c.download_media(media)
            telegraph_url = await c.create_telegraph_page(title='Document', content=[Document(image_path)])
        else:
            telegraph_url = None

        id = collection.insert_one({
            "caption": message.html,
            "title": message.splitlines()[0],
            "image_url": telegraph_url if telegraph_url else None
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
                      
