# ---------------------------------------------------------------------------------
# Name: ChatGPT
# Description: the module uses ChatGPT
# Author: BlackModules
# Commands:
# gpt / gpt_img
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @BlackModules
# scope: ChatGPT
# scope: ChatGPT 0.0.1
# requires: openai
# ---------------------------------------------------------------------------------

import asyncio
import logging
import openai
from telethon.tl.types import Message 

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ChatGPT(loader.Module):
    strings = {
        "name": "ChatGPT",
        "wait": "<emoji document_id=5471981853445463256>🤖</emoji><b> ChatGPT is generating response, please wait</b>",
        "wai_imgt": "<emoji document_id=5471981853445463256>🤖</emoji><b> ChatGPT is generating photo, please wait</b>",
        "quest": "\n\n\n<emoji document_id=5819167501912640906>❔</emoji><b> Your question to ChatGPT was:</b> {args}",
        "args_err": "<emoji document_id=5215534321183499254>⛔️</emoji><b> You didn't ask a question ChatGPT</b>",
        "args_err_img": "<emoji document_id=5215534321183499254>⛔️</emoji><b> You didn't specify a description for the photo  ChatGPT</b>",
        "conf_err": "<emoji document_id=5215534321183499254>⛔️</emoji><b> You didn't provide an api key for ChatGPT</b>",
        "y": "<emoji document_id=5197688912457245639>✅</emoji><b>Your generated photo ChatGPT</b>",
    }
    strings_ru = {
        "wait": "<emoji document_id=5471981853445463256>🤖</emoji><b> ChatGPT генерирует ответ, подождите</b>",
        "wai_imgt": "<emoji document_id=5471981853445463256>🤖</emoji><b> ChatGPT генерирует фотографии, подождите</b>",
        "quest": "\n\n\n<emoji document_id=5819167501912640906>❔</emoji><b> Ваш вопрос к ChatGPT был:</b> {args}",
        "args_err": "<emoji document_id=5215534321183499254>⛔️</emoji><b> Вы не задали вопрос ChatGPT</b>",
        "args_err_img": "<emoji document_id=5215534321183499254>⛔️</emoji><b> Вы не задали описание для фотографии ChatGPT</b>",
        "conf_err": "<emoji document_id=5215534321183499254>⛔️</emoji><b> Вы не указали api key для ChatGPT</b>",
        "y": "<emoji document_id=5197688912457245639>✅</emoji><b>Ваша сгенерированная фотография ChatGPT</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                lambda: "Api key for GPT-2",
                validator=loader.validators.Hidden(),
            ),
        )

    async def gptcmd(self, message: Message):
        """<question> - question for ChatGPT"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args_err"))
            return
        if self.config["api_key"] is None:
            await utils.answer(message, self.strings("conf_err"))
            return
        await utils.answer(message, self.strings("wait").format(args=args))
        openai.api_key = self.config["api_key"]
        model_engine = "text-davinci-003"
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=args,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completion.choices[0].text
        await utils.answer(message, response + self.strings("quest").format(args=args))
 
    async def gpt_imgcmd(self, message: Message):
        """<question> - photo for ChatGPT IMG"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args_err_img"))
            return
        if self.config["api_key"] is None:
            await utils.answer(message, self.strings("conf_err"))
            return
        await utils.answer(message, self.strings("wai_imgt").format(args=args))
        openai.api_key = self.config["api_key"]
        response = openai.Image.create(
            prompt=args,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await utils.answer_file(message, image_url, self.strings("y"))
        
        