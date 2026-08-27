from telegram import Update
from datetime import datetime

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 替换为你的 BotFather Token
TOKEN = "8691122434:AAHT4pieYQCJYklmaxjCLTfNVXyc4ix3sKM"


# /start 命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = f"""
User ID: {user.id}
Username: @{user.username}
First Name: {user.first_name}
Chat ID: {update.effective_chat.id}
"""
    print(msg)
    await update.message.reply_text(msg)


# 回显用户消息
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
  
    await update.message.reply_text(
        f"你发送的是：{user_text}"
    )



async def send_today_date(update, context):
    today = datetime.now().strftime("%Y-%m-%d")

    await update.message.reply_text(
        f"今天的日期是：{today}"
    )


from pathlib import Path


async def monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = f"""
User ID: {user.id}
Username: @{user.username}
First Name: {user.first_name}
Chat ID: {update.effective_chat.id}
"""
    try:
        # 获取当前脚本同级目录下的 monitor.txt
        txt_file = Path(__file__).parent / "monitor.txt"

        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()

        await update.message.reply_text(content+msg)

    except FileNotFoundError:
        await update.message.reply_text("monitor.txt 不存在")
    except Exception as e:
        await update.message.reply_text(f"读取文件失败: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    # 注册命令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("date", send_today_date))
    app.add_handler(CommandHandler("monitor", monitor))

    # 注册文本消息处理器
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo,
        )
    )

    print("Bot 已启动...")
    app.run_polling()


if __name__ == "__main__":
    main()