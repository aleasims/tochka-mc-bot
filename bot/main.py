import os

# this setup must be done before importing django models
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'botback.settings.dev')
django.setup()

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from telegram.ext import (Application, CommandHandler, ConversationHandler,
                          MessageHandler, filters, PicklePersistence)

from bot.conversation_manager import ConversationManager
from bot.database_manager import DatabaseManager

TOKEN = os.environ.get('TG_TOKEN')
if TOKEN is None:
    raise RuntimeError("Telegram Bot API token not found (env variable `TG_TOKEN` must be set")

CONVERSATION_DUMP = 'dump.pickle'

if __name__ == '__main__':
    persistence = PicklePersistence(CONVERSATION_DUMP)
    app = Application.builder().concurrent_updates(False).persistence(persistence).token(TOKEN).build()

    db_manager = DatabaseManager()
    c_manager = ConversationManager(db_manager)

    app.add_handler(ConversationHandler(
        name="convhandler",
        entry_points=[CommandHandler('start', c_manager.start)],
        states= {
            ConversationManager.State.REGISTRATION: [
                MessageHandler(filters.TEXT, c_manager.register),
            ],
        },
        conversation_timeout=None,
        persistent=True,
        fallbacks=[],
    ))

    app.run_polling()
