#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_promote
活动名称: new Env('平行时空')
Author: SheYu09
cron: 7 9 * * * promote.py
'''
try:
	from jd_promote import start
except:
	print('未知错误...')
	exit()

if __name__ == '__main__':
	start()