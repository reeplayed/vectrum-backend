import random 

all = []

for i in range(0,10):
  for j in range(0,10):
    all.append([i,j])

statki = [5, 4, 3, 2]

r = random.choice(all)
print(r)

find = False
i =0
while not find:
    if i == 2:
        find = True
    print(i)    
    i =+ 1