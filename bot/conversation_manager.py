import logging
from enum import Enum, auto
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from .admin_convertation_manager import AdminConversationManager
from .database_manager import DatabaseManager

import logging
from enum import Enum, auto
from typing import Dict, Union

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from telegram import (InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)


class ConversationManager:
    """Handlers for conversation."""

    class State(Enum):
        """Conversation state."""

        ADMIN = auto()
        """Admin mode is ON. One can access admin commands now."""

        MAIN_MENU = auto()
        """Main menu panel."""

        REGISTER_NAME = auto()
        """Enter user name."""

        REGISTER_SURNAME = auto()
        """Enter user surname."""

        REGISTER_GROUPID = auto()
        """Enter user phystech group id."""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self.admin = AdminConversationManager(self)

    async def start(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        logging.info(f"Started conversation - TG_ID={tg_id}")

        user = await self.db.get_user(tg_id)
        if user is None:
            # await update.message.reply_text("Привет, введи свое имя и фамилию:")
            await update.message.reply_text(''.join(open('bot/text_data/start_hello_get_name.txt', 'r').readlines()))
            return self.State.REGISTER_NAME
        
        await update.message.reply_text(f"Привет, {user.name}")
        # # TODO: return main menu markup here
        return await self.menu_no_getting(update, context)  #self.State.MAIN_MENU    

    async def stop(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        logging.info(f"Stopped conversation - TG_ID={tg_id}")

        await update.message.reply_text(
            "Вы отключились от бота!\n\nЧтобы в дальнейшем получать оповещения,"
            " нужно будет снова использовать /start)"
        )
        return ConversationHandler.END

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

    async def register_name(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        name = update.message.text
        logging.info(f"Registering user - TG_ID={tg_id} NAME={name}")

        await self.db.add_user(tg_id, name)
        user = await self.db.get_user(tg_id)

        await update.message.reply_text(f"Приятно познакомиться, {user.name} :) \n А какая у тебя фамилия?")
        return self.State.REGISTER_SURNAME

    async def register_surname(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        surname = update.message.text
        logging.info(f"Add user info - TG_ID={tg_id} SURNAME={surname}")

        # ADD SURNAME
        await self.db.update_user(tg_id, surname=surname)

        await update.message.reply_text(f''.join(open('bot/text_data/start_get_group_id.txt', 'r').readlines()))
        return self.State.REGISTER_GROUPID

    async def register_groupid(self, update: Update, context: CallbackContext):
        tg_id = update.message.from_user.id
        group_id = update.message.text
        logging.info(f"Add user info - TG_ID={tg_id} GROUPID={group_id}")

        # ADD GROUPID
        await self.db.update_user(tg_id, group_id=group_id)

        menu = [
            [
                InlineKeyboardButton("Что такое Мастерская?", callback_data='about')
                ],
            [
                InlineKeyboardButton("Расписание", callback_data='timetable'),
                InlineKeyboardButton("Записаться на курсы", callback_data='join')
                ],
            [
                InlineKeyboardButton("Выбранные курсы", callback_data='check'),
                InlineKeyboardButton("Связаться с организатором", callback_data='call')
                ]
        ]
        reply_markup = InlineKeyboardMarkup(menu)
        reply = f"Мы тебя зарегистрировали! Теперь ты можешь пользоваться нашим ботом :) \n Читай про курсы и записывайся на занятия!"
        await update.message.reply_text(f''.join(open('bot/text_data/start_intro_to_menu.txt', 'r').readlines()), reply_markup=reply_markup)
        return self.State.MAIN_MENU

    async def menu_no_getting(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        menu = [
            [
                InlineKeyboardButton("Что такое Мастерская?", callback_data='about'),
                # InlineKeyboardButton("Расписание", callback_data='timetable'),
                InlineKeyboardButton("Записаться на курсы", callback_data='join')
                ],
            [
                InlineKeyboardButton("Выбранные курсы", callback_data='check'),
                InlineKeyboardButton("Связаться с организатором", callback_data='call')
                ]
        ]
        reply_markup = InlineKeyboardMarkup(menu)
        reply = f"Читай про курсы и записывайся на занятия!"
        await update.message.reply_text(text=reply, reply_markup=reply_markup)
        return self.State.MAIN_MENU

    async def menu(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        query = update.callback_query
        
        await query.answer()
        menu = [
            [
                InlineKeyboardButton("Что такое Мастерская?", callback_data='about'),
                # InlineKeyboardButton("Расписание", callback_data='timetable'),
                InlineKeyboardButton("Записаться на курсы", callback_data='join')
                ],
            [
                InlineKeyboardButton("Выбранные курсы", callback_data='check'),
                InlineKeyboardButton("Связаться с организатором", callback_data='call')
                ]
        ]
        reply_markup = InlineKeyboardMarkup(menu)
        reply = f"Читай про курсы и записывайся на занятия!"
        await query.edit_message_text(
            text=reply, reply_markup=reply_markup
        ) 
        return self.State.MAIN_MENU

    async def about(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        query = update.callback_query
        
        await query.answer()
        reply = ''.join(open('bot/text_data/menu_description.txt', 'r').readlines())
        
        keyboard = [
            [InlineKeyboardButton("Записаться на курс", callback_data='join')],
            [InlineKeyboardButton("Вернуться в меню", callback_data='menu')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=reply, reply_markup=reply_markup
        ) 
        return self.State.MAIN_MENU
    
    async def call(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        query = update.callback_query
        
        await query.answer()
        reply = ''.join(open('bot/text_data/menu_call.txt', 'r').readlines())
        
        keyboard = [
            [InlineKeyboardButton("Вернуться в меню", callback_data='menu')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=reply, reply_markup=reply_markup
        ) 
        return self.State.MAIN_MENU

    async def join(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        query = update.callback_query
        await query.answer()
        reply = ''.join(open('bot/text_data/menu_join.txt', 'r').readlines())
        
        keyboard = []
        
        courses = sorted(await self.db.get_all_cousres(), key=lambda elem: elem.order)        
        for course in courses:

            name = course.name
            when = course.day
            time = course.time

            text = f'{name}\t\t{when}\t{time}'
            
            button = InlineKeyboardButton(text, callback_data='courses '+str(course.order))
            keyboard.append([button])
        keyboard.append([InlineKeyboardButton("Вернуться в меню", callback_data='menu')])

        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
        await query.edit_message_text(
            text=reply, reply_markup=reply_markup
        ) 

        return self.State.MAIN_MENU

    async def courses(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
        
        query = update.callback_query
        print(query.data)
        order = int(query.data[8:])
        await query.answer()

        course = sorted(await self.db.get_all_cousres(), key=lambda elem: elem.order)[order]
        
        keyboard = [
            [InlineKeyboardButton("Записаться на этот курс", callback_data='register_question')],
            [InlineKeyboardButton("Хочу на актёрку, но не могу в это время", callback_data='menu')],
            [InlineKeyboardButton("Назад в меню", callback_data='menu')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
        reply = f"Описание {order}"

        photo_path = 'bot/text_data/cources/photo/' + course.img_path
        print(photo_path)
        
        await query.message.reply_photo(photo=open(photo_path, 'rb'), caption=reply, reply_markup=reply_markup) 
        return self.State.MAIN_MENU