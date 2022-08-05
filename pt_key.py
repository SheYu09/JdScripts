#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JDScript / pt_key
活动名称: CK格式化
Author: SheYu09
cron: 0 12 * * * pt_key.py
new Env('CK格式化')
'''

import requests
s = requests.session()
from time import sleep
from json import loads
from re import compile

def start():
	with open("/ql/config/auth.json", "r", encoding="utf-8") as f:
		t = loads(f.read())
		f.close()
	s.headers['Authorization'] = 'Bearer ' + t['token']
	r = s.get('http://127.0.0.1:5700/api/envs').json()
	u = 1
	for i in r['data']:
		if i['status'] == 1 or i['name'] != 'JD_COOKIE':
			continue
		ck = i['value']
		id = i['_id']
		key = compile(r'pt_key=(.*?);').findall(ck)[0]
		pin = compile(r'pt_pin=(.*?);').findall(ck)[0]
		try:
			wsk = compile(r'wskey=(.*?);').findall(ck)[0]
		except:
			wsk = False
		body = {
			'name': 'JD_COOKIE',
			'value': f'pt_key={key};pt_pin={pin};wskey={wsk};' if wsk else f'pt_key={key};pt_pin={pin};',
			'_id': id
		}
		r = s.put('http://127.0.0.1:5700/api/envs', json=body).json()
		print(r)
		print()
		u += 1
		sleep(1.5)

if __name__ == '__main__':
	start()

