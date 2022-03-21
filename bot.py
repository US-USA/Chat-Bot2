# DO NOT REMOVE CREDITS
# Copyright (c) 2021 dakshy/droplink-bot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import requests
from os import getenv
from pyrogram import Client, filters
from googletrans import Translator

bot = Client("Chatbot", 
                bot_token=getenv("BOT_TOKEN"), 
                api_id=getenv("API_ID"), 
                api_hash=getenv("API_HASH"))

tr = Translator()


@bot.on_message(filters.command("start"))
async def startmsg(_, message):
    await message.reply_video(video="https://telegra.ph/file/b8f0cbdf67943328459d2.mp4", 
    caption=f"Hello {message.from_user.mention}. \nI'm AI Chat bot made by Tinura Dinith by Using Affiliateplus API, You can chat with me here.")

@bot.on_message(
    filters.text 
    & filters.private 
    & ~filters.edited 
    & ~filters.bot 
    & ~filters.channel 
    & ~filters.forwarded,
    group=1)
async def chatbot(_, message):
    if message.text[0] == "/":
        return
    await bot.send_chat_action(message.chat.id, "typing")
    lang = tr.translate(message.text).src
    trtoen = (message.text if lang=="en" else tr.translate(message.text, dest="en").text).replace(" ", "%20")
    text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
    affiliateplus = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={text}&botname=AI%20Chat%20Bot&ownername=Tinura%20Dinith&user=1")
    textmsg = (affiliateplus.json()["message"])
    msg = tr.translate(textmsg, src='en', dest=lang)
    await message.reply_text(msg.text)

bot.run()    
