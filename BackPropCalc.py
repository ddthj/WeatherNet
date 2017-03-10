import random
inputs = []
outputs = []

for i in range(3200):
    inputs.append(random.randint(-5,5))


realSum = float(sum(inputs))
targetSum = 5.0

error = (abs(realSum)-abs(targetSum)) / 3200
print(realSum)
print(error)


    
for item in inputs:
    if realSum < targetSum:
        pass
    else:
        pass
        
