import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_coro():
    return 42

res = asyncio.run(test_coro())
print("Asyncio with WindowsSelectorEventLoopPolicy result:", res)

