def intersec2d(k, l, m, n,):
    det = (n[0] - m[0]) * (l[1] - k[1])  -  (n[1] - m[1]) * (l[0] - k[0])

    if (det == 0.0):
        return 0 

    s = ((n[0] - m[0]) * (m[1] - k[1]) - (n[1] - m[1]) * (m[0] - k[0]))/ det
    t = ((l[0] - k[0]) * (m[1] - k[1]) - (l[1] - k[1]) * (m[0] - k[0]))/ det
    pi =(0,0)
    pi[0] = k[0] + (l[0]-k[0])*s
    pi[1] = k[1] + (l[1]-k[1])*s

    return pi

k = (0,1)
l = (5,4)
m = (0,3)
n = (5,0)

print(intersec2d(k,l,m,n))