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
import io
import logging
import time

from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import EditChatAdminRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights, Message

from .. import loader, utils


logger = logging.getLogger(__name__)


PROMOTE_RIGHTS = ChatAdminRights(
    post_messages=True,
    add_admins=None,
    invite_users=True,
    change_info=None,
    ban_users=True,
    delete_messages=True,
    pin_messages=True,
    edit_messages=True,
)

DEMOTE_RIGHTS = ChatAdminRights(
    post_messages=None,
    add_admins=None,
    invite_users=None,
    change_info=None,
    ban_users=None,
    delete_messages=None,
    pin_messages=None,
    edit_messages=None,
)

UNMUTE_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False,
)

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

# ---------------------------------------------------------------------------------


@loader.tds
class NetfollChat(loader.Module):
    """✉ Модуль для управления чатом"""

    strings = {
        "name": "NetfollChat",
        "rules_n": "<b>😪 You didnt make the rules</b>",
        "clicks": "😗 Click",
        "rulesch": "<b>⚠️ Rules for this chat</b>",
        "upd_rul": "<b>✅ Rules updated</b>",
        "promote_none": "<b>⬆️ No one to promote</b>",
        "who": "<b>⁉️ Who is it?</b>",
        "not_admin": "<b>🚫 Im not an admin here</b>",
        "promoted": "<b>💥 {} elevated as an administrator.\nRank: {}</b>",
        "wtf_is_it": "<b>⁉️ What is this?</b>",
        "this_isn`t_a_chat": "<b>‼️ This is not a chat!</b>",
        "demote_none": "<b>⬇️ No one to demote</b>",
        "demoted": "<b>😥 {} Demoted in admin privileges</b>",
        "no_rights": "<b>⚖ I do not have rights</b>",
        "can`t_kick": "<b>❗ Cant kick user</b>",
        "kicking": "<b>⏳ Kick...</b>",
        "kick_none": "<b>✌ Nobody to kick</b>",
        "kicked": "<b>👨‍⚖️ {} kicked from chat</b>",
        "kicked_for_reason": "🌧<b>{} kicked from chat\n🚔 Reason {}.</b>",
        "banning": "<b>🥱 Ban...</b>",
        "banned": "<b>😰 {} banned from chat</b>",
        "ban_none": "<b>🚫 No one to give a ban</b>",
        "unban_none": "<b>‼️ Someone to unban</b>",
        "unbanned": "<b>😊 {} unbanned in chat</b>",
        "mute_none": "<b>😥 No one to give mute</b>",
        "muted": "😗 <b>{} now in mute on </b>",
        "no_args": "<b>🚫 Invalid arguments</b>",
        "unmute_none": "<b>🛑 There is no one to unmute</b>",
        "unmuted": "<b>✔ {} no longer in the mute</b>",
        "no_reply": "<b>‼️ No replay</b>",
        "deleting": "<b>🧹 Deletion...</b>",
        "no_args_or_reply": "<b>📛 No arguments or replay</b>",
        "deleted": "<b>✨ All messages from {} removed</b>",
        "del_u_search": "<b>👀 Search for deleted accounts...</b>",
        "del_u_kicking": "<b>❌ Kick deleted accounts...</b>",
    }

    strings_ru = {
        "rules_n": "<b>😪 Вы не ввели правила</b>",
        "clicks": "😗 Клик",
        "rulesch": "<b>⚠️ Правила этого чата</b>",
        "upd_rul": "<b>✅ Правила обновлены</b>",
        "promote_none": "<b>⬆️ Некого повышать</b>",
        "who": "<b>⁉️ Кто это?</b>",
        "not_admin": "<b>🚫 Я здесь не админ</b>",
        "promoted": "<b>💥 {} повышен в правах администратора.\nРанг: {}</b>",
        "wtf_is_it": "<b>⁉️ Что это?</b>",
        "this_isn`t_a_chat": "<b>‼️ Это не чат!</b>",
        "demote_none": "<b>⬇️ Некого понижать</b>",
        "demoted": "<b>😥 {} понижен в правах администратора</b>",
        "no_rights": "<b>⚖ У меня нет прав</b>",
        "can`t_kick": "<b>❗ Не могу кикнуть пользователя</b>",
        "kicking": "<b>⏳ Кик...</b>",
        "kick_none": "<b>✌ Некого кикать</b>",
        "kicked": "<b>👨‍⚖️ {} кикнут из чата</b>",
        "kicked_for_reason": "🌧<b>{} кикнут из чата\n🚔 Причина: {}.</b>",
        "banning": "<b>🥱 Бан...</b>",
        "banned": "<b>😰 {} забанен в чате</b>",
        "banned_for_reason": "<b>🥺 {} забанен в чате\n🕳 Причина: {}</b>",
        "ban_none": "<b>🚫 Некому давать бан</b>",
        "unban_none": "<b>‼️ Некого разбанивать</b>",
        "unbanned": "<b>😊 {} разбанен в чате</b>",
        "mute_none": "<b>😥 Некому давать мут</b>",
        "muted": "😗 <b>{} теперь в муте на </b>",
        "no_args": "<b>🚫 Неверно указаны аргументы</b>",
        "unmute_none": "<b>🛑 Некого размучивать</b>",
        "unmuted": "<b>✔ {} теперь не в муте</b>",
        "no_reply": "<b>‼️ Нет реплая</b>",
        "deleting": "<b>🧹 Удаление...</b>",
        "no_args_or_reply": "<b>📛 Нет аргументов или реплая</b>",
        "deleted": "<b>✨ Все сообщения от {} удалены</b>",
        "del_u_search": "<b>👀 Поиск удалённых аккаунтов...</b>",
        "del_u_kicking": "<b>❌ Кик удалённых аккаунтов...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "rules", "🚫 Rules not set", lambda: "You chat rules"
        )

    @loader.unrestricted
    async def rulescmd(self, message: Message) -> None:
        """Команда для отображения добавленных правил"""
        await self.inline.form(
            text=self.strings("rulesch"),
            message=message,
            disable_security=True,
            reply_markup=[
                [
                    {
                        "text": self.strings("clicks"),
                        "callback": self.inline__callAnswer,
                    }
                ]
            ],
        )

    async def client_ready(self, client, db):
        self.db = db
        self.client = client


    async def inline__callAnswer(self, call) -> None:
        if self.config["rules"] != 0:
            await call.answer(self.config["rules"], show_alert=True)
        else:
            await call.answer(self.strings("rules_n"), show_alert=True)

    async def promotecmd(self, promt):
        """The .promote команда повышает пользователю права администратора.\nИспользуй: .promote <@ or реплай> <ранг>."""
        if promt.chat:
            try:
                args = utils.get_args_raw(promt).split(" ")
                reply = await promt.get_reply_message()
                rank = "admin"
                chat = await promt.get_chat()
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(promt, self.strings("not_admin", promt))
                if reply:
                    args = utils.get_args_raw(promt)
                    if args:
                        rank = args
                    else:
                        rank = rank
                    user = await utils.get_user(reply)
                else:
                    user = await promt.client.get_entity(args[0])
                    if len(args) == 1:
                        rank = rank
                    elif len(args) >= 2:
                        rank = utils.get_args_raw(promt).split(" ", 1)[1]
                try:
                    await promt.client(
                        EditAdminRequest(promt.chat_id, user.id, PROMOTE_RIGHTS, rank)
                    )
                except ChatAdminRequiredError:
                    return await utils.answer(promt, self.strings("no_rights", promt))
                else:
                    return await utils.answer(
                        promt,
                        self.strings("promoted", promt).format(user.first_name, rank),
                    )
            except ValueError:
                return await utils.answer(promt, self.strings("no_args", promt))
        else:
            return await utils.answer(promt, self.strings("this_isn`t_a_chat", promt))

    async def demotecmd(self, demt):
        """The .demote команда понижает пользователя в административных привилегиях.\nИспользуй: .demote <@ or реплай>."""
        if demt.chat:
            try:
                reply = await demt.get_reply_message()
                chat = await demt.get_chat()
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(demt, self.strings("not_admin", demt))
                if reply:
                    user = await utils.get_user(await demt.get_reply_message())
                else:
                    args = utils.get_args(demt)
                    if not args:
                        return await utils.answer(
                            demt, self.strings("demote_none", demt)
                        )
                    user = await demt.client.get_entity(args[0])
                if not user:
                    return await utils.answer(demt, self.strings("who", demt))
                try:
                    if demt.is_channel:
                        await demt.client(
                            EditAdminRequest(demt.chat_id, user.id, DEMOTE_RIGHTS, "")
                        )
                    else:
                        await demt.client(
                            EditChatAdminRequest(demt.chat_id, user.id, False)
                        )
                except:
                    return await utils.answer(demt, self.strings("no_rights", demt))
                else:
                    return await utils.answer(
                        demt, self.strings("demoted", demt).format(user.first_name)
                    )
            except:
                return await utils.answer(demt, self.strings("wtf_is_it"))
        else:
            return await utils.answer(demt, self.strings("this_isn`t_a_chat", demt))

    async def kickcmd(self, kock):
        """The .kick command kicks the user.\nИспользуй: .kick <@ or реплай>."""
        if kock.chat:
            try:
                args = utils.get_args_raw(kock).split(" ")
                reason = utils.get_args_raw(kock)
                reply = await kock.get_reply_message()
                chat = await kock.get_chat()
                reason = False
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(kock, self.strings("not_admin", kock))
                if reply:
                    user = await utils.get_user(reply)
                    args = utils.get_args_raw(kock)
                    if args:
                        reason = args
                else:
                    user = await kock.client.get_entity(args[0])
                    if args:
                        if len(args) == 1:
                            args = utils.get_args_raw(kock)
                            user = await kock.client.get_entity(args)
                            reason = False
                        elif len(args) >= 2:
                            reason = utils.get_args_raw(kock).split(" ", 1)[1]
                try:
                    await utils.answer(kock, self.strings("kicking", kock))
                    await kock.client.kick_participant(kock.chat_id, user.id)
                except ChatAdminRequiredError:
                    return await utils.answer(kock, self.strings("no_rights", kock))
                else:
                    if reason:
                        return await utils.answer(
                            kock,
                            self.strings("kicked_for_reason", kock).format(
                                user.first_name, reason
                            ),
                        )
                    if reason is False:
                        return await utils.answer(
                            kock, self.strings("kicked", kock).format(user.first_name)
                        )
            except ValueError:
                return await utils.answer(kock, self.strings("no_args", kock))
        else:
            return await utils.answer(kock, self.strings("this_isn`t_a_chat", kock))

    async def bancmd(self, bon):
        """The .ban команда для бана пользователя в чате.\nИспользуй: .ban <@ or реплай>."""
        if bon.chat:
            try:
                args = utils.get_args_raw(bon).split(" ")
                reason = utils.get_args_raw(bon)
                reply = await bon.get_reply_message()
                chat = await bon.get_chat()
                reason = False
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(bon, self.strings("not_admin", bon))
                if reply:
                    user = await utils.get_user(reply)
                    args = utils.get_args_raw(bon)
                    if args:
                        reason = args
                else:
                    user = await bon.client.get_entity(args[0])
                    if args:
                        if len(args) == 1:
                            args = utils.get_args_raw(bon)
                            user = await bon.client.get_entity(args)
                            reason = False
                        elif len(args) >= 2:
                            reason = utils.get_args_raw(bon).split(" ", 1)[1]
                try:
                    await utils.answer(bon, self.strings("banning", bon))
                    await bon.client(
                        EditBannedRequest(
                            bon.chat_id,
                            user.id,
                            ChatBannedRights(until_date=None, view_messages=True),
                        )
                    )
                except ChatAdminRequiredError:
                    return await utils.answer(bon, self.strings("no_rights", bon))
                except UserAdminInvalidError:
                    return await utils.answer(bon, self.strings("no_rights", bon))
                if reason:
                    return await utils.answer(
                        bon,
                        self.strings("banned_for_reason", bon).format(
                            user.first_name, reason
                        ),
                    )
                if reason is False:
                    return await utils.answer(
                        bon, self.strings("banned", bon).format(user.first_name)
                    )
            except ValueError:
                return await utils.answer(bon, self.strings("no_args", bon))
        else:
            return await utils.answer(bon, self.strings("this_isn`t_a_chat", bon))

    async def unbancmd(self, unbon):
        """The .unban команда для разбана пользователя в чате.\nИспользуй: .unban <@ or реплай>."""
        if unbon.chat:
            reply = await unbon.get_reply_message()
            chat = await unbon.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(unbon, self.strings("not_admin", unbon))
            if reply:
                user = await utils.get_user(reply)
            else:
                args = utils.get_args(unbon)
                if not args:
                    return await utils.answer(unbon, self.strings("unban_none", unbon))
                user = await unbon.client.get_entity(args[0])
            if not user:
                return await utils.answer(unbon, self.strings("who", unbon))
            logger.debug(user)
            try:
                await unbon.client(
                    EditBannedRequest(
                        unbon.chat_id,
                        user.id,
                        ChatBannedRights(until_date=None, view_messages=False),
                    )
                )
            except:
                return await utils.answer(unbon, self.strings("no_rights", unbon))
            else:
                return await utils.answer(
                    unbon, self.strings("unbanned", unbon).format(user.first_name)
                )
        else:
            return await utils.answer(unbon, self.strings("this_isn`t_a_chat", unbon))

    async def mutecmd(self, mot):
        """The .mute команда для заглушение пользователя в чате.\nИспользуй: .mute <@ or реплай> <time (1m, 1h, 1d)>."""
        if mot.chat:
            try:
                reply = await mot.get_reply_message()
                chat = await mot.get_chat()
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(mot, self.strings("not_admin", mot))
                if reply:
                    user = await utils.get_user(reply)
                else:
                    who = utils.get_args_raw(mot).split(" ")
                    user = await mot.client.get_entity(who[0])

                    if len(who) == 1:
                        timee = ChatBannedRights(until_date=True, send_messages=True)
                        await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                        await mot.edit(
                            "<b>🥰 {} теперь замолчал</b>".format(user.first_name)
                        )
                        return
                    if not user:
                        return await utils.answer(mot, self.strings("mute_none", mot))
                    if user:
                        tim = who[1]
                        if tim:
                            if len(tim) != 2:
                                return await utils.answer(
                                    mot, self.strings("no_args", mot)
                                )
                            num = ""
                            t = ""
                            for q in tim:
                                if q.isdigit():
                                    num += q
                                else:
                                    t += q
                            text = f"<b>{num}"
                            if t == "m":
                                num = int(num) * 60
                                text += " minute(-s).</b>"
                            elif t == "h":
                                num = int(num) * 3600
                                text += " day(-s/).</b>"
                            elif t == "d":
                                num = int(num) * 86400
                                text += " hour(-s).</b>"
                            else:
                                return await utils.answer(
                                    mot, self.strings("no_args", mot)
                                )
                            timee = ChatBannedRights(
                                until_date=time.time() + int(num), send_messages=True
                            )
                            try:
                                await mot.client(
                                    EditBannedRequest(mot.chat_id, user.id, timee)
                                )
                                await utils.answer(
                                    mot,
                                    self.strings("muted", mot).format(
                                        utils.escape_html(user.first_name)
                                    )
                                    + text,
                                )
                                return
                            except:
                                await utils.answer(mot, self.strings("no_rights", mot))
                        else:
                            timee = ChatBannedRights(
                                until_date=True, send_messages=True
                            )
                            await mot.client(
                                EditBannedRequest(mot.chat_id, user.id, timee)
                            )
                            await mot.edit(
                                "<b>🥰 {} теперь замолчал</b>".format(user.first_name)
                            )
                            return
                logger.debug(user)
                tim = utils.get_args(mot)
                if tim:
                    if len(tim[0]) < 2:
                        return await utils.answer(mot, self.strings("no_args", mot))
                    num = ""
                    t = ""
                    for q in tim[0]:
                        if q.isdigit():
                            num += q
                        else:
                            t += q
                    text = f"<b>{num}"
                    if t == "m":
                        num = int(num) * 60
                        text += " minute(-s).</b>"
                    elif t == "d":
                        num = int(num) * 86400
                        text += " day(-s) .</b>"
                    elif t == "h":
                        num = int(num) * 3600
                        text += " hour(-s).</b>"
                    else:
                        return await utils.answer(mot, self.strings("no_args", mot))
                    timee = ChatBannedRights(
                        until_date=time.time() + int(num), send_messages=True
                    )
                    try:
                        await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                        await utils.answer(
                            mot,
                            self.strings("muted", mot).format(
                                utils.escape_html(user.first_name)
                            )
                            + text,
                        )
                        return
                    except:
                        await utils.answer(mot, self.strings("no_rights", mot))
                else:
                    timee = ChatBannedRights(until_date=True, send_messages=True)
                    await mot.client(EditBannedRequest(mot.chat_id, user.id, timee))
                    await mot.edit("<b>🥰 {} теперь замолчал</b>".format(user.first_name))
                    return
            except:
                await utils.answer(mot, self.strings("mute_none", mot))
                return
        else:
            await utils.answer(mot, self.strings("this_isn`t_a_chat", mot))

    async def unmutecmd(self, unmot):
        """The .unmute команда для разглашение пользователя в чате.\nИспользуй: .unmute <@ или реплай>."""
        if unmot.chat:
            try:
                reply = await unmot.get_reply_message()
                chat = await unmot.get_chat()
                if not chat.admin_rights and not chat.creator:
                    return await utils.answer(unmot, self.strings("not_admin", unmot))
                if reply:
                    user = await utils.get_user(reply)
                else:
                    args = utils.get_args(unmot)
                    if not args:
                        return await utils.answer(
                            unmot, self.strings("unmute_none", unmot)
                        )
                    user = await unmot.client.get_entity(args[0])
                if not user:
                    return await utils.answer(unmot, self.strings("who", unmot))
                try:
                    await unmot.client(
                        EditBannedRequest(unmot.chat_id, user.id, UNMUTE_RIGHTS)
                    )
                except:
                    return await utils.answer(unmot, self.strings("not_admin", unmot))
                else:
                    return await utils.answer(
                        unmot, self.strings("unmuted", unmot).format(user.first_name)
                    )
            except:
                return await utils.answer(unmot, self.strings("wtf_is_it", unmot))
        else:
            return await utils.answer(unmot, self.strings("this_isn`t_a_chat", unmot))


    async def welcomecmd(self, message):
        """Включить/выключить приветствие новых пользователей в чате.
        Используй: .welcome <clearall (по желанию)>."""
        welcome = self.db.get("Welcome", "welcome", {})
        chatid = str(message.chat_id)
        args = utils.get_args_raw(message)
        if args == "clearall":
            self.db.set("Welcome", "welcome", {})
            return await message.edit(
                "<b>[Welcome Mode]</b> Все настройки модуля сброшены."
            )

        if chatid in welcome:
            welcome.pop(chatid)
            self.db.set("Welcome", "welcome", welcome)
            return await message.edit("<b>[Welcome Mode]</b> Деактивирован!")

        welcome.setdefault(chatid, {})
        welcome[chatid].setdefault("message", "Добро пожаловать в чат!")
        welcome[chatid].setdefault("is_reply", False)
        self.db.set("Welcome", "welcome", welcome)
        await message.edit("<b>[Welcome Mode]</b> Активирован!")

    async def setwelcomecmd(self, message):
        """Установить новое приветствие новых пользователей в чате.\nИспользуй: .setwelcome <текст (можно использовать {name}; {chat})>; ничего."""
        welcome = self.db.get("Welcome", "welcome", {})
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        chat = await message.client.get_entity(int(chatid))
        try:
            if not args and not reply:
                return await message.edit(
                    "<b>Приветствие новых "
                    "пользователей в "
                    f'"{chat.title}":</b>\n\n'
                    "<b>Статус:</b> Включено.\n"
                    f"<b>Приветствие:</b>{welcome[chatid]['message']}\n\n "
                    "<b>~ Установить новое приветствие "
                    "можно с помощью команды:</b> "
                    ".setwelcome <текст>."
                )
            else:
                if reply:
                    welcome[chatid]["message"] = reply.id
                    welcome[chatid]["is_reply"] = True
                else:
                    welcome[chatid]["message"] = args
                    welcome[chatid]["is_reply"] = False
                self.db.set("Welcome", "welcome", welcome)
                return await message.edit(
                    "<b>Новое приветствие установлено успешно!</b>"
                )
        except KeyError:
            return await message.edit(
                f'<b>Приветствие новых пользователей в "{chat.title}":</b>\n\n '
                "<b>Статус:</b> Отключено"
            )

    async def watcher(self, message):
        """Интересно, почему он именно watcher называется... 🤔"""
        try:
            welcome = self.db.get("Welcome", "welcome", {})
            chatid = str(message.chat_id)
            if chatid not in welcome:
                return
            if message.user_joined or message.user_added:
                user = await message.get_user()
                chat = await message.get_chat()
                if not welcome[chatid]["is_reply"]:
                    return await message.reply(
                        (welcome[chatid]["message"]).format(
                            name=user.first_name, chat=chat.title
                        )
                    )
                msg = await self.client.get_messages(
                    int(chatid), ids=welcome[chatid]["message"]
                )
                await message.reply(msg)
        except:
            pass
