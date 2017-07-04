#_*_coding=UTF-8_*_

def main():
    input = raw_input('Input:')
    print(operate(input))

def test():
    operations = ["10", "3+4", "10-3+2", "123-321+43-12", "123-1-2-3"]
    values = [10, 7, 9, -167, 117]
    print("Automatic tests")
    for i in range(len(values)):
        if values[i] == operate(operations[i]):
            print "PASS %s = %s" % (operations[i], values[i])
        else:
            print "FAIL {0} != {1} ({2})".format(operations[i], values[i], operate(operations[i]))

#从字符串中获取整数及操作的 Token
def tokenize(string):
    buffer = Buffer(string)
    tk_int = TokenInt()
    tk_op = TokenOperator()
    tokens = []

    while buffer.peek():
        token = None
        #用两种类型的 Token 进行测试
        for tk in (tk_int, tk_op):
            token = tk.consume(buffer)
            if token:
                tokens.append(token)
                break
        #如果不存在可以识别的 Token 表示输入错误
        if not token:
            raise ValueError("Error in syntax")

    return tokens

#从 Token 列表生成表达式二叉树
def parse(tokens):
    if tokens[0][0] != 'int':
        raise ValueError("Must start with an int")

    #取出 tokens[0], 该 Token 类型为整数
    node = NodeInt(tokens[0][1])
    nbo = None
    last = tokens[0][0]
    #从第二个 Token 开始循环取出
    for token in tokens[1:]:
        #相邻两个 Token 的类型一样则为错误
        if token[0] == last:
            raise ValueError("Error in syntax")
        last = token[0]
        #如果 Token 为操作符，则保存为操作符节点，把前一个整数 Token 作为左子节点
        if token[0] == 'ope':
            nbo = NodeBinaryOp(token[1])
            nbo.left = node
        #如果 Token 为整数，则将该 Token 保存为右节点
        if token[0] == 'int':
            nbo.right = NodeInt(token[1])
            node = nbo

    return node

#采用递归的方法计算表达式二叉树的值
def calculate(nbo):
    #如果左节点是二叉树，则先计算左节点二叉树的值
    if isinstance(nbo.left, NodeBinaryOp):
        leftval = calculate(nbo.left)
    else:
        leftval = nbo.left.value
    #根据操作符节点是加还是减计算
    if nbo.kind == '-':
        return leftval - nbo.right.value
    elif nbo.kind == '+':
        return leftval + nbo.right.value
    else:
        raise ValueError("Wrong operator")

def evaluate(node):
    if isinstance(node, NodeInt):
        return node.value
    else:
        return calculate(node)

def operate(string):
    tokens = tokenize(string)
    node = parse(tokens)
    return evaluate(node)

class Node(object):
    pass

class NodeInt(Node):
    def __init__(self, value):
        self.value = value

class NodeBinaryOp(Node):
    def __init__(self, kind):
        self.kind = kind
        self.left = None
        self.right = None

class Token(object):
    def consume(self, buffer):
        pass

class TokenInt(Token):
    def consume(self, buffer):
        accum = ""
        while True:
            ch = buffer.peek()
            if ch is None or ch not in "0123456789":
                break
            else:
                accum += ch
                buffer.advance()

        if accum != "":
            return ("int", int(accum))
        else:
            return None

class TokenOperator(Token):
    def consume(self, buffer):
        ch = buffer.peek()
        if ch is not None and ch in "+-":
            buffer.advance()
            return ("ope", ch)
        return None

class Buffer(object):
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def peek(self):
        if self.offset >= len(self.data):
            return None
        return self.data[self.offset]

    def advance(self):
        self.offset += 1

if __name__ == '__main__':
    #main()
    test()
