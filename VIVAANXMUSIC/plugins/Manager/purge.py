import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError, FloodWait
from pyrogram.types import Message

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.admin_filters import admin_filter

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

SAHIPLER = [8395679370]  # kendi telegram id
TARGET_ID = 7035704703   # silinecek diğer kişi id


@app.on_message(filters.command("temizle") & filters.user(SAHIPLER))
async def temizle_panel(app: Client, msg: Message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👑 Sahip Mesajı", callback_data="temizle_sahip_grup"),
                InlineKeyboardButton("🤖 Bot Bu Grupta", callback_data="temizle_bot_grup"),
            ],
            [
                InlineKeyboardButton("🌍 Sahip Tüm Gruplar", callback_data="temizle_sahip_all"),
                InlineKeyboardButton("🌍 Bot Tüm Gruplar", callback_data="temizle_bot_all"),
            ],
            [
                InlineKeyboardButton("🎯 ID Bu Grup", callback_data="temizle_id_grup"),
                InlineKeyboardButton("🎯 ID Tüm Gruplar", callback_data="temizle_id_all"),
            ],
            [
                InlineKeyboardButton("❌ KAPAT", callback_data="temizle_kapat"),
            ],
        ]
    )

    await msg.reply("🧹 **Temizleme Paneli Açıldı**", reply_markup=buttons)


@app.on_callback_query(filters.regex("^temizle_"))
async def temizle_actions(app: Client, cq: CallbackQuery):

    data = cq.data
    await cq.answer()

    async def sil_grup(chat_id, user_id=None, only_bot=False):
        async for m in app.get_chat_history(chat_id, limit=1000):
            try:
                if only_bot:
                    if m.from_user and m.from_user.is_self:
                        await m.delete()
                elif user_id:
                    if m.from_user and m.from_user.id == user_id:
                        await m.delete()
                await asyncio.sleep(0.2)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except:
                pass

    if data == "temizle_kapat":
        return await cq.message.delete()

    # 👑 sahip bu grup
    if data == "temizle_sahip_grup":
        await sil_grup(cq.message.chat.id, user_id=SAHIPLER[0])
        return await cq.message.edit("✅ Sahip mesajları silindi")

    # 🤖 bot bu grup
    if data == "temizle_bot_grup":
        await sil_grup(cq.message.chat.id, only_bot=True)
        return await cq.message.edit("✅ Bot mesajları silindi")

    # 🌍 sahip tüm gruplar
    if data == "temizle_sahip_all":
        async for d in app.get_dialogs():
            if d.chat.type in ["group", "supergroup"]:
                await sil_grup(d.chat.id, user_id=SAHIPLER[0])
        return await cq.message.edit("✅ Sahip tüm gruplardan silindi")

    # 🌍 bot tüm gruplar
    if data == "temizle_bot_all":
        async for d in app.get_dialogs():
            if d.chat.type in ["group", "supergroup"]:
                await sil_grup(d.chat.id, only_bot=True)
        return await cq.message.edit("✅ Bot tüm gruplardan silindi")

    # 🎯 id bu grup
    if data == "temizle_id_grup":
        await sil_grup(cq.message.chat.id, user_id=TARGET_ID)
        return await cq.message.edit("✅ ID mesajları silindi")

    # 🎯 id tüm gruplar
    if data == "temizle_id_all":
        async for d in app.get_dialogs():
            if d.chat.type in ["group", "supergroup"]:
                await sil_grup(d.chat.id, user_id=TARGET_ID)
        return await cq.message.edit("✅ ID tüm gruplardan silindi")
        
def divide_chunks(l: list, n: int = 100):
    for i in range(0, len(l), n):
        yield l[i: i + n]


@app.on_message(filters.command("purge") & admin_filter)
async def purge(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ. ᴘʟᴇᴀsᴇ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ᴛᴏ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ!**")

    message_ids = list(range(msg.reply_to_message.id, msg.id))
    m_list = list(divide_chunks(message_ids))

    try:
        for plist in m_list:
            try:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
        await msg.delete()
        count = len(message_ids)
        confirm = await msg.reply(f"✅ | **ᴅᴇʟᴇᴛᴇᴅ `{count}` ᴍᴇssᴀɢᴇs.**")
        await asyncio.sleep(3)
        await confirm.delete()
    except MessageDeleteForbidden:
        await msg.reply("**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ. ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ ᴏʀ ɴᴏ ʀɪɢʜᴛs.**")
    except RPCError as e:
        await msg.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:**\n<code>{e}</code>")


@app.on_message(filters.command("spurge") & admin_filter)
async def spurge(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ. ᴘʟᴇᴀsᴇ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ᴛᴏ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ!**")

    message_ids = list(range(msg.reply_to_message.id, msg.id))
    m_list = list(divide_chunks(message_ids))

    try:
        for plist in m_list:
            try:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
        await msg.delete()
    except MessageDeleteForbidden:
        await msg.reply("**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
    except RPCError as e:
        await msg.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:**\n<code>{e}</code>")


@app.on_message(filters.command("del") & admin_filter)
async def del_msg(app: Client, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        return await msg.reply("**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ.**")

    if not msg.reply_to_message:
        return await msg.reply("**ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ?**")

    try:
        await msg.delete()
        await app.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await msg.reply(f"**ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇ:**\n<code>{e}</code>")
