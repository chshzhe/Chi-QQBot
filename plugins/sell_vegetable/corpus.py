import random
from dataclasses import dataclass, field
from typing import List

import requests

BASE_URL = "https://raw.githubusercontent.com/Chi-Task-Force/Chi-Corpus/master"
qq_emoji = ['[CQ:face,id=111]', '[CQ:face,id=67]']


@dataclass
class Corpus:
    common: List[str] = field(default_factory=list)
    refuse: List[str] = field(default_factory=list)
    trigger: List[str] = field(default_factory=list)

    def update(self):
        self.common = (requests.get(f"{BASE_URL}/common.txt")).text.strip().split("\n") + qq_emoji
        self.refuse = (requests.get(f"{BASE_URL}/refuse.txt")).text.strip().split("\n")
        self.trigger = (requests.get(f"{BASE_URL}/trigger.txt")).text.strip().split("\n")

    def get_rnd_common(self):
        return random.choice(self.common)

    def get_rnd_refuse(self):
        return random.choice(self.refuse)
