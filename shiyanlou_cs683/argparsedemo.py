import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Process some integers.")
# 添加参数
parser.add_argument("-p", dest="port", type=int,
                    help="An port number!")
# 解析命令行参数
args = parser.parse_args()
print("Port: ", args.port)
