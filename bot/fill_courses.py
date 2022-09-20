"""Run this to fill data base with courses info."""

import os
import pandas as pd

# this setup must be done before importing django models
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "botback.settings.dev")
django.setup()

from panel.models import Course


def fill_courses():
    table = pd.read_csv('bot/text_data/cources/cources.csv', dtype=str)

    for i in range(table.shape[0]):
        name = table.loc[i, 'txt_short']
        with open('bot/text_data/cources/' + table.loc[i, 'txt_long'], 'r') as f:
            description = ''.join(f.readlines())
        who = table.loc[i, 'who']
        where = table.loc[i, 'where']
        day = table.loc[i, 'when']
        time = table.loc[i, 'time']
        img_path = table.loc[i, 'image_path']
        order = i

        course = Course(name=name,
                        description=description,
                        who=who,
                        where=where,
                        day=day,
                        time=time,
                        img_path=img_path,
                        order=order)
        course.save()


if __name__ == "__main__":
    fill_courses()
