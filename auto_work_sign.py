import asyncio

import nonebot
from nonebot import on_command,require
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot
from nonebot_plugin_apscheduler import scheduler
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
require("nonebot_plugin_apscheduler")

config = {
    "target_user_id": 2517519695,
    "group_id": 1045286266,
    "enable_auto_work": True,
    "enable_auto_buy": True
}

auto_work_message = MessageSegment.at(config["target_user_id"]) + Message(' 打工')
auto_sign_message = MessageSegment.at(config["target_user_id"]) + Message(' 签到')
auto_buy_message = Message('购买猫砂盆')
auto_present_message = Message('赠送猫砂盆')

ask_auto_work = on_command("自动打工状态", rule=to_me(), permission=SUPERUSER)
close_auto_work = on_command("自动打工关", rule=to_me(), permission=SUPERUSER)
start_auto_work = on_command("自动打工开", rule=to_me(), permission=SUPERUSER)
ask_auto_buy = on_command("自动购买状态", rule=to_me(), permission=SUPERUSER)
close_auto_buy = on_command("自动购买关", rule=to_me(), permission=SUPERUSER)
start_auto_buy = on_command("自动购买开", rule=to_me(), permission=SUPERUSER)

@ask_auto_work.handle()
async def ask_auto_work_function():
    global config
    if config["enable_auto_work"]:
        await ask_auto_work.finish("自动打工启用中")
    else:
        await ask_auto_work.finish("自动打工禁用中")

@ask_auto_buy.handle()
async def ask_auto_buy_function():
    global config
    if config["enable_auto_buy"]:
        await ask_auto_buy.finish("自动购买启用中")
    else:
        await ask_auto_buy.finish("自动购买禁用中")

@close_auto_work.handle()
async def close_function():
    global config
    config["enable_auto_work"] = False
    await close_auto_work.finish("停止自动打工了喵")

@start_auto_work.handle()
async def start_function():
    global config
    config["enable_auto_work"] = True
    await start_auto_work.finish("开始自动打工了喵")

@close_auto_buy.handle()
async def close_auto_buy_function():
    global config
    config["enable_auto_buy"] = False
    await close_auto_buy.finish("停止自动购买了喵")

@start_auto_buy.handle()
async def start_auto_buy_function():
    global config
    config["enable_auto_buy"] = True
    await start_auto_buy.finish("开始自动购买了喵")

async def send_group_message(bot: Bot, group_id: int, message: Message):
    try:
        await bot.send_group_msg(group_id=group_id, message=message)
    except Exception as e:
        print(f"发送消息失败: {e}")

@scheduler.scheduled_job('interval', minutes=61, id='send_group_message')
async def auto_work_main_function():
    global config
    bot = nonebot.get_bot()
    if config["enable_auto_work"]:
        await send_group_message(bot, config["group_id"], auto_work_message)
        await asyncio.sleep(5)
        await send_group_message(bot, config["group_id"], auto_buy_message)
        await asyncio.sleep(5)
        await send_group_message(bot, config["group_id"], auto_present_message)

@scheduler.scheduled_job('cron', hour=0, minute=5)
async def auto_sign_main_function():
    global config
    bot = nonebot.get_bot()
    if config["enable_auto_work"]:
        await send_group_message(bot, config["group_id"], auto_sign_message)



