import scipy.signal as ss
import scipy.misc as mi
import numpy as np
import matplotlib.pyplot as plt

MAT_PATH="./basis_data_1000/"
BASIS_PATH="./basis_data_1000/basis_array_"

x=np.loadtxt("image_x")
y=np.loadtxt("image_y")
#four points
#f_pt_x=np.array([50,100,150,200])
#f_pt_y=np.array([50,100,10,100])
f_pt_x=np.array([50,75,120,150])
f_pt_y=np.array([25,75,75,10])

y=200-y
x=x[:1027]
y=y[:1027]

m_x=np.mat(f_pt_x)
m_y=np.mat(f_pt_y)

phi_j=np.loadtxt(BASIS_PATH+str(4)+".txt")
m_phi=np.mat(phi_j)
sweep_spline_x=m_x*m_phi.T
sweep_spline_y=m_y*m_phi.T
plt.plot(sweep_spline_x,sweep_spline_y,',')

m_x=np.mat(x)
m_y=np.mat(y)

#bringing to low range
for i in range(10,0,-1):
    n=2**i+3
    a_mat=np.loadtxt(MAT_PATH+"A_mat_"+str(i)+".txt")
    m_a_mat=np.mat(a_mat)
    print m_a_mat.shape 
    m_x=m_x*m_a_mat.T
    m_y=m_y*m_a_mat.T
    
#x_fract=(x_spline*t)+(x_spline_1*(1-t))
#y_fract=(y_spline*t)+(y_spline_1*(1-t))

phi_j=np.loadtxt(BASIS_PATH+str(4)+".txt")
m_phi=np.mat(phi_j)
x_spline=m_x*m_phi.T
y_spline=m_y*m_phi.T
delta_c_j_x=f_pt_x-m_x
delta_c_j_y=f_pt_y-m_y

#taking to higher range
for i in range(1,11):
    n=2**i+3
    p_mat=np.loadtxt(MAT_PATH+"P_mat_"+str(i)+".txt")
    m_p_mat=np.mat(p_mat)
    print m_p_mat.shape 
    delta_c_j_x=delta_c_j_x*m_p_mat.T
    delta_c_j_y=delta_c_j_y*m_p_mat.T

m_x=np.mat(x)
m_y=np.mat(y)
changed_x=m_x+delta_c_j_x
changed_y=m_y+delta_c_j_y

phi_j=np.loadtxt(BASIS_PATH+str(1027)+".txt")
m_phi=np.mat(phi_j)
changed_x_spline=changed_x*m_phi.T
changed_y_spline=changed_y*m_phi.T

plt.figure()
plt.plot(sweep_spline_x,sweep_spline_y,',')
plt.plot(changed_x_spline,changed_y_spline,',')

at_first=1
m_x=changed_x
m_y=changed_y
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
    
#x_fract=(x_spline*t)+(x_spline_1*(1-t))
#y_fract=(y_spline*t)+(y_spline_1*(1-t))
   
    if at_first:
        at_first=0
        plt.figure()
#plt.plot(x,y,'x')
        plt.plot(x_spline,y_spline,',')
    
    plt.figure()
#plt.plot(m_x_1,m_y_1,'x')
    plt.plot(x_spline_1,y_spline_1,',')
plt.show()
