import ast

def to_json(node):
    if isinstance(node, ast.BoolOp):
        op = 'and' if isinstance(node.op, ast.And) else 'or'
        return {
            "type": op,
            "values": [to_json(v) for v in node.values]
        }
    elif isinstance(node, ast.BinOp):
        return {
            "type": type(node.op).__name__,
            "left": to_json(node.left),
            "right": to_json(node.right)
        }
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        return "unknown"

def parse(code):
    try:
        tree = ast.parse(code, mode='eval')
        return to_json(tree.body)
    except Exception as e:
        return {"error": str(e)}

# Try it out
print(parse("A and B"))
print(parse("x + 5 * y"))
