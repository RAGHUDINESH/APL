import sys

# checking if file name is given
if len(sys.argv)==1:
	print("Please provide the file name")

#checking for valid command line arguments
elif len(sys.argv)>2:
	print("Invalid number of command line arguments")

elif len(sys.argv)==2:
	
	#open file if the given filename is in correct format and exists
	try:
		filename=sys.argv[1]
		file=open(filename)
	except Exception:
		print("Invalid File")
		quit()

	#read all lines in the file as store them as a array of strings
	lines=file.readlines()
	
	nol=len(lines)
	start=-1
	end=-1

	for i in range(0,nol):
		#ignoring comments in the lines
		lines[i]=lines[i].split('#')
		lines[i]=lines[i][0]
		#spliting lines into words and reversing the order
		lines[i]=lines[i].split()
		lines[i].reverse()
		#checking for ".circuit" and ".end"
		if len(lines[i])==1:
			if lines[i][0]==".circuit":
				start=i
			if lines[i][0]==".end":
				end=i
				break
		lines[i]=" ".join(lines[i])
	file.close()
	
	if start==-1:
		print("No .circuit found")
		quit()
	if end==-1:
		print(".end not found")
		quit()

		#printing the lines
	for i in range(1,end-start):
		print(lines[end-i])