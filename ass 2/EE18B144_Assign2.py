# taking a .netlist file as an argument and solve it to get the nodal voltages and voltages through source

import numpy as np
import sys
import cmath

if len(sys.argv)==1:	# checking if file name is given
	print("Please provide the file name")
	quit()

try:
	filename=sys.argv[1]	# filename stores the file name as string
	file=open(filename)		# file is the object for the given file
except Exception:
	print("Invalid File")
	quit()

lines=file.readlines()	# lines stores each line as a element in the list
file.close()			# closing the file

nol=len(lines)			# nol is the variable with number of lines in the file
start,end,ac=[-1,-1,-1]

for i in range(0,nol):

	lines[i]=lines[i].split('#')	#	ignoring comments in the lines
	lines[i]=lines[i][0]
	lines[i]=lines[i].split() 		#	spliting lines into words
	
	#checking for ".circuit" and ".end"
	if len(lines[i])==0:
		continue
	if lines[i][0]==".circuit":
		start=i 			# start store the index of line containing .circuit 
	if lines[i][0]==".end":
		end=i 				# end store the index of line containing .end
	if lines[i][0]==".ac":
		ac=i     			# ac store the index of line containing .ac

# printing the error statements
if start==-1:
	print("No .circuit found") 		
	quit()
if end==-1:
	print(".end not found")
	quit()

 # freq defines the frequency of the circuit
if ac==-1:	
	freq=1e-40   # freq is taken too small for dc to take care of capacitors and inductors in dc circuit
else:
	freq=2*cmath.pi*float(lines[ac][2])  # freq is multiplied by 2pi to get angular frequency
nodes={} 		#	nodes is dicitonary with node name as keys with paramaters of elements attached to it as values of the corresponding keys
v_source={} 	# 	dictionary of voltage sources
k=0   			# 	k counts the number of voltage sources

for i in range(start+1,end): 			 # looping through all lines and them to the nodes dictionary
	
	if lines[i][0][0]=="R":  															 # if the element given in the line is a resistor
		if lines[i][1] in nodes:														 # check if the node 1 name exist already as a key, if yes store the parameters
			nodes[lines[i][1]].append([lines[i][0][0],lines[i][2],1/float(lines[i][3])]) # R, other node, conductance are the parameters stored as list
		elif lines[i][1]!="GND":														 # 	if node does not exist already and is not a GND, create a key and then add the parameters 
			nodes[lines[i][1]]=[[lines[i][0][0],lines[i][2],1/float(lines[i][3])]]
		
			# Following the same procedure for node 2
		if lines[i][2] in nodes:
			nodes[lines[i][2]].append([lines[i][0][0],lines[i][1],1/float(lines[i][3])])
		elif lines[i][2]!="GND":
			nodes[lines[i][2]]=[[lines[i][0][0],lines[i][1],1/float(lines[i][3])]]

		# Following the same procedure for the capacitor and the inductor
	elif lines[i][0][0]=="C":
		if lines[i][1] in nodes:
			nodes[lines[i][1]].append([lines[i][0][0],lines[i][2],1j*freq*float(lines[i][3])]) 
		elif lines[i][1]!="GND":
			nodes[lines[i][1]]=[[lines[i][0][0],lines[i][2],1j*freq*float(lines[i][3])]]

		if lines[i][2] in nodes:
			nodes[lines[i][2]].append([lines[i][0][0],lines[i][1],1j*freq*float(lines[i][3])])
		elif lines[i][2]!="GND":
			nodes[lines[i][2]]=[[lines[i][0][0],lines[i][1],1j*freq*float(lines[i][3])]]

	elif lines[i][0][0]=="L":
		if lines[i][1] in nodes:
			nodes[lines[i][1]].append([lines[i][0][0],lines[i][2],1/(1j*freq*float(lines[i][3]))])
		elif lines[i][1]!="GND":
			nodes[lines[i][1]]=[[lines[i][0][0],lines[i][2],1/(1j*freq*float(lines[i][3]))]]

		if lines[i][2] in nodes:
			nodes[lines[i][2]].append([lines[i][0][0],lines[i][1],1/(1j*freq*float(lines[i][3]))])
		elif lines[i][2]!="GND":
			nodes[lines[i][2]]=[[lines[i][0][0],lines[i][1],1/(1j*freq*float(lines[i][3]))]]


	elif lines[i][0][0]=="V":  			#	if the element in the line is a voltage source
		v_source[lines[i][0]]=k 		#	collect all voltage sources in the v_source dictionary
		k=k+1     						# 	incrementing the number of voltage sources
		if lines[i][3]=="dc":  			# 	check if the given voltage is dc 
			if lines[i][1] in nodes: 	# 	append the voltage source paramters to the list indicated by the corresponding key in nodes
				nodes[lines[i][1]].append([lines[i][0],-1,float(lines[i][4])])	# source name, polarty of source(-1 indicating that -ve terminal is attached),value
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0],-1,float(lines[i][4])]]
					
			# following the same procedure for node 2
			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0],1,float(lines[i][4])])	# source name, polarty of source(1 indicating that +ve terminal is attached),value
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0],1,float(lines[i][4])]]
	
			# following the same procedure for ac voltage source by using complex voltages
		if lines[i][3]=="ac":  			
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0],-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2]) # cmath.rect converts polar complex numbers to rectangular complex numbers 
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0],-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2]]
					
			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0],1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0],1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2]]

	# following the same procedure for current sources as that of voltage sources
	elif lines[i][0][0]=="I":
		if lines[i][3]=="dc":
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0][0],-1,float(lines[i][4])])
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0][0],-1,float(lines[i][4])]]
					
			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0][0],1,float(lines[i][4])])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0][0],1,float(lines[i][4])]]
	
		if lines[i][3]=="ac":
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0][0],-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2])
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0][0],-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2]]
					
			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0][0],1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0][0],1,cmath.rect(float(lines[i][4]),float(lines[i][5]))/2]]


m=0 # a stray variable
node_index=nodes.copy() # node_index contains all nodes and assign indexes to them starting from 0
for i in node_index:
	node_index[i]=m
	m=m+1
del m

n=len(nodes) # n indicates the number of nodes excluding GND
matrix_A=np.zeros([n+k,n+k],dtype="complex") # intializing a square matrix of dimensions n+K
matrix_B=np.zeros(n+k,dtype="complex") # intializing a row matrix of length n+K

for i in nodes:  	# looping through all nodes
	for j in nodes[i]: # looping through each elemnt connected to the node
		if j[0]=="R" or j[0]=="C" or j[0]=="L": # if either a Resisitor or a capcitor or a inductor is attached to the node fill the conductance values at the correspomding places in the matrix
			matrix_A[node_index[i],node_index[i]]+=j[2]  # fill the conductance value at index of column and row equal to the index of the node
			if j[1]!="GND":
				matrix_A[node_index[i],node_index[j[1]]]-=j[2] # if the other node is not ground fill the negative value of the conductance at index of row equal to index of intial node and column index equal to the index of this node
		elif j[0][0]=="V":
			matrix_A[node_index[i],n+v_source[j[0]]]=-1*j[1]  # if it is a voltage source fill +1 or -1 accordingly corresponding to +I and -I in the equation
			matrix_A[n+v_source[j[0]],node_index[i]]=j[1]   # fill +1 or -1  in matrix_Acorresponding to V1-V2 in the eqaution
			matrix_B[n+v_source[j[0]]]=j[2] 			# fill the value of the voltage source in matrix_B
		elif j[0]=="I":
			matrix_B[node_index[i]]=j[1]*j[2]			# fill the value of the current source  in matrix_B at index corresponding to the node which it is is attached to.

try:
	matrix_X=np.linalg.solve(matrix_A,matrix_B) # matrix_X stores the solution of the system of linear equations 
except Exception:
	print("The Circuit has no solution") # print the error message the matrix_A is a singular matrix
	quit()

j=0
for i in node_index:
	print("V(node {})=mag:{}, phase:{} ".format(i,list(cmath.polar(matrix_X[j]))[0],cmath.phase(matrix_X[j])))  # print the voltage values at each node
	j=j+1

j=int(n)
for i in v_source.keys():
	print("I({})=mag:{}, phase:{}".format(i,list(cmath.polar(matrix_X[j]))[0],cmath.phase(matrix_X[j])))	# print the value of current through each voltage source
	j=j+1
