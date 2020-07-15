import operator


class Function:
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body

    def __call__(self):
        return evaluate(self.body)


symbols = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def tokenize(text):
    return text.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    token = tokens.pop(0)
    if token == '(':
        branch = []
        while tokens[0] != ')':
            branch.append(parse(tokens))
        tokens.pop(0)
        return branch
    else:
        try:
            return (int(token))
        except ValueError:
            return token


def resolve(expression):
    return symbols.get(expression)


def evaluate(expression):
    if isinstance(expression, int):
        return expression
    elif expression[0] == 'defun':
        (_, NAME, ARGLIST, BODY) = expression
        symbols[NAME] = Function(ARGLIST, BODY)
    else:
        symbol = resolve(expression[0])
        arguments = [evaluate(argument) for argument in expression[1:]]
        return symbol(*arguments)


text = "(defun mypow(x)(* x x))(+ 1 (* (* 10 20) 1))"
tokens = tokenize(text)
print(f"tokens: {tokens}")
while tokens:
    ast = parse(tokens)
    print(f"AST: {ast}")
    retval = evaluate(ast)
print(retval)
breakpoint()
