#导入部分
import asyncio
import re
import nonebot
from nonebot.adapters.onebot.v11 import Message, MessageSegment,Bot,MessageEvent
from nonebot import require
from nonebot.plugin.on import on_keyword, on_startswith

from nonebot_plugin_apscheduler import scheduler
require("nonebot_plugin_apscheduler")

#全局变量
money_ask_msg = MessageSegment.at(2517519695) + Message(" 我的喵币")
group_id_tr = 1045286266
money = None
quantities = { '猫砂盆': 0,'小鱼干': 0, '猫抓板': 0, '逗猫棒': 0, '约会券': 0}

#发送函数
async def send_message_catlitterbox():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message="购买猫砂盆")
    await asyncio.sleep(2)
    await bot.send_group_msg(group_id=group_id_tr, message="赠送猫砂盆")
    await asyncio.sleep(2)
async def send_message_stockfish():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message="购买小鱼干")
    await asyncio.sleep(2)
    await bot.send_group_msg(group_id=group_id_tr, message="赠送小鱼干")
    await asyncio.sleep(2)
async def send_message_scratchers():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message="购买猫抓板")
    await asyncio.sleep(2)
    await bot.send_group_msg(group_id=group_id_tr, message="赠送猫抓板")
    await asyncio.sleep(2)
async def send_message_catstick():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message="购买逗猫棒")
    await asyncio.sleep(2)
    await bot.send_group_msg(group_id=group_id_tr, message="赠送逗猫棒")
    await asyncio.sleep(2)
async def send_message_appointment():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message="购买约会券")
    await asyncio.sleep(2)
    await bot.send_group_msg(group_id=group_id_tr, message="赠送约会券")
    await asyncio.sleep(2)



#商品最优期望计算函数
def favor_counter_function(budget):
    global quantities
    goods = [('猫砂盆', 5 / 10, 10),
             ('小鱼干', 3 / 6, 6),
             ('猫抓板', 4 / 14, 14),
             ('逗猫棒', 15 / 25, 25),
             ('约会券', 80 / 100, 100)]
    goods.sort(key=lambda x: x[1], reverse=True)
    quantities = { '猫砂盆': 0,'小鱼干': 0, '猫抓板': 0, '逗猫棒': 0, '约会券': 0}
    budget_int = int(budget)
    for good in goods:
        name, _, price = good
        max_quantity = budget_int // price
        quantities[name] = max_quantity
        budget_int -= max_quantity * price
    return quantities

#定时发信模块
@scheduler.scheduled_job('interval', minutes=90)
async def auto_work_main_function():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=group_id_tr, message=money_ask_msg)

#购买并赠送发信模块
get_money_value = on_keyword("您现在有")
@get_money_value.handle()
async def get_money_main_function(bot: Bot,event: MessageEvent):
    global money, quantities
    if str(event.user_id) == "2517519695":
        text_ache = event.get_message().extract_plain_text()
        if "小夏" in text_ache:
            match = re.search(r'\d+', text_ache)
            if match:
                money = match.group()
            else:
                money = None
            favor_counter_function(money)
            quantities = favor_counter_function(money)

        for _ in range(quantities['猫砂盆']):
            await send_message_catlitterbox()
        for _ in range(quantities['小鱼干']):
            await send_message_stockfish()
        for _ in range(quantities['猫抓板']):
            await send_message_scratchers()
        for _ in range(quantities['逗猫棒']):
            await send_message_catstick()
        for _ in range(quantities['约会券']):
            await send_message_appointment()
