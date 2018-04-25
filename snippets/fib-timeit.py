import sys
import timeit

def fib(n):
    if n == 0 or n == 1:
        r = 1
    else:
        r = fib(n-1)+fib(n-2)
    return r

def fibf(n):
    if n == 0 or n == 1:
        r = 1
    else:
        fa = fb = 1
        for i in range(2, n+1):
            fi = fa + fb
            fb = fa
            fa = fi

        r = fi
    return r

if __name__ == '__main__':
    number = 10000
    m = int(sys.argv[1])
    for i in range(m):
        ta = timeit.timeit('fib(%i)' % i, setup = 'from __main__ import fib', number = number) / number
        tb = timeit.timeit('fibf(%i)' % i, setup = 'from __main__ import fibf', number = number) / number
        print('%i: old = %.3e, new = %.3e, ratio = %.2f' % (i, ta, tb, ta/tb))













