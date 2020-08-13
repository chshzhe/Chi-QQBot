import random
from dataclasses import dataclass, field
from typing import List

from httpx import AsyncClient
from nonebot import logger

BASE_URL = "https://raw.githubusercontent.com/Chi-Task-Force/Chi-Corpus/master"


@dataclass
class Corpus:
    common: List[str] = field(default_factory=list)
    refuse: List[str] = field(default_factory=list)
    trigger: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.http = AsyncClient()

    async def update(self):
        common_words = (await self.http.get(f"{BASE_URL}/common.txt")).text.strip().split("\n")
        qq_emoji = (await self.http.get(f"{BASE_URL}/qq_emoji.txt")).text.strip().split("\n")
        self.common = common_words + qq_emoji
        self.refuse = (await self.http.get(f"{BASE_URL}/refuse.txt")).text.strip().split("\n")
        self.trigger = (await self.http.get(f"{BASE_URL}/trigger.txt")).text.strip().split("\n")

    def get_rnd_common(self):
        return random.choice(self.common)

    def get_rnd_refuse(self):
        return random.choice(self.refuse)

    def load_from_dir(self, dirname):
        try:
            with open(f'{dirname}/common.txt', mode='r', encoding='utf-8') as f:
                self.common = [line.strip() for line in f.readlines()]
            with open(f'{dirname}/trigger.txt', mode='r', encoding='utf-8') as f:
                self.trigger = [line.strip() for line in f.readlines()]
            with open(f'{dirname}/refuse.txt', mode='r', encoding='utf-8') as f:
                self.refuse = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            logger.warn('本地语料库加载失败')
