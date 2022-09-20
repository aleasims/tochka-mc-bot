from distutils import extension
import logging
from collections import namedtuple
from pathlib import Path

TYPES = ["images", "texts"]

EXTENSIONS = {
    "images": ["jpg", "jpeg", "png"],
    "texts": ["txt"],
}

MODES = {
    "images": "rb",
    "texts": "r",
}

StaticData = namedtuple("StaticData", TYPES)


def collect_static(prefix: str) -> StaticData:
    logging.info(f"Collecting static from `{prefix}`")

    data = {}

    for type_ in TYPES:
        data[type_] = {}
        for ext in EXTENSIONS[type_]:
            for path in Path(prefix).rglob(f"*.{ext}"):
                with open(path, MODES[type_]) as f:
                    data[type_][path.name] = f.read()

    n = sum(len(values) for values in data.values())
    logging.info(f"Collected {n} items")
    return StaticData(**data)
