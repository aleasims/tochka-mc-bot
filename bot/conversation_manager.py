import logging
from enum import Enum, auto
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from .admin_convertation_manager import AdminConversationManager
from .database_manager import DatabaseManager
from .menu_manager import MenuManager
from .static_data import StaticData


class ConversationManager:
    """Handlers for conversation."""

    class State(Enum):
        """Conversation state."""

        ADMIN = auto()
        """Admin mode is ON. One can access admin commands now."""

        MENU_ABOUT = auto()
        """About page."""

        MENU_APPLY = auto()
        """Apply to courses page."""

        MENU_CONTACTS = auto()
        """Contacts page."""

        MENU_COURSE = auto()
        """Course page."""

        MENU_MAIN = auto()
        """Main menu panel."""

        MENU_MYCOURSES = auto()
        """User applied courses page."""

        REGISTER_NAME = auto()
        """Enter user name."""

        REGISTER_SURNAME = auto()
        """Enter user surname."""

        REGISTER_GROUPID = auto()
        """Enter user phystech group id."""

    def __init__(self, db: DatabaseManager, static: StaticData):
        self.db = db
        self.static = static
        self.menu = MenuManager(self)
        self.admin = AdminConversationManager(self)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
        tg_id = update.message.from_user.id
        logging.info(f"Started conversation - TG_ID={tg_id}")

        user = await self.db.get_user(tg_id)
        if (user is None) or (user.surname is None) or (user.group_id is None):
            await update.message.reply_text(self.static.texts["start_hello_get_name.txt"])
            return self.State.REGISTER_NAME

        await update.message.reply_text(f"Привет, {user.name}")
        await self.menu.default(update, context)
        return self.State.MENU_MAIN

    async def register_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Registering user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Приятно познакомиться, {user.name} :) \n А какая у тебя фамилия?")
        return self.State.REGISTER_SURNAME

    async def register_surname(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
        tg_id = update.message.from_user.id
        surname = update.message.text
        logging.info(f"Add user info - TG_ID={tg_id} SURNAME={surname}")

        await self.db.update_user(tg_id, surname=surname)

        await update.message.reply_text(self.static.texts["start_get_group_id.txt"])
        return self.State.REGISTER_GROUPID

    async def register_groupid(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
        tg_id = update.message.from_user.id
        group_id = update.message.text
        logging.info(f"Add user info - TG_ID={tg_id} GROUPID={group_id}")

        await self.db.update_user(tg_id, group_id=group_id)

        await self.menu.intro(update, context)
        return self.State.MENU_MAIN

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_id = update.message.from_user.id
        logging.info(f"Stopped conversation - TG_ID={tg_id}")

        await update.message.reply_text(self.static.texts["stop.txt"])
        return ConversationHandler.END

    async def error(self, update: Optional[Update], context: ContextTypes.DEFAULT_TYPE):
        if context.error is not None:
            logging.exception(context.error)

        reply = "Произошла ошибка :( Попробуй еще раз позже"

        if update is not None:
            if update.message is not None:
                tg_id = update.message.from_user.id
                command = update.message.text
                logging.info(f"Error occured - TG_ID={tg_id}, TEXT=`{command}`")
                await update.message.reply_text(reply)
            else:
                tg_id = update.callback_query.from_user.id
                data = update.callback_query.data
                logging.info(f"Error occured - TG_ID={tg_id}, CALLBACK_DATA={data}")
                await update.callback_query.message.reply_text(reply)
