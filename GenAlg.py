import os
import random
import math
import sys
import pp
import time


CROSSOVER_RATE = 0.7
MUTATION_RATE  = 0.1
POP_SIZE       = 100		#must be an even number
CHROMO_LENGTH  = 300
GENE_LENGTH    =  4
MAX_ALLOWABLE_GENERATIONS = 400

class ShareConstant():
	def __init__(self, CROSSOVER_RATE = 0.7, MUTATION_RATE = 0.001, POP_SIZE = 100, CHROMO_LENGTH = 300, GENE_LENGTH = 4,MAX_ALLOWABLE_GENERATIONS = 40 ):
		self.CROSSOVER_RATE = CROSSOVER_RATE
		self.MUTATION_RATE = MUTATION_RATE
		self.POP_SIZE = POP_SIZE  # must be an even number
		self.CHROMO_LENGTH = CHROMO_LENGTH
		self.GENE_LENGTH = GENE_LENGTH
		self.MAX_ALLOWABLE_GENERATIONS = MAX_ALLOWABLE_GENERATIONS


class ChromoTyp():
	def __init__(self, bitString = "", fitnessFloat = 0.0):
		self.bits = bitString
		self.fitness = fitnessFloat


def GetRandomBits(length):
	tempBits = bin(random.getrandbits(length))[2:]
	while len(tempBits) < length:
		if(RANDOM_NUM() > 0.5):
			tempBits += '1'
		else:
			tempBits += '0'
	return ChromoTyp(tempBits,0.0)

def GetChildBits():
	tempBits = ""
	return ChromoTyp(tempBits,0.0)

def BinToDec(bits):
	val = 0
	valueToAdd = 1

	for i in range(len(bits)):
		if bits[i] == '1':
			val += valueToAdd
		valueToAdd *= 2

	return val

def testParse(bit_index):
	for i in range(0, CHROMO_LENGTH, GENE_LENGTH):
		print "i: {0}  bitsParse: {1}".format(i, bit_index[i:i+GENE_LENGTH])


def ParseBits( bits, buffer,valueConst):
	cBuff  = 0
	bOperator = True
	current_bits = bits
	#buffer = []
	this_gene = 0
	#print "bits: " + str(bits)
   #testParse(current_bits)
	for i in range(0,valueConst.CHROMO_LENGTH ,valueConst.GENE_LENGTH):
		this_gene = BinToDec(current_bits[i:i+valueConst.GENE_LENGTH])
		#print "i: {0} this_gene: {1} bitsParse: {2}".format(i,this_gene,current_bits[i:i+GENE_LENGTH])

	   # print "cBuff: {} this_gene: {}".format(cBuff,this_gene)
		if bOperator:
			if (this_gene < 10) | (this_gene > 13):
				continue
			else:
				bOperator = False

				buffer.insert(cBuff,this_gene)
				cBuff += 1
				continue
		else:
			if this_gene > 9:
				continue
			else:
				bOperator = True

				buffer.insert(cBuff, this_gene)
				cBuff += 1
				continue

	if cBuff % 2 == 0:
		for i in range(cBuff):
			if (buffer[i] == 13) and (buffer[i+1] == 0):
				buffer[i] = 10
	else:
		for i in range(cBuff-1):
			if (buffer[i] == 13) and (buffer[i+1] == 0):
				buffer[i] = 10

#    print "cBuff: {} this_gene: {}".format(cBuff,this_gene)
	return cBuff

def strPrint(message, value):
	print message + str(value)

def calcResult(buffer,number_of_elements):
	result = 0.0
	for i in range(0, number_of_elements, 2):
		if buffer[i] == 10:
			result += buffer[i + 1]
		elif buffer[i] == 11:
			result -= buffer[i + 1]
		elif buffer[i] == 12:
			result *= buffer[i + 1]
		elif buffer[i] == 13:
			result /= buffer[i + 1]


	return result


def AssignFitness( bits, target_value,valueConst):
	buffer = []

	num_elements = ParseBits(bits,buffer,valueConst)

	result = 0.0

	if num_elements % 2 == 0:
		result = calcResult(buffer,num_elements)
	else:
		result = calcResult(buffer, num_elements - 1)


	if result == float(target_value):
		print"Found Value"
		return 999.0,True
	else:
		return 1/float(math.fabs(target_value - result)),False


def PrintGeneSymbol( val):

	if val < 10:
		return str(val)
	else:
		if val == 10:
			return "+"
		elif val == 11:
			return "-"
		elif val == 12:
			return "*"
		elif val == 13:
			return "/"

def PrintChromo(bits,valueConst):
	buffer = [];
	num_elemnts = ParseBits(bits,buffer,valueConst)
	geneString = ""
	for gene_bits in buffer:
		geneString += PrintGeneSymbol(gene_bits)
		geneString += " "
	print geneString


def Roulette( total_fitness,  Population,valueConst):
#    strPrint("total_fitness: ",total_fitness)
	Slice = float(RANDOM_NUM() * total_fitness)
	#strPrint("slice: ",Slice)
	fitnessSoFar = 0.0

	for i in range(valueConst.POP_SIZE):
		fitnessSoFar += Population[i].fitness
	  #  print"i: {} Slice: {} Population[i].fitness: {}".format(i, Slice, Population[i].fitness)
		if fitnessSoFar >= Slice:
			return Population[i].bits
	return ""

def Mutate(bits,valueConst):


	list_bits = list(bits)
	for i in range(len(list_bits)):
		if RANDOM_NUM() <valueConst.MUTATION_RATE:
			if list_bits[i] == "1":
				list_bits[i] = "0"
			else:
				list_bits[i] = "1"
	return "".join(list_bits)

def RANDOM_NUM():
	return float(random.uniform(0, sys.maxsize) / (sys.maxsize + 1))


def Crossover( offspring1, offspring2,valueConst):

	#CROSSOVER_RATE = 0.7
	#CHROMO_LENGTH = 300

	if(RANDOM_NUM() < valueConst.CROSSOVER_RATE):
		crossover = int(RANDOM_NUM() * valueConst.CHROMO_LENGTH)
		#print"do crossover at: {}".format(crossover)
		child1 = offspring1[:crossover] + offspring2[crossover:]
		child2 = offspring2[:crossover] + offspring1[crossover:]
		#print "A1: {}      A2: {}".format(offspring1,offspring2)
		#print "C1: {}      C2: {}".format(child1,child2)
		return child1,child2
	else:
		#print "Do not crossover"
		return offspring1, offspring2

def ConstPrint(constValue):
	print("CROSSOVER_RATE: " + str(constValue.CROSSOVER_RATE))
	print("MUTATION_RATE: " + str(constValue.MUTATION_RATE))
	print("POP_SIZE: " + str(constValue.POP_SIZE))
	print("CHROMO_LENGTH: " + str(constValue.CHROMO_LENGTH))
	print("GENE_LENGTH: " + str(GENE_LENGTH))
	print("MAX_ALLOWABLE_GENERATIONS: " +str(constValue.MAX_ALLOWABLE_GENERATIONS))

# Checks the user input for either an integer value or q if its is not either value then continue to loop until the it is one of these value and return the value:
def userInput():
	while(True):
		Input = raw_input("Input an integer or q to quit: ")
		try:
			Target = int(Input)
		except ValueError as e:
			if Input == "q":
				return Input
			else:
				print "Not an integer"
		else:
			return Target
def createChilderen(TotalFitness,chromo_list,ProgConstant):

	child1 = Roulette(TotalFitness, chromo_list, ProgConstant)
	child2 = Roulette(TotalFitness, chromo_list, ProgConstant)
	child1, child2 = Crossover(child1, child2, ProgConstant)
	child1 = Mutate(child1, ProgConstant)
	child2 = Mutate(child2, ProgConstant)

	# strPrint("child1: ",child1)
	# strPrint("child2: ", child2)

	return ChromoTyp(child1, 0.0),ChromoTyp(child2, 0.0)


def main():
	ppservers = ("192.168.0.125:35000",)
	job_server = pp.Server(15, ppservers=ppservers)
	print "Starting parallel python with", job_server.get_ncpus(), "workers"
	print "*********************\n"
	ProgConstant = ShareConstant()
	ProgConstant.POP_SIZE = 200
	ProgConstant.CHROMO_LENGTH = 3000
	ProgConstant.MAX_ALLOWABLE_GENERATIONS = 30000
	
	ConstPrint(ProgConstant)


	while(True):
		chromo_list = []
		Target = userInput()
		random.seed
		if (Target == "q") or (Target == None):
			break

		print "Target Number: " + str(Target)

		#
		#jobs = [(input, job_server.submit(sum_primes, (input,), (isprime,), ("math",))) for input in inputs]
		getRandomBit_jobs = [(job_server.submit(GetRandomBits, (ProgConstant.CHROMO_LENGTH,),  (ChromoTyp,RANDOM_NUM,),("random",))) for i in range(ProgConstant.POP_SIZE)]

		for job in getRandomBit_jobs:
			chromo_list.append(job())

		#print "Time elapsed: ", time.time() - start_time, "s"


		GenerationsRequiredToFindASolution = 0
		bFound = False
		while(bFound == False):
			
			
			start_time = time.time()

			TotalFitness = 0.0
			foundIndex = -1;

			assignFit_jobs = [(job_server.submit(AssignFitness, (chromo_list[i].bits,Target,ProgConstant,),  (ChromoTyp,ParseBits,BinToDec,calcResult,ShareConstant,), ("random","math",))) for i in range(ProgConstant.POP_SIZE)]
			jobCount = 0
			TargetFound = False
			for job in assignFit_jobs:
				currentFit,foundIT = job()
				chromo_list[jobCount].fitness = currentFit
				TotalFitness += currentFit
				jobCount += 1
				if foundIT:
					TargetFound = True


			#for i in range(POP_SIZE):
			#	currentFit = AssignFitness(chromo_list[i].bits,Target,ProgConstant)
			#	chromo_list[i].fitness = currentFit
			#	TotalFitness += chromo_list[i].fitness
			
			if TargetFound:				
				print "Solution found in " + str(GenerationsRequiredToFindASolution) + " generations. "
				PrintChromo(chromo_list[i].bits,ProgConstant)
				bFound = True
				break
				

			#for i in range(POP_SIZE):
			#	if chromo_list[i].fitness == 999.0:
			#		foundIndex = i
			#		print "Solution found in " + str(GenerationsRequiredToFindASolution) + " generations. "
			#		PrintChromo(chromo_list[i].bits,ProgConstant)
			#		bFound = True
			#		break

			if(foundIndex != -1):
				if chromo_list[foundIndex].fitness == 999.0:
					break
			#strPrint("total_fitness: ", TotalFitness)
			temp_chromo_list = []
			#for i in range(ProgConstant.POP_SIZE):
				#temp_chromo_list.append(GetRandomBits())

			#start_time = time.time()
			createChild_jobs = [(job_server.submit(createChilderen, (TotalFitness,chromo_list,ProgConstant,),  (ChromoTyp,ParseBits,BinToDec,calcResult,ShareConstant,Roulette,Mutate,Crossover,), ("random","math",))) for i in range(ProgConstant.POP_SIZE)]
			
			for job in createChild_jobs:
				child1,child2 = job()
				temp_chromo_list.append(child1)
				temp_chromo_list.append(child2)

			#for i in range(0,ProgConstant.POP_SIZE,2):

			#	child1 = Roulette(TotalFitness, chromo_list,ProgConstant)
			#	child2 = Roulette(TotalFitness, chromo_list,ProgConstant)
			#	child1,child2 = Crossover(child1,child2,ProgConstant)
			#	child1 = Mutate(child1,ProgConstant)
			#	child2 = Mutate(child2,ProgConstant)


				#strPrint("child1: ",child1)
				#strPrint("child2: ", child2)
 
			#	temp_chromo_list.append(ChromoTyp(child2, 0.0))

			#for i in range(POP_SIZE):
			#    chromo_list[i] = temp_chromo_list[i]
			chromo_list = temp_chromo_list
			if (GenerationsRequiredToFindASolution % 1000) == 0:
				strPrint("Current generation: ", GenerationsRequiredToFindASolution)
				print "Time elapsed: ", time.time() - start_time, "s"
			GenerationsRequiredToFindASolution += 1

			if GenerationsRequiredToFindASolution > ProgConstant.MAX_ALLOWABLE_GENERATIONS:
				print "No solution found this run"
				bFound = True
main()

