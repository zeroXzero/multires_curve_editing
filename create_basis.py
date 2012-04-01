import scipy.signal as ss
import scipy.misc as mi
import numpy as np
import matplotlib.pyplot as plt

def deboor(k,t):
#   de Boor recursive algorithm
#   S(t) = sum(b[i][k](t) * P[i] for i in xrange(0, n))
#   b[i][k] = {if k == 0:           t[i] <= t_ < t[i + 1],
#              else:                a[i][k](t) * b[i][k - 1](t) + (1 - a[i + 1][k](t)) * b[i + 1][k - 1](t)}
#   a[i][k] = {if t[i] == t[i + k]: 0,
#              else:                (t_ - t[i]) / (t[i + k] - t[i])}
#   NOTE: for b[i][k](t), must iterate to t[:-1]; the number of [i, i + 1) spans in t
    m = len(t) - 1                                                          # get m
    a, b, _k, _m = [], [], xrange(k + 1), xrange(m)                         # initialize a, b, iterator over k, iterator over t[:-1]
    for i in _m:                                                            # iterate over t[:-1]
        a.append([]); b.append([])                                            # a[i]; b[i]
        for k in _k:                                                          # iterate over k
            a[i].append(None)                                                   # a[i][k]
            if k == 0: b[i].append(lambda t_, i = i: t[i] <= t_ < t[i + 1])     # if k == 0: b[i][k](t) is a step function in [t[i], t[i + 1])
            elif m < i + k: b[i].append(lambda t_: False)                       # if m < i + k: b[i][k](t) undefined
            else:                                                               # else: calculate b[i][k](t)
                if t[i] == t[i + k]: a[i][k] = lambda t_: False                   # if t[i] == t[i + k]: a[i][k] undefined
                else:                                                             # else: calculate a[i][k](t)
                    a[i][k] = lambda t_, i = i, k = k: ((t_ - t[i]) /
                                                       (t[i + k] - t[i]))           # a[i][k](t) = (t_ - t[i]) / (t[i + k] - t[i])
                b[i].append(lambda t_, i = i, k = k:
                                a[i][k](t_) * b[i][k - 1](t_) +
                                (1 - a[i + 1][k](t_)) * b[i + 1][k - 1](t_))      # b[i][k](t) = a[i][k](t) * b[i][k - 1](t) + (1 - a[i + 1][k](t)) * b[i + 1][k - 1](t)
    return b# set b

n = 10                                                           # n = len(P) - 1; (P[0], ... P[n])
k = 3                                                                   # degree of curve
m = n + k + 1                                                           # property of b-splines: m = n + k + 1
_t = 1.0 / (m - k * 2)                                                    # t between clamped ends will be evenly spaced (not a necessary condition, however)
# the endpoints of clamped splines have a multiplicity of k + 1 (the endpoint knots are repeated k + 1 times)
t = k * [0] + [t_ * _t for t_ in xrange(m - (k * 2) + 1)] + [1] * k     # clamp ends and get the t between them (+1 in the xrange to iterate to index m - k * 2)

b=deboor(3,t)
_n=xrange(len(t)-1-k-1+1)
x=[1]
y=[1]
delta=_t/5
#t_=np.arange(0,delta*6,delta)
t_=np.arange(0,1.001,.001)


#for j in t_:
#    x_,y_=0,0
#    for i in _n:                                                            # iterate over P
#        b_i = b[i][k](j)                                                     # calculate b[i][k](t)
#        x_ += x[i] * b_i                                                      # update x vector
#        y_ += y[i] * b_i                                                      # update y vector
#        print x_,y_ 

count=0
basis=0
out_y=[]
out_x=[]
print t_
for j in range(11):
    dummy=[]
    for i in t_:
        dummy.append(b[j][k](i))
    print j,dummy,t_
    out_y.append(dummy)
    out_x.append(t_)
#t_=t_+delta

plt.plot(out_x[0],out_y[0],out_x[1],out_y[1],out_x[2],out_y[2],out_x[3],out_y[3],out_x[4],out_y[4],out_x[5],out_y[5],out_x[6],out_y[6],out_x[7],out_y[7],out_x[8],out_y[8],out_x[9],out_y[9],out_x[10],out_y[10])
plt.show()
#x1=np.arange(0,1.01,0.01)
#y1=np.power(1-x1,3)
#
#y2=3*x1*np.power(1-x1,2)
#y3=3*np.power(x1,2)*(1-x1)
#y4=np.power(x1,3)
#
#b1=ss.bspline(y1,3)
#tck,u = ss.interpolate.splprep([x1,y1],s=0)
#plt.plot(x1,y1,x1,y2,x1,y3,x1,y4)
#plt.show()
