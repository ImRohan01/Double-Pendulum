import time
import math

M_PI   = 3.14159265358979323846
HEIGHT = 1000
WIDTH  = 600
dH     = 16
dW     = 8

class Timer:
	def __init__(self):
		self.beg = time.time()

	def reset(self):
		self.beg = time.time()
	
	def elapsed(self):
		return time.time() - self.beg

def gotoxy(x,y):
	print("\033[%d;%dH" % (y+1, x+1),end="")


def drawPoint(A, B, c):
	global platNo
	if A < 0 or B < 0 or A >= WIDTH/dW or B >= HEIGHT/dH:
		return
	platNo[B][A] = c

def drawLine(A, B, C, D, c):
	global platNo
	if A > C:
		t = A
		A = C
		C = t
		t = B
		B = D
		D = t

	if B == D:
		for i in range(A,C+1):
			drawPoint(i,B,c)
		return

	if A == C:
		min = B
		max = D
		if D < B:
			min = D
			max = B

		for i in range(min,max+1):
			drawPoint(A,i,c)
		return

	if abs(D-B) < abs(C-A):
		plotLineLow(A,B,C,D,c)
	else:
		if B > D:
			plotLineHigh(C,D,A,B,c)
		else:
			plotLineHigh(A,B,C,D,c)

def plotLineLow(x0, y0, x1, y1, c):
	global platNo
	dx = x1 - x0
	dy = y1 - y0 
	yi = 1
	if dy < 0:
		yi = -1
		dy = -dy
	D = 2*dy - dx
	y = y0
	for x in range(x0,x1+1):
		drawPoint(x,y,c)
		if D > 0:
			y += yi
			D -= 2*dx
		D += 2*dy

def plotLineHigh(x0, y0, x1, y1, c):
	global platNo
	dx = x1 - x0
	dy = y1 - y0
	xi = 1
	if dx < 0:
		xi = -1
		dx = -dx
	D = 2*dx - dy
	x = x0
	for y in range(y0,y1+1):
		drawPoint(x,y,c)
		if D > 0:
			x += xi
			D -= 2*dy
		D += 2*dx

if __name__ == "__main__":
	N 		= 10000 		# no. of pendulams
	g 		= 9.81			# acc. due to gravity
	epsilon = 0.000001
	

	l1, l2 = [150]*N, [150]*N	# lengths
	m1, m2 = [10]*N, [10]*N	    # masses
	w1, w2 = [0]*N, [0]*N		# angular velocities
	o1, o2 = [], []				# angles

	for i in range(N):
		o1.append(2.0 * (M_PI/2.0) + epsilon * (2*i - N+1))
		o2.append(2.0 * (M_PI/2.0))

	fps 	= 100				
	dt 		= 1/fps
	acc		= 0

	tmr 		= Timer()
	frameStart  = tmr.elapsed()

	platNo = [[0]*(WIDTH//dW + 1) for i in range(HEIGHT//dH)]

	for i in range(HEIGHT//dH - 1):
		platNo[i][WIDTH//dW] = '\n'

	platNo[HEIGHT//dH-1][WIDTH//dW] = '\0'

	for i in range(HEIGHT//dH):
		for j in range(WIDTH//dW):
			platNo[i][j] = ' '

	while True:
		gotoxy(0,0)
		currentTime =  tmr.elapsed()
		acc			+= currentTime - frameStart
		
		frameStart  =  currentTime

		if acc >= 1/30:
			acc = 1/30
		
		while(acc > dt):
			for i in range(N):
				alpha1 =  (-g*(2*m1[i]+m2[i])*math.sin(o1[i])-g*m2[i]*math.sin(o1[i]-2*o2[i])-2*m2[i]*math.sin(o1[i]-o2[i])*(w2[i]*w2[i]*l2[i]+w1[i]*w1[i]*l1[i]*math.cos(o1[i]-o2[i]))  )/(  l1[i]*(2*m1[i]+m2[i]-m2[i]*math.cos(2*o1[i]-2*o2[i])))
				alpha2 =  (2*math.sin(o1[i]-o2[i])  )*(  w1[i]*w1[i]*l1[i]*(m1[i]+m2[i]) + g*(m1[i]+m2[i])*math.cos(o1[i]) + w2[i]*w2[i]*l2[i]*m2[i]*math.cos(o1[i]-o2[i])  )/l2[i]/(  2*m1[i]+m2[i]-m2[i]*math.cos(2*o1[i]-2*o2[i]))
				w1[i]  += 10*dt*alpha1
				w2[i]  += 10*dt*alpha2
				o1[i]  += 10*w1[i]*dt
				o2[i]  += 10*w2[i]*dt
			
			acc -= dt
		
		for i in range(HEIGHT//dH):
			for j in range(WIDTH//dW):
				platNo[i][j] = ' '

		for i in range(N):
			x1 = int((WIDTH/2 + math.sin(o1[i]) * l1[i] + dW*0.5)/dW)
			y1 = int((math.cos(o1[i]) * l1[i] + dH*0.5)//dH + HEIGHT/dH/2)
			x2 = int(x1+(math.sin(o2[i])*l2[i]+dW*0.5)/dW)
			y2 = int(y1+(math.cos(o2[i])*l2[i]+dH*0.5)/dH)
			
			if i%2 == 0:
				drawLine(WIDTH//2//dW,HEIGHT//dH//2,x1,y1,'*')
				drawLine(x1,y1,x2,y2,'*')
				drawPoint(WIDTH//2//dW,HEIGHT//dH//2,'O')
				drawPoint(x1,y1,'@')
				drawPoint(x2,y2,'@')
			else:
				drawLine(WIDTH//2//dW,HEIGHT//dH//2,x1,y1,'.')
				drawLine(x1,y1,x2,y2,'.')
				drawPoint(WIDTH//2//dW,HEIGHT//dH//2,'O')
				drawPoint(x1,y1,'@')
				drawPoint(x2,y2,'@')
		res = ""
		for i in platNo:
			res += "".join(i)
		print(res,end = "")
