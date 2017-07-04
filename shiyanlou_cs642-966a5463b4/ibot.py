# _*_ coding: utf-8 _*_
# six

# 导入模块
from distutils.log import warn as printf
import sys
from bosonnlp import BosonNLP
from os.path import expanduser
import os
import collections
import subprocess
import datetime

# 配置 API 密钥
bosonnlp_token = 'BosonNLP API KEY'

# 调用 bosonnlp 对自然语言的查询语句实体进行识别
class QueryParser(object):
    def __init__(self):
        self.nlp = BosonNLP(bosonnlp_token)

    def parse(self, query_string):
        """
            input:
            3月19号 北京到长沙的高铁票
            # 调用 BosonNLP 命名实体识别接口
            # 参考：https://bosonnlp-py.readthedocs.io/#id2

            output:
            [{'entity': [[0, 3, 'time'], [3, 4, 'location'], [5, 6, 'location']],
            'tag': ['t', 'm', 'q', 'ns', 'p', 'ns', 'ude', 'n', 'n'],
            'word': ['3月', '19', '号', '北京', '到', '长沙', '的', '高铁', '票']}]

        """
        result = self.nlp.ner(query_string)[0]
        words = result['word']
        tags = result['tag']
        entities = result['entity']
        return (words, entities, tags)

    def get_entity(self, parsed_words, index_tuple):
        """
            获取已识别的实体
            采用 filter
            参考 python cookbook 部分
            input:
                entities: 二元组
                parsed_words: 解析好的词组

        """
        return parsed_words[index_tuple[0]: index_tuple[1]]

    def format_entities(self, entities):
        """
            给元组命名
        """ 
        namedentity = collections.namedtuple('namedentity', 'index_begin index_end entity_name')
        return [namedentity(entity[0], entity[1], entity[2]) for entity in entities]

    def get_format_time(self, time_entity):
        """
            # BosonNLP 时间描述转换接口
            output
            {'timestamp': '2017-03-18 16:30:29', 'type': 'timestamp'}

        """
        basetime = datetime.datetime.today()
        result = self.nlp.convert_time(time_entity, basetime)
        timestamp = result["timestamp"]
        return timestamp.split(" ")[0]

# 火车票查询函数
def pattern_train_ticket(query):
    query_parse = QueryParser()
    (words, entities, tags) = query_parse.parse(query)
    # 给元组命名，整体 filter    
    namedentities = query_parse.format_entities(entities)
    # 检查实体的数量，count，元组，token
    time_nameentity = [nameentity for nameentity in namedentities if nameentity.entity_name == "time"][0]
    location_nameentities = [nameentity for nameentity in namedentities if nameentity.entity_name == "location"]

    sorted_location_nameentities = sorted(location_nameentities, key = lambda a:a[1])
    # 排序为在序列表 list.sort() 按照第一个元素排序 sorted(a)，按顺序，sorted(a, key = lambda a:a[1]) 按第二个元素排序
    time_entity = query_parse.get_entity(words, (time_nameentity.index_begin, time_nameentity.index_end))
    time_string = "".join(time_entity)
    format_time = query_parse.get_format_time(time_string)

    location_from_nameentity = sorted_location_nameentities[0]
    # 较前边的，出发地
    location_from_entity = query_parse.get_entity(words, (location_from_nameentity.index_begin, location_from_nameentity.index_end))
    location_from_string = "".join(location_from_entity)

    location_to_nameentity = sorted_location_nameentities[1]
    # 较后边的，目的地
    location_to_entity = query_parse.get_entity(words, (location_to_nameentity.index_begin, location_to_nameentity.index_end))
    location_to_string = "".join(location_to_entity)
    # 正式查询
    call_train_ticket(location_from_string, location_to_string, format_time)
    return

# 调用 tickets
def call_train_ticket(location_from_entity, location_to_entity, time_entity):
    printf(subprocess.call(["tickets", location_from_entity, location_to_entity, time_entity]))

def main():
    query = " ".join(sys.argv[1:])
    printf(query)
    printf("*" * 8)
    pattern_train_ticket(query)

if __name__ == '__main__':
    main()
