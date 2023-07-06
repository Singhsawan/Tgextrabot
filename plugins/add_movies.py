import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import collection
from config import *
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
import pymongo
import telegraph
from telegraph import upload_file, Telegraph
from config import INDEXCHANNEL_ID

# Add Movie to database
@Client.on_message(filters.chat(ADMINS + INDEXCHANNEL_ID) & filters.media)
async def web_db(c: Client, m: Message):
    if m.media:
        message = m.caption

        # Save the image file locally
        file_path = await c.download_media(m)

        telegraph_account = telegraph.Telegraph()
        telegraph_account.create_account(short_name='YourAccountShortName')
        response = telegraph_account.upload_file(file_path)
        image_path = response[0]['src']  # Get the file path from the response
        image_url = f'https://telegra.ph{image_path}'

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
        
        # Send a message to each admin
        for admin_id in ADMINS:
            txt = await c.send_message(admin_id, f"New movie added:\n\n{message.splitlines()[0]}", reply_markup=reply_markup)

    else:
        # Send an error message to each admin
        for admin_id in ADMINS:
            txt = await c.send_message(admin_id, f"Something went wrong while saving:\n\n{message.splitlines()[0]}")

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await m.delete()
        await txt.delete()
        
