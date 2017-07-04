#! /usr/bin/python3
# coding: utf-8

"""火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help    显示帮助菜单
    -g    高铁
    -d    动车
    -t    特快
    -k    快速
    -z    直达

Example:
    tickets 北京 广州 2017-03-17
    tickets -dg 成都 上海 2017-03-17

"""

""" 
注意：以下几条语句一定要写在__doc__下面，否则会出现类似
      ‘TypeError: expected string or buffer’这样的错误

      上面__doc__每行加四个空格，否则会有错误

"""

from docopt import docopt
from stations import stations
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
from colorama import init, Fore

init()

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

            :param available_trains: 一个列表，包含可获得的火车班次，每个火车班次是一个字典
            :param options: 查询的选项，如高铁，动车，etc...

        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, raw_train):
        # 请看下面一条语句，较教程多了一处 ['queryLeftNewDTO'] 变化
        duration = raw_train['queryLeftNewDTO']['lishi'].replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_no = raw_train['queryLeftNewDTO']['station_train_code']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                # Fore.RESET 这句还是得有的，不然表格外框也会有颜色
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + raw_train['queryLeftNewDTO']['from_station_name'] + Fore.RESET,
                            Fore.RED + raw_train['queryLeftNewDTO']['to_station_name']]) + Fore.RESET,
                    '\n'.join([Fore.GREEN + raw_train['queryLeftNewDTO']['start_time'] + Fore.RESET,
                            Fore.RED + raw_train['queryLeftNewDTO']['arrive_time']]) + Fore.RESET,
                    self._get_duration(raw_train),
                    raw_train['queryLeftNewDTO']['zy_num'],
                    raw_train['queryLeftNewDTO']['ze_num'],
                    raw_train['queryLeftNewDTO']['rw_num'],
                    raw_train['queryLeftNewDTO']['yw_num'],
                    raw_train['queryLeftNewDTO']['yz_num'],
                    raw_train['queryLeftNewDTO']['wz_num'],
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """ command-line interface """
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    train_date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(train_date, from_station, to_station)
    # 获取参数
    options = ''.join([key for key, value in arguments.items() if value is True])
    headers = {
        'Host': 'kyfw.12306.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    """

    下面一条语句还是得有的，不然会出现如下错误：
    InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)

    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # 添加verify=False参数表示不验证证书，headers = headers假装自己是在浏览器查看页面
    r = requests.get(url, headers = headers, verify = False)

    available_trains = r.json()['data']
    TrainsCollection(available_trains, options).pretty_print()

if __name__ == '__main__':
    cli()
