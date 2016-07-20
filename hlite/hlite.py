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

def createLabelTable(fileName):
	try:
		asmFile = open(fileName,'r')
	
	except IOError:
		print("Cannot open file ",fileName)
		exit(1)
	
	else:
		curLine = -1	
		for line in asmFile:
			curLine += 1
			try:
				LABEL_TABLE[line.split()[2]] = curLine

			except IndexError:
				vprint("Line "+str(curLine)+": Label not found")
				continue

			else:
				vprint("Line "+str(curLine)+": Label found ---> "+line.split()[2])
				continue
		asmFile.close()


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

def asmCompile(fileName):
	
	try:
		asmFile = open(fileName,'r')
		binFile = open(fileName+"_BIN",'w')
	
	except IOError:
		print("Cannot open file ",fileName)
		exit(1)
	
	else:
		curLine = 0	
		for line in asmFile:
			
			# if the line is a comment line
			if(line[0] == "#"):
				continue
			
			temp = decodeInstruction(line,curLine)
			binFile.write(temp)
			curLine += 1
		
		asmFile.close()
		binFile.close()



# Decode Compile function:
#	the goal of this function is to 
#	take an assembly instruction
#	and convert into binary string

def decodeInstruction(asmi, lineNum):
	instruction = ""
	
	temp = asmi.split()
	opcode = temp[0]
	args = temp[1]
	instruction = opcode+args+"\n"

	return instruction


"""
# -----------------------------------------------------
#
# Main function
#
# -------------------------------------------------------
"""


createLabelTable(sys.argv[1])
asmCompile(sys.argv[1])