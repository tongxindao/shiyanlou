#_*_coding=UTF-8_*_
from __future__ import print_function
from collections import deque
from io import StringIO
import tokenize
import sys

def get_input(*args, **kw):
    if sys.version[0] == "2":
        return raw_input(*args, **kw)
    else:
        return input(*args, **kw)

class Stack(deque):#定义一个栈类
    #添加一个栈类
    push = deque.append

    #返回最后一个元素
    def top(self):
        return self[-1]

class Machine:
    def __init__(self, code):#预先定义一个初始化函数
        self.data_stack = Stack()
        self.return_addr_stack = Stack()
        self.code = code
        self.instruction_pointer = 0

    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()

    def run(self):#代码运行的条件
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)

    def dispatch(self, op):
        dispatch_map = {
            "%":        self.mod,
            "*":        self.mul,
            "+":        self.plus,
            "-":        self.minus,
            "/":        self.div,
            "==":       self.eq,
            "cast_int": self.cast_int,
            "cast_str": self.cast_str,
            "drop":     self.drop,
            "dup":      self.dup,
            "if":       self.if_stmt,
            "jmp":      self.jmp,
            "over":     self.over,
            "print":    self.print,
            "println":  self.println,
            "read":     self.read,
            "stack":    self.dump_stack,
            "swap":     self.swap,
        }

        if op in dispatch_map:
            dispatch_map[op]()
        elif isinstance(op, int):
            #如果指令是整型数据，就将数据存放到数据栈中
            self.push(op)
        elif isinstance(op, str) and op[0]==op[-1]=='"':
            #如果是字符串类型的，就将字符串内容存放到数据栈中
            self.push(op[1:-1])
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    def plus(self):
        self.push(self.pop() + self.pop())

    def exit(self):
        sys.exit(0)

    def minus(self):
        last = self.pop()
        self.push(self.pop() -last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)
       
    def mod(self):
        last = self.pop()
        self.push(self.pop() % last)
 
    def dup(self):
        self.push(self.top())

    def over(self):
        b = self.pop()
        a = self.pop()
        self.push(a)
        self.push(b)
        self.push(a)

    def drop(self):
        self.pop()

    def swap(self):
        b = self.pop()
        a = self.pop()
        self.push(b)
        self.push(a)

    def print(self):
        sys.stdout.write(str(self.pop()))
        sys.stdout.flush()

    def println(self):
        sys.stdout.write("%s\n" % self.pop())
        sys.stdout.flush()

    def read(self):
        self.push(get_input())

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

    def eq(self):
        self.push(self.pop() == self.pop())

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)

    def jmp(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")

    def dump_stack(self):
        print("Data stack (top first):")
        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))

def parse(text):
    if sys.version[0] == "2":
        stream = StringIO(unicode(text))
    else:
        stream = StringIO(text)

    #以StringIO的形式将text对象读入到内存中，并以字符串形式返回到generate_tokens()函数中
    tokens = tokenize.generate_tokens(stream.readline)
    #generate_tokens生成器生成一个5元祖：标记类型、标记字符串、标记开始位置二元组、标记结束位置二元组以及标记所在的行号
    #下面大写的单词都属于token模块的常量
    for toknum, tokval, _, _, _ in tokens:
        if toknum == tokenize.NUMBER:
            yield int(tokval)
        elif toknum in [tokenize.OP, tokenize.STRING, tokenize.NAME]:
            yield tokval
        elif toknum == tokenize.ENDMARKER:
            break
        else:
            raise RuntimeError("Unknown token %s: '%s'" % (tokenize.tok_name[toknum], tokval))

def constant_fold(code):
    #对简单的数字表达式诸如：2 3 ＋进行计算并将结果作为常数返回原指令列表中
    while True:#在指令中找到两个连续的数字以及一个算数运算符
        for i, (a, b, op) in enumerate(zip(code, code[1:], code[2:])):
            if isinstance(a, int) and isinstance(b, int) and op in {"+", "-", "*", "/"}:
                m = Machine((a, b, op))
                m.run()
                code[i:i+3] = [m.top()]
                print("Constant-folded %s%s%s to %s" % (a, op, b, m.top()))
                break
        else:
            break
    return code

def repl():
    print('Hit CTRL+D type "exit" to quit.')

    while True:
        try:
            source = get_input("> ")
            code = list(parse(source))
            code = constant_fold(code)
            Machine(code).run()
        except (RuntimeError, IndexError) as e:
            print("IndexError: %s" % e)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")

def test(code = [2, 3, "+", 5, "*", "println"]):
    print("Code before optimization: %s" % str(code))
    optimized = constant_fold(code)
    print("Code after optimization: %s" % str(optimized))
    print("Stack after running original program:")
    a = Machine(code)
    a.run()
    a.dump_stack()

    print("Stack after running optimized program:")
    b = Machine(optimized)
    b.run()
    b.dump_stack()

    result = a.data_stack == b.data_stack
    print("Result: %s" % ("OK" if result else "FAIL"))
    return result
    
def examples():
    print("** Program 1: Runs the code for `print((2+3)*4)`")
    Machine([2, 3, "+", 4, "*", "println"]).run()
    print("\n** Program 2: Ask for numbers, computes sum and product.")
    Machine([
        '"Enter a number: "', "print", "read", "cast_int",
        '"Enter another number: "', "print", "read", "cast_int",
        "over", "over",
        '"Their sum is: "', "print", "+", "println",
        '"Their product is: "', "print", "*", "println"
    ]).run()

    print("\n** Program 3: Shows branching and looping (use CTRL+D to exit).")
    Machine([
        '"Enter a number: "', "print", "read", "cast_int",
        '"The number "', "print", "dup", "print", '" is "', "print",
        2, "%", 0, "==", '"even."', '"odd."', "if", "println",
        0, "jmp" # loop forever!
]).run()

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "repl":
                repl()
            elif cmd == "test":
                test()
                examples()
            else:
                print("Commands: repl, test")
        else:
            repl()
    except EOFError:
        print("")
