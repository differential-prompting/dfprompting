N=int(input())
alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(0,N):
    a=int(input())
    b=str(input())
    ans=0
    for j in range(0,26):
        if j+1<=b.count(alpha[j]):
            ans+=1
    print(b,ans)















































