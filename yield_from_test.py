def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

def bottom():
    # Returning the yield lets the value that goes up the call stack to come right back
    # down.
    return (yield 42)

def middle():
    return (yield from bottom())

def top():
    return (yield from middle())


if __name__ == '__main__':
    # Get the generator.
    gen = top()
    value = next(gen)
    print(value)  # Prints '42'.
    try:
        value = gen.send(value * 2)
    except StopIteration as exc:
        value = exc.value
    print(value)  # Prints '84'.

    # c = consumer()
    # produce(c)
