import logging
from enum import Enum, auto
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from .admin_convertation_manager import AdminConversationManager
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
        self.admin = AdminConversationManager(self)

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
            "Вы отключились от бота!\n\nЧтобы в дальнейшем получать оповещения,"
            " нужно будет снова использовать /start)"
        )
        return ConversationHandler.END

    async def register(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Registering user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Привет, {user.name}")
        # TODO: return main menu markup here
        return self.State.MAIN_MENU

    async def change_name(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Changing name for user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Имя изменено. Привет, {user.name}")
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
