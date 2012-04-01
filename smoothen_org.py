import scipy.signal as ss
import scipy.misc as mi
import numpy as np
import matplotlib.pyplot as plt

MAT_PATH="./basis_data_1000/"
BASIS_PATH="./basis_data_1000/basis_array_"

x=np.loadtxt("image_x")
y=np.loadtxt("image_y")
y=200-y
print len(x),len(y)
x=x[:1027]
y=y[:1027]
print len(x),len(y)

m_x=np.mat(x)
m_y=np.mat(y)

at_first=1
t=0.7
for i in range(10,0,-1):
    print "Smoothening: "+str(i)
    n=2**i+3
    n_1=2**(i-1)+3
    a_mat=np.loadtxt(MAT_PATH+"A_mat_"+str(i)+".txt")
    phi_j=np.loadtxt(BASIS_PATH+str(n)+".txt")
    phi_j_1=np.loadtxt(BASIS_PATH+str(n_1)+".txt")
    m_phi=np.mat(phi_j)
    m_phi_1=np.mat(phi_j_1)
    
    m_a_mat=np.mat(a_mat)
    x_spline=m_x*m_phi.T
    y_spline=m_y*m_phi.T
    
    m_x_1=m_x*a_mat.T
    m_y_1=m_y*a_mat.T
    
    x_spline_1=m_x_1*m_phi_1.T
    y_spline_1=m_y_1*m_phi_1.T

    m_x=m_x_1
    m_y=m_y_1
   
    if i==5:
        x_fract=(x_spline*t)+(x_spline_1*(1-t))
        y_fract=(y_spline*t)+(y_spline_1*(1-t))
        plt.figure(0)
        plt.title("fract_5_4")
        plt.plot(x_fract,y_fract,',')
        
   
    if at_first:
        at_first=0
        plt.figure()
        plt.title("smooth_"+str(i))
#plt.plot(x,y,'x')
        plt.plot(x_spline,y_spline,',')
    
    plt.figure()
    plt.title("smooth_"+str(i))
#plt.plot(m_x_1,m_y_1,'x')
    plt.plot(x_spline_1,y_spline_1,',')
plt.show()
