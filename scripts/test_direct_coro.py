async def f():
    return 42

coro = f()
res = None
try:
    coro.send(None)
except StopIteration as e:
    res = e.value

print("Direct send result:", res)

