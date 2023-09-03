# pt_sign

## 功能特性

1. 使用aiohttp模块实现异步请求签到
2. 使用cloudscraper模块实现cf盾签到（todo）

## 文件说明

├─config_template.json                  配置文件模板内容
├─pt_sign_aiohttp.py                    入口
├─readme.md                             说明文件
└─requirements.txt                      依赖文件

### config_template.json

- "name": "xxx"                           名称，消息提示
- "method": "GET"                         请求方法
- "url": "https://xxx.xxx/xxx"            请求地址
- "headers": {}                           请求时所需的cookie等相关数据
- "body": {}                              可选，POST
- "success_reg": "xxx"                    签到请求成功的正则表达式
- "repeat_reg": "xxx"                     签到请求重复的正则表达式
- "type": "aiohttp"                       暂时无用，预留字段

## 使用说明

1. 通过抓包获取config数据
2. 通过config_template.json 创建config.json 配置文件
3. 安装requirements.txt 中的模块
4. 远行pt_sign_aiohttp.py文件
