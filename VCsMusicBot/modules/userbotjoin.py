from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from VCsMusicBot.helpers.decorators import authorized_users_only, errors
from VCsMusicBot.services.callsmusic.callsmusic import client as USER
from VCsMusicBot.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>ارفعني مشرف اولاً</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "تم انضـمام حسـاب المسـاعد")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>حساب المساعد بلفعل موجود!</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⚠️ خطأ انتظار  \n المستخدم {user.first_name} تعذر الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام ! "
            "\n\nOr يمكنك اضافته يدوياً @VCsMusicPlayer الى مجموعتك</b>",
        )
        return
    await message.reply_text(
        "<b>تم انضمام حساب المساعد</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>لا يمكن للمستخدم مغادرة مجموعتك! ."
            "\n\nأو اطردني يدويًا من إلى مجموعتك</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("مساعد مغادرة جميع الدردشات")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"غادر النساعد... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"غادر المساعد... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("هل الدردشة مرتبطة حتى")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>ارفعني مسؤول اولاً</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicBot"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "تم انضمام المساعد")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>المساعد موجود بلفعل</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 خطأ الانضمام 🛑 \n المستخدم {user.first_name} تعذر الانضمام إلى مجموعتك بسبب كثرة طلبات الانضمام ! ."
            "\n\nيمكنك اضافته يدوياً @VCsMusicPlayer الى مجموعتك</b>",
        )
        return
    await message.reply_text(
        "<b>تم انضمام المساعد</b>",
    )
    
