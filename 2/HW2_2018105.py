# CSE 101 - IP HW2
# K-Map Minimization
# Name: Suchet Aggarwal
# Roll Number: 2018105
# Section: A
# Group: 1
# Date: 09.10.18

grayCode1 = ['0','1']
grayCode2 = ['00','01','10','11']
grayCode3 = ['000','001','010','011','100','101','110','111']
grayCode4 = ['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']

def combine(min1, min2):
	"""
		This python function takes 2 minterms as input and depennding upon whether 
		they can be combined returns the combined expression
		as the output.
		For combining two terms they must only diifer at only one position

	Input: Two minterms of the form XXXX and YYYY where X,Y=0,1
	
	Output: Combined term if they can be combined 
			Else returns None
		
	"""
	comb = ''
	count = 0
	for i in range(len(min1)):
		#Two terms are combined only if they differ by only one place
		if(min1[i] == min2[i]):
			comb += min1[i]
		else:
			comb += '-'
			count += 1

	if(count > 1):
		return None
	else:
		return comb


def noofOnes(minterm):
	'''
		This python function takes a single minterm as input and returns the number of 
		ones in its binary representation as the output.
		
	Input: One minterm (in Binary Representation) 
	
	Output: No of ones occuring
		
	'''
	n=minterm.count('1')
	return n

def inPI(primeImplicants,minterm,numVar):
	'''
		This python function takes a single minterm and a single prime implicant as
		input and returns whether the minterm is used to form that implicant
		
	Input: One minterm, Prime Implicant (in Binary Representation) and the no of variables
	
	Output: True if minterm is used to form that prime implicatn
			False Otherwise
		
	'''
	for j in range(numVar):
		if not(minterm[j] == primeImplicants[j] or primeImplicants[j] =='-'):
			return False
	return True

def findPrimeImplicants(stringFunction):
    '''
		This python function (Recursive) implements the Quine Mclusskey method to minimise a given boolean finction
		it takes a single list depicting the function to be minimised as
		input and returns a list of all possible Prime Implicants
		
	Input: list containing the function to be minimised expressed in graycode (minterms + dont cares)
	
	Output: list of Prime Implicants
		
	'''
    size = len(stringFunction)
    Out = []
    #contains grouped terms
    intmed = []
    #Contains Non repitative entries from intmed
    intmed2 = []
    #mark1 indicates whether given minterm is combined with others or not
    mark1=[]
    #initialse mark1
    for i in range(size):
    	mark1.append(0)
    #no of single minterm entrie in PI's
    count = 0
    #Combining Terms
    for i in range(size):
        for j in range(i+1, size):
            c = combine( str(stringFunction[i]), str(stringFunction[j]) )
            if c != None:
                intmed.append(str(c))
                mark1[i] = 1
                mark1[j] = 1
            else:
                continue
    #mark2 checks whteher a term is repeated in intmed
    mark2 = []
    for i in range(len(intmed)):
    	mark2.append(0)

    #eliminate the duplicate terms from a group
    for p in range(len(intmed)):
        for n in range(p+1, len(intmed)):
            if( p != n and mark2[n] == 0):
                if( intmed[p] == intmed[n]):
                    mark2[n] = 1

    #Adding only those entries from intmed to intmed2 which dont repeat
    for r in range(len(intmed)):
        if(mark2[r] == 0):
            intmed2.append(intmed[r])

    #Adding those entries that couldn't be combined with any other entry in the function
    for q in range(size):
        if( mark1[q] == 0 ):
            Out.append( str(stringFunction[q]) )
            count+=1

    if(count == size or size == 1):
        return Out
    else:
        return Out + findPrimeImplicants(intmed2)

def findEssentialPrimeImplicants(primeImplicants,minterm,dontCare,numVar):
	'''
		This python function takes a list prime implicants,list of minterms and dont cares and no of variables 
		as input and returns a list of the final minised terms
		
	Input:a list prime implicants,list of minterms and dont cares and no of variables
	
	Output: list of terms occuring in the final expression
		
	'''
	noofMinterms=len(minterm)
	noofprimeImplicants=len(primeImplicants)
	
	#Nested list to hold the prime implcant table
	mrk=[]
	#initialising mrk
	for i in range(noofprimeImplicants):
		m=[]
		for j in range(noofMinterms):
			m.append(0)
		mrk.append(m)
	#Dictionary to hold the PI and the cooresponding minterms that it contains
	group={}
	#Dictionary to reference minterms with integers
	intm={}

	mint=minterm+dontCare

	#Finding groups
	for i in range(len(mint)):
		intm[mint[i]]=i
	for i in primeImplicants:
		for j in mint:
			if inPI(i,j,numVar):
				if i in group:
					group[i].append(j)
				else:
					group[i] = [j]
	#Computing the Prime IMplicant Table
	for i in range(len(list(group.keys()))):
		for j in group[list(group.keys())[i]]:
			if j in minterm:
				mrk[i][intm[j]]=1
	#holds list of ESSENTIAL PRIME IMPLICANTS
	EPI=[]
	#holds list of all PIMRE IMPLICANTS that are not ESSENTIAL PRIME IMPLICANTS
	PI=[]
	#indicates which minterm occurs inside only one PI
	sumofcol=[]

	for j in range(noofMinterms):
		sumofcol.append(0)

	for j in range(noofMinterms):
		for i in range(noofprimeImplicants):
			sumofcol[j]+=mrk[i][j]
		if sumofcol[j] == 1:
			for k in group:
				if minterm[j] in group[k]:
					EPI.append(k)
	#to eleminate duplicate entries in EPI				
	EPI =list(set(EPI))
	
	for i in primeImplicants:
		if i not in EPI:
			PI.append(i)

	#mark indiactes whether a minterm is included in the final expression or not
	mark=[]
	for i in minterm:
		mark.append(0)

	for i in minterm:
		for j in EPI:
			if i in group[j]:
				mark[intm[i]]=1
	#final expression			
	final = EPI
	#adding those PI which contain minterms not contained in the EPI's
	for i in minterm:
		if mark[intm[i]]==0:
			for j in PI:
				if i in group[j]:
					final.append(j)
					mark[intm[i]]=1
					break
				else:
					pass
	return final

def minFunc(numVar, stringIn):
	"""
		This python function takes function of maximum of 4 variables
		as input and gives the corresponding minimized function(s)
		as the output (minimized using the K-Map methodology),
		considering the case of Don’t Care conditions.

	Input: A string of the format (a0,a1,a2, ...,an) d(d0,d1, ...,dm)
	
	Output: A string representing the simplified Boolean Expression in
	SOP form.
		
	"""
	#check Whether there is no minterm
	if stringIn.replace(' ','')[:2]=='()' or stringIn.replace(' ','')[0]=='d':
		return '0'
	else:
		#Conversion of data from string to a list
		n=numVar
		# l1 contains minterms
		l1=[]
		f=1
		d=stringIn.find('d')
		stringIn.replace(' ','')
		l=stringIn.find('(')+1
		if stringIn.find(',') != -1:
			u=stringIn.find(',')
		else:
			u=stringIn.find(')')
			l1.append(int(stringIn[l:u]))
			f=0
		flag =1
		while f==1:
			if flag==0:
				f=0
			l1.append(int(stringIn[l:u]))
			l=u+1
			u=stringIn.find(',',l,d)
			if u == -1:
				u=stringIn.find(')',l,d)
				flag=0

		#l2 contains don't cares
		l2=[]
		if stringIn.find('d-') ==-1:
			l=stringIn.find('(',d)+1
			f=1
			if stringIn.find(',',d) != -1:
				u=stringIn.find(',',d)
			else:
				u=stringIn.find(')',d)
				l2.append(int(stringIn[l:u]))
				f=0

			flag =1
			while f==1:
				if flag==0:
					f=0
				l2.append(int(stringIn[l:u]))
				l=u+1
				u=stringIn.find(',',l)
				if u == -1:
					u=stringIn.find(')',l)
					flag=0


		#Converting data from decimal to graycode
		if numVar ==4:
			for i in range(len(l1)):
				l1[i]=grayCode4[l1[i]]
			for i in range(len(l2)):
				l2[i]=grayCode4[l2[i]]
		elif numVar ==3:
			for i in range(len(l1)):
				l1[i]=grayCode3[l1[i]]
			for i in range(len(l2)):
				l2[i]=grayCode3[l2[i]]
		elif numVar ==2:
			for i in range(len(l1)):
				l1[i]=grayCode2[l1[i]]
			for i in range(len(l2)):
				l2[i]=grayCode2[l2[i]]
		else:
			for i in range(len(l1)):
				l1[i]=grayCode1[l1[i]]
			for i in range(len(l2)):
				l2[i]=grayCode1[l2[i]]

		#finding prime implicants	
		primeImplicants=findPrimeImplicants(l1+l2)	
		A = findEssentialPrimeImplicants(primeImplicants,l1,l2,numVar)
		#Converting expression expressed in 0's and 1's to expressed in terms of the variables A,B,C,D and their complements
		B=[]
		#B is a list storing the Essential Prime implicants and those prime implicants that occir in the expression.
		for i in A:
			c=''
			for j in range(len(i)):
				if i[j] == '1':
					c=c+chr(ord("w")+j)
				elif i[j] == '0':
					c=c+chr(ord("w")+j)+"'"
			B.append(c)
		B.sort()
		#stringOut is the final minimised expression
		stringOut=B[0]
		for i in B[1:]:
			stringOut = stringOut + ' + ' + i
		
		if stringOut !='':
			return stringOut 
		elif stringIn.replace(' ','') =='()':
			return '0'
		else:
			return '1'
		

if __name__ == '__main__':

	numVar = int(input('No. of variables: '))
	stringIn = str(input('Function: '))
	print('Simplified expression: '+minFunc(numVar,stringIn))
	