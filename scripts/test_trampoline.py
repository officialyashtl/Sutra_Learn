async def sub():
    return "hello from sub"

async def parent():
    val = await sub()
    return f"parent got: {val}"

def run_sync(coro):
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value

# Test with async generator / task runner
async def main():
    return await parent()

# Let's test standard runner without socket
import inspect

def step(coro):
    stack = [coro]
    val = None
    while stack:
        curr = stack[-1]
        try:
            res = curr.send(val)
            if inspect.iscoroutine(res):
                stack.append(res)
                val = None
            else:
                val = res
        except StopIteration as e:
            stack.pop()
            val = e.value
    return val

res = step(parent())
print("Trampoline result:", res)

