import sys
import re
import requests
import bs4
import time
import json
import urllib as urlparse
import http.client
from get_city import get_CityName

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
}


def get_weather_li():

    def get_city_code(city):
        try:
            parameter = urlparse.parse.urlencode({'cityname': city})
            conn = http.client.HTTPConnection('toy1.weather.com.cn', 80, timeout=5)
            conn.request('GET', '/search?' + parameter)
            r = conn.getresponse()
            data = r.read().decode()[1:-1]
            json_data = json.loads(data)
            code = json_data[0]['ref'].split('~')[0]
            return code
        except:
            print(' [!] 错误，未能找到该地区信息')
            print(" [#] 退出脚本")
            sys.exit()

    def get_weaPage(url, headers):
        res = requests.get(url, headers=headers)
        s = res.content
        s.decode('ISO-8859-1')
        bs = bs4.BeautifulSoup(s, "html.parser")
        html = bs.prettify()
        return html

    def GetItem(name, list):
        name = re.findall(r'"' + list + '":"(.*?)"', name)
        name = "".join(name)
        return name

    def get_weather(City_code, li):

        headers1 = {
            'Referer': "http://www.weather.com.cn",
            'Cookie': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
        }

        t = time.time()
        timestamp = str(int(round(t * 1000)))
        port = "http://d1.weather.com.cn/weather_index/" + City_code + ".html?_=" + timestamp
        html = get_weaPage(port, headers1)

        wea_list_all = html.split("var")
        html1 = wea_list_all[1]
        wea_list1 = html1.split(",")

        # 城市英文
        city_en = wea_list1[1]
        city_en = GetItem(city_en, "cityname")
        # 温度区间
        maxtemp = wea_list1[2]
        maxtemp = GetItem(maxtemp, "temp")

        mintemp = wea_list1[3]
        mintemp = GetItem(mintemp, "tempn")
        # 实时天气
        wea_now = wea_list1[4]
        wea_now = GetItem(wea_now, "weather")

        # alarmDZ
        # -----------------------------------------------------
        wea_list2 = wea_list_all[2]
        wea_alarm_all = re.findall(r'alarmDZ ={"w":\[(.*?)\]};', wea_list2)
        warning = 0
        EmptyList = ['']
        if wea_alarm_all == EmptyList:
            pass
        else:
            warning = 1

        # dataSK
        # -----------------------------------------------------
        html3 = wea_list_all[3]
        wea_list3 = html3.split(",")
        # 城市
        cityname = wea_list3[1]
        cityname = GetItem(cityname, "cityname")
        # 当前温度
        temp_now = wea_list3[3]
        temp_now = GetItem(temp_now, "temp")
        # 湿度
        wet = wea_list3[9]
        wet = GetItem(wet, "SD")
        # 时间
        update = wea_list3[13]
        update = GetItem(update, "time")
        # 空气质量
        aqi = wea_list3[16]
        aqi = GetItem(aqi, "aqi")
        # PM2.5
        aqi_pm25 = wea_list3[17]
        aqi_pm25 = GetItem(aqi_pm25, "aqi_pm25")
        # 日期
        date = wea_list3[22]
        date = GetItem(date, "date")
        # dataZS
        wea_list4 = wea_list_all[4]
        umbrella = GetItem(wea_list4, "ys_des_s")
        # 和风天气
        qwea_url = "https://www.qweather.com/weather/" + city_en + "-" + City_code + ".html"
        qwea_html = get_weaPage(qwea_url, headers)
        wea_comment = re.findall(r'<p class="c-city-weather-current__abstract">(.*?)</p>'
                                 , qwea_html, flags=16)
        wea_comment = "".join(wea_comment)
        aqi_level = re.findall(r'<p class="air-chart-container__aqi-level">(.*?)</p>'
                               , qwea_html, flags=16)
        aqi_level = aqi_level[0].replace("\n", "")
        aqi_level = aqi_level.replace(" ", "")
        # wea_comment = wea_comment.strip('\n')
        wea_comment = wea_comment.replace(" ", "").replace("\n", "")

        res_weather_lines = li

        res_weather_lines.append(wea_comment)

        res_weather_lines.append(" ==================================")
        res_weather_lines.append(" 定位城市:  " + cityname)
        res_weather_lines.append(" 实时天气:  " + wea_now)
        res_weather_lines.append(" 实时温度:  " + temp_now + "℃")
        res_weather_lines.append(" 温度区间:  " + maxtemp + "℃ - " + mintemp + "℃")
        res_weather_lines.append(" 空气湿度:  " + wet)
        res_weather_lines.append(" 空气质量:  " + aqi + "(" + aqi_level + "),PM2.5: " + aqi_pm25)
        res_weather_lines.append(" 雨具携带:  " + umbrella)
        res_weather_lines.append(" [更新时间: " + date + " " + update + "]")
        res_weather_lines.append(" ==================================")
        if warning == 1:
            wea_alarm_all = "".join(wea_alarm_all)
            wea_alarm = re.findall(r'"w9":"(.*?)"', wea_alarm_all)
            wea_counter = len(wea_alarm)
            if wea_counter == 1:
                res_weather_lines.append(" [!]气象部门发布预警,请注意:")
            else:
                res_weather_lines.append(" [!]气象部门发布" + str(wea_counter) + "则预警,请注意:")
            if wea_alarm == "":
                res_weather_lines.append(" [!]无法获取气象预警详情")
            else:
                i = 1
                for alarm in wea_alarm:
                    alarm = alarm.replace("\\", "")
                    alarm = alarm.replace("：", ":\n ", 1)
                    if wea_counter == 1:
                        res_weather_lines.append(" " + alarm)
                    else:
                        res_weather_lines.append(" [" + str(i) + "]" + alarm)
                        i = i + 1
        return res_weather_lines

    try:
        address = get_CityName()
        li = []
        li.append(" [+] 自动定位位置：" + address)
        code = get_city_code(address)
        li = get_weather(code, li)
        return li
    except Exception as Error:
        raise Error
    pass
