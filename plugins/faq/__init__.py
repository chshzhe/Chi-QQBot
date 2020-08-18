import json
from typing import List

from nonebot import on_command, CommandSession

__plugin_name__ = '自助答疑'
__plugin_usage__ = r"""自助答疑

分流 电院/工试 [排名]
问 [内容]
"""

ep = [('电子信息与电气工程学院', 670), ('机械与动力工程学院', 880), ('船舶海洋与建筑工程学院', 1180),
      ('材料科学与工程学院', 1080), ('生物医学工程学院', 930), ('海洋学院', 1150), ('航空航天学院', 1100)]
seiee = [('计算机科学与技术', 90), ('软件工程', 300), ('信息安全', 250),
         ('信息工程', 450), ('自动化', 300), ('电气工程及其自动化', 580),
         ('电子科学与技术', 510), ('微电子科学与工程', 580), ('测控技术与仪器', 630)]


def query_rank(query_type: str, rank: int) -> List[str]:
    res_list = []
    if query_type == '工试':
        res_list = [item[0] for item in ep if item[1] > rank]
    if query_type == '电院':
        res_list = [item[0] for item in seiee if item[1] > rank]
    return res_list


@on_command('divide', aliases=('分流',), only_to_me=True)
async def _(session: CommandSession):
    try:
        query_type, rank = session.current_arg_text.strip().split(' ')
        rank = int(rank)
    except ValueError:
        await session.send('命令格式错误。命令格式为：分流 工试/电院 排名\n例如：\n分流 工试 1\n分流 电院 1')
        return
    res_list = query_rank(query_type, rank)
    qq = session.event.user_id
    msg = f'[CQ:at,qq={qq}] 根据去年收集的数据（已做模糊化处理），你的排名有希望进入：\n'
    for res in res_list:
        msg = msg + res + '\n'
    warn = '以上内容仅供参考，Bot对今年情况概不负责！'
    msg = msg + warn
    await session.send(msg)
    if rank < 100:
        await session.send('你已经很强了，不要再学了，带带我吧')
    elif rank < 500:
        await session.send('你已经是顶级选手了，不要再虐我了，快来 CS 带带我吧')
    else:
        await session.send('以后转专业，快来 CS 带带我这个老废物吧')


faq = {'帮助': '@Bot并输入：问 [内容]'}


def load_faq():
    global faq
    with open('data/faq.json', mode='r', encoding='utf-8') as f:
        faq = json.load(f)


load_faq()


@on_command('query', aliases=('问',), only_to_me=True)
async def _(session: CommandSession):
    question = session.current_arg_text.strip()
    ans = faq.get(question)
    if not ans:
        await session.send('未能查询到相关信息')
    else:
        await session.send(ans)


@on_command('add', aliases=('添加',), only_to_me=True)
async def _(session: CommandSession):
    question, ans = session.current_arg_text.strip().split('#')
    faq[question] = ans
    with open('data/faq.json', mode='w', encoding='utf-8') as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)
    await session.send('已添加到问题库')


@on_command('delete', aliases=('删除',), only_to_me=True)
async def _(session: CommandSession):
    question = session.current_arg_text.strip()
    if faq.get(question):
        del faq[question]
    with open('data/faq.json', mode='w', encoding='utf-8') as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)
    await session.send(f'已删除{question}')


@on_command('load_faq', only_to_me=True)
async def _(session: CommandSession):
    load_faq()
    await session.send('已重新加载问题库')


@on_command('all', aliases=('所有问题',), only_to_me=True)
async def _(session: CommandSession):
    msg = '当前支持提问的内容有：\n\n'
    for item in faq.keys():
        msg = msg + item + '\n'
    await session.send(msg)
