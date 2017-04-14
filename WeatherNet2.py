import numpy as np
import pygame

pygame.init()
display = pygame.display.set_mode((200,100))
white = [200,200,200]
display.fill(white)
pygame.display.update()

def render(image,x,y,w,h):
    image = pygame.transform.scale(image,(100,100))
    RECT = pygame.Rect(x,y,w,h)
    display.blit(image,RECT)

def make_linear(image):
    image = pygame.transform.scale(image,(100,100))
    data = []
    for i in range(0,50):
        for j in range(0,50):
            color = image.get_at((i*2,j*2))
            red = color[0]
            data.append(float(red/255))
    return data

def undo_linear(data):
    image = pygame.Surface((100,100))
    for i in range(0,50):
        for j in range(0,50):
            color = [int(data[0][int(i*50 + j)]) * 255,0,0]
            image.set_at((i*2,j*2),color)
            image.set_at(((i*2)-1,(j*2)),color)
    return image

def sig(x,dx=False):
    if dx == True:
        return (x*(1-x))
    else:
        return (1/(1+np.exp(-x)))
    
temp = []
temp_two = []

for i in range(1,9):
    name = "test" + str(i) + str(".png")
    image = pygame.image.load(name)
    temp.append(make_linear(image))

for i in range(1,9):
    name = "result" + str(i) + str(".png")
    image = pygame.image.load(name)
    temp_two.append(make_linear(image))

X = np.array(temp)
Y = np.array(temp_two)

np.random.seed(1)

w0 = 2*np.random.random((2500,2500)) -1
w1 = 2*np.random.random((2500,2500)) -1
w2 = 2*np.random.random((2500,2500)) -1

for z in range(1000):
    l0 = X
    l1 = sig(np.dot(l0,w0))
    l2 = sig(np.dot(l1,w1))
    l3 = sig(np.dot(l2,w2))

    l3_error = Y - l3
    if z % 100 == 0:
        print("l3 error progress: " + str(np.mean(np.abs(l3_error))))
    l3_delta = l3_error * sig(l3,dx = True)

    l2_error = l3_delta.dot(w2.T) #w2.T ?
    l2_delta = l2_error*sig(l2, dx=True)

    l1_error = l2_delta.dot(w1.T)
    l1_delta = l1_error*sig(l2, dx=True)

    w2 += l2.T.dot(l3_delta)
    w1 += l1.T.dot(l2_delta)
    w0 += l0.T.dot(l1_delta)

print("l3 error after training: " + str(np.mean(np.abs(l3_error))))
temp = []
temp.append(make_linear(pygame.image.load("test1.png")))
X = np.array(temp)
result = pygame.image.load("result1.png")

l0 = X
l1 = sig(np.dot(l0,w0))
l2 = sig(np.dot(l1,w1))
l3 = sig(np.dot(l2,w2))

imageFinal = undo_linear(l3)
render(imageFinal,0,0,100,100)
render(result,100,0,100,100)
pygame.display.update()

