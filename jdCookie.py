#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JdScript / jdCookie
活动名称: 读取COOKIE / WSKEY
Author: SheYu09
'''
import requests
s = requests.session()
s.keep_alive = False
from os import environ
from USER_AGENTS import *
from re import findall, split

def Name():
	try:
		if len(environ["Name"]):
			n = environ["Name"].split('&')
			print(f"已获取并使用Env环境 Name: {n}\n")
			return n
	except:
		print("自行添加环境变量：Name, 不同好友中间用&符号隔开\n")
		exit()

def ql_envs(e):
	try:
		if len(environ[f'JD_{e}']):
			print(f"   ****** 已获取并使用Env环境: {e} ******\n")
			c = environ[f'JD_{e}']
	except:
		print(f"   ****** 获取Env环境: {e} 失败❌❌❌ ******\n")
		print(f"自行添加环境变量：JD_{e}\n")
		c = ''
	if not c:
		return (e == 'COOKIE' and [''] or [('', '')])[0]
	elif e == 'COOKIE':
		return [i + v for i, v in zip(findall('pt_key=.*?;', c), findall('pt_pin=.*?;', c))]
	elif e == 'WSKEY':
		p = findall('pin=.*?;', c)
		return p, [i + v for i, v in zip(p, findall('wskey=.*?;', c))]

def jdCookie():
	c = ql_envs('COOKIE')
	p, w = ql_envs('WSKEY')
	w and [c.remove(i) for i in [i for i in c if findall('pin=.*?;', i)[0] in p]]
	k = (not w and [c] or not c and [w] or w and c and [w + c])[0]
	print(f"====================共{len(k)}个京东账号Cookie=====================\n")
	print(f"==================脚本执行- 北京时间(UTC+8)：{strftime('%Y-%m-%d %H:%M:%S', localtime())}==================\n")
	return k and k or exit()
