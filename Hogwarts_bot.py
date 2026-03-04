import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))


async def start(update, context):
    await update.message.reply_text(
        "🏰✨🖤 ¡Bienvenido!\n\n"
        "Con este bot podrás enviar mensajes a la Directiva Superior.\n"
        "Si quieres que tu mensaje sea anónimo, escribe:\n"
        "/anonimo Tu mensaje aquí\n\n"
        "Si escribes sin /anonimo, los administradores verán tu nombre.\n\n"
        "Siéntete libre de proponer nuevas ideas, dar sugerencias o quejarte."
    )


async def anonimo(update, context):
    contenido = " ".join(context.args)
    if contenido.strip():
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Mensaje anónimo: {contenido}"
        )
        await update.message.reply_text("✅ Tu mensaje anónimo fue enviado a los administradores.")
    else:
        await update.message.reply_text("⚠️ Debes escribir un mensaje después de /anonimo.")


async def manejar_mensaje(update, context):
    texto = update.message.text or ""
    usuario = update.message.from_user.username or update.message.from_user.first_name
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"De {usuario}: {texto}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anonimo", anonimo))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    app.run_polling()


if __name__ == "__main__":
    main()
