
def bitcoutn(n):
    count = 0
    while n:
        n ^= n - 1
        count += 1
    return count
print(bitcoutn(10))
print(bitcoutn(67))

print(bitcoutn(8192))

print(bitcoutn(-1024))

print(bitcoutn(15))

print(bitcoutn(-1))

print(bitcoutn(0))

print(bitcoutn(0x80000000))



"""
Bitcount
bitcount


Input:
    n: a nonnegative int

Output:
    The number of 1-bits in the binary encoding of n

Examples:
    >>> bitcount(127)
    7
    >>> bitcount(128)
    1
"""
