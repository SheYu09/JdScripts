#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_fcwb
活动名称: 灭菌挖宝
Author: SheYu09, HarbourJ
cron: 0 0 * * * jd_fcwb.py
new Env('灭菌挖宝')
'''
from newUserInfo import *
requests.packages.urllib3.disable_warnings()

def JD_API_HOST(e = 'happyDigHome', t = False):
	s.headers['Referer'] = 'https://bnzf.jd.com/'
	s.headers['User-Agent'] = userAgent()
	s.params = {
		'functionId': e,
		'body': '',
		't': int(time()*1e3),
		'appid': 'activities_platform',
		'client': 'ios',
		'clientVersion': s.headers['User-Agent'].split(';')[2]
	}
	s.body = {
		'linkId': 'pTTvJeSTrpthgk9ASBVGsw'
	}
	if t:
		s.body['round'] = s.round
	if e == 'happyDigDo':
		s.body = {
			"round": s.round,
			"rowIdx": s.rowIdx,
			"colIdx": s.colIdx,
			**s.body
		}
	elif e == 'happyDigHelp':
		s.body = {
			**s.body,
			"inviter": s.inviter,
			"inviteCode": s.inviteCode
		}
	elif e == 'happyDigHelpList':
		s.body = {
			"pageNum": 1,
			"pageSize": 50,
			**s.body
		}
	s.params['body'] = dumps(s.body, separators=(',', ':'))
	if e in ['happyDigHome', 'happyDigHelp']:
		appid = e == 'happyDigHome' and 'ce6c2' or '8dd95'
		h5st(appid)
	r = s.get('https://api.m.jd.com/', verify=False, timeout=30)
	return r.json() if r.content else ''

def BoostCode(i):
	s.headers['Cookie'] = i
	if newUserInfo(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n")
	r = JD_API_HOST()
	try:
		if r and r['success']:
			r = r['data']
			inviter = r['markedPin']
			inviteCode = r['inviteCode']
		if DigTreasure(): return
		if inviter and inviteCode:
			inviterList.append(inviter)
			inviteCodeList.append(inviteCode)
			r = JD_API_HOST('happyDigHelpList')
			if r and r['success']:
				personNum = r['data']['personNum']
			personNumList.append(personNum)
			print(f"inviter: {inviter}\ninviteCode: {inviteCode}\n邀请人数: {personNum}\n")
	except Exception as err:
		print(f"BoostCode Error: {err}\n")

def HelpFriends(i):
	s.headers['Cookie'] = i
	if newUserInfo(): return
	s.inviter, s.inviteCode, s.personNum = inviterList[0], inviteCodeList[0], personNumList[0]
	print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{s.inviter}\n")
	if s.personNum >= 111:
		print(len(inviterList))
		if len(inviterList) == 1 and len(inviteCodeList) == 1:
			[DigTreasure(c) for c in Nameck]
			exit()
		else:
			inviterList.remove(s.inviter)
			inviteCodeList.remove(s.inviteCode)
			personNumList.remove(s.personNum)
			return
	r = JD_API_HOST('happyDigHelp')
	try:
		if r and r['success']:
			s.personNum += 1
			print(f"{r['errMsg']}\n邀请人数: {s.personNum}\n")
		elif r['code'] in [16144, 16149]:
			print(f"{r['errMsg']}\n")
		else:
			print(f"{r}\n")
	except Exception as err:
		print(f"HelpFriends Error: {err}\n")

def DigTreasure(i = False):
	if i:
		s.headers['Cookie'] = i
		if newUserInfo(): return
		print(f"开始挖宝【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n")
	for i in range(3):
		s.round = i+1
		r = JD_API_HOST('happyDigHome', True)
		try:
			if r and r['success']:
				for i in r['data']['roundList']:
					if i['state'] != 0: continue
					for i in i['chunks']:
						if i['type'] == 1:
							print("半黑号……, 跳过助力此账号\n")
							return True
						elif i['type']: continue
						else:
							s.rowIdx = i['rowIdx']
							s.colIdx = i['colIdx']
							r = JD_API_HOST('happyDigDo')
							if r and r['success']:
								r = r['data']['chunk']
								t = r['type']
								if t == 1:
									print("半黑号……, 跳过助力此账号\n")
									return True
								v = t == 4 and '💣' or r['value'] and r['value'] or '👽'
								t = t == 1 and '优惠卷' or t == 2 and '京东红包' or t == 3 and '微信红包' or t == 4 and '炸弹' or ''
								print(f"挖到{t}: {v}\n")
							elif r and r['code'] == 16142:
								print(f"{r['errMsg']}")
								return
							else:
								print(f"{r}\n")
			else:
				print(f"{r}\n")
				break
		except Exception as err:
			print(f"DigTreasure Error: {err}\n")

def start():
	global Nameck, ckList, inviterList, inviteCodeList, personNumList
	print("🔔发财挖宝, 开始!\n")
	inviterList, inviteCodeList, personNumList = list(), list(), list()
	Names = Name()
	ckList = jdCookie()
	Nameck = [c for c in ckList if re_pin(c) in Names]
	[BoostCode(c) for c in Nameck]
	inviterList and inviteCodeList and [HelpFriends(c) for c in ckList if c not in Nameck]
	[DigTreasure(c) for c in Nameck]

if __name__ == '__main__':
	start()
