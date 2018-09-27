# -*- coding: utf-8 -*-
from csv_functions import *
from manbiapi import *
from basic_functions import *
from process_functions import *
from init_functions import *
from integration_function import *
import random

coin_name = 'ZIPT'
coin_type = 'zipteth'
appi_id = "839ef903111dd71fae0265c5a75974d5"
secret_id = "265aacf52ac04036a20e7e79a8890def"

empty_file('trade_list.csv')
empty_file('trade_result.csv')
empty_file('bought_by_others.csv')
empty_file('bought_by_others_one_loop.csv')

#send_order(appi_id, secret_id, 500, 'buy-limit', '0.00002460', coin_type)

print check_balance(appi_id, secret_id, coin_name)

sell_order_id = sell_info_entrusment(appi_id, secret_id, coin_type, 'orderid')
# 取消当前委托单
cancel_orders(appi_id, secret_id, sell_order_id)
