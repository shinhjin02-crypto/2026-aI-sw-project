import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python", args=["C:/Users/NT551XED/2026-aI-sw-project/12.ANTROPHIC/3.mcp/2.mcp_server.py"])

    async with stdio_client(server_params) as (read, write):
        # 아래 코드를 통해서 서버/클라 간에 handshake 가 이루어짐
        async with ClientSession(read, write) as session:
            print(f"[CLIENT] 서버와 HS 전", file=sys.stderr)
            await session.initialize()
            print(f"[CLIENT] 서버와 HS 후", file=sys.stderr)

            # 너는 어떤 도구가 있니??
            tools = (await session.list_tools()).tools
            print(f"[CLIENT] 서버가 쓸 수 있는 도구 받아옴. 도구: {[t.name for t in tools]}", file=sys.stderr)

            # 여기서부터 실제로 내가 서버에 호출하고 싶은 코드를 작성
            result = await session.call_tool("hello", {"name": "John"})

            print(result.content[0].text) #  기대하는건 "Hello, John!"

if __name__ == '__main__':
    print(f"[CLIENT] 클라이언트가 시작됨", file=sys.stderr)
    asyncio.run(main())