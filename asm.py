import asyncio
from pyrogram import Client, filters, errors, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import config


def __p_chat(chat):
    return ("@" + chat.username) if chat.username else chat.id


def get_chat_mention(m: Message):
    return "ID: {} Title: {}".format(
        __p_chat(m.chat), m.chat.title[:15] + "..." if len(m.chat.title) > 15 else m.chat.title
    )


async def service_message(c: Client, m: Message):
    try:
        await m.delete()
    except errors.MessageDeleteForbidden as e:
        print("{}, {}".format(e.MESSAGE, get_chat_mention(m)))
        await c.send_message(m.chat.id, "Failed to delete this service message as chat admin privilege not granted.")


async def main():
    app = Client("asm", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, )
    app.add_handler(MessageHandler(service_message, filters.service))
    await app.start()
    print("Anti Service Bot is up and accepting message updates. Status OK.")
    await idle()


if __name__ == "__main__":
    asyncio.run(main())
