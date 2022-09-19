import logging
from enum import Enum, auto
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from .database_manager import DatabaseManager


class ConversationManager:
    """Handlers for conversation."""

    class State(Enum):
        """Conversation state."""

        ADMIN = auto()
        """Admin mode is ON. One can access admin commands now."""

        REGISTRATION = auto()
        """Enter user name/surname."""

        MAIN_MENU = auto()
        """Main menu panel."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    async def start(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        logging.info(f"Started conversation - TG_ID={tg_id}")

        user = await self.db.get_user(tg_id)
        if user is None:
            await update.message.reply_text("Привет, введи свое имя и фамилию:")
            return self.State.REGISTRATION

        await update.message.reply_text(f"Привет, {user.name}")
        # TODO: return main menu markup here
        return self.State.MAIN_MENU

    async def stop(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        logging.info(f"Stopped conversation - TG_ID={tg_id}")

        await update.message.reply_text(
            "Пока! (Чтобы получать оповещения, "
            "нужно будет снова использовать /start)"
        )
        return ConversationHandler.END

    async def admin_on(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        logging.info(f"Admin authentication - TG_ID={tg_id}")

        admins = await self.db.get_all_admins()
        if tg_id in [admin.tg_id for admin in admins]:
            logging.info(f"Admin mode ON - TG_ID={tg_id}")
            await update.message.reply_text("Admin mode ON\n\n"
                "Commands:\n"
                "/registered - list all registered users\n"
                "/stop - stop conversation")
            return self.State.ADMIN

        logging.info(f"Admin authentication failed - TG_ID={tg_id}")
        await update.message.reply_text("Admin authentication failed")

    async def registered(self, update: Update, context: CallbackContext):
        users = await self.db.get_all_users()
        response = '\n'.join(
            f"{user.name} (TG_ID={user.tg_id})" for user in users
        )
        await update.message.reply_text(response or "No users registered.")

    async def register(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Registering user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Привет, {user.name}")
        # TODO: return main menu markup here
        return self.State.MAIN_MENU

    async def change_name(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Registering user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Привет, {user.name}")
        # TODO: return main menu markup here
        return self.State.MAIN_MENU

    async def error(self, update: Optional[Update], context: CallbackContext):
        if context.error is not None:
            logging.exception(context.error)

        if update is not None:
            tg_id = update.message.from_user.id
            command = update.message.text
            logging.info(f"Error occured - TG_ID={tg_id}, TEXT=`{command}`")

        await update.message.reply_text("Произошла ошибка :(")
