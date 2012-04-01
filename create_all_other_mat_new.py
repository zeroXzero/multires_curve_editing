import scipy as sp
import scipy.signal as ss
import numpy as np
import scipy.misc as mi
import matplotlib.pyplot as plt

BASIS_PATH="./basis_data_2500/basis_array_"
MAT_PATH="./basis_data_2500/"
#BASIS_PATH="./basis_data/basis_array_"
#MAT_PATH="./basis_data/"
#t_=np.arange(0,1.01,.01)
t_=np.arange(0,1.0004,.0004)



def null(A, eps=1e-15):
    u, s, vh = np.linalg.svd(A)
    x,y=A.shape
    diff=y-x
    null_mask = (s <= eps)
#for rectangular matrix
    null_mask=np.append(null_mask,[True]*diff)
    null_space = np.compress(null_mask, vh, axis=0)
    return np.transpose(null_space)

def reduced_mat(A):
    m,n=A.shape
    zero=1e-9
    row,col,dummy_col=0,0,0
#upper zeros
    while ((col < n-1) and (row < m)):
        while ((dummy_col < n-1) and (np.abs(A[row,dummy_col]) < zero)):
            dummy_col=dummy_col+1
        pivot_col=dummy_col
        dummy_col=dummy_col+1
#print pivot_col,row
        for var_col in range(pivot_col+1,n):
            A[:,var_col]=A[:,var_col]-(A[:,pivot_col]*A[row,var_col]/A[row,pivot_col])
#print A
        row=row+1
        col=col+1

#down zeros
    row,col,dummy_col=m-1,n-1,n-1
    while ((col > 0) and (row > 0)):
        while ((dummy_col > 0) and (np.abs(A[row,dummy_col]) < zero)):
            dummy_col=dummy_col-1
        pivot_col=dummy_col
        dummy_col=dummy_col-1
#print pivot_col,row
        for var_col in range(pivot_col-1,-1,-1):
            A[:,var_col]=A[:,var_col]-(A[:,pivot_col]*A[row,var_col]/A[row,pivot_col])
#print A
        row=row-1
        col=col-1
    return A


for power in range(10):
    n=2**power+3
    n_plus_1=2**(power+1)+3
    print "Generating Matrices: "+str(power+1)
    phi_j=np.loadtxt(BASIS_PATH+str(n)+".txt")
    phi_j_plus_1=np.loadtxt(BASIS_PATH+str(n_plus_1)+".txt")
#matrices
    m_phi_j=np.mat(phi_j)
    m_phi_j_plus_1=np.mat(phi_j_plus_1)
    P_j=m_phi_j_plus_1.I*m_phi_j
    comb_a=m_phi_j.T*m_phi_j_plus_1
    null_comb_a=null(comb_a)
    Q_j=null_comb_a
#making wavelet_mat compact
#Q_j=np.array([[1,2,3,4],[5,10,7,8],[9,10,1,1]])
    red_Q_j=reduced_mat(Q_j)
#normalizing wavelet_mat
    k,l=red_Q_j.shape
    for i in range(l):
        red_Q_j[:,i]=red_Q_j[:,i]/np.sqrt(red_Q_j[:,i].T*red_Q_j[:,i])

    m_psi=m_phi_j_plus_1*red_Q_j
    k,l=m_psi.shape
    for i in range(l):
        plt.plot(t_,m_psi[:,i])
    plt.savefig(MAT_PATH+"psi_fig_level_"+str(power+1)+".png")
    plt.clf()
#plt.show()
    P_j_Q_j=np.mat(np.column_stack((P_j,red_Q_j)))
    A_j_B_j=P_j_Q_j.I
    A_j=A_j_B_j[0:n:]
    B_j=A_j_B_j[n::]
    print A_j_B_j.shape
    print A_j.shape
    print B_j.shape
    f_h0=open(MAT_PATH+"P_mat_"+str(power+1)+".txt",'w')
    f_h1=open(MAT_PATH+"Q_mat_"+str(power+1)+".txt",'w')
    f_h2=open(MAT_PATH+"A_mat_"+str(power+1)+".txt",'w')
    f_h3=open(MAT_PATH+"B_mat_"+str(power+1)+".txt",'w')
    np.savetxt(f_h0,P_j)
    np.savetxt(f_h1,red_Q_j)
    np.savetxt(f_h2,A_j)
    np.savetxt(f_h3,B_j)
    f_h0.close()
    f_h1.close()
    f_h2.close()
    f_h3.close()
    print "Saving files Complete "

