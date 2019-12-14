#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import copy
import sys
import time

import unicornhat as unicorn


WEATHER_LABEL = {
    '999': (9, 9, 9),
    # Group 2xx: Thunderstorm
    '200': (252, 252, 3),  # Thunderstorm	thunderstorm with light rain	11d
    '201': (252, 252, 3),  # Thunderstorm	thunderstorm with rain	11d
    '202': (252, 252, 3),  # Thunderstorm	thunderstorm with heavy rain	11d
    '210': (252, 252, 3),  # Thunderstorm	light thunderstorm	11d
    '211': (252, 252, 3),  # Thunderstorm	thunderstorm	11d
    '212': (252, 252, 3),  # Thunderstorm	heavy thunderstorm	11d
    '221': (252, 252, 3),  # Thunderstorm	ragged thunderstorm	11d
    '230': (252, 252, 3),  # Thunderstorm	thunderstorm with light drizzle	11d
    '231': (252, 252, 3),  # Thunderstorm	thunderstorm with drizzle	11d
    '232': (252, 252, 3),  # Thunderstorm	thunderstorm with heavy drizzle	11d
    # Group 3xx: Drizzle
    '300': (3, 170, 252),  # Drizzle	light intensity drizzle	09d
    '301': (3, 166, 252),  # Drizzle	drizzle	09d
    '302': (3, 162, 252),  # Drizzle	heavy intensity drizzle	09d
    '310': (3, 158, 252),  # Drizzle	light intensity drizzle rain	09d
    '311': (3, 154, 252),  # Drizzle	drizzle rain	09d
    '312': (3, 152, 252),  # Drizzle	heavy intensity drizzle rain	09d
    '313': (3, 148, 252),  # Drizzle	shower rain and drizzle	09d
    '314': (3, 144, 252),  # Drizzle	heavy shower rain and drizzle	09d
    '321': (3, 140, 252),  # Drizzle	shower drizzle	09d
    # Group 5xx: Rain
    '500': (3, 39, 252),  # Rain	light rain	10d
    '501': (3, 35, 252),  # Rain	moderate rain	10d
    '502': (3, 31, 252),  # Rain	heavy intensity rain	10d
    '503': (3, 27, 252),  # Rain	very heavy rain	10d
    '504': (3, 23, 252),  # Rain	extreme rain	10d
    '511': (3, 19, 252),  # Rain	freezing rain	13d
    '520': (3, 15, 252),  # Rain	light intensity shower rain	09d
    '521': (3, 11, 252),  # Rain	shower rain	09d
    '522': (3, 7, 252),  # Rain	heavy intensity shower rain	09d
    '531': (3, 3, 252),  # Rain	ragged shower rain	09d
    # Group 6xx: Snow
    '600': (255, 255, 255),  # Snow	light snow	13d
    '601': (255, 255, 255),  # Snow	Snow	13d
    '602': (255, 255, 255),  # Snow	Heavy snow	13d
    '611': (255, 255, 255),  # Snow	Sleet	13d
    '612': (255, 255, 255),  # Snow	Light shower sleet	13d
    '613': (255, 255, 255),  # Snow	Shower sleet	13d
    '615': (255, 255, 255),  # Snow	Light rain and snow	13d
    '616': (255, 255, 255),  # Snow	Rain and snow	13d
    '620': (255, 255, 255),  # Snow	Light shower snow	13d
    '621': (255, 255, 255),  # Snow	Shower snow	13d
    '622': (255, 255, 255),  # Snow	Heavy shower snow	13d
    # Group 7xx: Atmosphere
    '701': (3, 252, 252),  # Mist	mist	50d
    '711': (3, 248, 252),  # Smoke	Smoke	50d
    '721': (3, 244, 252),  # Haze	Haze	50d
    '731': (3, 240, 252),  # Dust	sand/ dust whirls	50d
    '741': (3, 236, 252),  # Fog	fog	50d
    '751': (3, 232, 252),  # Sand	sand	50d
    '761': (3, 228, 252),  # Dust	dust	50d
    '762': (3, 224, 252),  # Ash	volcanic ash	50d
    '771': (3, 220, 252),  # Squall	squalls	50d
    '781': (3, 216, 252),  # Tornado	tornado	50d
    # Group 800: Clear
    '800': (252, 140, 3),  # Clear	clear sky	01d 01n
    # Group 80x: Clouds
    '801': (192, 192, 192),  # Clouds	few clouds: 11-25%	02d 02n
    '802': (168, 168, 168),  # Clouds	scattered clouds: 25-50%	03d 03n
    '803': (144, 144, 144),  # Clouds	broken clouds: 51-84%	04d 04n
    '804': (120, 120, 120),  # Clouds	overcast clouds: 85-100%	04d 04n
}


def show(args):
    # for test
    args = ['803', '804', '804', '804', '500', '500', '804', '803', '802', '800', '800', '800', '800', '800', '800', '800', '800', '800', '800', '800',
            '802', '804', '804', '804', '804', '500', '500', '804', '500', '500', '500', '500', '804', '804', '804', '804', '500', '500', '803', '803']

    # ダミー要素を追加する前にリストの長さを取得
    len_args = len(args)

    # 8 / 2 = 4末尾にダミーの要素を追加
    for i in range(4):
        args.append('999')

    print('args')
    print(args)

    # Unicorn HATの設定
    unicorn.set_layout(unicorn.AUTO)
    unicorn.rotation(0)
    unicorn.brightness(0.5)
    width, height = unicorn.get_shape()

    #  リストを走査しながらLEDに出力
    print('for')
    for index in range(len_args+1):
        # 内側
        # print(WEATHER_LABEL[args[index]])
        show_leds(0, *WEATHER_LABEL[args[index]])
        # print(WEATHER_LABEL[args[index+1]])
        show_leds(1, *WEATHER_LABEL[args[index + 1]])
        # print(WEATHER_LABEL[args[index+2]])
        show_leds(2, *WEATHER_LABEL[args[index + 2]])
        # print(WEATHER_LABEL[args[index + 3]])
        show_leds(3, *WEATHER_LABEL[args[index + 3]])
        print('------------')
        unicorn.show()

    time.sleep(1)


def show_leds(num, r, g, b):
    print('{} {} {} {}'.format(num, r, g, b))
    if 0 == num:
        unicorn.set_pixel(3, 3, r, g, b)
        unicorn.set_pixel(3, 4, r, g, b)
        unicorn.set_pixel(4, 3, r, g, b)
        unicorn.set_pixel(4, 4, r, g, b)
    elif 1 == num:
        unicorn.set_pixel(2, 2, r, g, b)
        unicorn.set_pixel(2, 3, r, g, b)
        unicorn.set_pixel(2, 4, r, g, b)
        unicorn.set_pixel(2, 5, r, g, b)
        unicorn.set_pixel(3, 2, r, g, b)
        unicorn.set_pixel(3, 5, r, g, b)
        unicorn.set_pixel(4, 2, r, g, b)
        unicorn.set_pixel(4, 5, r, g, b)
        unicorn.set_pixel(5, 2, r, g, b)
        unicorn.set_pixel(5, 3, r, g, b)
        unicorn.set_pixel(5, 4, r, g, b)
        unicorn.set_pixel(5, 5, r, g, b)
    elif 2 == num:
        unicorn.set_pixel(1, 1, r, g, b)
        unicorn.set_pixel(1, 2, r, g, b)
        unicorn.set_pixel(1, 3, r, g, b)
        unicorn.set_pixel(1, 4, r, g, b)
        unicorn.set_pixel(1, 5, r, g, b)
        unicorn.set_pixel(1, 6, r, g, b)
        unicorn.set_pixel(2, 1, r, g, b)
        unicorn.set_pixel(2, 6, r, g, b)
        unicorn.set_pixel(3, 1, r, g, b)
        unicorn.set_pixel(3, 6, r, g, b)
        unicorn.set_pixel(4, 1, r, g, b)
        unicorn.set_pixel(4, 6, r, g, b)
        unicorn.set_pixel(5, 1, r, g, b)
        unicorn.set_pixel(5, 6, r, g, b)
        unicorn.set_pixel(6, 1, r, g, b)
        unicorn.set_pixel(6, 2, r, g, b)
        unicorn.set_pixel(6, 3, r, g, b)
        unicorn.set_pixel(6, 4, r, g, b)
        unicorn.set_pixel(6, 5, r, g, b)
        unicorn.set_pixel(6, 6, r, g, b)
    elif 3 == num:
        unicorn.set_pixel(0, 0, r, g, b)
        unicorn.set_pixel(0, 1, r, g, b)
        unicorn.set_pixel(0, 2, r, g, b)
        unicorn.set_pixel(0, 3, r, g, b)
        unicorn.set_pixel(0, 4, r, g, b)
        unicorn.set_pixel(0, 5, r, g, b)
        unicorn.set_pixel(0, 6, r, g, b)
        unicorn.set_pixel(0, 7, r, g, b)
        unicorn.set_pixel(1, 0, r, g, b)
        unicorn.set_pixel(1, 7, r, g, b)
        unicorn.set_pixel(2, 0, r, g, b)
        unicorn.set_pixel(2, 7, r, g, b)
        unicorn.set_pixel(3, 0, r, g, b)
        unicorn.set_pixel(3, 7, r, g, b)
        unicorn.set_pixel(4, 0, r, g, b)
        unicorn.set_pixel(4, 7, r, g, b)
        unicorn.set_pixel(5, 0, r, g, b)
        unicorn.set_pixel(5, 7, r, g, b)
        unicorn.set_pixel(6, 0, r, g, b)
        unicorn.set_pixel(6, 7, r, g, b)
        unicorn.set_pixel(7, 0, r, g, b)
        unicorn.set_pixel(7, 1, r, g, b)
        unicorn.set_pixel(7, 2, r, g, b)
        unicorn.set_pixel(7, 3, r, g, b)
        unicorn.set_pixel(7, 4, r, g, b)
        unicorn.set_pixel(7, 5, r, g, b)
        unicorn.set_pixel(7, 6, r, g, b)
        unicorn.set_pixel(7, 7, r, g, b)


if __name__ == "__main__":
    print("""Circles

    時系列の数値データを、同心円状に広がる光として表示する。
    """)
    args = sys.argv
    args.pop(0)  # 先頭にある、スクリプト名の要素を除去
    show(args)
