"""
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
"""

# some imports.

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

# function to generate label dictionary

def createLabelTable():
	vprint("\n\n\n*******************************************\nGENERATE LABEL TABLE: \n*******************************************\n")

	for key in FILE_DATA:
		try:
			LABEL_TABLE[FILE_DATA[key][2]] = key

		except IndexError:
			vprint("Line "+str(key)+": Label not found")

		else:
			vprint("Line "+str(key)+": Label found ---> "+FILE_DATA[key][2])
			FILE_DATA[key] = [FILE_DATA[key][0], FILE_DATA[key][1]]

	vprint("\n--------------------------------------------\n*\t\tLABEL TABLE\n*")

	for labelName in LABEL_TABLE:
		vprint("*\t"+labelName+": \t\t"+str(LABEL_TABLE[labelName]))

	vprint("*\n--------------------------------------------\n")



# Variable Table data structure
# keeps track of what variables exist
# and what their memory address is

VAR_TABLE = {}

# function to generate variable dictionary
# Also converts data in argument field to
# integer if its not a variable
#
# It also sorts out the information of other
# arguments while they are at it.

def createVarTable():
	vprint("\n\n\n*******************************************\nDECODE ARGUMENTS: \n*******************************************\n")
	memLocation = 0

	for key in FILE_DATA:
		varFound = False
		labelFound = False
		keywordFound= False

		try:
			FILE_DATA[key][1] = int(FILE_DATA[key][1])
			vprint("Line "+str(key)+": Integer found ---> "+str(FILE_DATA[key][1]))

		except IndexError:
			print("\n*\t*\t*\t*\t*\nError! No argument found in Line "+str(key))
			exit(1)

		except ValueError:

			# REGISTER REFERENCE B1 AND B2

			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "B1", key, 0, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "B2", key, 8, keywordFound)

			# ADD SPECIFIC ARGUMENTS

			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "B1+B2", key, 0, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "B1-B2", key, 1, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "-B1+B2", key, 2, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "-B1-B2", key, 3, keywordFound)

			# BOOL SPECIFIC ARGUMENTS

			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BAND", key, 0, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LAND", key, 1, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BOR", key, 2, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LOR", key, 3, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BXOR", key, 4, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BXNOR", key, 5, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LB1", key, 6, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LB2", key, 7, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BNAND", key, 8, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LNAND", key, 9, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "BNOR", key, 10, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "LNOR", key, 11, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "NB1", key, 12, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "NB2", key, 13, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "RB1", key, 14, keywordFound)
			FILE_DATA[key][1], keywordFound = evaluateKeyword(FILE_DATA[key][1], "RB2", key, 15, keywordFound)

			# IF NOT KEYWORD -> THEN ITS A VARIABLE
			if(not keywordFound):

				# check to see if variable aldready exists in table
				for varIndex in VAR_TABLE:

					if(VAR_TABLE[varIndex] == FILE_DATA[key][1]):
						varFound = True
						vprint("Line "+str(key)+": Old Var found ---> "+FILE_DATA[key][1]+" ("+str(varIndex)+")")
						FILE_DATA[key][1] = varIndex
						break

				# check to see if its actuall a label
				for labelName in LABEL_TABLE:

					if(labelName  == FILE_DATA[key][1]):
						labelFound = True
						vprint("Line "+str(key)+": Label   found ---> "+FILE_DATA[key][1])
						FILE_DATA[key][1] = labelOffset(FILE_DATA[key][1], key, FILE_DATA[key][0])
						break

				# if both cases are not found, then add it to the table
				if((not varFound) and (not labelFound)):
					vprint("Line "+str(key)+": New Var found ---> "+FILE_DATA[key][1]+" ("+str(memLocation)+")")
					VAR_TABLE[memLocation] = FILE_DATA[key][1]
					FILE_DATA[key][1] = memLocation
					memLocation += 1


	vprint("\n--------------------------------------------\n*\t\tVARIABLE TABLE\n*")

	for varLocation in VAR_TABLE:
		vprint("*\t"+str(varLocation)+": "+VAR_TABLE[varLocation])

	vprint("*\n--------------------------------------------\n")


def evaluateKeyword(curArg, keyword, linenum, keywordValue, keywordFound):
	if(curArg == keyword):
		keywordFound = True
		vprint("Line "+str(linenum)+": Keyword found ---> "+keyword)
		return keywordValue, keywordFound
	else:
		return curArg, keywordFound

# function to calculate offset of current line number
# relative to a label's line number

def labelOffset(label,linenum, instruction):
	offsetVal = LABEL_TABLE[label] - linenum
	
	# SHFF offsets have to be positive.
	if(instruction == "SHFF"):
		if(offsetVal > 0):
			return offsetVal

		elif(offsetVal == 0):
			print("\n*\t*\t*\t*\t*\nError! SHFF points to itself! Found in Line "+str(linenum))
			exit(1)

		else:
			print("\n*\t*\t*\t*\t*\nError! SHFF is pointing backwards! Use SHFB. Found in Line "+str(linenum))
			exit(1)

	# SHFB offsets have to be negative
	# but they must be stored as positives
	elif(instruction == "SHFB"):
		if(offsetVal < 0):
			return -offsetVal

		elif(offsetVal == 0):
			print("\n*\t*\t*\t*\t*\nError! SHFF points to itself! Found in Line "+str(linenum))
			exit(1)

		else:
			print("\n*\t*\t*\t*\t*\nError! SHFB is pointing forwards! Use SHFF. Found in Line "+str(linenum))
			exit(1)

	# if its neither of these instructions
	# its safe to just return calculated 
	# offset value.
	else:
		return offsetVal
	# Its probably BNR. But if its not,
	# its just a value anyway...



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
		vprint("\n\n\n*******************************************\nPARSE INPUT FILE:\n*******************************************\n")
		humFile = open(FILE_NAME,'r')

	except IOError:
		print("\n*\t*\t*\t*\t*\nError! Cannot open file ",FILE_NAME)
		exit(1)

	else:
		curLine = 0
		for line in humFile:

			if(line[0] == "#"):
				continue

			FILE_DATA[curLine] = line.split()
			vprint("Line "+str(curLine)+" ---> "+str(FILE_DATA[curLine]))
			curLine += 1

# Write File Data Function:
#	write the file data into a 
#	an actualy file

def writeFileData():
	try:
		binFile = open(FILE_NAME+"_BIN",'w')

	except IOError:
		print("\n*\t*\t*\t*\t*\nError! Unable to write to file ",FILE_NAME+"_BIN")
		exit(1)

	else:
		for line in FILE_DATA:
			binFile.write(FILE_DATA[line][0]+" "+FILE_DATA[line][1]+"\n")

		binFile.close()


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

		elif(FILE_NAME == ""):
			FILE_NAME = argu

		elif(argu[0] == "-" and argu[1] == "-"):
			helpDialouge("commandError")

		else:
			helpDialouge("fileError")

	parseInputFile()


# Help function:
#	Displays the help dialouge.
#	changes with status

def helpDialouge(status):
	exitCode = 0

	if(status == "help"):
		print("Welcome to Help")

	elif(status == "commandError"):
		print("You have entered an invalid command")

	elif(status == "fileError"):
		print("You have entered another filename, there can only be one file")

	exit(exitCode)



# Display file function:
#	a function to display the contents of 
#	FILE_DATA data structure

def displayFileData():
	vprint("\n\n\n*******************************************\nDISPLAYING FILE DATA:\n*******************************************\n")
	curLine = 0
	for item in FILE_DATA:
		vprint(str(curLine)+":\t"+str(FILE_DATA[item]))
		curLine += 1

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
	curLine = 0
	for line in FILE_DATA:
		FILE_DATA[line][0],FILE_DATA[line][1] = decodeInstruction(FILE_DATA[line][0], FILE_DATA[line][1], curLine)
		curLine += 1


# Decode Compile function:
#	the goal of this function is to
#	take an assembly instruction
#	and convert into binary string

def decodeInstruction(opcode, argi, curLine):
	return decodeOpcode(opcode, curLine), intToBin(argi, curLine)

# Decode Instruction function:
#	this function finds the instruction 
#	and returns its proper binary string

def decodeOpcode(opcode, curLine):
	opcodeFound = False
	
	# search for opcode
	opcode, opcodeFound = decodeHelper(opcode, "HALT" , "0000", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "SHFF" , "0001", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "SHFB" , "0010", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "BNR"  , "0011", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "INP"  , "0100", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "STR"  , "0101", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "LDB1" , "0110", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "LDB2" , "0111", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "ADDB1", "1000", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "ADDB2", "1001", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "BOOL" , "1010", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "ADD"  , "1011", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "SUBB1", "1100", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "SUBB2", "1101", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "STM"  , "1110", opcodeFound)
	opcode, opcodeFound = decodeHelper(opcode, "MEMC" , "1111", opcodeFound)
	
	# if opcode not found return error
	if(not opcodeFound):
		print("\n*\t*\t*\t*\t*\nError! Unable to decode opcode: "+opcode+" : On line -> "+str(curLine))
		exit(1)

	# else return the found value
	return opcode

# Decode Instruction Helper function:
#	a simple if statement handler.

def decodeHelper(inCode, asmString, binString, Found):
	if((inCode == asmString) and (not Found)):
		Found = True
		return binString, Found
	else:
		return inCode, Found

# integer to binary function:
#	this function takes and integer
#	and returns its binary string
#	Fails if integer out of bounds.

def intToBin(argi, curLine):
	argiFound = False
	
	# positive or unsigned numbers
	argi, argiFound = decodeHelper(argi, 0,  "0000", argiFound)
	argi, argiFound = decodeHelper(argi, 1,  "0001", argiFound)
	argi, argiFound = decodeHelper(argi, 2,  "0010", argiFound)
	argi, argiFound = decodeHelper(argi, 3,  "0011", argiFound)
	argi, argiFound = decodeHelper(argi, 4,  "0100", argiFound)
	argi, argiFound = decodeHelper(argi, 5,  "0101", argiFound)
	argi, argiFound = decodeHelper(argi, 6,  "0110", argiFound)
	argi, argiFound = decodeHelper(argi, 7,  "0111", argiFound)
	argi, argiFound = decodeHelper(argi, 8,  "1000", argiFound)
	argi, argiFound = decodeHelper(argi, 9,  "1001", argiFound)
	argi, argiFound = decodeHelper(argi, 10, "1010", argiFound)
	argi, argiFound = decodeHelper(argi, 11, "1011", argiFound)
	argi, argiFound = decodeHelper(argi, 12, "1100", argiFound)
	argi, argiFound = decodeHelper(argi, 13, "1101", argiFound)
	argi, argiFound = decodeHelper(argi, 14, "1110", argiFound)
	argi, argiFound = decodeHelper(argi, 15, "1111", argiFound)
	
	# negative numbers
	argi, argiFound = decodeHelper(argi, -8,  "1000", argiFound)
	argi, argiFound = decodeHelper(argi, -7,  "1001", argiFound)
	argi, argiFound = decodeHelper(argi, -6, "1010", argiFound)
	argi, argiFound = decodeHelper(argi, -5, "1011", argiFound)
	argi, argiFound = decodeHelper(argi, -4, "1100", argiFound)
	argi, argiFound = decodeHelper(argi, -3, "1101", argiFound)
	argi, argiFound = decodeHelper(argi, -2, "1110", argiFound)
	argi, argiFound = decodeHelper(argi, -1, "1111", argiFound)
	
	# if still not found return error
	if(not argiFound):
		print("\n*\t*\t*\t*\t*\nError! Integer out of bounds (-8 <= x <= 15) : "+str(argi)+"\nFound on line -> "+str(curLine))
		exit(1)
	
	# else return the found value
	return argi





"""
# ----------------------------------------------------
#
# Simulation Functions
#
# ----------------------------------------------------
"""

def simulation():

	vprint("intializing system")
	# program counter
	programCounter = 0
	# register b1
	registerB1 = "0000 0000"
	# register b2
	registerB2 = "0000 0000"
	# result register
	registerRS = "0000 0000"
	# setup main memory
	mainMem = {}
	mainMem["0000"] = "0000 0000"
	mainMem["0001"] = "0000 0000"
	mainMem["0010"] = "0000 0000"
	mainMem["0011"] = "0000 0000"
	mainMem["0100"] = "0000 0000"
	mainMem["0101"] = "0000 0000"
	mainMem["0110"] = "0000 0000"
	mainMem["0111"] = "0000 0000"
	mainMem["1000"] = "0000 0000"
	mainMem["1001"] = "0000 0000"
	mainMem["1010"] = "0000 0000"
	mainMem["1011"] = "0000 0000"
	mainMem["1100"] = "0000 0000"
	mainMem["1101"] = "0000 0000"
	mainMem["1110"] = "0000 0000"
	mainMem["1111"] = "0000 0000"

	# start program
	while(True):

		# perform safety checks here

		# Display current status of the program

		# start reading instructions.
		
		# HALT
		if(FILE_DATA[programCounter][0] == "0000"):
			break

		# SHFF
		elif(FILE_DATA[programCounter][0] == "0001"):
			pass
		
		# SHFB
		elif(FILE_DATA[programCounter][0] == "0010"):
			pass
			
		# BNR
		elif(FILE_DATA[programCounter][0] == "0011"):
			pass
		
		# INP
		elif(FILE_DATA[programCounter][0] == "0100"):
			pass
		
		# STR
		elif(FILE_DATA[programCounter][0] == "0101"):
			pass
		
		# LDB1
		elif(FILE_DATA[programCounter][0] == "0110"):
			pass
		
		# LDB2
		elif(FILE_DATA[programCounter][0] == "0111"):
			pass
		
		# ADDB1
		elif(FILE_DATA[programCounter][0] == "1000"):
			pass
		
		# ADDB2
		elif(FILE_DATA[programCounter][0] == "1001"):
			pass
		
		# BOOL
		elif(FILE_DATA[programCounter][0] == "1010"):
			pass
		
		# ADD
		elif(FILE_DATA[programCounter][0] == "1011"):
			pass
		
		# SUBB1
		elif(FILE_DATA[programCounter][0] == "1100"):
			pass
		
		# SUBB2
		elif(FILE_DATA[programCounter][0] == "1101"):
			pass
		
		# STM
		elif(FILE_DATA[programCounter][0] == "1110"):
			pass
		
		# MEMC
		elif(FILE_DATA[programCounter][0] == "1111"):
			mainMem["0000"] = "0000 0000"
			mainMem["0001"] = "0000 0000"
			mainMem["0010"] = "0000 0000"
			mainMem["0011"] = "0000 0000"
			mainMem["0100"] = "0000 0000"
			mainMem["0101"] = "0000 0000"
			mainMem["0110"] = "0000 0000"
			mainMem["0111"] = "0000 0000"
			mainMem["1000"] = "0000 0000"
			mainMem["1001"] = "0000 0000"
			mainMem["1010"] = "0000 0000"
			mainMem["1011"] = "0000 0000"
			mainMem["1100"] = "0000 0000"
			mainMem["1101"] = "0000 0000"
			mainMem["1110"] = "0000 0000"
			mainMem["1111"] = "0000 0000"
		programCounter += 1


"""
# -----------------------------------------------------
#
# Main functions
#
# -------------------------------------------------------
"""

def main():
	parseCmdLineArg()
	
	if(ASSEMBLE):
		createLabelTable()
		createVarTable()
		asmCompile()
		displayFileData()

	if(ASSEMBLE and (not SIMULATE)):
		writeFileData()

	if(SIMULATE):
		simulation()





# start the main function
main()


