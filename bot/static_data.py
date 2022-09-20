import logging
from collections import namedtuple
from pathlib import Path

StaticData = namedtuple("StaticData",
                        ["images", "texts"])


def collect_static(prefix: str) -> StaticData:
    logging.info(f"Collecting static from `{prefix}`")
    texts = {}
    for path in Path(prefix).rglob("*.txt"):
        with open(path) as f:
            texts[path.name] = f.read()

    images = {}
    for path in Path(prefix).rglob("*.jpg"):
        with open(path, "rb") as f:
            images[path.name] = f.read()

    logging.info(f"Collected {len(texts)} texts, {len(images)} images")
    return StaticData(texts=texts, images=images)
