
# ---------------------------------------------------------------------------------
# Name: WebShot
# Description: Create a screenshot of webpage
# Author: @BlackModules
# Commands:
# .webshot [link]
# ---------------------------------------------------------------------------------                      
            
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @BlackModules
# scope: Webshot
# scope: webshot 0.0.1

import asyncio
import functools
from urllib.parse import quote_plus

import requests
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class WebshotMod(loader.Module):
    """Take screenshot of the webpage"""

    strings = {"name": "Webshot"}
    strings_ru = {
        "_cmd_doc_webpage": "Take screenshot of webpage .webshot [link]"

    }


    @loader.unrestricted
    async def webshotcmd(self, message: Message):
        """Take a screenshot of webpage .webshot [link]"""
        user_link = message.message.split(maxsplit=2)[1]
        await message.edit("<b>📸 Try create screenshot...</b>")
        try:
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await message.client.send_file(message.to_id, full_link, caption=f"<b>Screenshot of the page ⟶ {user_link}</b>")
        except Exception as dontload:
            await message.edit(f"Error! {dontload}\nTrying again create screenshot...")
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await message.client.send_file(message.to_id, full_link, caption="<b>Screenshot of the page ⟶ {user_link}/b>")
        await message.delete()

