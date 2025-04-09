import nonebot
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageEvent, Bot,Message
from src.plugins.nonebot_plugin_apscheduler import scheduler


AUTO_ROB_ENABLED = False
TARGET_ID = "无目标"
GROUP_ID = 207596549
GROUP_NAME = "AITFS"

close_auto_rob = on_command("自动打劫关", rule=to_me(), permission=SUPERUSER)
start_auto_rob = on_command("自动打劫开", rule=to_me(), permission=SUPERUSER)
group_switch = on_command("自动打劫群聊切换", rule=to_me(), permission=SUPERUSER)
ask_auto_rob = on_command("自动打劫状态", rule=to_me(), permission=SUPERUSER)
auto_rob_command = on_command("自动打劫", rule=to_me(), permission=SUPERUSER)


async def update_status(bot: Bot, event: MessageEvent, status: bool, message: str):
    global AUTO_ROB_ENABLED
    AUTO_ROB_ENABLED = status
    await bot.send(event, message)

@close_auto_rob.handle()
async def close_auto_rob_function(bot: Bot, event: MessageEvent):
    await update_status(bot, event, False, "停止自动打劫了喵")

@start_auto_rob.handle()
async def start_auto_rob_function(bot: Bot, event: MessageEvent):
    await update_status(bot, event, True, "开始自动打劫了喵")

@group_switch.handle()
async def group_switch_function():
    pass

@group_switch.got("group_name", prompt="请指定群聊")
async def got_location(bot: Bot, event: MessageEvent):
    global GROUP_ID
    group_name = event.get_message().extract_plain_text()
    group_id_mapping = {
        "MC群": 830398487,
        "泰拉群": 1045286266,
        "AITFS": 207596549,
    }
    GROUP_ID = group_id_mapping.get(group_name, None)
    if GROUP_ID:
        await bot.send(event, f"群聊已设置为{group_name}:{GROUP_ID}")
    else:
        await bot.send(event, "未识别的群聊名称，请重新输入。")

@ask_auto_rob.handle()
async def ask_auto_rob_function(bot: Bot, event: MessageEvent):
    global AUTO_ROB_ENABLED, TARGET_ID
    ask_reply_msg_true = Message(' 自动打劫启用中,对象为') + Message(TARGET_ID)
    ask_reply_msg_false = Message(' 自动打劫禁用中')
    if AUTO_ROB_ENABLED:
        await ask_auto_rob.finish(ask_reply_msg_true)
    else:
        await ask_auto_rob.finish(ask_reply_msg_false)


@auto_rob_command.handle()
async def auto_rob_function(event: MessageEvent):
    global TARGET_ID
    TARGET_ID = event.get_message()["at"]
    auto_rob_set_msg = Message(' 自动打劫对象已设置为') + Message(TARGET_ID)
    await auto_rob_command.finish(auto_rob_set_msg)


@scheduler.scheduled_job('interval', minutes=61, id='send_group_message')
async def auto_rob_main_function():
    bot = nonebot.get_bot()
    global AUTO_ROB_ENABLED, GROUP_ID, TARGET_ID
    if AUTO_ROB_ENABLED:
        await bot.send_group_msg(group_id=GROUP_ID, message=f'{TARGET_ID} 打劫')


