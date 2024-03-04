from Close_Enough_Test_Cases_Test import Target, Payload, compare, order_payloads

#Payload 1 Info
dock1 = 1
shape1 = ""
shapeColor1 = "" 
alphanumColor1 = ""
alphanum1 = ""

#Payload 2 Info
dock2 = 2
shape2 = ""
shapeColor2 = "" 
alphanumColor2 = ""
alphanum2 = ""

#Payload 3 Info
dock3 = 3
shape3 = ""
shapeColor3 = "" 
alphanumColor3 = ""
alphanum3 = ""

#Payload 4 Info
dock4 = 4
shape4 = ""
shapeColor4 = "" 
alphanumColor4 = ""
alphanum4 = ""

#Payload 5 Info
dock5 = 5
shape5 = ""
shapeColor5 = "" 
alphanumColor5 = ""
alphanum5 = ""




targets = []
targets.append(Target('triangle', 10, 9, 'no', 'mbrah', 'y'))
targets.append(Target('circle', 9, 8, 'no', 'mbrah', 'no'))
targets.append(Target('square', 9, 9, 'no', 'mbrah', 'z'))
targets.append(Target('rectangle', 9, 8, 'no', 'mbrah', '8'))
targets.append(Target('cross', 9, 9, 'no', 'mbrah', '20'))

payloads = []
payloads.append(Payload(1, shape1,shapeColor1, alphanumColor1, alphanum1))
payloads.append(Payload(2, shape2,shapeColor2, alphanumColor2, alphanum2))
payloads.append(Payload(3, shape3,shapeColor3, alphanumColor3, alphanum3))
payloads.append(Payload(4, shape4,shapeColor4, alphanumColor4, alphanum4))
payloads.append(Payload(5, shape5,shapeColor5, alphanumColor5, alphanum5))

for item in range(len(targets)):
    print(compare(payloads[item],targets[item]))
'''
ordered_payloads = order_payloads(targets,payloads)
for i in range(len(ordered_payloads)):
    print(ordered_payloads[i])
'''