import asyncio
import re
from pyrogram import Client, filters
from .database import collection
from bson.objectid import ObjectId
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r"^send")) 
async def cb_send_handler(c,m):
    await m.answer()
    id = m.data.split('#')[1]
    result = collection.find_one({'_id': ObjectId(id)})

    try:
        caption = result['caption']
        image_path = result['image_path'] # Get the image URL from the database

    except Exception as e:
        return await m.message.reply("Some error occurred")

    caption = await replace_username(caption)
    if m.message.chat.id in ADMINS:  
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Delete", callback_data=f"delete#{id}")],
            ])
    else:
        reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Click here For How To Download", url=f"{HOWTO}")
        ]
        ])

    
    txt = await c.send_photo(
        chat_id=m.message.chat.id,
        photo=image_path,
        caption=caption,
        reply_markup=reply_markup,
        disable_notification=True
    )

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(300)
        await m.message.delete()
        return await txt.delete()


@Client.on_callback_query(filters.regex(r"^delete"))
async def cb_delete_handler(c,m):
    await m.answer()
    try:

        id = m.data.split('#')[1]
        my_query = {'_id': ObjectId(id)}
        collection.delete_one(my_query)
        txt = await m.message.edit(f"Deleted Successfully", disable_web_page_preview=True)
    except:
        txt = await m.message.edit(f"Some error occurred while deleting", disable_web_page_preview=True)

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await m.message.delete()
        return await txt.delete()
  
        
async def replace_username(text):
    usernames = re.findall("([@#][A-Za-z0-9_]+)", text)

    for i in usernames:
        text = text.replace(i, f"@{USERNAME}")

    telegram_links = re.findall(r'[(?:http|https)?://]*(?:telegram.dog|telegram.dog)[^\s]+', text)

    for i in telegram_links:
        text = text.replace(i, f"@{USERNAME}")

    return text
