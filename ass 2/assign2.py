import numpy as np
import sys
import cmath
# checking if file name is given
if len(sys.argv)==1:
	print("Please provide the file name")
	quit()

#checking for valid command line arguments
if len(sys.argv)>2:
	print("Invalid number of command line arguments")
	quit()

try:
	filename=sys.argv[1]
	file=open(filename)
except Exception:
	print("Invalid File")
	quit()

#read all lines in the file as store them as a array of strings
lines=file.readlines()
file.close()

nol=len(lines)
start=-1
end=-1
ac=-1

for i in range(0,nol):
#ignoring comments in the lines
	lines[i]=lines[i].split('#')
	lines[i]=lines[i][0]
	#spliting lines into words and reversing the order
	lines[i]=lines[i].split()
	#checking for ".circuit" and ".end"
	if lines[i][0]==".circuit":
		start=i
	if lines[i][0]==".end":
		end=i
	if lines[i][0]==".ac":
		ac=i


if start==-1:
	print("No .circuit found")
	quit()
if end==-1:
	print(".end not found")
	quit()

if ac==-1:	
	nodes={}
	k=0

	for i in range(start+1,end):
		if lines[i][0][0]=="R":
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0][0],lines[i][2],1/float(lines[i][3])])
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0][0],lines[i][2],1/float(lines[i][3])]]

			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0][0],lines[i][1],1/float(lines[i][3])])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0][0],lines[i][1],1/float(lines[i][3])]]

		if lines[i][0][0]=="V":
			k=k+1
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0][0],int(lines[i][0][1]),-1,float(lines[i][3])])
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0][0],int(lines[i][0][1]),-1,float(lines[i][3])]]
				
			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0][0],int(lines[i][0][1]),1,float(lines[i][3])])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0][0],int(lines[i][0][1]),1,float(lines[i][3])]]

	n=len(nodes)

	matrix_A=np.zeros([n+k,n+k],dtype="complex")
	matrix_B=np.zeros(n+k,dtype="complex")

	m=0
	node_index=nodes.copy()
	for i in node_index:
		node_index[i]=m
		m=m+1
	del m

	for i in nodes:
		for j in nodes[i]:
			if j[0]=="R":
				matrix_A[node_index[i],node_index[i]]+=j[2]
				if j[1]!="GND":
					matrix_A[node_index[i],node_index[j[1]]]-=j[2]
			elif j[0]=="V":
				matrix_A[node_index[i],n-1+j[1]]=-1*j[2]
				matrix_A[n-1+j[1],node_index[i]]=j[2]
				matrix_B[n-1+j[1]]=j[3]

	print(matrix_A)

	matrix_X=np.linalg.solve(matrix_A,matrix_B)

	j=0
	for i in node_index:
		print("V(node {})={}".format(i,matrix_X[j]))
		j=j+1

	j=int(n)
	for i in range(k):
		print("I(V{})={}".format(i+1,matrix_X[j]))
		j=j+1

else:
	freq=float(lines[ac][2])
	source_number=lines[ac][1][1]
	nodes={}
	k=0

	for i in range(start+1,end):
		if lines[i][0][0]=="R":
			if lines[i][1] in nodes:
				nodes[lines[i][1]].append([lines[i][0][0],lines[i][2],1/float(lines[i][3])])
			elif lines[i][1]!="GND":
				nodes[lines[i][1]]=[[lines[i][0][0],lines[i][2],1/float(lines[i][3])]]

			if lines[i][2] in nodes:
				nodes[lines[i][2]].append([lines[i][0][0],lines[i][1],1/float(lines[i][3])])
			elif lines[i][2]!="GND":
				nodes[lines[i][2]]=[[lines[i][0][0],lines[i][1],1/float(lines[i][3])]]

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


		elif lines[i][0][0]=="V":
			k=k+1
			if lines[i][3]=="dc":
				if lines[i][1] in nodes:
					nodes[lines[i][1]].append([lines[i][0][0],int(lines[i][0][1]),-1,float(lines[i][4])])
				elif lines[i][1]!="GND":
					nodes[lines[i][1]]=[[lines[i][0][0],int(lines[i][0][1]),-1,float(lines[i][4])]]
					
				if lines[i][2] in nodes:
					nodes[lines[i][2]].append([lines[i][0][0],int(lines[i][0][1]),1,float(lines[i][4])])
				elif lines[i][2]!="GND":
					nodes[lines[i][2]]=[[lines[i][0][0],int(lines[i][0][1]),1,float(lines[i][4])]]
			if lines[i][3]=="ac":
				if lines[i][1] in nodes:
					nodes[lines[i][1]].append([lines[i][0][0],int(lines[i][0][1]),-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))])
				elif lines[i][1]!="GND":
					nodes[lines[i][1]]=[[lines[i][0][0],int(lines[i][0][1]),-1,cmath.rect(float(lines[i][4]),float(lines[i][5]))]]
					
				if lines[i][2] in nodes:
					nodes[lines[i][2]].append([lines[i][0][0],int(lines[i][0][1]),1,cmath.rect(float(lines[i][4]),float(lines[i][5]))])
				elif lines[i][2]!="GND":
					nodes[lines[i][2]]=[[lines[i][0][0],int(lines[i][0][1]),1,cmath.rect(float(lines[i][4]),float(lines[i][5]))]]
	print(cmath.rect(float(lines[i][4]),float(lines[i][5])))
	n=len(nodes)
	print()
	matrix_A=np.zeros([n+k,n+k],dtype="complex")
	matrix_B=np.zeros(n+k,dtype="complex")

	m=0
	node_index=nodes.copy()
	for i in node_index:
		node_index[i]=m
		m=m+1
	del m

	print(nodes)

	for i in nodes:
		for j in nodes[i]:
			if j[0]=="R" or j[0]=="C" or j[0]=="L":
				matrix_A[node_index[i],node_index[i]]+=j[2]
				if j[1]!="GND":
					matrix_A[node_index[i],node_index[j[1]]]-=j[2]
			elif j[0]=="V":
				matrix_A[node_index[i],n-1+j[1]]=-1*j[2]
				matrix_A[n-1+j[1],node_index[i]]=j[2]
				matrix_B[n-1+j[1]]=j[3]


	matrix_X=np.linalg.solve(matrix_A,matrix_B)

	j=0
	for i in node_index:
		print("V(node {})=mag:{}, phase:{} ".format(i,list(cmath.polar(matrix_X[j]))[0],cmath.phase(matrix_X[j])))
		j=j+1

	j=int(n)
	for i in range(k):
		print("I(V{})=mag:{}, phase:{}".format(i+1,list(cmath.polar(matrix_X[j]))[0],cmath.phase(matrix_X[j])))
		j=j+1
