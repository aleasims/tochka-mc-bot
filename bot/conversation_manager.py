import logging

from enum import Enum, auto
from sre_parse import State
from asgiref.sync import sync_to_async

from telegram import Update
from telegram.ext import ContextTypes

from .database_manager import DatabaseManager

class ConversationManager:
    class State(Enum):
        """Conversation state."""

        REGISTRATION = auto()
        """Waiting for user name/surname."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def start(self, update: Update, context: ContextTypes):
        logging.info(f'Started conversation with {update.message.chat_id}')
        await update.message.reply_text("Привет, введи свое имя и фамилию:")
        return self.State.REGISTRATION

    async def register(self, update: Update, context: ContextTypes):
        logging.info(f'Registering user {update.message.chat_id} with name {update.message.text}')
