import argparse
import logging
import os
from typing import Dict, Tuple

# this setup must be done before importing django models
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "botback.settings.dev")
django.setup()

from telegram.ext import (Application, CommandHandler, ConversationHandler,
                          MessageHandler, filters, PicklePersistence, CallbackQueryHandler)

from bot.conversation_manager import ConversationManager
from bot.database_manager import DatabaseManager
from bot.static_data import collect_static

TOKEN = os.environ.get("TG_TOKEN")
if TOKEN is None:
    raise RuntimeError("Telegram Bot API token not found "
                       "(environment variable `TG_TOKEN` must be set)")

CONVERSATION_DUMP = "conversation.pickle"
STATIC_PREFIX = "bot/static"


def build_app() -> Application:
    persistence = PicklePersistence(CONVERSATION_DUMP)
    app = Application.builder().concurrent_updates(False)\
        .persistence(persistence).token(TOKEN).build()

    static = collect_static(STATIC_PREFIX)
    db_manager = DatabaseManager()
    conv = ConversationManager(db_manager, static)

    app.add_handler(ConversationHandler(
        name="convhandler",
        entry_points=[
            CommandHandler("start", conv.start),
        ],
        allow_reentry=False,
        states= {
            ConversationManager.State.ADMIN: [
                CommandHandler("registered", conv.admin.registered),
                CommandHandler("messages", conv.admin.messages),
                CommandHandler("scheduled", conv.admin.scheduled),
                CommandHandler("sendall", conv.admin.send_all),
            ],
            ConversationManager.State.REGISTER_NAME: [
                MessageHandler(filters.TEXT & (~ filters.COMMAND), conv.register_name),
            ],
            ConversationManager.State.REGISTER_SURNAME: [
                MessageHandler(filters.TEXT & (~ filters.COMMAND), conv.register_surname),
            ],
            ConversationManager.State.REGISTER_GROUPID: [
                MessageHandler(filters.TEXT & (~ filters.COMMAND), conv.register_groupid),
            ],
            ConversationManager.State.MAIN_MENU: [
                CallbackQueryHandler(conv.about, pattern='^about$'),
                CallbackQueryHandler(conv.join, pattern='^join$'),
                CallbackQueryHandler(conv.call, pattern='^call$'),
                CallbackQueryHandler(conv.menu, pattern='^menu$'),
                CallbackQueryHandler(conv.courses, pattern='^courses')],
        },
        conversation_timeout=None,
        persistent=True,
        fallbacks=[
            CommandHandler("stop", conv.stop),
            CommandHandler("admin", conv.admin.on),
        ],
    ))

    app.add_error_handler(conv.error)

    return app


def parse_args():
    parser = argparse.ArgumentParser(description="Run Telegram Bot polling")
    parser.add_argument("--clear",
                        "-c",
                        action="store_true",
                        help="Clear all conversation states.")
    parser.add_argument("--verbose",
                        "-v",
                        action="store_true",
                        help="Verbosity level.")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.clear:
        try:
            os.remove(CONVERSATION_DUMP)
        except FileNotFoundError:
            pass

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO
    )

    app = build_app()
    app.run_polling()


if __name__ == "__main__":
    main()
