#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import configparser
import datetime
import json
import requests


ini = configparser.ConfigParser()
ini.read('./config.ini', 'UTF-8')


city = "Tokyo,jp"
key = ini['api']['key']
url = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q=' + \
    city + '&APPID=' + key


def utc_to_jst(timestamp_utc):
    datetime_utc = datetime.datetime.strptime(
        timestamp_utc + "+0000", "%Y-%m-%d %H:%M:%S%z")
    datetime_jst = datetime_utc.astimezone(
        datetime.timezone(datetime.timedelta(hours=+9)))
    timestamp_jst = datetime.datetime.strftime(
        datetime_jst, '%Y-%m-%d %H:%M:%S')
    return timestamp_jst


print(url)
response = requests.get(url)

data = json.loads(response.text)

for i in range(len(data["list"])):
    print(utc_to_jst(data["list"][i]["dt_txt"]))
    print("   main", data["list"][i]["weather"][0]["main"])
    print("   temp", data["list"][i]["main"]["temp"])
    print("   pressure:", data["list"][i]["main"]["pressure"])
    print("   humidity:", data["list"][i]["main"]["humidity"])
    print("   temp_min:", data["list"][i]["main"]["temp_min"])
    print("   temp_max:", data["list"][i]["main"]["temp_max"])
