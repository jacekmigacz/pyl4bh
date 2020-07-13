import operator

symbols = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}


def tokenize(text):
    return text.replace('(', '( ').replace(')', ' )').split()


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
    symbol = resolve(expression[0])
    arguments = [evaluate(argument) for argument in expression[1:]]
    return symbol(*arguments)


text = "(+ 1 (+ (* 10 20) 1))"
tokens = tokenize(text)
ast = parse(tokens)
retval = evaluate(ast)
print(retval)
