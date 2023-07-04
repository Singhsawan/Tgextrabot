import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import collection
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from translation import *
from plugins.search_movies import search_for_videos
from plugins.callback import replace_username
from bson.objectid import ObjectId
from plugins.search_movies import escape_url
import validate_query

@Client.on_message(filters.group & filters.text & filters.incoming)
async def group_handler(c: Client, m:Message):
    try:

        if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", m.text):
          return

        if ("https://" or "http://") in m.text:
            return

        query = m.text #

        if len(query) < 2:
            return 

        query = await validate_query.validate_q(query)
        results = await search_for_videos(query)

        txt = await m.reply('Processing...')
        bot = await c.get_me()
        buttons = []

        for result in results:   

            id = str(result['_id'])
            command = f"https://telegram.dog/{bot.username}?start={id}"
            buttons += [InlineKeyboardButton(result['title'], callback_data=f"send#{id}"), ],

        reply_markup=InlineKeyboardMarkup(buttons)
        await txt.edit(text=f"**Click On Your Movie/Series Name 👇👇 \n And start**", reply_markup=reply_markup)
  

    
    except Exception as e:

        google_search_url = "https://www.google.com/search?q=" + escape_url(f"{m.text} Movie")
        release_date_url = "https://www.google.com/search?q=" + escape_url(f"{m.text} Release Date")


        reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Check correct spelling ✅", url=google_search_url)],
            [InlineKeyboardButton("Check realease date 📅", url=release_date_url)]
        ])

        m = await txt.edit(text=NO_RESULTS_FOUND.format(m.text, "https://www.google.com/search"), reply_markup=reply_markup)
        await asyncio.sleep(60)
        await m.delete()


 





async def group_send_handler(c: Client, m:Message):
    txt = await m.reply('Searching...')
    id  = m.command[1]
    result = collection.find_one({'_id': ObjectId(id)})
    caption = result['caption']
    caption = await replace_username(caption)

    if m.chat.id in ADMINS:  
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Delete", callback_data=f"delete#{id}")],
            ])
    else:
        reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("How To Watch", url=f"{HOWTO}")
        ]
        ])    
        
        

    await txt.edit(
        caption, 
        disable_web_page_preview=True, 
        reply_markup=reply_markup)

    # Auto Delete
    if AUTO_DELETE is not False:
        await asyncio.sleep(300)
        await m.delete()
        await txt.delete()
