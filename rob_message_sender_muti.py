import asyncio

from nonebot import on_command,on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me


target_id_list = []
target_id_ache = None
spy_list_text = None

add_target = on_command("打工监听对象添加",rule=to_me(),permission=SUPERUSER)
@add_target.handle()
async def add_target_function():
    pass
@add_target.got("target_id_ache", prompt="请输入添加对象qq号")
async def add_function(bot: Bot,event: MessageEvent):
    global target_id_ache
    target_id_ache = event.get_message().extract_plain_text()
    target_id_list.append(target_id_ache)
    add_msg = Message('打工监听对象已添加') + MessageSegment.at(target_id_ache)
    await bot.send(event,add_msg)


del_target = on_command("打工监听对象移除",rule=to_me(),permission=SUPERUSER)
@del_target.handle()
async def del_target_function():
    pass
@del_target.got("target_id_ache", prompt="请输入移除对象qq号")
async def del_function(bot: Bot,event: MessageEvent):
    global target_id_ache
    target_id_ache= event.get_message().extract_plain_text()
    target_id_list.remove(target_id_ache)
    del_msg = Message('打工监听对象已移除') + MessageSegment.at(target_id_ache)
    await bot.send(event,del_msg)

spy_list = on_command("打工监听对象列表",rule=to_me(),permission=SUPERUSER)
@spy_list.handle()
async def spy_list_function():
    global spy_list,spy_list_text
    spy_list_text = "\n".join(target_id_list)
    if not target_id_list:
        await spy_list.finish("无目标")
    else:
        await spy_list.finish(spy_list_text)

send_rob_message = on_keyword([' 打工'])
@send_rob_message.handle()
async def send_rob_message_function(event: Event):
    rob_message = MessageSegment.at(str(event.user_id)) + Message(' 打劫')
    if str(event.user_id) in target_id_list:
        await asyncio.sleep(3)
        await send_rob_message.finish(rob_message)
    else:
        await send_rob_message.finish()
