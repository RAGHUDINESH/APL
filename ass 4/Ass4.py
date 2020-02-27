import pylab as pl
import scipy.integrate as si
import scipy.linalg as sl
import numpy as np

def exp(x):  		# "exp" function takes a array as input and returns e^(x) of each element of array
	return pl.exp(x)
def f(x):	 		# "f"" function takes a array as input and returns cos(cos(x)) of each element of array
	return pl.cos(pl.cos(x))
def ue(x,k):		# "ue" functions takes a array and a integer returns e^(x) * cos(k*x)
	return exp(x)*pl.cos(k*x)  
def ve(x,k):		# "ve" functions takes a array and a integer returns e^(x) * sin(k*x)
	return exp(x)*pl.sin(k*x)
def uc(x,k):		# "uc" functions takes a array and a integer returns cos(cos(x)) * cos(k*x)
	return f(x)*pl.cos(k*x)
def vc(x,k):		# "vc" functions takes a array and a integer returns cos(cos(x)) * sin(k*x)
	return f(x)*pl.sin(k*x)


x=pl.linspace(-2*pl.pi,4*pl.pi,1000)  # x is an array of 1000 numbers which are linearly spaced between -2pi and 4pi

pl.figure(1)							 
pl.title("Actual")
pl.semilogy(x,np.absolute(exp(x)))		#plotting the values e^(x) vs x for all values in array x
pl.xlabel("x")
pl.ylabel("e^x")
pl.grid()
pl.title("Fourier")
pl.semilogy(x,np.absolute(exp(x%(2*pl.pi)))) #plotting the values inverse of fourier transform of e^(x) vs x
pl.xlabel("x")
pl.ylabel("e^x")
pl.grid()


pl.figure(2)							 
pl.title("Actual")
pl.plot(x,f(x))						#plotting the values cos(cos(x)) vs x for all values in array x
pl.xlabel("x")
pl.ylabel("cos(cos(x))")
pl.grid()
pl.title("Fourier")
pl.plot(x,f(x%(2*pl.pi)))			#plotting the values inverse of fourier transform of cos(cos(x)) vs x
pl.ylabel("cos(cos(x))")
pl.grid()


NOC=26   #NOC defines number of sets of fourier cofficient needed 

e=[0];c=[0]

e[0]=(0.5/pl.pi)*si.quad(exp,0,2*pl.pi)[0] # calculating fourier cofficient a0 for e^x
c[0]=(0.5/pl.pi)*si.quad(f,0,2*pl.pi)[0]	# calculating fourier cofficient a0 for e^x

for k in range(1,NOC):
	e.append((1/pl.pi)*si.quad(ue,0,2*pl.pi,args=(k))[0]) # calculating fourier cofficients 'an' for e^x
	e.append((1/pl.pi)*si.quad(ve,0,2*pl.pi,args=(k))[0]) # calculating fourier cofficients 'bn' for e^x
	c.append((1/pl.pi)*si.quad(uc,0,2*pl.pi,args=(k))[0]) # calculating fourier cofficients 'an' for cos(cos(x))
	c.append((1/pl.pi)*si.quad(vc,0,2*pl.pi,args=(k))[0]) # calculating fourier cofficients 'bn' for cos(cos(x))

n=range(1,NOC)

pl.figure(3)    
pl.semilogy(0,abs(e[0]),"ro")
pl.semilogy(n,np.absolute(e[1:51:2]),"ro",label="integration")  # plotting fourier cofficients of e^(x) an vs n in semilog axis
pl.semilogy(n,np.absolute(e[2:51:2]),"ro")						# plotting fourier cofficients of e^(x) bn vs n in semilog axis
pl.title("Fourier coefficients of e^x vs n on semilog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")

pl.figure(4)
pl.loglog(n,np.absolute(e[1:51:2]),"ro",label="integration")	# plotting fourier cofficients of e^(x) an vs n in loglog axis
pl.loglog(n,np.absolute(e[2:51:2]),"ro")						# plotting fourier cofficients of e^(x) an vs n in loglog axis
pl.title("Fourier coefficients of e^x vs n on loglog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")

pl.figure(5)
pl.semilogy(0,abs(c[0]),"ro")
pl.semilogy(n,np.absolute(c[1:51:2]),"ro",label="integration") # plotting fourier cofficients of cos(cos(x)) an vs n in semilog axis
pl.semilogy(n,np.absolute(c[2:51:2]),"ro")						# plotting fourier cofficients of cos(cos(x)) bn vs n in semilog axis
pl.title("Fourier coefficients of cos(cos(x)) vs n on semilog scale")	
pl.ylabel("Fourier coefficients")
pl.xlabel("n")

pl.figure(6)
pl.loglog(n,np.absolute(c[1:51:2]),"ro",label="integration")	# plotting fourier cofficients of cos(cos(x)) an vs n in loglog axis
pl.loglog(n,np.absolute(c[2:51:2]),"ro")						# plotting fourier cofficients of cos(cos(x)) bn vs n in loglog axis
pl.title("Fourier coefficients of cos(cos(x)) vs n on loglog scale")	
pl.ylabel("Fourier coefficients")
pl.xlabel("n")

x=np.linspace(0,2*pl.pi,401)
x=x[:-1] # drop last term to have a proper periodic integral

A=np.zeros((400,51)) # allocate space for A

A[:,0]=1 # col 1 is all ones

for k in range(1,26):
	A[:,2*k-1]=pl.cos(k*x) 	# cos(kx) column
	A[:,2*k]=pl.sin(k*x) 	 # sin(kx) column

# finding the cofficients for which the least mean square error between the calculated and actual function is minimum
c1=sl.lstsq(A,exp(x))[0]
c2=sl.lstsq(A,f(x))[0]

pl.figure(3)
pl.semilogy(0,abs(c1[0]),"go")
pl.semilogy(n,np.absolute(c1[1:51:2]),"go",label="least mean square coefficients")	# plotting fourier cofficients of e^(x) an vs n in semilog axis
pl.semilogy(n,np.absolute(c1[2:51:2]),"go")											# plotting fourier cofficients of e^(x) bn vs n in semilog axis
pl.title("Fourier coefficients of e^x vs n on semilog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")
pl.legend()

pl.figure(4)
pl.loglog(n,np.absolute(c1[1:51:2]),"go",label="least mean square coefficients")	# plotting fourier cofficients of e^(x) an vs n in loglog axis
pl.loglog(n,np.absolute(c1[2:51:2]),"go")											# plotting fourier cofficients of e^(x) bn vs n in loglog axis
pl.title("Fourier coefficients of e^x vs n on loglog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")
pl.legend()

pl.figure(5)
pl.semilogy(0,abs(c2[0]),"go")
pl.semilogy(n,np.absolute(c2[1:51:2]),"go",label="least mean square coefficients")  # plotting fourier cofficients of cos(cos(x)) an vs n in semilog axis
pl.semilogy(n,np.absolute(c2[2:51:2]),"go")											# plotting fourier cofficients of cos(cos(x)) bn vs n in loglog axis
pl.title("Fourier coefficients of cos(cos(x)) vs n on semilog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")
pl.legend()

pl.figure(6)
pl.loglog(n,np.absolute(c2[1:51:2]),"go",label="least mean square coefficients")    # plotting fourier cofficients of cos(cos(x)) an vs n in semilog axis
pl.loglog(n,np.absolute(c2[2:51:2]),"go")											# plotting fourier cofficients of cos(cos(x)) bn vs n in loglog axis
pl.title("Fourier coefficients of cos(cos(x)) vs n on loglog scale")
pl.ylabel("Fourier coefficients")
pl.xlabel("n")
pl.legend()

erre=np.absolute(c1-e)# erre is an array containg the absolute error between fourier coefficients calculated using integration and least squares method for e^x
errf=np.absolute(c2-c)# errf is an array containg the absolute error between fourier coefficients calculated using integration and least squares method for cos(cos(x))
mde=np.amax(erre) # maximum absolute error between fourier coefficients calculated using integration and least squares method for e^x
mdf=np.amax(errf) #	maximum error between fourier coefficients calculated using integration and least squares method for cos(cos(x))
print("The max error between the fourier coefficients calculated using integration and least squares method for e^x is : ",mde)
print("The max error between the fourier coefficients calculated using integration and least squares method for cos(cos(x)) is : ",mdf)

f1=A.dot(c1)   # calculating the values of e^x found by inverse fourier transform for x in 0 to 2pi 
f2 =A.dot(c2)	# calculating the values of cos(cos(x)) found by inverse fourier transform for x in 0 to 2pi

pl.figure(1)
pl.semilogy(x,f1,"go",markersize=2)  # plotting the values of e^x found by inverse fourier transform for x in 0 to 2pi
pl.figure(2)
pl.semilogy(x,f2,"go",markersize=2)  # plotting the values of e^x found by inverse fourier transform for x in 0 to 2pi
pl.show()

# end of program