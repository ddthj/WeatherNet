'''
Heat Weather by ddthj/Squidfairy

TODO:
[#] create maps - created test map
[#] create map decoder
[] create neural net
[] create weathermap creater
[] train it
'''

import pygame
import random

pygame.init()
display = pygame.display.set_mode((800,400))
pygame.display.set_caption("AlgLearn")
white = (255,255,255)
black = (0,0,0)
display.fill(white)

heatmap = pygame.image.load('test1.png')

def translate(value, leftMin = -2000, leftMax = 2000, rightMin = 0, rightMax = 255):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def render(image,x,y,w,h):
    image = pygame.transform.scale(image,(w,h))
    RECT = pygame.Rect(x,y,w,h)
    display.blit(image,RECT)

def makeTempMap(size):
    tempMap = [None] * size
    for i in range(size):
        tempMap[i] = [None] * size
    for i in range(size):
        for j in range(size):
            color = display.get_at((i*10,j*10))
            if color[0] >=250 and color[1] >= 250 and color[2] >= 250:
                color[0] = 127
            tempMap[i][j] = color[0]
    return tempMap

def fixRawOut(raw,size):
    fixed = [None] * size
    for i in range(size):
        fixed[i] = [None] * size
    for i in range(size):
        for j in range(size):
            fixed[i][j] = raw[(i*size)+j]
    return fixed

def renderOut(out):
    for i in range(40):
        for j in range(40):
            color = (int(abs(out[i][j].output)),0,100)
            try:
                pygame.draw.rect(display,color,((i*10)+400,j*10,40,40))
            except:
                print(str(color))
        pygame.display.update()
        
class Hneuron():
    def __init__(self,layer,ident,prevW,follW):
        self.layer = layer
        self.ident = ident
        self.prevW = prevW #may not be needed
        self.follW = follW #may not be needed
        self.weights = []
        for i in range(follW):
            self.weights.append(random.randint(-5,5))
        self.output = 0
        self.maxInput = prevW * 5
    def calculate(self,prevList):
        total = 0.0
        for item in prevList:
            total += (float(item.output) * float(item.weights[self.ident]))
        total = float(total)/float(self.maxInput)
        self.output = total
        #self.toString()
        #if random.randint(0,400) > 396:
        #    print("Hidden Neuron ident #%s, totalled %s and hype is %s" % (str(self.ident),str(testing),str(total)))
    def toString(self):
        print("Hneuron ident #%s\n" % (str(self.ident)))
        print("Weights are: "+str(self.weights))
        print("Output is: " + str(self.output))
    def backProp(self,target,hidden,inputs):
        total = 0
        
        for item in prevList:
            total+= item.output * item.weights[self.ident]

        error = target - total

        current_average = total / len(prevList)
        target_average = target/ len(prevList)

        average_error = target_average - current_average
        for i in range(0,len(prevList)):
            perscription = prevList[i].weights[self.ident] + avgdiff
            perscription += (1/3) * (prevList[i].weights[self.ident] - target_average)
            prevList[i].backProp(perscription)
        
        

class Ineuron():
    def __init__(self,follW,ident):
        self.follW = follW #may not be needed
        self.weights = []
        for i in range(follW):
            self.weights.append(random.randint(-5,5))
        self.output = 0
        self.ident = ident
    def calculate(self,fromMap):
        
        hype = float(fromMap)/float(255)
        self.output = hype
        
        #random sample 
        #if random.randint(0,400) > 396:
        #    print("Input Neuron ident #%s, recieved %s and hype is %s" % (str(self.ident),str(fromMap),str(hype)))
        #self.toString()
    def toString(self):
        print("Ineuron ident #%s\n" % (str(self.ident)))
        print("Weights are: "+str(self.weights))
        print("Output is: " + str(self.output))
        
class Oneuron():
    def __init__(self,ident):
        self.output = 0
        self.ident = ident
        
    def calculate(self,prevList):
        maxOut = len(prevList) * 5
        total = 0
        for item in prevList:
            total +=item.output * item.weights[self.ident]
        total = float(total) / (float(maxOut) * 5)
        total = total * 2550000000
        self.output = total
        #self.toString()
    def toString(self):
        print("Oneuron ident #%s\n" % (str(self.ident)))
        print("Output is: " + str(self.output))
    def backProp(self,target,prevList):
        perscriptionList = []
        total = 0
        for item in prevList:
            total+= item.output * item.weights[self.ident]

        error = target - total

        current_average = total / len(prevList)
        target_average = target/ len(prevList)

        average_error = target_average - current_average
        for i in range(len(prevList)):
            perscription = prevList[i].weights[self.ident] + average_error
            perscription += (1/3) * (prevList[i].weights[self.ident] - target_average)
            perscriptionList.append(perscription)
        return perscriptionList

class nn():
    def __init__(self,inSize,hiddenLayers,hiddenWidth,outSize):
        self.inputs = []
        self.outputs = []
        self.hiddenLayers = hiddenLayers
        self.hiddenWidth = hiddenWidth
        for x in range(inSize):
            self.inputs.append(Ineuron(hiddenWidth,x))
        for y in range(outSize):
            self.outputs.append(Oneuron(y))        
        self.hidden = [None] * hiddenLayers
        for z in range(hiddenLayers):
            self.hidden[z] = [None] * hiddenWidth
        for i in range(hiddenLayers):
            print("Creating Hidden Layer %s of %s.." % (str(i),str(self.hiddenLayers)))
            for j in range(hiddenWidth):
                if i == 0 and hiddenLayers > 1:
                    self.hidden[i][j] = Hneuron(i,j,inSize,hiddenWidth)
                elif i == hiddenLayers - 1:
                    self.hidden[i][j] = Hneuron(i,j,hiddenWidth,outSize)
                else:
                    self.hidden[i][j] = Hneuron(i,j,hiddenWidth,hiddenWidth)
        '''
        print(str(self.inputs))
        print(str(self.outputs))
        print(str(self.hidden))
        '''
    def inputMap(self,tempMap):
        ticker = 0
        for i in range(40):
            for j in range(40):
                try:
                    self.inputs[ticker].calculate(tempMap[i][j])
                except:
                    pass
                ticker+=1
        for layer in range(self.hiddenLayers):
            for neuron in range(self.hiddenWidth):
                if layer == 0:
                    self.hidden[layer][neuron].calculate(self.inputs)
                else:
                    self.hidden[layer][neuron].calculate(self.hidden[layer-1])
        for output in self.outputs:
            output.calculate(self.hidden[self.hiddenLayers-1])
            output.output = translate(output.output)
        return self.outputs
    def train(self):
        '''
        1: get a heatmap
        2: calculate output
        3: compare output to expected
        4: back propigate error       
        '''

        for i in range(8):
            print("Training on image %s of 10..."%(str(i)))
            inName = "test"+str(i+1)+".png"
            inImage = pygame.image.load(inName)
            render(inImage,0,0,400,400)
            pygame.display.update()
            #getting heatmap
            inMap = makeTempMap(40)
            outName = "result"+str(i+1)+".png"
            outImage = pygame.image.load(outName)
            render(outImage,0,0,400,400)
            pygame.display.update()
            #getting expected
            outMap = makeTempMap(40)
            #calculating output
            testResult = self.inputMap(inMap)
            resultMap = fixRawOut(testResult,40)
            
            for j in range(40):
                for k in range(40):
                    corrections = self.outputs[(j*40)+k].backProp(outMap[j][k],self.hidden[len(self.hidden)-1])
                    for p in range(len(corrections)):
                        self.hidden[len(self.hidden)-1][p].weights[self.outputs[(j*40)+k].ident] = corrections[p]

        
                    
                    
            
            
print("attempting to train network...")

#print("Created Heat Map!")
a = nn(1600,3,1600,1600)
#print("Created Neural Network!")
a.train()
print("Trained Network!\nRunning Sample...")
render(heatmap,0,0,400,400)
pygame.display.update()
temp = makeTempMap(40)
rawOut = a.inputMap(temp)
#print("Ran Heat Map Through Network!")
Out = fixRawOut(rawOut,40)
renderOut(Out)

