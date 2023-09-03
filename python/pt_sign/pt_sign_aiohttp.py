#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
import time
import re
import json
import asyncio
import traceback
import aiohttp
# import notify

# custom
config_file = r"config.json"

# global
script_path = os.path.abspath(sys.argv[0])
script_dir  = os.path.dirname(script_path)
output_dir = Path().joinpath(script_dir, r'output')
success_message = ''
repeat_message = ''
exception_message = ''
failed_message_list = [] 

def get_config():
    config_path = Path().joinpath(script_dir, config_file)
    config_data = []
    with open(config_path, mode="r", encoding="utf-8") as f:
        config_data = json.loads(f.read()).get("list")
    return config_data

        
async def get_respones(config):
    if config.get("success_reg") == '':
        return
    print(time.strftime(r'%Y-%m-%d %H:%M:%S'), 'start', config.get("name"))
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(method=config.get("method"), url=config.get("url"), headers=config.get("headers"), data=config.get("body"), timeout=60) as response:
                html = await response.text()
                if html.startswith('{') and html.endswith('}') and '\\u' in html:
                    html = bytes(html, 'utf-8').decode('unicode_escape')
                success_reg = config.get("success_reg")
                repeat_reg = config.get("repeat_reg")
                if succeed_msg := re.search(success_reg, html):
                    sign_success = re.sub("<.*?>|&shy;|&nbsp;||\n\n|\n", "",succeed_msg.group(0))
                    print(time.strftime(r'%Y-%m-%d %H:%M:%S'), config.get("name"), sign_success)
                    global success_message
                    success_message += time.strftime(r'%Y-%m-%d %H:%M:%S') + ' ' +  config.get("name") + ' ' + sign_success + '\n'
                elif repeat_msg := re.search(repeat_reg, html):
                    sign_success = re.sub("<.*?>|&shy;|&nbsp;||\n\n|\n", "",repeat_msg.group(0))
                    print(time.strftime(r'%Y-%m-%d %H:%M:%S'), config.get("name"), sign_success)
                    global repeat_message
                    repeat_message += time.strftime(r'%Y-%m-%d %H:%M:%S') + ' ' +  config.get("name") + ' ' + sign_success + '\n'
                else:
                    failed_message_list.append([config.get("name"), time.strftime(r'%Y-%m-%d %H:%M:%S') + ' ' +  config.get("name") + ' ' + html])
        except Exception:
            print(time.strftime(r'%Y-%m-%d %H:%M:%S'), config.get("name"), str(Exception))
            traceback.print_exc()
            global exception_message
            exception_message += time.strftime(r'%Y-%m-%d %H:%M:%S') + ' ' +  config.get("name") + ' ' + str(Exception) + '\n'
            
    print(time.strftime(r'%Y-%m-%d %H:%M:%S'), 'end', config.get("name"))
    
async def main():
    print("脚本执行开始")
    config_data = get_config()
    if len(config_data) == 0:
        return
    tasks = [asyncio.create_task(get_respones(i)) for i in config_data]
    await asyncio.gather(*tasks)
    total_times = (len(success_message.split('\n')) - 1) + (len(repeat_message.split('\n')) - 1) + len(failed_message_list)  + (len(exception_message.split("\n")) - 1)
    total_info = '共数据 {0} 个\n签到 {1} 个\n签到成功 {2} 个\n签到重复 {3} 个\n签到失败 {4} 个\n任务异常 {5} 个\n\n\n' \
        .format(
            str(len(config_data)),
            str(total_times),
            str(len(success_message.split("\n"))- 1),
            str(len(repeat_message.split('\n')) - 1),
            str(len(failed_message_list)),
            str(len(exception_message.split("\n")) - 1)
        )
    print(total_info)
    print(success_message)
    print(repeat_message)
    for failed_message in failed_message_list:
        print(failed_message[0], '\n', failed_message[1])
    # notify.send("PT 签到",  total_info + success_message + repeat_message + exception_message)
    print("脚本执行完毕")

if __name__ == "__main__":
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
