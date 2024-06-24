t=int(input())
while t>0:
    n=int(input())
    k=int(input())
    row=[]
    col=[]
    for i in range(0,n):
        row.append(int(input()))
        col.append(int(input()))
    for j,k in zip(row,col):
        print(j,k)
    t-=1


