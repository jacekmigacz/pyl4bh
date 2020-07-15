import operator

top_level_symbols = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    't': True,
    '>=': operator.ge,
    '<=': operator.le,
}


class Function:
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body
        print(f"*FUNCTION*: args={arguments}, body={body}")

    def __call__(self, *arguments):
        local_symbols = dict(zip(self.arguments, arguments))
        local_symbols.update(top_level_symbols)
        return evaluate(self.body, local_symbols)


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


def evaluate(expression, local_symbols=top_level_symbols):
    print(f"type={type(expression)}, expression={expression}, local_symbols={local_symbols}")
    if isinstance(expression, int):
        return expression
    elif isinstance(expression, str):
        return local_symbols[expression]
    elif expression[0] == 'defun':
        (_, NAME, ARGLIST, BODY) = expression
        top_level_symbols[NAME] = Function(ARGLIST, BODY)
    elif expression[0] == 'if':
        (_, COND, THEN, ELSE) = expression
        print(f"COND={COND}, THEN={THEN}, ELSE={ELSE}")
        return evaluate(THEN if evaluate(COND, local_symbols) else ELSE, local_symbols)
    else:
        symbol = local_symbols.get(expression[0])
        arguments = [evaluate(argument, local_symbols) for argument in expression[1:]]
        return symbol(*arguments)


# text = "(defun mypow(x)(* x x))(+ 1 (mypow (* 10 (mypow 40))))"
# text = "(if t 10 1)"
text = "(if (<= 10 9) 1 0)"
tokens = tokenize(text)
print(f"tokens: {tokens}")
while tokens:
    ast = parse(tokens)
    print(f"AST: {ast}")
    retval = evaluate(ast)
print(retval)
