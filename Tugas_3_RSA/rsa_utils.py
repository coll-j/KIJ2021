import random
import math

def exp(a, b, n=1000007):
    """
    Compute a^b mod n.
    """
    result = 1
    while b > 0:
        if b & 1:
            result = (result * a) % n
        a = (a * a) % n
        b >>= 1
    return result

def miller_rabin(n, k=10):
    """Miller Rabin Primality Test
    Return False if n is composite, True(probably prime) otherwise.
    Args:
        n: integer to be tested for primality
        k: number of iterations to run the test
    NOTES
    =====
    If n is composite then the Miller–Rabin primality test declares n probably
    prime with a probability at most 4^(−k). Hence, larger the value of k we
    choose, better is the chance of reducing false positives.
    REFERENCES
    ==========
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    EXAMPLES
    ========
    >>> miller_rabin(561)
    False
    >>> miller_rabin(29)
    True
    >>> miller_rabin(221)
    False
    """
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False

    # Represent n - 1 as (2^s)*d
    s, d = 0, n - 1
    while not d % 2:
        s += 1
        d //= 2
    assert(2**s*d == n - 1)

    def check_if_composite_using(a):
        x = exp(a, d, n)
        if x == 1 or x == n - 1:
            return False  # probably prime
        for _ in range(s):
            x = (x * x) % n  # check for each a^((2^i)*d)
            if x == n - 1:
                return False  # probably prime
        return True  # definitely composite

    # Test for k random integers a
    for _ in range(k):
        a = random.randint(2, n-1)
        if check_if_composite_using(a):
            return False  # definitely composite
    return True  # probably prime


def generate_large_prime(n=1000007):
    """
    Generate a large prime number.
    """
    while True:
        p = random.randint(2**(n-1), 2**n)
        if miller_rabin(p):
            return p


def inverse(a, n):
    """
    Compute the multiplicative inverse of a in the integers modulo n.
    """
    return pow(a, -1, n)


def as_bytes(string):
    """
    Convert a string to a list of bytes.
    """
    return bytes(string, 'utf-8')
