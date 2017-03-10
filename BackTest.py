import random
list_size = random.choice([1600, 3200])
'''
if list_size == 1600:
    total = random.uniform(8000, -8000)
else:
    total = random.uniform(16000, -16000)
'''
total = 5
lst = []
for i in range(0, list_size):
    lst.append(random.uniform(-5, 5))

current_list_sum = sum(lst)

diff = total - current_list_sum

currentaverage = current_list_sum/list_size

wantedaverage = total/list_size

avgdiff = wantedaverage-currentaverage

for i in range(0, list_size):
    lst[i] = lst[i] + avgdiff
    lst[i] += (1/3) * (lst[i] - wantedaverage)
