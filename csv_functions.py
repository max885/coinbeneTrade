# -*- coding: utf-8 -*-
import csv
from manbiapi import *
import random

# csv文件读取某行数据
def read_n_line(file_name,n):
    with open(file_name, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for i, rows in enumerate(reader):
            if i == n:
                row = rows
                return row


# csv文件中第一个空行数
def finished_trade(file_name):
    myfile = open(file_name)
    lines = len(myfile.readlines())
    return lines

# 清空csv文件
def empty_file(file_name):
    file = open(file_name, 'w')
    file.truncate()
    file.close()


# 把数组保存到文件中
def save_list(file_name,list_name):
    file = open(file_name, 'ab+')
    writer = csv.writer(file)
    writer.writerow(list_name)


# 把当此下卖单的完成情况写入csv文件
def write_trade_result(file_name,price):
    file = open(file_name, 'ab+')
    writer = csv.writer(file)
    temp = []
    temp.append(price)
    writer.writerow(temp)
    file.close()


# 把这一次的下单价格写入csv文档
def save_price_csv(file_name,price):
    file = open(file_name, 'w+')
    writer = csv.writer(file)
    temp = []
    temp.append(price)
    writer.writerow(temp)
    file.close()


# 计算现在已经完成了多少总交易量
def current_finished(file_name):
    file = open(file_name, 'r')
    reader = csv.reader(file)
    sum_trade = 0
    for aa in reader:
        trade_number = aa
        sum_trade = sum_trade + int(trade_number[0])
    return sum_trade


# 从csv文档中读上一个挂单数据
def read_price_csv(file_name):
    file = open(file_name, 'r')
    reader = csv.reader(file)
    for aa in reader:
        price = aa
    return price