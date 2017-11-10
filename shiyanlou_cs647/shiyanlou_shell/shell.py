import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import *

# 命令与函数间映射字典
built_in_cmds = {}

def register_command(name, func):
    """
    注册命令，使命令与相应处理函数建立映射关系
    @param name: 命令名
    @param func: 函数名
    """

    built_in_cmds[name] = func


def init():
    """
    注册所有命令
    """

    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)


def display_cmd_prompt():
    # getpass.getuser 用于获取当前用户名
    user = getpass.getuser()

    # socket.gethostname() 返回当前运行 python 程序的机器的主机名
    hostname = socket.gethostname()

    # 获取当前工作路径
    cwd = os.getcwd()

    # 获取路径 cwd 的最低一级目录
    # cwd = '/home/shiyanlou' 
    # 在执行后变成 base_dir = 'shiyanlou'
    base_dir = os.path.basename(cwd)

    # 如果用户当前位于用户根目录之下，使用 `~` 代替目录名
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # 输出命令提示符
    if platform.system() != 'Windows':
        # \033[显示方式；前景色；背景色m字符串
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir))
    else:
        sys.stdout.write("[%s@%s %s]" % (user, hostname, base_dir))
    sys.stdout.flush()


def ignore_signals():
    if platform.system() != "Windows":
        # 忽略 Ctrl-Z 信号
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)    
    # 忽略 Ctrl-C 信号
    signal.signal(signal.SIGINT, signal.SIG_IGN)    


def tokenize(string):
    # 将 string 按 shell 的语法规则进行分割
    # 返回 string 的分割列表
    # 即以空格为分割符将命令与参数分开
    # 例, `ls -l /home/shiyanlou` 变成
    # ['ls', '-l', '/home/shiyanlou']
    return shlex.split(string)


def preprocess(tokens):
    # 存储处理之后的 token
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            # os.getenv() 用于获取环境变量的值，比如 `HOME`
            # 如变量不存在则返回空
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token


def handler_kill(signum, frame):
    # 自定义信号处理函数，在当前进程被强制中断时触发
    raise OSError("Killed!")


def execute(cmd_tokens):
    # `a` 模式表示以添加的方式打开指定文件
    # 此模式下文件对象的 write 操作不会覆盖文件原有的信息，
    # 而是添加到文件原有信息之后
    with open(HISTORY_PATH, 'a') as history_file:
        # os.linesep 给出当前平台的行终止符
        history_file.write(' '.join(cmd_tokens) + os.linesep)

    if cmd_tokens:
        # 获取命令
        cmd_name = cmd_tokens[0]
        # 获取命令参数
        cmd_args = cmd_tokens[1:]

        # 若当前命令在命令表中
        # 则传入参数，调用相应函数执行
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)

        # 监听 Ctrl-C 信号
        signal.signal(signal.SIGINT, handler_kill)

        # 如果当前系统不是 Windows
        # 则创建子进程
        if platform.system() != "Windows":
            # Unix 平台
            # 调用子进程执行命令
            p = subprocess.Popen(cmd_tokens)
            
            # 父进程从子进程中读取数据至 EOF
            # 此处主要用来等待子进程终止运行
            p.communicate()
        else:
            # Windows 平台
            command = ""
            command = ' '.join(cmd_tokens)
            # 执行 command
            os.system(command)
    # 返回状态
    return SHELL_STATUS_RUN


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # 打印命令提示符，形如 `[<user>@<hostname> <base_dir>]$`
        display_cmd_prompt()

        # 忽略 Ctrl-Z 或者 Ctrl-C 信号
        ignore_signals()

        try:
            # 读取命令
            cmd = sys.stdin.readline()

            # 解析命令
            # 将命令拆分并返回一个列表
            cmd_tokens = tokenize(cmd)

            # 预处理函数
            # 将命令中的环境变量使用真实值进行替换
            # 比如将 $HOME 变量替换为实际值
            cmd_tokens = preprocess(cmd_tokens)

            # 执行命令，并返回 shell 的状态
            status = execute(cmd_tokens)
        except:
            # sys.exc_info 函数返回一个包含三个值的元组 (type, value, traceback)
            # 这三个值产生于最近一次被处理的异常
            # 此处取中间的值
            _, err, _ = sys.exc_info()
            print(err)


def main():
    # 在执行 shell_loop 函数进行循环监听之前，首先进行初始化
    # 即建立命令与函数映射关系表
    init()

    # 处理命令的主程序
    shell_loop()


if __name__ == "__main__":
    main()
