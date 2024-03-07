from Close_Enough_Test_Cases_Test import Target, Payload, compare, order_payloads

#TODO Create pools of possible competition attributes
possibleColors = []
possibleAlphnum = []
possibleShapes = []

#TODO Create random number gen to assign payload info

#Payload 1 Info (The Givens)
dock1 = 1
shape1 = "circle"
shapeColor1 = "GRAY"
alphanumColor1 = "ORANGE"
alphanum1 = "y"

#Payload 2 Info
dock2 = 2
shape2 = "circle"
shapeColor2 = "RED" 
alphanumColor2 = "YELLOW"
alphanum2 = "no"

#Payload 3 Info
dock3 = 3
shape3 = "circle"
shapeColor3 = "GREEN" 
alphanumColor3 = "PURPLE"
alphanum3 = "z"

#Payload 4 Info
dock4 = 4
shape4 = "rectangle"
shapeColor4 = "WHITE" 
alphanumColor4 = "BROWN"
alphanum4 = "8"

#Payload 5 Info
dock5 = 5
shape5 = "cross"
shapeColor5 = "PURPLE" 
alphanumColor5 = "WHITE"
alphanum5 = "20"

def printObjectValues(objectList):
    print(f'Dock: {objectList[i].dock}, Shape:{objectList[i].shape}, Shape Color: {objectList[i].shapeColor}, Alphnum Color: {objectList[i].alphanumColor}, Alphnum: {objectList[i].alphanum}')

def matchCheck(objectList1,objectList2):
    print(f'Dock Matched: {objectList1[i].dock == objectList2[i].dock}')
    print(f'Shape Matched: {objectList1[i].shape == objectList2[i].shape}')
    print(f'Shape Color Matched: {objectList1[i].shapeColor == objectList2[i].shapeColor}')
    print(f'Alphnum Color Matched: {objectList1[i].alphanumColor == objectList2[i].alphanumColor}')
    print(f'Alphnum Matched: {objectList1[i].alphanum == objectList2[i].alphanum}\n')

#TODO Create random a gen for "detected" target attributes, run through comparison/test cases n amount of times.

targets = []
targets.append(Target(1,'square', 10, 9, 'WHITE', 'ORANGE', 'y'))
targets.append(Target(2,'square', 9, 8, 'RED', 'YELLOW', 'D'))
targets.append(Target(3,'square', 9, 9, 'GREEN', 'PURPLE', 'z'))
targets.append(Target(4,'cross', 9, 8, 'WHITE', 'BROWN', '8'))
targets.append(Target(5,'rectangle', 9, 9, 'YELLOW', 'WHITE', '20'))

payloads = []
payloads.append(Payload(1, shape1,shapeColor1, alphanumColor1, alphanum1))
payloads.append(Payload(2, shape2,shapeColor2, alphanumColor2, alphanum2))
payloads.append(Payload(3, shape3,shapeColor3, alphanumColor3, alphanum3))
payloads.append(Payload(4, shape4,shapeColor4, alphanumColor4, alphanum4))
payloads.append(Payload(5, shape5,shapeColor5, alphanumColor5, alphanum5))

for item in range(len(targets)):
    print(compare(payloads[item],targets[item]))
print("")

ordered_loads = order_payloads(targets,payloads)
print("Assigned payload values:")
for i in range(len(payloads)):
    #print(f'P{i+1}:', end=' ')
    printObjectValues(payloads)
    print("")

print("Ordered Loads:")
for i in range(len(ordered_loads)):
    printObjectValues(ordered_loads)
    matchCheck(ordered_loads,payloads)

