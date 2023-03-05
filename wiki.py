# ---------------------------------------------------------------------------------
# Name: Wikipedia
# Description: Search in wikipedia
# Author: @BlackModules
# Commands:
# .wiki [lang] [text]
# ---------------------------------------------------------------------------------


#                  ▄▄  ▄  ▄
#                  █▄█ █▙▟█
#                  █▄█ █  █
#              © Copyright 2023
#           https://t.me/BlackModules
#
#        Licensed under the GNU AGPLv3
#   https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @BlackModules
# scope: Wiki
# scope: Wiki 0.0.1

import asyncio
import functools
import openai
import random
from urllib.parse import quote_plus

import requests
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class WikiMod(loader.Module):
    """Search in Wikipedia"""

    strings = {
        "name": "Wikipedia",
        "_cmd_doc_wiki": "[lang] [text] Search in Wikipedia",
        "search_inf": "<b>Searching info...</b>",
        "inf": """"<b><emoji document_id=5350682287560203685>💬</emoji> Text:</b>
<code>{text}</code>

<b><emoji document_id=5280658777148760247>🌐</emoji> Info:</b>
<code>{result}</code>""",
        "err_syn": "<b>Use <code>{pref}wiki</code> [lang] [text]</b>",
    }
    strings_ru = {
        "_cmd_doc_wiki": "[язык] [текст] Поиск в Википедии",
        "search_inf": "<b>Поиск информации...</b>",
        "inf": """<b><emoji document_id=5350682287560203685>💬</emoji> Текст:</b>
<code>{text}</code>

<b><emoji document_id=5280658777148760247>🌐</emoji> Информация:</b>
<code>{result}</code>""",
        "err_inf": """
<b><emoji document_id=5350682287560203685>💬</emoji> Запрос:</b>
<code>{text}</code>
<b><emoji document_id=5280658777148760247>🌐</emoji> Ответ:</b>
<code>{exc}</code>
""",
        "err_syn": "<b>Используй <code>{pref}wiki</code> [язык] [текст]</b>",
    }


    @loader.unrestricted
    async def wikicmd(self, message: Message):
        """[lang] [text] Search in wikipedia"""
        try:
          lang = message.message.split(maxsplit=2)[1]
          text = message.message.split(maxsplit=2)[2]
        except IndexError:
            return await message.edit(self.strings("err_syn").format(pref=self.get_prefix()))
        await message.edit(self.strings("search_inf"))
        try:
           wikipedia.set_lang(lang)
           result = wikipedia.summary(text)
           await message.edit(self.strings("inf").format(text=text, result=result))
        except Exception as exc:
           await message.edit(self.strings("err_inf").format(text=text, result=exc))
