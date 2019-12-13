#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import copy
import sys
import time

# import unicornhat as unicorn


WEATHER_LABEL = {
    '999': (9, 9, 9),
    # Group 2xx: Thunderstorm
    '200': (2, 0, 0),  # Thunderstorm	thunderstorm with light rain	11d
    '201': (2, 0, 1),  # Thunderstorm	thunderstorm with rain	11d
    '202': (2, 0, 2),  # Thunderstorm	thunderstorm with heavy rain	11d
    '210': (2, 1, 0),  # Thunderstorm	light thunderstorm	11d
    '211': (2, 1, 1),  # Thunderstorm	thunderstorm	11d
    '212': (2, 1, 2),  # Thunderstorm	heavy thunderstorm	11d
    '221': (2, 2, 1),  # Thunderstorm	ragged thunderstorm	11d
    '230': (2, 3, 0),  # Thunderstorm	thunderstorm with light drizzle	11d
    '231': (2, 3, 1),  # Thunderstorm	thunderstorm with drizzle	11d
    '232': (2, 3, 2),  # Thunderstorm	thunderstorm with heavy drizzle	11d
    # Group 3xx: Drizzle
    '300': (3, 0, 0),  # Drizzle	light intensity drizzle	09d
    '301': (3, 0, 1),  # Drizzle	drizzle	09d
    '302': (3, 0, 2),  # Drizzle	heavy intensity drizzle	09d
    '310': (3, 1, 0),  # Drizzle	light intensity drizzle rain	09d
    '311': (3, 1, 1),  # Drizzle	drizzle rain	09d
    '312': (3, 1, 2),  # Drizzle	heavy intensity drizzle rain	09d
    '313': (3, 1, 3),  # Drizzle	shower rain and drizzle	09d
    '314': (3, 1, 4),  # Drizzle	heavy shower rain and drizzle	09d
    '321': (3, 2, 1),  # Drizzle	shower drizzle	09d
    # Group 5xx: Rain
    '500': (5, 0, 0),  # Rain	light rain	10d
    '501': (5, 0, 1),  # Rain	moderate rain	10d
    '502': (5, 0, 2),  # Rain	heavy intensity rain	10d
    '503': (5, 0, 3),  # Rain	very heavy rain	10d
    '504': (5, 0, 4),  # Rain	extreme rain	10d
    '511': (5, 1, 1),  # Rain	freezing rain	13d
    '520': (5, 2, 0),  # Rain	light intensity shower rain	09d
    '521': (5, 2, 1),  # Rain	shower rain	09d
    '522': (5, 2, 2),  # Rain	heavy intensity shower rain	09d
    '531': (5, 3, 1),  # Rain	ragged shower rain	09d
    # Group 6xx: Snow
    '600': (6, 0, 0),  # Snow	light snow	13d
    '601': (6, 0, 1),  # Snow	Snow	13d
    '602': (6, 0, 2),  # Snow	Heavy snow	13d
    '611': (6, 1, 1),  # Snow	Sleet	13d
    '612': (6, 1, 2),  # Snow	Light shower sleet	13d
    '613': (6, 1, 3),  # Snow	Shower sleet	13d
    '615': (6, 1, 5),  # Snow	Light rain and snow	13d
    '616': (6, 1, 6),  # Snow	Rain and snow	13d
    '620': (6, 2, 0),  # Snow	Light shower snow	13d
    '621': (6, 2, 1),  # Snow	Shower snow	13d
    '622': (6, 2, 2),  # Snow	Heavy shower snow	13d
    # Group 7xx: Atmosphere
    '701': (7, 0, 1),  # Mist	mist	50d
    '711': (7, 1, 1),  # Smoke	Smoke	50d
    '721': (7, 2, 1),  # Haze	Haze	50d
    '731': (7, 3, 1),  # Dust	sand/ dust whirls	50d
    '741': (7, 4, 1),  # Fog	fog	50d
    '751': (7, 5, 1),  # Sand	sand	50d
    '761': (7, 6, 1),  # Dust	dust	50d
    '762': (7, 6, 2),  # Ash	volcanic ash	50d
    '771': (7, 7, 1),  # Squall	squalls	50d
    '781': (7, 8, 1),  # Tornado	tornado	50d
    # Group 800: Clear
    '800': (8, 0, 0),  # Clear	clear sky	01d 01n
    # Group 80x: Clouds
    '801': (8, 0, 1),  # Clouds	few clouds: 11-25%	02d 02n
    '802': (8, 0, 2),  # Clouds	scattered clouds: 25-50%	03d 03n
    '803': (8, 0, 3),  # Clouds	broken clouds: 51-84%	04d 04n
    '804': (8, 0, 4),  # Clouds	overcast clouds: 85-100%	04d 04n
}


def main():
    args = sys.argv
    args.pop(0)  # 先頭にある、スクリプト名の要素を除去

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

    # # Unicorn HATの設定
    # unicorn.set_layout(unicorn.AUTO)
    # unicorn.rotation(0)
    # unicorn.brightness(0.5)
    # width, height = unicorn.get_shape()

    # for y in range(height):
    #     for x in range(width):
    #         unicorn.set_pixel(x, y, 255, 0, 255)
    #         unicorn.show()

    #  リストを走査しながらLEDに出力
    print('for')
    for index in range(len_args+1):
        # 内側
        print(WEATHER_LABEL[args[index]])
        print(WEATHER_LABEL[args[index+1]])
        print(WEATHER_LABEL[args[index+2]])
        print(WEATHER_LABEL[args[index + 3]])
        print('------------')

    time.sleep(1)


if __name__ == "__main__":
    print("""Circles

    時系列の数値データを、同心円状に広がる光として表示する。
    """)
    main()
