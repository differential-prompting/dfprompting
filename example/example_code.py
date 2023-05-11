def program(a,b):
    if b==0:
        return a
    else:
        return program(a,a%b)
