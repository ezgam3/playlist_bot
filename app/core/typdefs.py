from dataclasses import dataclass
from typing import NamedTuple

from pendulum.datetime import DateTime


class TimeInterval(NamedTuple):
    start: DateTime
    end: DateTime


@dataclass
class PlaylistData:
    author_name: str
    author_telegram_id: int
    link: str
    description: str
