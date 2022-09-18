import os

# this must be done before importing django models
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

if __name__ == '__main__':
    TOKEN = os.environ.get('TG_TOKEN')
    persistence = PicklePersistence('dump.pickle')
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
