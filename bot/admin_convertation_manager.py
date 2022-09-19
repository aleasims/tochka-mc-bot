from email import message
import logging

from telegram import Update
from telegram.ext import ContextTypes

from .database_manager import DatabaseManager

class AdminConversationManager:
    """Handlers for admin mode."""

    COMMANDS_DESC = '\n'.join([
        "/registered - list all registered users",
        "/messages - list all created messages",
        "/scheduled - list all sceduled messages",
        "/stop - stop conversation",
        "/sendall - send all scheduled messages",
    ])

    def __init__(self, base):
        self.base = base

    @property
    def db(self) -> DatabaseManager:
        return self.base.db

    @property
    def State(self):
        return self.base.State

    async def on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"Admin authentication - TG_ID={tg_id}")

        admins = await self.db.get_all_admins()
        if tg_id in [admin.tg_id for admin in admins]:
            logging.info(f"Admin mode ON - TG_ID={tg_id}")
            await update.message.reply_text(
                f"Admin mode ON\n\nCommands:\n{self.COMMANDS_DESC}"
            )
            return self.State.ADMIN

        logging.info(f"Admin authentication failed - TG_ID={tg_id}")
        await update.message.reply_text("Admin authentication failed")

    async def registered(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"admin.registered - TG_ID={tg_id}")

        users = await self.db.get_all_users()
        response = '\n'.join(
            f"{user.name} (TG_ID={user.tg_id})" for user in users
        )
        await update.message.reply_text(response or "No users registered.")

    async def messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"admin.messages - TG_ID={tg_id}")

        messages = await self.db.get_all_messages()
        if not messages:
            await update.message.reply_text("No messages.")
            return
        for message in messages:
            await update.message.reply_text(message.text)

    async def scheduled(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"admin.scheduled - TG_ID={tg_id}")

        messages = await self.db.get_all_messages()
        if not messages:
            await update.message.reply_text("No messages.")
            return
        for message in messages:
            recipients = ', '.join([
                str(user) for user in await self.db.get_recipients(message)
            ])
            await update.message.reply_text(f"{message.text}\n\nTo: {recipients}")

    async def send_all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"admin.send_all - TG_ID={tg_id}")

        msgs = await self.db.get_all_scheduled_messages()
        for scheduled in msgs:
            print(scheduled)
            # await context.bot.send_message(scheduled.recipient.tg_id,
            #                                scheduled.message.text)
