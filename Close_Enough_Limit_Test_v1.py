from Close_Enough_Test_Cases_Test import Target, Payload, compare, order_payloads

#TODO Create random number gen to assign payload info

#Payload 1 Info (The Givens)
dock1 = 1
shape1 = "SEMICIRCLE"
shapeColor1 = "PURPLE"
alphanumColor1 = "BROWN"
alphanum1 = "4"

#Payload 2 Info
dock2 = 2
shape2 = "TRIANGLE"
shapeColor2 = "BLUE" 
alphanumColor2 = "ORANGE"
alphanum2 = "M"

#Payload 3 Info
dock3 = 3
shape3 = "STAR"
shapeColor3 = "WHITE" 
alphanumColor3 = "RED"
alphanum3 = "Q"

#Payload 4 Info
dock4 = 4
shape4 = "PENTAGON"
shapeColor4 = "YELLOW" 
alphanumColor4 = "GREEN"
alphanum4 = "C"

#Payload 5 Info
dock5 = 5
shape5 = ""
shapeColor5 = "" 
alphanumColor5 = ""
alphanum5 = ""

def printObjectValues(objectList):
    return f'Dock: {objectList[i].dock}, Shape:{objectList[i].shape}, Shape Color: {objectList[i].shapeColor}, Alphnum Color: {objectList[i].alphanumColor}, Alphnum: {objectList[i].alphanum}'

def matchCheck(objectList1,objectList2):
    print(f'Dock Matched: {objectList1[i].dock == objectList2[i].dock}')
    print(f'Shape Matched: {objectList1[i].shape == objectList2[i].shape}')
    print(f'Shape Color Matched: {objectList1[i].shapeColor == objectList2[i].shapeColor}')
    print(f'Alphnum Color Matched: {objectList1[i].alphanumColor == objectList2[i].alphanumColor}')
    print(f'Alphnum Matched: {objectList1[i].alphanum == objectList2[i].alphanum}\n')
    

#TODO Create random a gen for "detected" target attributes, run through comparison/test cases n amount of times.

targets = []
targets.append(Target('SEMICIRCLE', 10, 9, 'BROWN', 'ORANGE', '3',3))
targets.append(Target('SQUARE', 10, 9, 'PURPLE', 'ORANGE', '7',1))
targets.append(Target('CIRCLE', 10, 9, 'WHITE', 'PURPLE', 'K',4))
targets.append(Target('RECTANGLE', 10, 9, 'BLUE', 'YELLOW', 'D',2))

payloads = []
payloads.append(Payload(dock1, shape1,shapeColor1, alphanumColor1, alphanum1))
payloads.append(Payload(dock2, shape2,shapeColor2, alphanumColor2, alphanum2))
payloads.append(Payload(dock3, shape3,shapeColor3, alphanumColor3, alphanum3))
payloads.append(Payload(dock4, shape4,shapeColor4, alphanumColor4, alphanum4))


ordered_loads = order_payloads(targets,payloads)

for i in range(len(ordered_loads)):
    print("Given: ",printObjectValues(payloads))
    print("Ordered: ",printObjectValues(ordered_loads),"\n")
    matchCheck(ordered_loads,payloads)

'''
for item in range(len(targets)):
    print(payloads[item],ordered_loads[item])
    print(compare(payloads[item],ordered_loads[item]))
print("")
'''
