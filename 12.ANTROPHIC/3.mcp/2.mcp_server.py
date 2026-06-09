# fastapi <-- flask 떠올리면 됨..

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def hello(name):
    return f"Hello, {name}!"

if __name__ == '__main__':
    mcp.run()
