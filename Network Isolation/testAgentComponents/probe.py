__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'

class Probe(object):

	def __init__(self):
		self.testinstances = {}
		self.atomicOperations = []

	def appendAtomic(self,action,rollback):
		self.atomicOperations.append({"action":action,"rollback":rollback})
		return

	def appendAtomics(self):
		pass

	def run(self,testcase):
		for testinstance in testcase.getTestInstances():
			testinstances_inputs = testinstance.getInputs()
			if testinstance.getOperation() not in self.testinstances:
				self.testinstances[testinstance.getOperation()] = {}
			for singleInput in testinstances_inputs:
				self.testinstances[testinstance.getOperation()][singleInput] = testinstances_inputs[singleInput]

		counter=0
		previousOutput = None
		try:
			for operation in self.atomicOperations:
				previousOutput = operation["action"](previousOutput, self.testinstances)
				counter = counter+1
			return True, previousOutput
		except Exception as e:
			#raise
			#print ("Phase " + str(counter) + " got exception. Reverting previous phases")
			counter = counter -1
			#print "Stepped back to " + str(counter)
			try:
				rollbackPrevOut = previousOutput
				for rollback in xrange(counter,-1,-1):
					self.atomicOperations[counter]["rollback"](rollbackPrevOut,self.testinstances)
					counter = counter-1
			except:
				pass
			return False