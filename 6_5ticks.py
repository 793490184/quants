# -*- coding: utf-8 -*-
import requests
from time import sleep
from datetime import datetime, time, timedelta  # Δy/Δx
#from dateutil import parser
#import pandas as pd
import os
import numpy as np
#from dateutil import parser


class AstockTrading(object):
	def __init__(self,  strategy_name):
		self._Open = None
		self._High = None
		self._tick = None
		self._Dt = []
		self._is_new_bar = False

	def get_history_data_from_loacal_machine(self):
		self._Open = [1, 2, 3]
		self._High = [2, 3, 4]

	def bar_generator(self, tick):
		# update open, high......
		pass

	def strategy(self, strategy_name = "ma"):
		self.strategy_ma()

	def strategy_ma(self):
		# use self._High, self._Open... cal sell or long
		if self._is_new_bar:  # _is_new_bar == True:
			# sum_ = 0
			# for item in self._Close[1:21]:
			#     sum_ = sum_ + item
			self._ma20.insert(1, sum(self._Close[1:21]) / 20)
			self._close_minus_ma20[2:] = self._close_minus_ma20[1:len(self._close_minus_ma20) - 1]
			self._close_minus_ma20[1] = self._Close[1] - self._ma20[1]
		if 0 == len(self._current_orders):
			if self._Close[0] < 0.98 * self._ma20[1]:
				if (self._close_minus_ma20 < 0).sum() > 10 and \
						self._close_minus_ma20.sum() / self._Close[1] < -0.02:
					# 100000/44.28 = 2258
					# 2258 -> 2200
					volume = int(100000 / self._Close[0] / 100) * 100  # 2200shares
					self.buy(self._Close[0] + 0.01, volume)

		elif 1 == len(self._current_orders):  # have long position
			if self._Close[0] > self._ma20[1] * 1.02:
				key = list(self._current_orders.keys())[0]
				if self._Dt[0].date() != self._current_orders[key]['open_datetime'].date():
					self.sell(key, self._Close[0] - 0.01)
					print('open date is %s, close date is: %s.' % (self._history_orders[key]['open_datetime'].date(), self._Dt[0].date()))
				else:
					# if same dates, sell order aborted due to T+0 limit
					print('sell order aborted due to T+0 limit')

		else:  # len() == 2
			raise ValueError("we have more than 1 current orders!")

	def getTicks(self):
		#   func: for paper trading or real trading, not for backtesting
		#   It goes to sina to get last tick info,
		#   # http://hq.sinajs.cn/?format=text&list=sh600519
		#   'sh600519' needs to be changed.
		#   A股的开盘时间是9：15， 9：15-9：25是集合竞价-> 开盘价， 9:25
		#   9:25-9:30不交易， 时间>9:30,交易开始.
		#   start this method after 9:25. 
		#   tick info is organized in tuple,
		#   such as (trade_datetime, last_price),
		#   tick info is saved in self._tick.
		# param: not param
		# return: None
		page = requests.get("http://hq.sinajs.cn/?format=text&list=sh600519")
		stock_info = page.text
		mt_info = stock_info.split(",")

		last = float(mt_info[1])
		trade_datetime = mt_info[30] + ' ' + mt_info[31]

		# 9:25 -> 9:30, move first tick's time from 9:25 to 9:30
		# 2020/12/10 9:25, -> 2020/12/10 9:30
		# if trade_datetime.time() < time(9, 30):
		# trade_datetime = datetime.combine(trade_datetime.date(), time(9, 30))

		self._tick = (trade_datetime, last)

	# -------------------------------------------------------------------------
	def buy(self, price, volume):
		# creat an long order
		# needs two params
		# param1 price: buying price
		# param2 volume: buying volume
		# return: None
		self._order_number += 1
		# {key: value}
		key = "order" + str(self._order_number)
		self._current_orders[key] = {
			"open_datetime": self._Dt[0],
			"open_price": price,
			"volume": volume
		}

	# -------------------------------------------------------------------------

	def sell(self, key, price):
		# close a long order
		# It needs two params
		# param1 key: long order's key
		# param2 price: selling price
		# return: None
		self._current_orders[key]['close_price'] = price
		self._current_orders[key]['close_datetime'] = self._Dt[0]
		self._current_orders[key]['pnl'] = \
			(price - self._current_orders[key]['open_price']) \
			* self._current_orders[key]['volume'] \
			- price * self._current_orders[key]['volume'] * 1 / 1000 \
			- (price + self._current_orders[key]['open_price']) \
			* self._current_orders[key]['volume'] * 3 / 10000

		# move order from current orders to history orders
		self._history_orders[key] = self._current_orders.pop(key)

	def run(self):
		self.getTicks()
		self.bar_generator()
		self.strategy()


ma = AstockTrading('ma')
ma.get_history_data_from_loacal_machine()
while time(9, 26) < datetime.now().time() < time(11, 32) or \
		time(13) < datetime.now().time() < time(15, 2):
	ma.getTicks()
	ma.bar_generator()
	ma.strategy("ma")
	sleep(3)

