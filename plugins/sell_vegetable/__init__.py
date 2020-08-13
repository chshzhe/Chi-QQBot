from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult, scheduler

from plugins.sell_vegetable.corpus import Corpus

corpus = Corpus()
corpus.load_from_dir('data')

question_words = ["为什么", "怎么", "如何", "怎样", "教我"]


@scheduler.scheduled_job('interval', hours=2)
async def update_corpus():
    await corpus.update()


@on_command('sell', aliases=('卖弱',))
async def cmd_sell(session: CommandSession):
    await session.send(corpus.get_rnd_common())


@on_natural_language(corpus.trigger, only_to_me=True)
async def auto_sell(session: NLPSession):
    return NLPResult(80.0, ('sell',), None)


@on_natural_language(question_words, only_to_me=True)
async def auto_refuse(session: NLPSession):
    await session.send(corpus.get_rnd_refuse())
