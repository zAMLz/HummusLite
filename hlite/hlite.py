# -----------------------------------------------------------------	# 
# 		HLITE - HummusLite Compiler and Simulator					#
# 																	#
#	The goal of this program is to convert hummuslite assembly		#
#	into binary strings. This program also has the capability		#
#	to run these binary strings and simulate its behaviour			#
#	as it would on the minecraft world.								#
#																	#
#																	#
# -----------------------------------------------------------------	#

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

VERBOSE=True

# Function to control verbose

def vprint(strTemp):
	if(VERBOSE):
		print(strTemp)


# Option to toggle between compiling
# or simulating.
# Defaults to compiling=(False)

COMPSIM = False


# Label Table data structure
# Keep track of which line number each 
# label is.

LABEL_TABLE = {}

# function to generate label dictionary

def createLabelTable():
	vprint("\nGENERATE LABEL TABLE: \n")
	curLine = -1	
	for key in FILE_DATA:
		curLine += 1
		try:
			LABEL_TABLE[FILE_DATA[key][2]] = curLine

		except IndexError:
			vprint("Line "+str(curLine)+": Label not found")
			continue

		else:
			vprint("Line "+str(curLine)+": Label found ---> "+FILE_DATA[key][2])
			continue


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

FILE_NAME = sys.argv[1]
FILE_DATA = {}

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


#	x	x	x	x	x	x	x	x	x	x	x	x	x	


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


createLabelTable()
asmCompile()