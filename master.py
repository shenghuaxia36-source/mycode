from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import zabbix_worker
import hyperv_worker
import mysql_worker

# 允许访问的用户
ALLOWED_USERS = {
    123456789,
    987654321
}

MASTER_TOKEN = "MASTER_BOT_TOKEN"


def auth(user_id):
    return user_id in ALLOWED_USERS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not auth(update.effective_user.id):
        await update.message.reply_text("failed")
        return

    await update.message.reply_text(
        """
Available Commands

/problem
/list_vms
/status VM01
/cpu VM01
/memory VM01
/disk VM01

/hello_hyperv
/hello_mysql
"""
    )


async def command_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not auth(update.effective_user.id):
        await update.message.reply_text("failed")
        return

    command = update.message.text.strip()

    if command.startswith("/problem"):
        result = zabbix_worker.problem()

    elif command.startswith("/list_vms"):
        result = zabbix_worker.list_vms()

    elif command.startswith("/status"):
        vm = command.split()[1]
        result = zabbix_worker.status(vm)

    elif command.startswith("/cpu"):
        vm = command.split()[1]
        result = zabbix_worker.cpu(vm)

    elif command.startswith("/memory"):
        vm = command.split()[1]
        result = zabbix_worker.memory(vm)

    elif command.startswith("/disk"):
        vm = command.split()[1]
        result = zabbix_worker.disk(vm)

    elif command.startswith("/hello_hyperv"):
        result = hyperv_worker.start()

    elif command.startswith("/hello_mysql"):
        result = mysql_worker.start()

    else:
        result = "Unknown command"

    await update.message.reply_text(result)


app = ApplicationBuilder().token(MASTER_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("problem", command_router))
app.add_handler(CommandHandler("list_vms", command_router))
app.add_handler(CommandHandler("status", command_router))
app.add_handler(CommandHandler("cpu", command_router))
app.add_handler(CommandHandler("memory", command_router))
app.add_handler(CommandHandler("disk", command_router))
app.add_handler(CommandHandler("hello_hyperv", command_router))
app.add_handler(CommandHandler("hello_mysql", command_router))

print("Master Bot Started...")
app.run_polling()