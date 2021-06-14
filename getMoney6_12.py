# -*- coding: utf-8 -*-
import requests
import execjs
import traceback
import matplotlib.pyplot as plt
import time



def get_url(code):
    # http://fund.eastmoney.com/pingzhongdata/005352.js?v=20210105201244
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = code + '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    url = head + tail
    print(url)
    return url


def get_worth(fund_code):
    content = requests.get(get_url(fund_code))
    js_content = execjs.compile(content.text)
    name = js_content.eval('fS_name')
    code = js_content.eval('fS_code')
    #单位净值走势
    net_worth_trend = js_content.eval('Data_netWorthTrend')
    AC_worth_trend = js_content.eval('Data_ACWorthTrend')
    net_worth = []
    AC_worth = []
    growth_rate = []



    for day_worth in net_worth_trend[::-1]:
        net_worth.append(day_worth['y'])
        growth_rate.append(day_worth['equityReturn'])
    for day_AC_worth in AC_worth_trend[::-1]:
        AC_worth.append(day_AC_worth[1])
    print(name, code)
    write_info_to_local(code, name, net_worth, AC_worth)
    return net_worth, AC_worth, name, growth_rate


def get_all_code():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    content = requests.get(url)
    js_content = execjs.compile(content.text)
    raw_data = js_content.eval('r')
    allCode = []
    for code in raw_data:
        allCode.append(code[0])
    return allCode


def get_info_from_local():
    netWorthFile = open('./netWorth.csv', 'r+')
    ACWorthFile = open('./ACWorth.csv', 'r+')
    str = netWorthFile.readline()
    str_list = str.split('\n')
    str_list = str_list[0].split(',')
    code = str_list[0]
    name = str_list[1]
    value = str_list[2:]
    net_worth = []
    for i in value:
        net_worth.append(float(i))

    netWorthFile.close()
    ACWorthFile.close()
    print(code)
    print(name)
    print(net_worth)
    return code, name, net_worth



def write_info_to_local(code, name, net_worth, AC_worth):
    net_worth_file = open('./netWorth.csv', 'w')
    AC_worth_file = open('./ACWorth.csv', 'w')
    net_worth_file.write("\' " + code + "\' ,")
    net_worth_file.write("\' " + name + "\' ,")
    net_worth_file.write(",". join(list(map(str, net_worth))))
    net_worth_file.write("\n")
    AC_worth_file.write("\' " + code + "\' ,")
    AC_worth_file.write("\' " + name + "\' ,")
    AC_worth_file.write(",". join(list(map(str, AC_worth))))
    AC_worth_file.write("\n")
    print("write" + code + "'s data success.")
    net_worth_file.close()
    AC_worth_file.close()
    return

def write_pic(list):
    plt.figure(figsize=(10, 5))
    plt.plot(list[:60][::-1])
    plt.show()





def others():
    print('start')
    all_code = get_all_code()

    net_worth, AC_worth, name, growth_rate = get_worth('001549')
    # 净值曲线
    plt.figure(figsize=(10, 5))
    plt.plot(net_worth[:60][::-1])
    plt.show()

    # 增长率曲线
    # plt.figure(figsize=(10, 5))
    # plt.plot(growth_rate[::-1])
    # plt.show()

    # 0.001

    growth_rate.reverse()
    net_worth.reverse()
    print(growth_rate)
    print(net_worth)

    growth_rate.sort()
    # -7.8767 7.6609
    rate_min = growth_rate[0]
    rate_max = growth_rate[-1]
    rate_start = float((int(rate_min * 10000) / 10) / 10000.0)
    rate_end = float((int(rate_max * 10000) / 10) / 10000.0)
    print(len(growth_rate))
    print(rate_min, rate_max)
    print(rate_start, rate_end)
    print('---------------')


    print(len(growth_rate))
    print(len(rate_div))
    print(len(set(growth_rate)))
    plt.plot(rate_x, rate_div, 'r')
    plt.show()


def strategy(net_worth, growth_rate):
    cash = 0
    total_hand = 0
    hand = 500
    cash -= hand * 1
    total_hand += hand
    max = len(net_worth)
    worth = cash + hand * 1
    worth_list = []
    worth_list.append(worth)
    for i in range(1, max - 1):
        if (growth_rate[i] > 0):
            if (total_hand >= hand):
                total_hand -= hand
                cash += net_worth[i] * hand
                worth = cash + hand * net_worth[i]
                worth_list.append(worth)
        if (growth_rate[i] < 0):
            total_hand += hand
            cash -= net_worth[i] * hand
            worth = cash + hand * net_worth[i]
            worth_list.append(worth)
    strategy_result(cash, hand, total_hand, worth_list)

def get_grow_rate(growth_rate, net_worth, s):
    growth_rate.reverse()
    net_worth.reverse()
    print(growth_rate)
    print(net_worth)
    growth_rate.sort()
    # -7.8767 7.6609
    rate_min = growth_rate[0]
    rate_max = growth_rate[-1]
    count = 0
    rate_r = rate_min
    rate_div = []
    rate_x = []
    flag = 0
    while (rate_r <= rate_max):
        while (rate_r <= growth_rate[flag] <= rate_r + s):
            count += 1
            flag += 1
            if (flag == len(growth_rate)):
                break
        rate_div.append(count)
        rate_x.append(rate_r)
        count = 0
        rate_r += s

    plt.figure(figsize=(20, 10))
    print(rate_div)
    print('sumR: ' + str(sum(growth_rate)))
    print('sumN: ' + str(sum(rate_div)))
    print(sum(growth_rate) / float((sum(rate_div))))


def strategy_result(cash, hand, total_hand, worth_list):
    plt.figure(figsize=(10, 5))
    plt.plot(worth_list[::-1])
    plt.show()

    print('---------strategy_result---------')
    print('cash: ' + str(cash))
    print('total_hand: ' + str(total_hand))
    worth_list.sort()
    print('worth:  ' + '\t' + str(cash + hand * net_worth[-1]))
    print('worst: ' + '\t' + str(worth_list[0]))
    print('best: ' + '\t' + str(worth_list[-1]))


def aver_list_start_to_end(w_list, start, end):
    sum_list_start_to_end = 0
    for i in range(start, end):
        sum_list_start_to_end += w_list[i]
    aver_list = sum_list_start_to_end / (end - start)
    return aver_list



def ma_20(worth_list):
    w_list = len(worth_list)
    ma_20_worth_list = []
    start = 0
    num = 0
    ma_20_worth_list.append(worth_list[0])
    for i in range(1, w_list):
        start = i - 20 if i - 20 > 0 else 0
        ma_20_worth_list.append(aver_list_start_to_end(worth_list, start, i))

    plt.figure(figsize=(10, 5))
    plt.plot(worth_list)
    plt.plot(ma_20_worth_list)
    plt.show()


    print(worth_list)
    print(ma_20_worth_list)
    return ma_20_worth_list


def ma_day_strategy(day, worth_list):
    w_list = len(worth_list)
    ma_worth_list = []
    start = 0
    num = 0
    ma_worth_list.append(worth_list[0])
    for i in range(1, w_list):
        start = i - day if i - day > 0 else 0
        ma_worth_list.append(aver_list_start_to_end(worth_list, start, i))
    return ma_worth_list


def ma_signal(worth_list, ma_worth1, ma_worth2):
    stage = [0.1, 0.2, 0.3, 0.4]
    amount = 100
    w_list = len(worth_list)
    ma_worth_list = []
    cash = []
    hand = []
    total_hand = []
    value = []
    cash.append(10)
    hand.append(0)
    total_hand.append(0)
    value.append(0)
    flag = 0
    print('in s')
    for i in range(1, w_list):
        if(ma_worth1[i] > ma_worth2[i]):
            if(flag < 4 and flag >= 0):
                hand.append(stage[flag])
                total_hand_p = total_hand[-1]
                total_hand.append(total_hand_p + hand[-1])
                cash_p = cash[-1]
                cash_d = cash_p - hand[-1] * (worth_list[i])
                cash.append(cash_d)
                value_d = cash[-1] + total_hand[-1] * worth_list[i]
                value.append(value_d)
            flag += 1
            if(flag > 4):
                hand.append(stage[3])
                cash.append(cash[-1])
                total_hand.append(total_hand[-1])
                value.append(cash[-1] + total_hand[-1] * worth_list[i])
        else:
            flag = 0
            total_hand_p = total_hand[-1]
            hand.append(total_hand_p * -1)
            total_hand.append(0)
            cash_p = cash[-1]
            cash.append(cash_p + total_hand_p * worth_list[i])
            value.append(cash[-1])
    #print('out s')
    #print(worth_list)
    #print(value)
    num = 0
    pre = 1
    for i in value:
        if i < pre:
            num += 1

    print(num)
    print(len(worth_list))
    print(len(value))
    value2 = []
    for i in worth_list:
        value2.append(i * 100)
    print(len(value2))
    print(value[-1])
    plt.figure(figsize=(10, 5))
    plt.plot(value)
    #plt.plot(cash[-200: -100])
    plt.plot(worth_list)
    #plt.plot(total_hand[-200: -100])
    # plt.plot(value2[-200: -100])
    '''
    plt.plot(net_worth[day:])
    plt.plot(ma_short1[day:], 'red')
    plt.plot(ma_short2[day:], 'yellow')
    plt.plot(ma_long1[day:], 'blue')
    plt.plot(ma_long2[day:], 'green')
    '''
    plt.show()


def ma_strategy(day_short_1, day_short_2, day_long_1, day_long_2, net_worth, day = 30):
    #net_worth.append(net_worth[-1] * 1)
    #net_worth.append(net_worth[-1] * 1)
    #net_worth.append(net_worth[-1] * 1)
    #net_worth.append(net_worth[-1] * 1)
    ma_short1 = ma_day_strategy(day_short_1, net_worth)
    print(ma_short1[-1])
    net_worth[-1] = net_worth[-1] * 1
    ma_short1 = ma_day_strategy(day_short_1, net_worth)

    print(ma_short1[-1])
    ma_short1 = ma_day_strategy(day_short_1, net_worth)
    ma_short2 = ma_day_strategy(day_short_2, net_worth)
    ma_long1 = ma_day_strategy(day_long_1, net_worth)
    ma_long2 = ma_day_strategy(day_long_2, net_worth)


    # ma_signal(worth_list, ma_short1, ma_short2)

    plt.figure(figsize=(10, 5))
    day *= -1
    #plt.plot(value[day:])

    plt.plot(net_worth[day:])
    plt.plot(ma_short1[day:], 'red')
    plt.plot(ma_short2[day:], 'yellow')
    plt.plot(ma_long1[day:], 'blue')
    plt.plot(ma_long2[day:], 'green')

    plt.show()



if __name__ == '__main__':
    code, name, net_worth = get_info_from_local()
    #net_worth, AC_worth, name, growth_rate = get_worth('001549')
    # strategy(net_worth, growth_rate)
    net_worth.reverse()
    print(net_worth)
    ma_strategy(6, 20, 60, 200, net_worth)


