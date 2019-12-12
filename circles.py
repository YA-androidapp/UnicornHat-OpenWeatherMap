#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import copy
import sys
import time

# import unicornhat as unicorn


WEATHER_LABEL = {
    '000': (0, 0, 0),
    # Group 2xx: Thunderstorm
    '200': (0, 0, 0),  # Thunderstorm	thunderstorm with light rain	11d
    '201': (0, 0, 0),  # Thunderstorm	thunderstorm with rain	11d
    '202': (0, 0, 0),  # Thunderstorm	thunderstorm with heavy rain	11d
    '210': (0, 0, 0),  # Thunderstorm	light thunderstorm	11d
    '211': (0, 0, 0),  # Thunderstorm	thunderstorm	11d
    '212': (0, 0, 0),  # Thunderstorm	heavy thunderstorm	11d
    '221': (0, 0, 0),  # Thunderstorm	ragged thunderstorm	11d
    '230': (0, 0, 0),  # Thunderstorm	thunderstorm with light drizzle	11d
    '231': (0, 0, 0),  # Thunderstorm	thunderstorm with drizzle	11d
    '232': (0, 0, 0),  # Thunderstorm	thunderstorm with heavy drizzle	11d
    # Group 3xx: Drizzle
    '300': (0, 0, 0),  # Drizzle	light intensity drizzle	09d
    '301': (0, 0, 0),  # Drizzle	drizzle	09d
    '302': (0, 0, 0),  # Drizzle	heavy intensity drizzle	09d
    '310': (0, 0, 0),  # Drizzle	light intensity drizzle rain	09d
    '311': (0, 0, 0),  # Drizzle	drizzle rain	09d
    '312': (0, 0, 0),  # Drizzle	heavy intensity drizzle rain	09d
    '313': (0, 0, 0),  # Drizzle	shower rain and drizzle	09d
    '314': (0, 0, 0),  # Drizzle	heavy shower rain and drizzle	09d
    '321': (0, 0, 0),  # Drizzle	shower drizzle	09d
    # Group 5xx: Rain
    '500': (0, 0, 0),  # Rain	light rain	10d
    '501': (0, 0, 0),  # Rain	moderate rain	10d
    '502': (0, 0, 0),  # Rain	heavy intensity rain	10d
    '503': (0, 0, 0),  # Rain	very heavy rain	10d
    '504': (0, 0, 0),  # Rain	extreme rain	10d
    '511': (0, 0, 0),  # Rain	freezing rain	13d
    '520': (0, 0, 0),  # Rain	light intensity shower rain	09d
    '521': (0, 0, 0),  # Rain	shower rain	09d
    '522': (0, 0, 0),  # Rain	heavy intensity shower rain	09d
    '531': (0, 0, 0),  # Rain	ragged shower rain	09d
    # Group 6xx: Snow
    '600': (0, 0, 0),  # Snow	light snow	13d
    '601': (0, 0, 0),  # Snow	Snow	13d
    '602': (0, 0, 0),  # Snow	Heavy snow	13d
    '611': (0, 0, 0),  # Snow	Sleet	13d
    '612': (0, 0, 0),  # Snow	Light shower sleet	13d
    '613': (0, 0, 0),  # Snow	Shower sleet	13d
    '615': (0, 0, 0),  # Snow	Light rain and snow	13d
    '616': (0, 0, 0),  # Snow	Rain and snow	13d
    '620': (0, 0, 0),  # Snow	Light shower snow	13d
    '621': (0, 0, 0),  # Snow	Shower snow	13d
    '622': (0, 0, 0),  # Snow	Heavy shower snow	13d
    # Group 7xx: Atmosphere
    '701': (0, 0, 0),  # Mist	mist	50d
    '711': (0, 0, 0),  # Smoke	Smoke	50d
    '721': (0, 0, 0),  # Haze	Haze	50d
    '731': (0, 0, 0),  # Dust	sand/ dust whirls	50d
    '741': (0, 0, 0),  # Fog	fog	50d
    '751': (0, 0, 0),  # Sand	sand	50d
    '761': (0, 0, 0),  # Dust	dust	50d
    '762': (0, 0, 0),  # Ash	volcanic ash	50d
    '771': (0, 0, 0),  # Squall	squalls	50d
    '781': (0, 0, 0),  # Tornado	tornado	50d
    # Group 800: Clear
    '800': (0, 0, 0),  # Clear	clear sky	01d 01n
    # Group 80x: Clouds
    '801': (0, 0, 0),  # Clouds	few clouds: 11-25%	02d 02n
    '802': (0, 0, 0),  # Clouds	scattered clouds: 25-50%	03d 03n
    '803': (0, 0, 0),  # Clouds	broken clouds: 51-84%	04d 04n
    '804': (0, 0, 0),  # Clouds	overcast clouds: 85-100%	04d 04n
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
        args.append('000')

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
    for item in args:
        pass

    time.sleep(1)


if __name__ == "__main__":
    print("""Circles

    時系列の数値データを、同心円状に広がる光として表示する。
    """)
    main()
