# -----------------------------------------------------------------	 
# 		HLITE - HummusLite Compiler and Simulator					
# 																	
#	The goal of this program is to convert hummuslite assembly		
#	into binary strings. This program also has the capability		
#	to run these binary strings and simulate its behaviour			
#	as it would on the minecraft world.								
#																	
#																	
# -----------------------------------------------------------------	

import sys

"""
# ---------------------------------------------------
#
# Global variables that
# control the way the program operates.
#
# ---------------------------------------------------
"""

# Option to display or supress the output.
# Defaults to supressing

VERBOSE=False

# Function to control verbose

def vprint(strTemp):
	if(VERBOSE):
		print(strTemp)


# Option to state that it is compiling

ASSEMBLE = False

# Option to state that it is simulating
SIMULATE = False

# Option to open help dialogue
HELP = False


# Label Table data structure
# Keep track of which line number each 
# label is.

LABEL_TABLE = {}

# Variable Table data structure
# keeps track of what variables exist
# and what their memory address is

VAR_TABLE = {}

# function to generate label dictionary

def createLabelTable():
	vprint("\nGENERATE LABEL TABLE: \n")
	
	for key in FILE_DATA:
		try:
			LABEL_TABLE[FILE_DATA[key][2]] = key

		except IndexError:
			vprint("Line "+str(key)+": Label not found")

		else:
			vprint("Line "+str(key)+": Label found ---> "+FILE_DATA[key][2])
	
	vprint("\n--------------------------------------------\n*\t\tLABEL TABLE\n*")
	
	for labelName in LABEL_TABLE:
		vprint("*\t"+labelName+": \t\t"+str(LABEL_TABLE[labelName])) 

	vprint("*\n--------------------------------------------\n")



# function to generate variable dictionary
# Also converts data in argument field to
# integer if its not a variable
#
# It also sorts out the information of other
# arguments while they are at it.

def createVarTable():
	vprint("\nDECODE ARGUMENTS: \n")
	memLocation = 0
	varNotFound = False

	for key in FILE_DATA:
		varFound = False

		try:
			FILE_DATA[key][1] = int(FILE_DATA[key][1])
			vprint("Line "+str(key)+": Integer found ---> "+str(FILE_DATA[key][1]))

		except IndexError:
			print("\n*\t*\t*\t*\t*\nError! No argument found in Line "+str(key))
			exit(1)

		except ValueError:

			# REGISTER REFERENCE B1 AND B2
			if(FILE_DATA[key][1] == "B1"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 0
			
			elif(FILE_DATA[key][1] == "B2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 1

			# ADD SPECIFIC ARGUMENTS
			elif(FILE_DATA[key][1] == "B1+B2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 0
			
			elif(FILE_DATA[key][1] == "B1-B2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 1
			
			elif(FILE_DATA[key][1] == "-B1+B2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 2
			
			elif(FILE_DATA[key][1] == "-B1-B2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 3

			# BOOL SPECIFIC ARGUMENTS
			elif(FILE_DATA[key][1] == "BAND"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 0
			
			elif(FILE_DATA[key][1] == "LAND"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 1
			
			elif(FILE_DATA[key][1] == "BOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 2
			
			elif(FILE_DATA[key][1] == "LOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 3
			
			elif(FILE_DATA[key][1] == "XOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 4
			
			elif(FILE_DATA[key][1] == "XNOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 5
			
			elif(FILE_DATA[key][1] == "LB1"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 6
			
			elif(FILE_DATA[key][1] == "LB2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 7
			
			elif(FILE_DATA[key][1] == "BNAND"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 8
			
			elif(FILE_DATA[key][1] == "LNAND"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 9
			
			elif(FILE_DATA[key][1] == "BNOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 10
			
			elif(FILE_DATA[key][1] == "LNOR"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 11
			
			elif(FILE_DATA[key][1] == "NB1"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 12
			
			elif(FILE_DATA[key][1] == "NB2"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 13
			
			elif(FILE_DATA[key][1] == "RB1"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 14
			
			elif(FILE_DATA[key][1] == "RB1"):
				vprint("Line "+str(key)+": Keyword found ---> "+str(FILE_DATA[key][1]))
				FILE_DATA[key][1] = 15

			# IF NOT KEYWORD -> THEN ITS A VARIABLE
			else:
				
				# check to see if variable aldready exists in table
				for varIndex in VAR_TABLE:
					
					if(VAR_TABLE[varIndex] == FILE_DATA[key][1]):
						varFound = True
						vprint("Line "+str(key)+": Old Variable found ---> "+FILE_DATA[key][1]+" ("+str(varIndex)+")")
						FILE_DATA[key][1] = varIndex
						break

				# check to see if its actuall a label
				for labelName in LABEL_TABLE:
					
					if(labelName  == FILE_DATA[key][1]):
						varFound = True
						vprint("Line "+str(key)+": Label Pointer found ---> "+FILE_DATA[key][1])
						break

				# if both cases are not found, then add it to the table
				if(not varFound):
					vprint("Line "+str(key)+": New Variable found ---> "+FILE_DATA[key][1]+" ("+str(memLocation)+")")
					VAR_TABLE[memLocation] = FILE_DATA[key][1]
					FILE_DATA[key][1] = memLocation
					memLocation += 1


	vprint("\n--------------------------------------------\n*\t\tVARIABLE TABLE\n*")
	
	for varLocation in VAR_TABLE:
		vprint("*\t"+str(varLocation)+": "+VAR_TABLE[varLocation]) 

	vprint("*\n--------------------------------------------\n")


# function to calculate offset of current line number
# relative to a label's line number

def labelOffset(label,linenum):
	pass


"""
# ---------------------------------------------------
#
# Get command line arguments
# and parse that info.
#
# ----------------------------------------------------
"""

# File data .
# input file is read and processed into
# a data structure.

FILE_NAME = ""
FILE_DATA = {}


# Parse Input File Function:
#	parses the input file obtatined 
#	from the command line arguments

def parseInputFile():
	try:
		vprint("\nPARSE INPUT FILE:\n")
		humFile = open(FILE_NAME,'r')

	except IOError:
		print("Cannot open file ",FILE_NAME)
		exit(1)

	else:
		curLine = 0
		for line in humFile:
			
			if(line[0] == "#"):
				continue
			
			FILE_DATA[curLine] = line.split()
			vprint("Line "+str(curLine)+" ---> "+str(FILE_DATA[curLine]))
			curLine += 1


# Command Line Argument Function:
#	figures out what the user 
#	wants the program to do.

def parseCmdLineArg():
	
	global FILE_NAME
	global VERBOSE
	global ASSEMBLE
	global SIMULATE

	firstTime = True

	for argu in sys.argv:
		if(firstTime):
			firstTime = False
			continue

		if(argu == "--verbose"):
			VERBOSE = True

		elif(argu == "--assemble"):
			ASSEMBLE = True

		elif(argu == "--simulate"):
			SIMULATE = True

		elif(argu == "--help"):
			helpDialouge("help")

		elif(argu[0] == "-"):
			for character in argu:
				if(character == "-"):
					continue
				elif(character == "a"):
					ASSEMBLE = True
				elif(character == "s"):
					SIMULATE = True
				elif(character == "v"):
					VERBOSE = True
				elif(character == "h"):
					helpDialouge("help")
				else:
					helpDialouge("commandError")

		elif(FILE_NAME == "" and argu != "hlite.py"):
			FILE_NAME = argu

		else:
			helpDialouge("fileError")

	parseInputFile()


# Help function:
#	Displays the help dialouge.
#	changes with status

def helpDialouge(status):
	print(status)



"""
# ----------------------------------------------------
#
# Assembly Compile Functions
#
# ----------------------------------------------------
"""

# Compile function:
# 	Reads input from the file and 
#	produces binary strings

def asmCompile():
	
	try:
		binFile = open(FILE_NAME+"_BIN",'w')
	
	except IOError:
		print("Unable to write to file ",FILE_NAME+"_BIN")
		exit(1)
	
	else:
		curLine = 0	
		for line in FILE_DATA:
			
			temp = decodeInstruction(FILE_DATA[line],curLine)
			binFile.write(temp)
			curLine += 1
		
		binFile.close()



# Decode Compile function:
#	the goal of this function is to 
#	take an assembly instruction
#	and convert into binary string

# argsType chart
#		arg structure = value
#	-------------------------------------
#	 	---- = 0	\dtype
#		xxxx = 1	\xtype
#		zxxx = 2	\ztype
#		yyyy = 3	\ytype
#		mmmm = 3	\mtype
#		cccc = 4	\ctype

def decodeInstruction(asmi, lineNum):
	instruction = asmi[0]
	return instruction


"""
# -----------------------------------------------------
#
# Main functions
#
# -------------------------------------------------------
"""

parseCmdLineArg()
createLabelTable()
createVarTable()
asmCompile()

for item in FILE_DATA:
	print(str(FILE_DATA[item]))