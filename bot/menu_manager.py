from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ContextTypes

from .database_manager import DatabaseManager
from .static_data import StaticData


class CallbackData:
    """Callback data values."""

    about = "about"
    apply = "apply"
    contacts = "contacts"
    course = "course"
    main = "main"
    mycourses = "mycourses"
    remove = "remove"
    select = "select"


class Buttons:
    """All existing buttons."""

    about = InlineKeyboardButton("Что такое Мастерская?",
                                 callback_data=CallbackData.about)
    apply = InlineKeyboardButton("Записаться на курс",
                                 callback_data=CallbackData.apply)
    contacts = InlineKeyboardButton("Связаться с организатором",
                                   callback_data=CallbackData.contacts)
    main = InlineKeyboardButton("Вернуться в меню",
                                callback_data=CallbackData.main)
    mycourses = InlineKeyboardButton("Выбранные курсы",
                                     callback_data=CallbackData.mycourses)


class MenuManager:
    """Handlers for menu buttons."""

    def __init__(self, base):
        self.base = base

    @property
    def db(self) -> DatabaseManager:
        return self.base.db

    @property
    def State(self):
        return self.base.State

    @property
    def static(self) -> StaticData:
        return self.base.static

    keyboards = {
        "default": InlineKeyboardMarkup([
            [ Buttons.about, Buttons.apply ],
            [ Buttons.mycourses, Buttons.contacts ],
        ]),
        "about": InlineKeyboardMarkup([
            [ Buttons.apply ],
            [ Buttons.main ],
        ]),
        "contacts": InlineKeyboardMarkup([
            [ Buttons.main ]
        ]),
    }

    async def default(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_photo(
            photo=self.static.images["Фиолетовая_мастерская.jpeg"],
            caption="Читай про курсы и записывайся на занятия!",
            reply_markup=self.keyboards["default"]
        )

    async def intro(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            text=self.static.texts["start_intro_to_menu.txt"],
            reply_markup=self.keyboards["default"],
        )

    async def main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_photo(
            self.static.images["Фиолетовая_мастерская.jpeg"],
            caption="Читай про курсы и записывайся на занятия!",
            reply_markup=self.keyboards["default"]
        )
        return self.State.MENU_MAIN

    async def about(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_text(
            self.static.texts["menu_description.txt"],
            reply_markup=self.keyboards["about"],
        )
        return self.State.MENU_ABOUT

    async def contacts(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_text(
            self.static.texts["menu_call.txt"],
            reply_markup=self.keyboards["contacts"]
        )
        return self.State.MENU_CONTACTS

    async def apply(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        courses = sorted(await self.db.get_all_cousres(), key=lambda elem: elem.order)
        keyboard = []
        for course in courses:
            text = f'{course.name}\t\t{course.day}\t{course.time}'
            button = InlineKeyboardButton(
                text,
                callback_data=f"{CallbackData.course}_{course.id}"
            )
            keyboard.append([ button ])
        keyboard.append([ Buttons.main ])

        reply_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True)

        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_photo(
            self.static.images["Фиолетовая_мастерская.jpeg"],
            # caption=self.static.texts["menu_join.txt"],
            reply_markup=reply_markup
        )
        return self.State.MENU_APPLY

    async def course(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        tg_id = query.from_user.id
        applications = [apl.course_id for apl in await self.db.get_applications(tg_id)]
        course_id = int(query.data.replace(f"{CallbackData.course}_", ""))
        is_applied = course_id in applications
        await query.answer()

        course = await self.db.get_course(course_id)

        if is_applied:
            button = InlineKeyboardButton(
                "Покинуть этот курс",
                callback_data=f"{CallbackData.remove}_{course_id}"
            )
        else:
            button = InlineKeyboardButton(
                "Записаться на этот курс",
                callback_data=f"{CallbackData.select}_{course_id}"
            )
        keyboard = [
            [ button ],
            [ Buttons.main ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True)

        await update.callback_query.message.edit_media(
            InputMediaPhoto(self.static.images[course.img_path])
        )
        await update.callback_query.message.edit_caption(
            caption=course.description[:1023],
            reply_markup=reply_markup,
        )
        return self.State.MENU_COURSE

    async def select(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        tg_id = query.from_user.id
        applications = [apl.course_id for apl in await self.db.get_applications(tg_id)]
        course_id = int(query.data.replace(f"{CallbackData.select}_", ""))

        if course_id not in applications:
            course = await self.db.get_course(course_id)
            user = await self.db.get_user(tg_id)
            await self.db.add_application(user, course)

            button = InlineKeyboardButton(
                "Покинуть этот курс",
                callback_data=f"{CallbackData.remove}_{course_id}"
            )
            keyboard = [
                [ button ],
                [ Buttons.main ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True)
            await update.callback_query.message.edit_reply_markup(reply_markup)

            await query.answer(f"Вы записались на курс {course.name}")

    async def remove(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        tg_id = query.from_user.id
        applications = [apl.course_id for apl in await self.db.get_applications(tg_id)]
        course_id = int(query.data.replace(f"{CallbackData.remove}_", ""))

        if course_id in applications:
            await self.db.delete_application(tg_id, course_id)
            course = await self.db.get_course(course_id)

            button = InlineKeyboardButton(
                "Записаться на этот курс",
                callback_data=f"{CallbackData.select}_{course_id}"
            )
            keyboard = [
                [ button ],
                [ Buttons.main ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True)
            await update.callback_query.message.edit_reply_markup(reply_markup)

            await query.answer(f"Вы покинули курс {course.name}")

    async def mycourses(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        tg_id = query.from_user.id
        applications = [apl.course_id for apl in await self.db.get_applications(tg_id)]

        if len(applications) == 0:
            caption = "Вы пока не записались ни на один курс."
        else:
            caption = None

        courses = [await self.db.get_course(course_id) for course_id in applications]

        keyboard = []
        for course in courses:
            text = f'{course.name}\t\t{course.day}\t{course.time}'
            button = InlineKeyboardButton(
                text,
                callback_data=f"{CallbackData.course}_{course.id}"
            )
            keyboard.append([ button ])

        keyboard.append([ Buttons.main ])

        reply_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True)

        await update.callback_query.answer()
        await update.callback_query.delete_message()
        await update.callback_query.message.reply_photo(
            self.static.images["Фиолетовая_мастерская.jpeg"],
            caption=caption,
            reply_markup=reply_markup
        )
        return self.State.MENU_MYCOURSES
