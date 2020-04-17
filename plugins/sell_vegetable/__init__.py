import random

from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult

from config import GROUPS

text_list = ['我好菜啊', '我菜爆了', '我是什么垃圾', '我好堕落',
             '我好菜菜啊 再这样下去就没人要了 我就只能混吃等死了',
             '我越来越觉得自己是废物一个', '我想要有大佬带', '哭哭',
             '我现在啥也不想干', '求大佬带我', '💩', '我好废物啊',
             '[CQ:face,id=111]', '[CQ:face,id=67]']
refuse_list = ['哦', '冷漠', '不知道.jpg']
key_words = {'菜', '太强了', 'tql', 'cxs', 'ddw', '带带我', '迟先生', '吃先生'}


@on_command('sell', aliases=('卖弱',))
async def cmd_sell(session: CommandSession):
    await session.send(random.choice(text_list))


@on_command('refuse')
async def cmd_refuse(session: CommandSession):
    await session.send(random.choice(refuse_list))


@on_natural_language(key_words, only_to_me=False)
async def auto_sell(session: NLPSession):
    if session.event.group_id in GROUPS:
        return NLPResult(80.0, ('sell',), None)
