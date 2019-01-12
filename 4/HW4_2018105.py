#IP Home Assignment 4
#Suchet Aggarwal
#2018105
#CSE
#Section A Group 1

#import Necesary Modules
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import math


def matrixMult(a,b):
	'''Performs Matrix Multiplication on two matices a and b as a*b
		Input: a, b two nested lists
		Output: matrix, nested list denoting their product
	'''

	#Initialse the resultant matrix 
	matrix = [[0 for column in range(len(b[0]))] for row in range(len(a))]

	for i in range(len(a)):
		for j in range(len(b[0])):
			for k in range(len(b)):
				matrix[i][j] += (a[i][k]) * (b[k][j])
	return matrix


def scale(sM,sm,x,y,figure,strScale):
	'''Performs scaling operation about the origin by linear transformation of an input matrix
		Input: sM, sm : Major and minor Axis of the ellipse
				x,y : lists denoting the vertices of the polygon
				figure : Denotes which figure is to processed
				strSclale : Input for Scaling
		Output: updated values of sM, sm or lists x, y
	'''

	strScale=strScale.split()
	# transfromation matrix for scaling
	transformationMatrix = [[float(strScale[1]),0,0],[0,float(strScale[2]),0],[0,0,1]]

	#check for figure
	if figure=='polygon':
		for i in range(len(x)):
			inp = [[x[i]],[y[i]],[1]]
			lst=matrixMult(transformationMatrix,inp)
			x[i] = lst[0]
			y[i] = lst[1]

		#Extracting updated values from the obatined resultant matrix
		#reduce precession to two
		q = ['%0.2f' %j[0] for j in x]
		w = ['%0.2f' %j[0] for j in y]

		q=list(map(float,q))
		w=list(map(float,w))

		return q,w

	else:
		inp=[[sM],[sm],[1]]
		lst=matrixMult(transformationMatrix,inp)
		semiMajorAxis = lst[0][0]
		semiMinorAxis = lst[1][0]

		semiMajorAxis = '%0.2f' %semiMajorAxis 
		semiMinorAxis = '%0.2f' %semiMinorAxis

		semiMajorAxis=float(semiMajorAxis)
		semiMinorAxis=float(semiMinorAxis)

		return semiMajorAxis,semiMinorAxis


def rotate(a,b,x,y,figure,strRotate):
	'''Performs rotation operation about the origin by linear transformation of an input matrix
		Input:  a,b : Center of the ellipse
				x,y : lists denoting the vertices of the polygon
				figure : Denotes which figure is to processed
				strRotate : Input for Scaling
		Output: updated values of a, b or lists x, y
	'''
	strRotate=strRotate.split()
	theta = float(strRotate[1])
	theta = math.radians(theta)

	# transfromation matrix for rotation
	transformationMatrix = [[math.cos(theta),-1 * math.sin(theta),0], [math.sin(theta),math.cos(theta),0],[0,0,1]]

	#check for figure
	if figure=='polygon':
		for i in range(len(x)):
			inp = [[x[i]],[y[i]],[1]]
			lst=matrixMult(transformationMatrix,inp)
			x[i] = lst[0]
			y[i] = lst[1]

		#Extracting updated values from the obatined resultant matrix
		#reduce precession to two
		q = ['%0.2f' %j[0] for j in x]
		w = ['%0.2f' %j[0] for j in y]

		q=list(map(float,q))
		w=list(map(float,w))
		return q,w

	else:
		inp=[[a],[b],[1]]
		lst=matrixMult(transformationMatrix,inp)
		a = lst[0][0]
		b = lst[1][0]

		a = '%0.2f' %a 
		b = '%0.2f' %b

		a=float(a)
		b=float(b)

		return a,b	

def translate(a,b,x,y,figure,strTranslate):
	'''Performs translation operation about the origin by non-linear transformation of an input matrix
		Input:  a,b : Major and minor Axis of the ellipse
				x,y : lists denoting the vertices of the polygon
				figure : Denotes which figure is to processed
				strTranslate : Input for Scaling
		Output: updated values of a, b or lists x, y
	'''
	strTranslate=strTranslate.split()
	dx = float(strTranslate[1])
	dy = float(strTranslate[2])

	# transfromation matrix for translation
	transformationMatrix = [[1,0,dx],[0,1,dy],[0,0,1]]

	#check for figure
	if figure=='polygon':
		for i in range(len(x)):
			inp = [[x[i]],[y[i]],[1]]
			lst=matrixMult(transformationMatrix,inp)
			x[i] = lst[0]
			y[i] = lst[1]

		#Extracting updated values from the obatined resultant matrix
		#reduce precession to two
		q = ['%0.2f' %j[0] for j in x]
		w = ['%0.2f' %j[0] for j in y]

		q=list(map(float,q))
		w=list(map(float,w))
		return q,w

	else:
		inp=[[a],[b],[1]]
		lst=matrixMult(transformationMatrix,inp)
		a = lst[0][0]
		b = lst[1][0]

		a = '%0.2f' %a 
		b = '%0.2f' %b

		a=float(a)
		b=float(b)

		return a,b


if __name__ == '__main__':
	
	#initialse values
	figure='None'
	a=0
	b=0
	r=0
	x=[]
	y=[]


	#Main Program Begins
	while figure != 'polygon' and figure != 'disc' :
		figure = input()
		if figure == "polygon":
			x=list(map(int,input().split()))
			y=list(map(int,input().split()))
		elif figure == "disc":
			a,b,r=input().split()
			a=int(a)
			b=int(b)
			r=int(r)
		else:
			print('invalid figure')

	#At first Disc is circle but in general has to be an ellipse
	semiMajorAxis = r
	semiMinorAxis = r

	#Transformations Begin
	operation = 'None'
	while operation != 'quit' :
		operation= input()
		
		#Scaling
		if operation[0] == 'S':
			if figure == 'polygon':
				x,y =scale(semiMajorAxis, semiMinorAxis,x,y,figure,operation)
			else:
				semiMajorAxis,semiMinorAxis = scale(semiMajorAxis,semiMinorAxis,x,y,figure,operation)
		
		#Rotation
		elif operation[0] == 'R':
			if figure == 'polygon':
				x,y =rotate(a,b,x,y,figure,operation)
			else:
				a,b = rotate(a,b,x,y,figure,operation)
		
		#Translation
		elif operation[0] == 'T':
			if figure == 'polygon':
				x,y = translate(a,b,x,y,figure,operation)
			else:
				a,b = translate(a,b,x,y,figure,operation)

		#Printing the Updated values of co-ordinates of vertices/ center, Major,Minor axes
		if figure == 'polygon':
			print(x)
			print(y)
		else:
			print(a,b,semiMajorAxis,semiMinorAxis)
		
		
		#Final PLotting
		if figure == 'polygon':
			plt.ion()
			fig ,axis  = plt.subplots()
			axis.set(xlim=[-20,20],ylim=[-20,20])
			inp=[]
			for i in range(len(x)):
				inp.append([x[i],y[i]])
			poly = Polygon(inp,closed=True,fill=False)
			axis.add_artist(poly)
			plt.show()
	
		else:
			plt.ion()
			fig ,axis  = plt.subplots()
			ellipse = Ellipse(xy=[a,b], width=semiMajorAxis*2, height=semiMinorAxis*2,fill=False)			
			axis.add_artist(ellipse)
			axis.set(xlim=[-20, 20], ylim=[-20, 20])
			plt.show()
			
		

	


		
		
		





