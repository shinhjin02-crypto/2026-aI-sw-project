# fastapi <-- flask 떠올리면 됨..
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def hello(name: str) -> str:
    print(f"[SERVER] hello 함수 호출됨: name={name}", file=sys.stderr)
    return f"Hello, {name}!"

if __name__ == '__main__':
    print(f"[SERVER] 서버가 시작됨", file=sys.stderr)
    mcp.run()
