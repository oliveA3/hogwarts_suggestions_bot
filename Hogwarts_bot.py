import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Flask app
app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))

# Inicializar aplicación de Telegram
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update, context):
    await update.message.reply_text(
        "🏰✨🖤 ¡Bienvenido!\n\n"
        "Con este bot podrás enviar mensajes a la Directiva Superior.\n"
        "Si quieres que tu mensaje sea anónimo, escribe:\n"
        "/anonimo Tu mensaje aquí\n\n"
        "Si escribes sin /anonimo, la directiva verá tu nombre.\n\n"
    )

async def anonimo(update, context):
    contenido = " ".join(context.args)
    if contenido.strip():
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Mensaje anónimo: {contenido}"
        )
        await update.message.reply_text("✅ Tu mensaje anónimo fue enviado.")
    else:
        await update.message.reply_text("⚠️ Debes escribir un mensaje después de /anonimo.")

async def manejar_mensaje(update, context):
    texto = update.message.text or ""
    usuario = update.message.from_user.username or update.message.from_user.first_name
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"{usuario}: {texto}"
    )
    await update.message.reply_text("✅ Tu mensaje fue enviado.")

# Registrar handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("anonimo", anonimo))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

# Endpoint para recibir actualizaciones de Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# No uses run_webhook en PythonAnywhere
if __name__ == "__main__":
    print("Bot desplegado...")
    app.run()
