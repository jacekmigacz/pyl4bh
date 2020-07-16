# pyl4bh - minimal LISP interpreter
![](logo.png)

Provides commmand-line interpreter for minimal LISP with basic ALU, conditionals, functions and recursion.

## Installation

Only python3 is required.

## Usage
Run `python3 ./pyl4bh.py "<TEXT>"` to evaluate LISP code.

### Example

```shell
# Addition
$ python3 ./pyl4bh.py "(+ 1 1)"
2
```

```shell
# Recursion
$ python3 ./pyl4bh.py "(defun f(x) (if (<= x 4) x (f(- x 1))))(f (* 10 10))"
4
```

### Special case
Run `python3 ./pyl4bh.py "(self-test)"` built-in function to self-evaluate interpreter.
