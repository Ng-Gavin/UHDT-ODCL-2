from Close_Enough_Test_Cases_Test import Target, Payload, compare, order_payloads

#Payload 1 Info
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
    print(f'shape:{objectList[i].shape}, Shape Color: {objectList[i].shapeColor}, Alphnum Color: {objectList[i].alphanumColor}, Alphnum: {objectList[i].alphanum}\n')


targets = []
targets.append(Target('triangle', 10, 9, 'WHITE', 'ORANGE', 'y'))
targets.append(Target('circle', 9, 8, 'RED', 'YELLOW', 'no'))
targets.append(Target('square', 9, 9, 'GREEN', 'PURPLE', 'z'))
targets.append(Target('rectangle', 9, 8, 'WHITE', 'BROWN', '8'))
targets.append(Target('cross', 9, 9, 'PURPLE', 'WHITE', '20'))

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
print("Ordered Loads:")
for i in range(len(ordered_loads)):
    printObjectValues(ordered_loads)
print("Assigned payload values:")
for i in range(len(payloads)):
    print(f'P{i+1}:', end=' ')
    printObjectValues(payloads)

