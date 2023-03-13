
# Name: Search
# Author: BlackModules
# Commands:
# .google 
# .yandex 
# .duckduckgo 
# .bing 
# .you 
# ---------------------------------------------------------------------------------

# meta developer: @BlackModules
# scope: hikka_only

from telethon.tl.types import Message  # type: ignore

from .. import loader, utils


@loader.tds
class Search(loader.Module):
    strings = {
        "name": "Search",
        "search": (
            "<emoji document_id=5188311512791393083>🔎</emoji><b> I searched for information for"
            " you</b>\n"
        ),
        "lade": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching…</b>",
        "p-auf": "<b>Oops, problem …</b>",
        "n-gef": "<b>Sorry, stop, not found… :(</b>",
        "gef": "<b>Looks like something is found!..</b>",
        "q": "Query:",
        "args?": "📝 <b>Where is arguments, young man?</b>",
    }
    strings_ru = {
        "search": (
            "<emoji document_id=5188311512791393083>🔎</emoji><b> Я поискал информацию за"
            " тебя</b>\n"
        ),
        "lade": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Ищу…</b>",
        "p-auf": "<b>Упс, проблема…</b>",
        "n-gef": "<b>Жаль, нет, не нашлось… :(</b>",
        "gef": "<b>Кажется, нашлось!..</b>",
        "q": "Запрос:",
        "args?": "📝 <b>И где аргументы, молодой человек?</b>",
    }

    async def googlecmd(self, message: Message):
        """поискать в Google"""
        args = utils.get_args_raw(message)
        g = args.replace(" ", "%20")
        google = f"https://google.com/?q={g}"
        await utils.answer(message, self.strings("search") + f'<a href="{google}">Ссылка</a>')

    async def yandexcmd(self, message: Message):
        """поискать в Yandex"""
        args = utils.get_args_raw(message)
        y = args.replace(" ", "%20")
        yandex = f"https://yandex.ru/?q={y}"
        await utils.answer(message, self.strings("search") + f'<a href="{yandex}">Ссылка</a>')

    async def duckduckgocmd(self, message: Message):
        """поискать в Duckduckgo"""
        args = utils.get_args_raw(message)
        d = args.replace(" ", "%20")
        duckduckgo = f"https://duckduckgo.com/?q={d}"
        await utils.answer(message, self.strings("search") + f'<a href="{duckduckgo}">Ссылка</a>')

    async def bingcmd(self, message: Message):
        """поискать в Bing"""
        args = utils.get_args_raw(message)
        b = args.replace(" ", "%20")
        bing = f"https://bing.com/?q={b}"
        await utils.answer(message, self.strings("search") + f'<a href="{bing}">Ссылка</a>')

    async def youcmd(self, message: Message):
        """поискать в You"""
        args = utils.get_args_raw(message)
        y = args.replace(" ", "%20")
        you = f"https://you.com/?q={y}"
        await utils.answer(message, self.strings("search") + f'<a href="{you}">Ссылка</a>')
