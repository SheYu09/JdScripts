#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_jlhb
活动名称: 疯狂吧锦鲤
Author: SheYu09, HarbourJ
cron: 0 0 * * * jd_jlhb.py
new Env('疯狂吧锦鲤')
'''
import urllib3
from newUserInfo import *
requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def JD_API_HOST(e = 'h5activityIndex', t = False):
	s.headers['Referer'] = 'https://happy.m.jd.com/'
	s.params = {
		'appid': 'jinlihongbao',
		'functionId': e,
		'loginType': 2,
		'client': 'jinlihongbao',
		't': int(time()*1e3),
		'clientVersion': s.headers['User-Agent'].split(';')[2],
		'osVersion': -1,
		'body': {}
	}
	if e == 'h5activityIndex':
		s.body = {
			"isjdapp": 1
		}
	elif e in ['h5launch', 'jinli_h5assist', 'h5receiveRedpacketAll', 'startTask']:
		LOG_API()
		s.body = {
			'random': s.random,
			'log': s.log,
			'sceneid': 'JLHBhPageh5'
		}
		if t:
			s.body['taskType'] = s.taskType
		elif e in ['h5launch', 'jinli_h5assist']:
			s.body['followShop'] = 0
			if e == 'jinli_h5assist':
				s.body['redPacketId'] = s.redPacketId
	elif e in ['getTaskDetailForColor', 'taskReportForColor']:
		s.body = {
			'taskType': s.taskType
		}
		if e == 'taskReportForColor':
			s.body['detailId'] = s.detailId
	if e != 'taskHomePage':
		s.params['body'] = dumps(s.body, separators=(',', ':'))
	r = s.post('https://api.m.jd.com/api', verify=False, timeout=30)
	return r.json() if r.content else ''

def getTaskDetailForColor():
	r = JD_API_HOST('getTaskDetailForColor')
	try:
		if r['code'] == 0 and r['rtn_code'] == 0:
			advertDetails = r['data']['result']['advertDetails']
			for i in advertDetails:
				if i['status'] == 0:
					s.detailId = i['id']
					r = JD_API_HOST('taskReportForColor')
					if r['code'] == 0 and r['rtn_code'] == 0:
						print(f"{r['data']['biz_msg']}\n")
				elif i['status'] == 2:
					print(f"任务: {i['name']}, 已完成\n")
					continue
	except Exception as err:
		print(f"getTaskDetailForColor Error: {err}\n")

def iostask():
	if s.taskType == 1:
		r = sign({"monitorSource":"ccgroup_ios_index_task","taskType":f"{s.taskType}","taskId":f"{s.sceneId}"}, 'getCcTaskList')
		if r['success'] and r['code'] == '0':
			print(f"{r['message']}\n")
		print(f"等待: ⏳{s.requireCount}/s")
		sleep(s.requireCount)
		r = sign({"monitorSource":"ccgroup_ios_index_task","taskType":f"{s.taskType}","taskId":f"{s.sceneId}"}, 'reportCcTask')
		if r['success'] and r['code'] == '0':
			print(f"{r['message']}\n")
	else:
		s.params = {
			'appid': 'XPMSGC2019',
			'monitorSource': '',
			'functionId': 'getSinkTaskList',
			'body': dumps({
				'platformType': '1',
				'taskId': f'{s.taskType}'
			}, separators=(',', ':')),
			'client': 'm',
			'clientVersion': '5.8.0',
			'uuid': s.headers['User-Agent'].split(';')[4]
		}
		s.headers['Referer'] = 'https://h5.m.jd.com/'
		r = s.post('https://api.m.jd.com/client.action', verify=False, timeout=3).json()
		if r['success'] and r['code'] == '0':
			print(f"{r['result']['sinkTaskData']['subMsg']}\n")
		print(f"等待: ⏳{s.requireCount}/s")
		sleep(s.requireCount)
		s.params['functionId'] = 'reportSinkTask'
		r = s.post('https://api.m.jd.com/client.action', verify=False, timeout=3).json()
		if r['success'] and r['code'] == '0':
			print(f"{r['result']['reportTaskData']['subMsg']}\n")

def Doatask(i):
	if JD_UUID(i): return
	r = JD_API_HOST('taskHomePage')
	try:
		if r['code'] == 0 and r['rtn_code'] == 0:
			taskInfos = r['data']['result']['taskInfos']
			for i in taskInfos:
				s.taskType = i['taskType']
				s.sceneId = i['sceneId']
				s.requireCount = i['requireCount']
				if s.taskType == 0: continue
				if i['innerStatus'] == 7:
					print(f"开始: {i['title']}任务\n")
					r = JD_API_HOST('startTask', True)
					if r['code'] == 0 and r['data']['biz_code'] == 0:
						if s.taskType in [1, 9]:
							iostask()
						else:
							getTaskDetailForColor()
					else:
						print(f"{r['data']['biz_msg']}\n")
						break
				elif i['innerStatus'] == 2:
					print(f"任务: {i['title']}未完成, 开始做此任务\n")
					if s.taskType in [1, 9]:
						iostask()
					else:
						getTaskDetailForColor()
				elif i['innerStatus'] == 3:
					print(f"任务: {i['title']}已做完, 红包🧧未领取\n")
				elif i['innerStatus'] == 4:
					print(f"{i['title']}, 红包🧧已拆开\n")
					continue
				r = JD_API_HOST('h5receiveRedpacketAll', True)
				if r['code'] == 0 and r['rtn_code'] == 0:
					print(f"{r['data']['biz_msg']}: {r['data']['result']['discount']}元\n")
				elif r['code'] == 0 and r['rtn_code'] == 403:
					print("注意⚠️注意⚠️半黑号...来临‼️\n")
				else:
					print(f"{r}\n")
	except Exception as err:
		print(r)
		print(f"Doatask Error: {err}\n")

def jdkoi(i, e = 'jinli_h5assist'):
	if e == 'jinli_h5assist':
		t = True
		s.redPacketId = es[0]
	else:
		t = False
	if JD_UUID(i, t): return
	try:
		T = True
		while T:
			T = False
			r = JD_API_HOST(e)
			if r['code'] == 0 and r['rtn_code'] == 0:
				if e == 'h5receiveRedpacketAll':
					if r['data']['biz_code'] not in [7, 10]:
						print(f"{r['data']['biz_msg']}: {r['data']['result']['discount']}元\n")
						T = True
					else:
						print(f"{r['data']['biz_msg']}")
				else:
					print(f"{r['data']['result']['statusDesc']}\n")
			elif r['code'] == 3 and r['rtn_code'] == 406:
				print("注意⚠️注意⚠️半黑号...来临‼️\n")
			else:
				print(f"{r}\n")
				if s.u%10 == 0:
					exit()
				s.u += 1
			if e == 'jinli_h5assist' and r['data']['result']['status'] == 2:
				if len(es) == 1:
					h5receiveRedpacketAll()
					exit()
				else:
					es.remove(es[0])
	except Exception as err:
		print(f"jdkoi Error: {err}\n")

def BoostCode(i):
	id = ''
	if JD_UUID(i): return
	r = JD_API_HOST()
	try:
		if r and r['data']['code'] == 10002:
			r = JD_API_HOST('h5launch')
			if r and r['data']['code'] == 0:
				id = r['data']['result']['redPacketId']
				print(f"{id}\n")
			elif r and r['data']['code'] == 403:
				print(f"{r}\n")
				return
			else:
				print(f"{r['data']['result']['statusDesc']}\n")
				return
		elif r and r['data']['code'] == 20001:
			if r['data']['result']['redpacketConfigFillRewardInfo'][-1]['packetStatus'] == 1:
				print("助力已满，红包🧧未领取\n")
			else:
				id = r['data']['result']['redpacketInfo']['id']
				print(f"{id}\n")
		elif r and r['data']['code'] == 20002:
			print(f"{r['data']['msg']}\n")
			return
		id and es.append(id)
	except Exception as err:
		print(f"BoostCode Error: {err}\n")

def JD_UUID(i, t = False):
	s.headers['Cookie'] = i
	if newUserInfo(): return True
	if t:
		print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{s.redPacketId}\n")
	else:
		print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n")

def h5receiveRedpacketAll():
	sleep(5)
	try:
		e = environ["jlhb_All"]
	except:
		print("自动开包, 环境变量：export jlhb_All=\"True\"\n")
	else:
		e and [jdkoi(i, 'h5receiveRedpacketAll') for i in Namek]
	try:
		e = environ["jlhb_Doa"]
	except:
		print("小任务, 环境变量：export jlhb_Doa=\"True\"\n")
	else:
		e and [Doatask(i) for i in Namek]

def start():
	global ckList, Namek, es
	print("🔔锦鲤红包, 开始!\n")
	Names = Name()
	ckList = jdCookie()
	es = list()
	s.u = 1
	Namek = [i for i in ckList if re_pin(i) in Names]
	[BoostCode(i) for i in Namek]
	es and [jdkoi(i) for i in ckList if i not in Namek]
	h5receiveRedpacketAll()

if __name__ == '__main__':
	start()
