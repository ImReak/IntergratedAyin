import asyncio

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, MessageSegment

target_qq = 2517519695

v5 = on_command("v我5币",rule=to_me(),permission=SUPERUSER)
@v5.handle()
async def v5_function():
    v5_at_message = MessageSegment.at(1701173738) + Message(' v你5币')
    await v5.finish(v5_at_message)

v5o = on_command("v他5币",rule=to_me(),permission=SUPERUSER)
@v5o.handle()
async def v5o_function(event:MessageEvent):
    object_id = event.get_message()["at"]
    v5o_at_message = Message(object_id) + Message(' v你5币')
    await v5o.finish(v5o_at_message)


emozhili = on_command("恶魔之力", rule=to_me(), permission=SUPERUSER)
@emozhili.handle()
async def emozhili_function(bot,event: GroupMessageEvent):
    this_group_id = event.group_id
    await bot.send_group_msg(group_id=this_group_id, message="购买恶魔之力")
    await asyncio.sleep(3)
    await bot.send_group_msg(group_id=this_group_id, message="使用恶魔之力")
    await emozhili.finish()

yuehuiquan = on_command("约会券", rule=to_me(), permission=SUPERUSER)
@yuehuiquan.handle()
async def yuehuiquan_function(bot,event: GroupMessageEvent):
    this_group_id = event.group_id
    await bot.send_group_msg(group_id=this_group_id, message="购买约会券")
    await asyncio.sleep(3)
    await bot.send_group_msg(group_id=this_group_id, message="使用约会券")
    await yuehuiquan.finish()



kucun = on_command("查看库存", rule=to_me())
@kucun.handle()
async def kucun_function():
    global target_qq
    at_message = MessageSegment.at(target_qq) + Message(' 我的库存')
    await kucun.finish(at_message)



rob_ta_command = on_command("帮我打劫", rule=to_me(), permission=SUPERUSER)
@rob_ta_command.handle()
async def rob_ta_function(event: MessageEvent):
    victim_id_ta = event.get_message()["at"]
    msg_ta = Message(victim_id_ta) + Message(' 打劫')
    await rob_ta_command.finish(msg_ta)

rob_tb_command = on_command("帮我劫涩", rule=to_me(), permission=SUPERUSER)
@rob_tb_command.handle()
async def rob_tb_function(event: MessageEvent):
    victim_id_tb = event.get_message()["at"]
    msg_tb = Message(victim_id_tb) + Message(' 劫涩')
    await rob_tb_command.finish(msg_tb)




