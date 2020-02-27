import pylab as pl 
import scipy.special as sp
import scipy.linalg as spl

def g(t,A,B): # this function returns the true value array for given A and B
	y=A*sp.jn(2,t)+(B*t)
	return y

data=pl.loadtxt("fitting.dat")# Data contains all the data in the file as a numpy array

t=data[:,0]
values=data[:,1:]
sigma=pl.logspace(-1,-3,9)
y_true=g(t,1.05,-0.105)

# Plot each column of data against time
for i in range(len(sigma)):
	pl.plot(t,values[:,i],label="sigma ="+str(sigma[i]))
# Plot the true value vs time graph in the same figure
pl.plot(t,y_true,label="true value")
pl.title('Figure 0')
pl.xlabel('t')
pl.ylabel('Values')
pl.legend()
pl.show()

# Drawing errorbar for first column of data Vs time
pl.errorbar(t[::5],values[:,0][::5],sigma[0],fmt='ro')
pl.plot(t,y_true,label="true value")
pl.title('errorbar for first column of data')
pl.xlabel('t')
pl.ylabel('Values')
pl.legend() 
pl.show()


M=pl.c_[sp.jn(2,t),t] # M is a matrix with bessel function values in column 1 and corresponding time in column 2
p=[1.05,-1.05]
print((pl.dot(M,p)==g(t,p[0],p[1])).all()) # printing whether they are equal or  not

A=pl.arange(0,2.1,0.1)
B=pl.arange(-0.2,0.01,0.01)
e=pl.zeros([len(A),len(B)]) # e is a rectangular matrix with all zero entries. the MSE for different A and B will be stored in this matrix

# calculating the MSE for different A and B
k=0
for i in A:
	p=0
	for j in B:
		e[k][p]=(pl.sum((values[:,0]-g(t,i,j))**2))
		p+=1
	k+=1

# plotting the contour for MSE for varying A and B
a, b=pl.meshgrid(A, B)
cp=pl.contour(a,b,e,21)
pl.clabel(cp)
pl.xlabel("A")
pl.ylabel("B")
pl.show()

# finding the best estimate for A and B for first column of data
A_best, B_best=spl.lstsq(M,values[:,0])[0]
print("For first Column: the best estimate of A={} and B={}".format(A_best,B_best))

# finding the best estimate for A and B for all column of data
A_err=[];B_err=[];
for i in range((len(sigma))):
	A_best, B_best=spl.lstsq(M,values[:,i])[0]
	A_err.append(abs(A_best-1.05)); B_err.append(abs(B_best+0.105))

# plotting A_err vs sigma and B_err vs sigma in different subplots
pl.subplot(211)
pl.title("Estimation of A")
pl.xlabel("Noise standard deviation")
pl.ylabel("MS Error in A")
pl.plot(sigma,A_err,color="red",marker='o',linestyle='dashed')
pl.subplot(212)
pl.title("Estimation of B")
pl.xlabel("Noise standard deviation")
pl.ylabel("MS Error in B")
pl.plot(sigma,B_err,color="green",marker='o',linestyle='dashed')
pl.show()

# plotting log(A_err) vs log(sigma) and log(B_err) vs log(sigma)
pl.title("A_err vs sigma and B_err vs sigma")
pl.xlabel("Noise standard deviation")
pl.ylabel("MSerror")
pl.loglog(sigma,A_err,color="red",marker='o',linestyle="None",label="A_err")
pl.errorbar(sigma,A_err,sigma,color="red",linestyle="None")
pl.loglog(sigma,B_err,color="green",marker="o",linestyle="None",label="B_err")
pl.errorbar(sigma,B_err,sigma,color="green",linestyle="None")
pl.legend()
pl.show()