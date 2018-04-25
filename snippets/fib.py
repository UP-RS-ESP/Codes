def fib(n):
    if n == 0 or n == 1:
        r = 1
    else:
        r = fib(n-1)+fib(n-2)
    print r
    return r

def main():
    while True:
        try:
            n = int(input("Please enter a number: "))
            break
        except:
            print("Oops! That was no valid number. Try again..")

    print 'Running fib(%i) now..' % n
    fib(n)

if __name__ == '__main__':
    main()
