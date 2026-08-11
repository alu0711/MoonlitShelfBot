import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from openai import OpenAI


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")


client = OpenAI(
    api_key=OPENAI_KEY,
    base_url="https://api.deepseek.com"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 你好，我是 Luna。\n\n"
        "我是你的私人 AI 助手，也是月光书架的守护者 📚\n\n"
        "你可以和我聊天、写作、学习、整理想法，也可以探索书籍世界。\n\n"
        "随时告诉我你的想法吧～"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是 Luna，一个温柔、聪明的私人AI助手。"
                    "你喜欢帮助用户解决问题，语气自然、有耐心。"
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    answer = response.choices[0].message.content

    await update.message.reply_text(answer)


app = Application.builder().token(TELEGRAM_TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)


app.run_polling()
