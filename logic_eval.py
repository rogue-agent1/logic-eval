#!/usr/bin/env python3
"""logic_eval - Propositional logic evaluator with truth tables."""
import sys, itertools

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i] in "()!~":
            tokens.append(expr[i])
            i += 1
        elif expr[i:i+2] in ("&&", "||", "->", "<>"):
            tokens.append(expr[i:i+2])
            i += 2
        elif expr[i:i+3] == "<->":
            tokens.append("<->")
            i += 3
        elif expr[i].isalpha():
            j = i
            while j < len(expr) and expr[j].isalnum():
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif expr[i] in "01":
            tokens.append(expr[i] == "1")
            i += 1
        else:
            i += 1
    return tokens

def parse(tokens, pos=0):
    return parse_impl(tokens, pos)

def parse_impl(tokens, pos):
    left, pos = parse_or(tokens, pos)
    if pos < len(tokens) and tokens[pos] in ("->", "<>", "<->"):
        op = tokens[pos]
        pos += 1
        right, pos = parse_impl(tokens, pos)
        return (op, left, right), pos
    return left, pos

def parse_or(tokens, pos):
    left, pos = parse_and(tokens, pos)
    while pos < len(tokens) and tokens[pos] == "||":
        pos += 1
        right, pos = parse_and(tokens, pos)
        left = ("||", left, right)
    return left, pos

def parse_and(tokens, pos):
    left, pos = parse_not(tokens, pos)
    while pos < len(tokens) and tokens[pos] == "&&":
        pos += 1
        right, pos = parse_not(tokens, pos)
        left = ("&&", left, right)
    return left, pos

def parse_not(tokens, pos):
    if pos < len(tokens) and tokens[pos] in ("!", "~"):
        pos += 1
        operand, pos = parse_not(tokens, pos)
        return ("!", operand), pos
    return parse_atom(tokens, pos)

def parse_atom(tokens, pos):
    if tokens[pos] == "(":
        pos += 1
        expr, pos = parse_impl(tokens, pos)
        pos += 1  # skip )
        return expr, pos
    val = tokens[pos]
    return val, pos + 1

def evaluate(tree, env):
    if isinstance(tree, bool):
        return tree
    if isinstance(tree, str):
        return env.get(tree, False)
    op = tree[0]
    if op == "!":
        return not evaluate(tree[1], env)
    a = evaluate(tree[1], env)
    b = evaluate(tree[2], env)
    if op == "&&": return a and b
    if op == "||": return a or b
    if op == "->": return (not a) or b
    if op in ("<>", "<->"): return a == b
    return False

def get_vars(tree):
    if isinstance(tree, bool): return set()
    if isinstance(tree, str): return {tree}
    result = set()
    for i in range(1, len(tree)):
        result |= get_vars(tree[i])
    return result

def truth_table(expr):
    tokens = tokenize(expr)
    tree, _ = parse(tokens, 0)
    variables = sorted(get_vars(tree))
    rows = []
    for vals in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, vals))
        result = evaluate(tree, env)
        rows.append((dict(env), result))
    return variables, rows

def test():
    tokens = tokenize("A && B")
    tree, _ = parse(tokens, 0)
    assert evaluate(tree, {"A": True, "B": True}) == True
    assert evaluate(tree, {"A": True, "B": False}) == False
    tokens2 = tokenize("A || !B")
    tree2, _ = parse(tokens2, 0)
    assert evaluate(tree2, {"A": False, "B": False}) == True
    assert evaluate(tree2, {"A": False, "B": True}) == False
    tokens3 = tokenize("A -> B")
    tree3, _ = parse(tokens3, 0)
    assert evaluate(tree3, {"A": True, "B": False}) == False
    assert evaluate(tree3, {"A": False, "B": False}) == True
    variables, rows = truth_table("A && B")
    assert len(variables) == 2
    assert len(rows) == 4
    true_rows = [r for r in rows if r[1]]
    assert len(true_rows) == 1
    _, rows2 = truth_table("A || B")
    true_rows2 = [r for r in rows2 if r[1]]
    assert len(true_rows2) == 3
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("logic_eval: Logic evaluator. Use --test")
