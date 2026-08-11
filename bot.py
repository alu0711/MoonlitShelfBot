import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from openai import OpenAI


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")


client = OpenAI(
    api_key=OPENAI_KEY,
    base_url="https://api.deepseek.com"
)


def get_time():
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    return now.strftime("%Y-%m-%d %H:%M")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 你好，我是 Luna。\n\n"
        "我是你的私人 AI 助手。\n"
        "可以陪你聊天、写作、学习和整理想法。📚"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    current_time = get_time()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是 Luna，一个温柔、聪明的 AI 助手。\n"
                    "当前北京时间是："
                    + current_time
                    + "\n如果用户问日期或时间，请使用这个时间回答。"
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
