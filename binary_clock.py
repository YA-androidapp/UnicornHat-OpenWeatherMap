#!/usr/bin/env python
from __future__ import print_function
from time import sleep
import configparser
import datetime
import json
import math
import requests
import sys
import time
import unicornhat

print("""True Binary Clock made by Jarrod Price, inspired by Iorga Dragos Florian and reviewed by Philip Howard
Displays the time on the LEDs as follows:
Top row ->  First 4 = Month(Pink), Last 4 = Day(Blue/Green. If Green add 16 to value shown, no lights = 16th)
Second row ->  First 2 = Alarm(Orange), Last 6 = Hour(Red)
Third row -> First 2 = Alarm(Orange), Last 6 = Minute(Yellow)
Fourth row ->  First 2 = Alarm(Orange), Last 6 = Second(Green)""")

unicornhat.set_layout(unicornhat.AUTO)
# default brightness does not need to be too bright
unicornhat.brightness(0.5)
# get the width of the hat because the LEDs are displayed from the righ to the left
width, height = unicornhat.get_shape()
right_most_pixel = width - 1

# colour tuples
red = (255, 0, 0)
orange = (255, 127, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 127, 255)
lightblue = (100, 200, 255)
magenta = (255, 0, 255)
white = (255, 255, 255)

TEMP_LABEL = {
    -5: (0x00, 0x55, 0xFF),
    -4: (0x33, 0x94, 0xFF),
    -3: (0x61, 0xC5, 0xFF),
    -2: (0x90, 0xE7, 0xFF),
    -1: (0xBf, 0xFA, 0xFF),
    0: (0xEF, 0xFF, 0xDE),
    1: (0xFF, 0xF5, 0xAE),
    2: (0xFF, 0xE7, 0x8E),
    3: (0xFF, 0xD2, 0x6F),
    4: (0xFF, 0xB5, 0x50),
    5: (0xFF, 0x95, 0x30),
    6: (0xFF, 0x6D, 0x14),
    7: (0xFF, 0x55, 0x00),
    8: (0xFF, 0x00, 0x00)
}

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


# alarm must be 24 hour format
alarm_time = '07:00'
# how many minutes should the alarm flash for
alarm_flash_time = 5
# inform the world what time the alarm will go off
print('Alarm set for: ', alarm_time)


def draw_time_string(time_string, length, offset, row, colour):
    """Draw the binary time on a specified row in a certain colour.

    :param time_string: string containing time value that will be used for the bit comparison
    :param length: width of the binary string once converted, e.g. 5 bits for day, 6 bits for hour and minute
    :param offset: left offset - all values are displayed with right alignment as conventional binary dictates, the offest will move it to the left
    :param row: row on which to display the time, this is the y-axis
    :param colour: colour to draw in

    """
    # convert the time string to an integer
    value = int(time_string)
    # loop through the pixels from the right to the left
    for i in range(right_most_pixel, right_most_pixel - length, -1):
        # use the & operator to do a bit comparison
        # for example:
        # 1 & 1 = 1 (ie: 0b1 & 0b1 = 0b1)
        # 2 & 1 = 0 (ie: 0b10 & 0b01 = 0b00)
        if value & 1:
            rgb = colour
        else:
            rgb = (0, 0, 0)
        # determine where on the row it should display this LED
        # either at the given location in the loop or shifted over to the left a little
        column = (i - offset)
        # set the pixels colour
        unicornhat.set_pixel(column, row, rgb)
        # use a binary shift to move all the values over to the right
        # for example:
        # 10 = 0b1010 shifted by 1 place becomes 0b0101 = 5
        # 5 = 0b101 shifted by place becomes 0b010 = 2
        value >>= 1


def show_id(x, index):
    unicornhat.set_pixel(x, 5, *WEATHER_LABEL[str(index)])


def show_max(x, tp):
    unicornhat.set_pixel(x, 6, *TEMP_LABEL[tp // 5])


def show_min(x, tp):
    unicornhat.set_pixel(x, 7, *TEMP_LABEL[tp // 5])


def show_weather(ids, maxs, mins):
    for i in range(8):
        show_id(i, ids[i])
        show_max(i, maxs[i])
        show_min(i, mins[i])


def utc_to_jst(timestamp_utc):
    datetime_utc = datetime.datetime.strptime(
        timestamp_utc + "+0000", "%Y-%m-%d %H:%M:%S%z")
    datetime_jst = datetime_utc.astimezone(
        datetime.timezone(datetime.timedelta(hours=+9)))
    timestamp_jst = datetime.datetime.strftime(
        datetime_jst, '%Y-%m-%d %H:%M:%S')
    return timestamp_jst


def get_owm():
    ini = configparser.ConfigParser()
    ini.read('./config.ini', 'UTF-8')

    city = "Tokyo,jp"
    key = ini['api']['key']
    url = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q=' + \
        city + '&APPID=' + key

    print(url)
    response = requests.get(url)
    data = json.loads(response.text)

    id_list = []
    min_list = []
    max_list = []

    for i in range(8):  # range(len(data["list"])):
        print(utc_to_jst(data["list"][i]["dt_txt"]))
        print("   main", data["list"][i]["weather"][0]["id"])
        print("   main", data["list"][i]["weather"][0]["main"])
        print("   temp", data["list"][i]["main"]["temp"])
        print("   pressure:", data["list"][i]["main"]["pressure"])
        print("   humidity:", data["list"][i]["main"]["humidity"])
        print("   temp_min:", data["list"][i]["main"]["temp_min"])
        print("   temp_max:", data["list"][i]["main"]["temp_max"])

        # Weather condition codes
        id_list.append(data["list"][i]["weather"][0]["id"])

        # temp
        temp_min = 0
        temp_max = 0
        try:
            temp_min = float(data["list"][i]["main"]["temp_min"])
        except Exception as e:
            print(e)

        try:
            temp_max = float(data["list"][i]["main"]["temp_max"])
        except Exception as e:
            print(e)

        min_list.append(temp_min)
        max_list.append(temp_max)

    return id_list, min_list, max_list


ids, mins, maxs = get_owm()

# this function will make use of the remaining space to light up when indicated


def alarm(t, c):
    # by default we will assume the alarm will not be triggered so keep the default states of the brightness and LED colours
    unicornhat.brightness(0.5)
    b = '0'
    # grab the hour and minute from the set alarm time
    h = int(alarm_time[:2])
    m = int(alarm_time[3:])
    s = 0
    # create time slot for alarm for today
    at = t.replace(hour=h, minute=m, second=s)
    # create a new time object by adding x minutes to the alarm time
    ft = at + datetime.timedelta(minutes=alarm_flash_time)
    # now check if it's time to flash the alarm or not, by checking if we have passed the time it is meant to go off or 5 minutes have not gone passed
    if t >= at and t < ft:
        # signal the alarm!
        # set the brightness to max
        unicornhat.brightness(1)
        # this will make it flash ON when a second is equal and OFF when it is odd
        if int(t.second % 2) == 0:
            # when converted to binary becomes 0b11, so this will turn ON 2 LEDs per row
            b = '3'
    # always update the pixels, the logic above will decide if it displays or not
    # 3 rows, 2 LEDs wide for the alarm, padded to left by 6
    draw_time_string(b, 2, 6, 1, c)
    draw_time_string(b, 2, 6, 2, c)
    draw_time_string(b, 2, 6, 3, c)


# this is the main function, will get the current time and display each time and check the alarm
def binary_clock():
    try:
        run_i = 0
        while True:

            if run_i > 57 * 60:  # for using other scripts
                break

            now = datetime.datetime.now()

            # draw each time string in their specific locations
            draw_time_string(now.month, 4, 4, 0, magenta)

            # Day field is 4 bits (lights) long, and as we don't use 0-indexed
            # days of the month, that means we can only represent 1-15 (0b1 - 0b1111)
            # To solve this, if the day > 15 (0b1111), we change the colour to indidcate
            # that 16 (0b10000) must be added to the displayed value.
            if now.day > 0b1111:
                # Day > 15

                # Truncate the day to only 4 bits, as we only have 4 lights
                # This will remove the bit representing 16, which will
                # be encoded as colour
                day = now.day & 0b1111

                # Encode the missing bit as colour
                day_colour = green
            else:
                # Day is 15 or less so the bit representing 16 is not set and the number can be displayed normally
                day = now.day
                day_colour = blue

            draw_time_string(day, 4, 0, 0, day_colour)
            draw_time_string(now.hour, 6, 0, 1, red)
            draw_time_string(now.minute, 6, 0, 2, yellow)
            draw_time_string(now.second, 6, 0, 3, green)

            # check if the alarm needs to be signalled or not
            alarm(now, orange)

            show_weather(ids, maxs, mins)

            # we've now set all the LEDs, time to show the world our glory!
            unicornhat.show()

            # sleep for 1 second, because we don't want to waste unnecessary CPU
            sleep(1)

            run_i += 1

    except Exception as e:
        print(e)

    print("Exiting")


if __name__ == "__main__":
    binary_clock()
