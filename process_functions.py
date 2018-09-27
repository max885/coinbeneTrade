# -*- coding: utf-8 -*-
from manbiapi import *
import random
from basic_functions import *
from csv_functions import *
from init_functions import *

appi_id = ""
secret_id = ""
# coin_name = 'BTC'
# coin_type = 'btcusdt'


# 过滤掉买单或者卖单前面小的单子，视为不影响策略的报价
def filter_small_quantity(coin_type, bid_type, filter_quantity):
    time.sleep(0.1)
    bid_ask_price = get_orderbook(coin_type, 5)
    time.sleep(0.2)
    if bid_ask_price is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_price['status'] == 'ok':
            for ii in range(5):
                if bid_ask_price['orderbook'][bid_type][ii]['quantity'] > filter_quantity:
                    return ii
        else:
            if bid_ask_price['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_price['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_price['description'] == 'Permission Denied.':
                print 'API ID don not have permission'
                return 'Error api'
            else:
                print 'other API error'
                return 'Error api'


# gap_ratio是判断卖1和买1 差价除以买价大于百分之多少gap_ratio时，下买单价格是买1加上当前差价buy_price_position比例
def decide_set_price(coin_type, gap_ratio, buy_price_position):
    bid_ask_price = get_orderbook(coin_type, 5)
    time.sleep(0.2)
    if bid_ask_price is None:
        print "Internet Connection Error. Please check the website link."
        return 'Error web'
    else:
        if bid_ask_price['status'] == 'ok':
            buy_price_0 = bid_ask_price['orderbook']['bids'][0]['price']
            sell_price_0 = bid_ask_price['orderbook']['asks'][0]['price']
            if (sell_price_0 - buy_price_0) / buy_price_0 > gap_ratio:
                return buy_price_0 + (sell_price_0 - buy_price_0) * buy_price_position
        else:
            if bid_ask_price['description'] == 'Invalid sign.':
                print 'Sign Error. Please Check API ID or try to change a new one'
                return 'Error api'
            elif bid_ask_price['description'] == 'System Busy.':
                print 'Website System Busy!'
                return 'Error api'
            elif bid_ask_price['description'] == 'Permission Denied.':
                print 'API ID don not have permission'
                return 'Error api'
            else:
                print 'other API error'
                return 'Error api'


# 总量sum_v，份n次成交，每次数量随机.每次交易的数量最小值通过min_quantity设定
def generate_rand_m(n, sum_v, quantity_precision, min_quantity=2):
    min_quantity = int(sum_v / (min_quantity * n))
    max_quantity = int(round((2 * sum_v) / n) - min_quantity)
    temp = random.sample(range(min_quantity, max_quantity), n)
    gap_number = sum_v - sum(temp)
    if gap_number > 0:
        temp[temp.index(min(temp))] = round(temp[temp.index(min(temp))] + gap_number,quantity_precision)
    else:
        for ii in range(n):
            vector = int(temp[ii] / 2)
            if (-gap_number) > vector:
                temp[ii] = round(temp[ii] - vector,quantity_precision)
                gap_number = gap_number + vector
            else:
                temp[ii] = round(temp[ii] + gap_number,quantity_precision)
                break
    return temp


# 挂单被买去N个，中止这次交易，撤单, trade_num为挂的卖单总量，buy_sum为自己已经买入的数量,被别人买掉大于cancel_setpoint数量时，取消还没成交的卖单
def cancel_trade(appi_id, secret_id, trade_num, sulf_buy_sum, coin_name, cancel_setpoint, order_number):
    balance_result = check_balance(appi_id, secret_id, coin_name)
    time.sleep(0.2)
    if balance_result == 'Error api':
        return 'Error api'
    elif balance_result == 'Error web':
        print 'Error web'
    else:
        reserved_number = float(str(balance_result['reserved']))  # 冻结的数量,还没卖出的数量
        if trade_num - sulf_buy_sum - reserved_number > cancel_setpoint:
            dic = {"apiid": appi_id, "secret": secret_id, "timestamp": 112231121111231, "orderid": order_number}
            print 'Cancel unsold orders ', post_cancel(dic)


# 判断有没有被别人买去，如果有，在被别人买入数量不大于阈值的时候，自己挂一个低价的买单买回来
def buy_back(appi_id, secret_id, trade_num, self_buy_sum, coin_name, coin_type, buy_price_position):
    balance_result = check_balance(appi_id, secret_id, coin_name)
    reserved_number = float(str(balance_result['reserved']))  # 冻结的数量,还没卖出的数量
    others_buy = trade_num - self_buy_sum - reserved_number
    buy_price = decide_set_price(coin_type, 0.0, buy_price_position)
    if others_buy > 0:
        send_order = {"apiid": appi_id, "secret": secret_id,
                      "timestamp": create_timestamp(), "type": "buy-limit", "price": buy_price,
                      "quantity": others_buy,
                      "symbol": coin_type}
        buy_order_result = post_order_place(send_order)
        time.sleep(1)
        print buy_order_result


# 防止别人逼单，把卖单价格逐渐降到很低的位置被别人吃掉
def prevent_forced_down(coin_type, prevent_forced_gap, current_sell_price):
    print "Waiting for enough sell and buy price gap ..."
    wait_for_trade = True
    while wait_for_trade:
        current_buy_1 = check_current_price(coin_type, 'bids', 0)
        time.sleep(0.2)
        if (current_sell_price - current_buy_1) / current_buy_1 > prevent_forced_gap:
            print "Current sell and buy price gap is enough."
            wait_for_trade = False


# 求和第一列数据， 被用来计算被别人买去的总数
def whether_end_ruuning(file_name):
    f = open(file_name,'r')
    su = 0
    for line in f.readlines():
        su = su + float(line)
    return su


# 当有人买单，把buy_list的每个买单数量根据别人买的数量降下来, ii表示从第几次self buy之后才开始更新 list
def reduce_buy_list(buy_list, ii, bought_by_other):
    if sum(buy_list[ii:])/2.5 > bought_by_other:
        d_factor = 3.0
    elif sum(buy_list[ii:])/2.5 <= bought_by_other < sum(buy_list[ii:])/1.5:
        d_factor = 2.0
    else:
        d_factor = 1.0
    len_buy_list = len(buy_list)
    for i in range(ii, len_buy_list):
        if bought_by_other <= round(buy_list[i] / d_factor):
            buy_list[i] = buy_list[i] - bought_by_other
            break
        else:
            temp = round(buy_list[i] / d_factor)
            buy_list[i] = buy_list[i] - temp
            bought_by_other = bought_by_other - temp
    return buy_list


# 检查当前有没有别人买了自己的卖单，如有，把数量写入csv，并计算当前被买的总数量是否超过阈值
def check_bought_by_other(appi_id, secret_id, self_buy_list, ii, sell_quantity, reserved_number, self_buy_sum, others_bought_sum_oneloop,
                          end_due_bought, coin_type, price_precision, debug_switch, boughtBuyOhterCount):
    buy_back_quantity = float(sell_quantity) - float(reserved_number) - float(self_buy_sum) - others_bought_sum_oneloop
    if debug_switch is True:
        print "buy_back_quantity", buy_back_quantity

    if buy_back_quantity > 0:
        boughtBuyOhterCount = boughtBuyOhterCount + 1
    else:
        pass

    print "buy_back_quantity", buy_back_quantity, "float(sell_quantity) - float(reserved_number) - float(self_buy_sum)" \
                                                  " - others_bought_sum_oneloop", float(sell_quantity),\
                                                float(reserved_number), float(self_buy_sum), others_bought_sum_oneloop

    if boughtBuyOhterCount > 0:
        buy_back_price = decide_set_price(coin_type, 0, 0.1)
        buy_back_price = convert_E_to_str(buy_back_price, price_precision)
        print "buy back quantity ", buy_back_quantity, "buy back price ", buy_back_price
        write_trade_result('bought_by_others_one_loop.csv', buy_back_quantity)


    others_bought_sum_oneloop = whether_end_ruuning('bought_by_others_one_loop.csv')

    if buy_back_quantity > 0:
        reduce_buy_list(self_buy_list, ii, buy_back_quantity)
        if debug_switch is True:
            print "self_buy_list", self_buy_list
    # 检查已经被别人买去的总和
    others_bought_sum = whether_end_ruuning('bought_by_others.csv') + \
                        whether_end_ruuning('bought_by_others_one_loop.csv')
    bought_sum_exceed = False

    if others_bought_sum > end_due_bought:
        print "Totally ", others_bought_sum, " have been bought by others. End the program."
        bought_sum_exceed = True

    if boughtBuyOhterCount > 0 and bought_sum_exceed is False:
        print "bought_sum_exceed is ", bought_sum_exceed
        send_order(appi_id, secret_id, buy_back_quantity, 'buy-limit', buy_back_price, coin_type)
        boughtBuyOhterCount = boughtBuyOhterCount - 1

    return others_bought_sum_oneloop, boughtBuyOhterCount, bought_sum_exceed

