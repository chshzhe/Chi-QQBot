from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult

from plugins.sell_vegetable.corpus import Corpus

corpus = Corpus()
corpus.update()

question_words = ["为什么", "怎么", "如何", "怎样", "教我"]


@on_command('sell', aliases=('卖弱',))
async def cmd_sell(session: CommandSession):
    await session.send(corpus.get_rnd_common())


@on_natural_language(corpus.trigger, only_to_me=False)
async def auto_sell(session: NLPSession):
    return NLPResult(80.0, ('sell',), None)


@on_natural_language(question_words)
async def auto_refuse(session: NLPSession):
    await session.send(corpus.get_rnd_refuse())
