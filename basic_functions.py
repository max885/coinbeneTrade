# -*- coding: utf-8 -*-
from utils import *
from manbiapi import *
import time


# 查询具体数字币的余额,此处以字典形式传参
def check_balance(appi_id,secret_id,coin_name):
    dic = {"apiid": appi_id, "secret": secret_id,
           "timestamp": create_timestamp(), "account": "exchange"}
    request_result = post_balance(dic)
    time.sleep(0.2)
    if request_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if request_result['status'] == 'ok':
            balance_data = request_result['balance']
            data_length = len(balance_data)
            asset_loc_init = {'MOAC': 0, 'USDT': 0, 'SWTC': 0, 'BTC': 0, 'MXM':0, 'NTY': 0,'LUC':0, 'ZIPT':0}
            for ci in range(data_length):
                for ii in range(len(asset_loc_init)):
                    if balance_data[ci]['asset'] == asset_loc_init.keys()[ii]:
                        asset_loc_init[asset_loc_init.keys()[ii]] = ci
            asset_loc_info = asset_loc_init
            return balance_data[asset_loc_info[coin_name]]
        else:
            if request_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif request_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif request_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif request_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif request_result['description'] == 'Permission Denied.':
                print 'API ID don not have permission'
                return 'Error api'
            else:
                print 'Other API error'
                return 'Error api'


# 获取买单或者卖单价格, bit_type
def check_current_price(coin_type, bit_type, n):
    bid_ask_price = get_orderbook(coin_type, 5)
    time.sleep(0.2)
    if bid_ask_price is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_price['status'] == 'ok':
            buy_price = bid_ask_price['orderbook'][bit_type][n]['price']
            return buy_price
        else:
            if bid_ask_price['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_price['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid symbol.':
                print 'Invalid symbol. Check coin_type, coin_name'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 获取买单或者卖单交易量
def check_current_quantity(coin_type, bit_type, n):
    bid_ask_quantity = get_orderbook(coin_type, 5)
    time.sleep(0.2)
    if bid_ask_quantity is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_quantity['status'] == 'ok':
            quantiy = bid_ask_quantity['orderbook'][bit_type][n]['quantity']
            return quantiy
        else:
            if bid_ask_quantity['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_quantity['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_quantity['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_quantity['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_quantity['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif bid_ask_quantity['description'] == 'Invalid symbol.':
                print 'Invalid symbol. Check coin_type, coin_name'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 下订单, order_type 为'sell-limit' 或'buy-limit'
def send_order(appi_id, secret_id, order_quantity, order_type,  order_price, coin_type):
    dic = {"apiid": appi_id, "secret": secret_id,
                  "timestamp": create_timestamp(), "type": order_type, "price": order_price,
                  "quantity": order_quantity,
                  "symbol": coin_type}
    order_result = post_order_place(dic)
    time.sleep(1)
    if order_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if order_result['status'] == 'ok':
            return order_result['orderid']
        else:
            if order_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif order_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif order_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif order_result['description'] == 'Insufficient balance of assets':
                print 'Insufficient balance of assets'
                return 'Error api'
            elif order_result['description'] == 'Invalid price precision.':
                print 'Invalid price precision.'
                return 'Error api'
            elif order_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif order_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif order_result['description'] == 'Invalid quantity precision.':
                print 'Invalid quantity precision.'
                return 'Error api'
            elif order_result['description'] == 'Invalid price.':
                print 'Invalid price.'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 根据订单号取消委托单
def cancel_orders(appi_id, secret_id, sell_order_id):
    dic = {"apiid": appi_id, "secret": secret_id,
                  "timestamp": create_timestamp(),"orderid":sell_order_id}
    cancel_result = post_cancel(dic)
    time.sleep(0.2)
    if cancel_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if cancel_result['status'] == 'ok':
            return cancel_result['status']
        else:
            if cancel_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif cancel_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif cancel_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif cancel_result['description'] == 'Invalid Order ID.':
                print 'Invalid Order ID.'
                return 'Error api'
            elif cancel_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif cancel_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif cancel_result['description'] == 'Invalid Order Status.':
                print 'Invalid Order Status. Orders are done'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 查询当前委托,以字典形式传参,所有卖单还未成交的总量减去所有买单还未成交的总量
def quanlity_in_entrusment(appi_id, secret_id, coin_type):
    entrustment = {"apiid": appi_id, "secret": secret_id, "timestamp": 1122311211231, "symbol": coin_type}
    entrustment_result = post_open_orders(entrustment)
    time.sleep(0.2)
    if entrustment_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if entrustment_result['status'] == 'ok':
            if entrustment_result['orders'] is None:
                return 0
            else:
                entrustment_number = entrustment_result['orders']['totalcount']
                quantity_in_entrustment = 0.0
                for ii in range(entrustment_number):
                    if entrustment_result['orders']['result'][ii]['type'] == 'sell-limit':
                        quantity_in_entrustment = quantity_in_entrustment + float(
                            str(entrustment_result['orders']['result'][ii]['orderquantity']))
                    else:
                        quantity_in_entrustment = quantity_in_entrustment - float(
                            str(entrustment_result['orders']['result'][ii]['orderquantity']))
                return quantity_in_entrustment
        else:
            if entrustment_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif entrustment_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif entrustment_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif entrustment_result['description'] == 'Insufficient balance of assets':
                print 'Insufficient balance of assets'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid price precision.':
                print 'Invalid price precision.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid quantity precision.':
                print 'Invalid quantity precision.'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 查询当前所有买委托中还剩要买入数量总和
def quanlity_buy_entrusment(appi_id, secret_id, coin_type):
    entrustment = {"apiid": appi_id, "secret": secret_id, "timestamp": 1122311211231, "symbol": coin_type}
    entrustment_result = post_open_orders(entrustment)
    time.sleep(0.2)
    if entrustment_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if entrustment_result['status'] == 'ok':
            if entrustment_result['orders'] is None:
                return 0
            else:
                entrustment_number = entrustment_result['orders']['totalcount']
                quantity_in_entrustment = 0.0
                for ii in range(entrustment_number):
                    if entrustment_result['orders']['result'][ii]['type'] == 'buy-limit':
                        quantity_in_entrustment = quantity_in_entrustment + float(
                            str(entrustment_result['orders']['result'][ii]['orderquantity']))
                return quantity_in_entrustment
        else:
            if entrustment_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif entrustment_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif entrustment_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order ID.':
                print 'Invalid Order ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order Status.':
                print 'Invalid Order Status. Orders are done'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 查询当前所有卖委托中还剩要卖出数量总和
def quanlity_sell_entrusment(appi_id, secret_id, coin_type):
    entrustment = {"apiid": appi_id, "secret": secret_id, "timestamp": 1122311211231, "symbol": coin_type}
    entrustment_result = post_open_orders(entrustment)
    time.sleep(0.2)
    if entrustment_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if entrustment_result['status'] == 'ok':
            if entrustment_result['orders'] is None:
                return 0
            else:
                entrustment_number = entrustment_result['orders']['totalcount']
                quantity_in_entrustment = 0.0
                for ii in range(entrustment_number):
                    if entrustment_result['orders']['result'][ii]['type'] == 'sell-limit':
                        quantity_in_entrustment = quantity_in_entrustment + float(
                            str(entrustment_result['orders']['result'][ii]['orderquantity']))
                return quantity_in_entrustment
        else:
            if entrustment_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif entrustment_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif entrustment_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order ID.':
                print 'Invalid Order ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order Status.':
                print 'Invalid Order Status. Orders are done'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 查询当前卖委托的 'orderid'， 'price', 'orderquantity', 注意price和orderquantity返回的是字符串，应float(str())转化为浮点型
def sell_info_entrusment(appi_id, secret_id, coin_type, command_type):
    entrustment = {"apiid": appi_id, "secret": secret_id, "timestamp": 1122311211231, "symbol": coin_type}
    entrustment_result = post_open_orders(entrustment)
    time.sleep(0.2)
    if entrustment_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if entrustment_result['status'] == 'ok':
            if entrustment_result['orders'] is None:
                return 0
            else:
                entrustment_number = entrustment_result['orders']['totalcount']
                for ii in range(entrustment_number):
                    if entrustment_result['orders']['result'][ii]['type'] == 'sell-limit':
                        return entrustment_result['orders']['result'][ii][command_type]
        else:
            if entrustment_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif entrustment_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif entrustment_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order ID.':
                print 'Invalid Order ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order Status.':
                print 'Invalid Order Status. Orders are done'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 查询当前买委托的 'orderid'， 'price', 'orderquantity', 注意price和orderquantity返回的是字符串，应float(str())转化为浮点型
def buy_info_entrusment(appi_id, secret_id, coin_type, command_type):
    entrustment = {"apiid": appi_id, "secret": secret_id, "timestamp": 1122311211231, "symbol": coin_type}
    entrustment_result = post_open_orders(entrustment)
    time.sleep(0.2)
    if entrustment_result is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if entrustment_result['status'] == 'ok':
            if entrustment_result['orders'] is None:
                return 0
            else:
                entrustment_number = entrustment_result['orders']['totalcount']
                for ii in range(entrustment_number):
                    if entrustment_result['orders']['result'][ii]['type'] == 'buy-limit':
                        return entrustment_result['orders']['result'][ii][command_type]
        else:
            if entrustment_result['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif entrustment_result['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif entrustment_result['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order ID.':
                print 'Invalid Order ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif entrustment_result['description'] == 'Invalid Order Status.':
                print 'Invalid Order Status. Orders are done'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 检查自己的卖单价格上是否有别人挂相同的价格
def check_sell_unique(appi_id, secret_id, coin_name, sell_price, bit_type, coin_type,
                      filter_setpoint, debug_switch):
    check_balanced = check_balance(appi_id, secret_id, coin_name)
    reserved_number = check_balanced['reserved']
    if float(reserved_number) == 0:
        print "reserved number is 0, sell over or bought by others"
        return 3
    sell_price = float(sell_price)
    reserved_number = float(reserved_number)
    bid_ask_price = get_orderbook(coin_type, 5)
    time.sleep(0.2)
    if bid_ask_price is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_price['status'] == 'ok':
            for i in range(5):
                price = bid_ask_price['orderbook'][bit_type][i]['price']
                if debug_switch is True:
                    print "sell_price == price",sell_price == price
                if sell_price == price:
                    quantity = bid_ask_price['orderbook'][bit_type][i]['quantity']
                    if debug_switch is True:
                        print "sell price", sell_price, "price", price
                        print 'reserved_number', reserved_number, 'quantity - filter_setpoint', quantity - filter_setpoint
                    if reserved_number >= quantity - filter_setpoint:
                        return True
            return False
        else:
            if bid_ask_price['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_price['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid symbol.':
                print 'Invalid symbol. Check coin_type, coin_name'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'


# 检查自己的卖单价格所处卖单位置
def check_sell_position(sell_price, bit_type, coin_type):
    bid_ask_price = get_orderbook(coin_type, 10)
    time.sleep(0.2)
    if bid_ask_price is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_price['status'] == 'ok':
            for i in range(10):
                price = bid_ask_price['orderbook'][bit_type][i]['price']
                if sell_price == price:
                    return i
        else:
            if bid_ask_price['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_price['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid API ID.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid api id.':
                print 'Invalid API ID.'
                return 'Error api'
            elif bid_ask_price['description'] == 'Permission Denied.':
                print 'API ID donnot have t have permission'
                return 'Error api'
            elif bid_ask_price['description'] == 'Invalid symbol.':
                print 'Invalid symbol. Check coin_type, coin_name'
                return 'Error api'
            else:
                print 'other api error'
                return 'Error api'
