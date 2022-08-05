#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JdScript / newUserInfo
活动名称: 账号信息
Author: SheYu09, HarbourJ
'''
from sign_log import *
from requests.utils import dict_from_cookiejar
requests.packages.urllib3.disable_warnings()

def set_cookies(func):
	def set_change(*args, **kwargs):
		if 'wskey=' in s.headers['Cookie'] and getToken():
			return True
		if func(*args, **kwargs):
			return True
	return set_change

def getToken():
	r = sign()
	t = r and r['tokenKey'] or ''
	s.params = {
		'tokenKey': t if t != 'xxx' else '',
		'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
	}
	if s.get(r['url'], verify=False, allow_redirects=False, timeout=30).status_code == 302:
		r = dict_from_cookiejar(s.cookies)
	try:
		if 'fake_' in r['pt_key']:
			print(f"【提示】wskey已失效, 京东账号 {re_key('pin=(.*?);', s.headers['Cookie'])}\n请重新抓包获取\nhttps://api.m.jd.com/client.action?functionId=newUserInfo\n")
			return True
		elif 'app_open' in r['pt_key']:
			s.headers['Cookie'] = ';'.join([f'{i}={r[i]}' for i in r])
	except EOFError as err:
		print(f"getToken Error: {err}\n")
		return True

@set_cookies
def newUserInfo():
	try:
		s.Token = environ["JlhbToken"]
	except:
		print("自行添加环境变量：JlhbToken\n")
		exit()
	try:
		s.headers['Referer'] = ''
		r = sign(
			{
				'flag': 'nickname',
				'fromSource': 1,
				'sourceLevel': '1'
			},
			'newUserInfo'
		)
		if r and r['enc'] == 0:
			r = r['userInfoSns']
			s.levelName = r['uclass']
			s.nickName = r['petName'] and r['petName'] or r['unickName']
			s.userLevel = r['userLevel']
		else:
			print(f"【提示】Cookie已失效, 京东账号 {re_key('pin=(.*?);', s.headers['Cookie'])}\n请重新抓包获取\nhttps://bean.m.jd.com/bean/signIndex.action\n")
			return True
	except Exception as err:
		print(f"newUserInfo Error: {err}\n")
		return True

