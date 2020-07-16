import argparse
import operator
import unittest

top_level_symbols = {
    '+':   operator.add,
    '-':   operator.sub,
    '*':   operator.mul,
    '/':   operator.floordiv,
    '>=':  operator.ge,
    '<=':  operator.le,
    'and': operator.and_,
    'or':  operator.or_,
    'xor': operator.xor,
    'not': operator.not_,
}


class Function:
    """Abstract LISP function with variable-length argument list."""
    def __init__(self, arguments, body):
        self.arguments = arguments
        self.body = body

    def __call__(self, *arguments):
        local_symbols = dict(zip(self.arguments, arguments))
        local_symbols.update(top_level_symbols)
        return evaluate(self.body, local_symbols)


def tokenize(text):
    """Chunk stream of characters into a series of words and symbols.

    Args:
        text (str): LISP source code.

    Returns:
        Vector of words and symbols.
    """
    return text.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    """Build an AST that mirrors the nested nature of the grammar.

    Args:
        tokens ([]): Vector of words and symbols.

    Returns:
        The abstract syntax tree (AST).
    """
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
    """Evaluate abstract syntax tree.

    Args:
        expression ([]): AST branch.
        local_symbols ({}, optional): Dictionary of symbols.

    Returns:
        AST's root evaluation result.
    """
    if isinstance(expression, int):
        return expression
    elif isinstance(expression, str):
        return local_symbols[expression]
    elif expression[0] == 'defun':
        (_, NAME, ARGLIST, BODY) = expression
        top_level_symbols[NAME] = Function(ARGLIST, BODY)
    elif expression[0] == 'if':
        (_, COND, THEN, ELSE) = expression
        return evaluate(THEN if evaluate(COND, local_symbols) else ELSE, local_symbols)
    else:
        symbol = local_symbols.get(expression[0])
        arguments = [evaluate(argument, local_symbols) for argument in expression[1:]]
        return symbol(*arguments)


def lisp(text):
    """Run minimal LISP interpreter.

    Args:
        text (str): LISP source code.

    Returns:
        AST's root evaluation result.
    """
    tokens = tokenize(text)
    while tokens:
        ast = parse(tokens)
        retval = evaluate(ast)
    return retval


class TestLisp(unittest.TestCase):
    """Basic self-test."""
    def test_boolean(self):
        self.assertEqual(lisp("(+ (and 1 1) (+ (and 0 1) (+ (and 1 0) (and 0 0))))"), 1)
        self.assertEqual(lisp("(+ (or 1 1) (+ (or 0 1) (+ (or 1 0) (or 0 0))))"), 3)
        self.assertEqual(lisp("(+ (xor 1 1) (+ (xor 0 1) (+ (xor 1 0) (xor 0 0))))"), 2)
        self.assertEqual(lisp("(+ (not 1) (not 0))"), 1)

    def test_arithmetic(self):
        self.assertEqual(lisp("(/ 99999 (- (+ 10 20) (* 78 11)))"), -121)

    def test_defun(self):
        self.assertEqual(lisp("(defun mypow2(x)(* x x))(+ 1 (mypow2 (* 10 (mypow2 (if (<= 44 33) 10 20)))))"), 16000001)

    def test_recursion(self):
        self.assertEqual(lisp("(defun f(x) (if (<= x 4) x (f(- x 1))))(f (* 10 10))"), 4)


parser = argparse.ArgumentParser(description='Interpret LISP.', epilog="Remember it is minimal by design!")
parser.add_argument('text', help="Lisp source code.", action='store', type=str)
args = parser.parse_args()

if args.text == '(self-test)':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLisp)
    unittest.TextTestRunner(verbosity=2).run(suite)
else:
    print(lisp(args.text))
