import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, Photo, Document
from .database import collection
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo
import telegraph
from telegraph import upload_file, Telegraph

# Add Movie to database
@Client.on_message(filters.chat(ADMINS) & filters.media)
async def web_db(c: Client, m: Message):
    if m.media:
        message = m.caption

        # Save the image file locally
        file_path = await c.download_media(m)

        telegraph_account = telegraph.Telegraph()
        telegraph_account.create_account(short_name='YourAccountShortName')
        response = telegraph_account.upload_file(file_path)
        image_url = f'https://telegra.ph{response[0]}'

        id = collection.insert_one(
            {"caption": message.html,
             "title": message.splitlines()[0],
             "image_url": image_url}
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

