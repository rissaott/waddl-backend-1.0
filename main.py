from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ast

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 Limit this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Parser ===
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
    elif isinstance(node, ast.IfExp):
        return {
            "type": "if_expr",
            "test": to_json(node.test),
            "body": to_json(node.body),
            "orelse": to_json(node.orelse)
        }
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        return {"unknown_node": ast.dump(node)}

# === API Route ===
@app.post("/parse")
async def parse_code(request: Request):
    data = await request.json()
    code = data.get("code", "")

    try:
        tree = ast.parse(code, mode='eval')
        parsed = to_json(tree.body)
        return {"parsed": parsed}
    except Exception as e:
        return {"error": str(e)}
