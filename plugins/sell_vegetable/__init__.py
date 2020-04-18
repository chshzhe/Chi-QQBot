import random
from time import sleep

from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult, scheduler

import config
from plugins.sell_vegetable.corpus import Corpus

corpus = Corpus()
corpus.update()

question_words = ["为什么", "怎么", "如何", "怎样", "教我"]


@scheduler.scheduled_job('interval', minutes=10)
async def update_corpus():
    corpus.update()


@on_command('sell', aliases=('卖弱',))
async def cmd_sell(session: CommandSession):
    await session.send(corpus.get_rnd_common())


@on_natural_language(corpus.trigger, only_to_me=False)
async def auto_sell(session: NLPSession):
    if config.ENABLE_RANDOM_DELAY:
        sleep(random.random() * config.MAX_DELAY_TIME)
    return NLPResult(80.0, ('sell',), None)


@on_natural_language(question_words)
async def auto_refuse(session: NLPSession):
    if config.ENABLE_RANDOM_DELAY:
        sleep(random.random() * config.MAX_DELAY_TIME)
    await session.send(corpus.get_rnd_refuse())
