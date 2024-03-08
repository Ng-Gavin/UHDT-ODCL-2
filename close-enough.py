import math


class Target:
    def __init__(self, shape, latitude, longitude, shapeColor, alphanumColor, alphanum, dock=0):
        self.shape = shape
        self.latitude = latitude
        self.longitude = longitude
        self.shapeColor = shapeColor
        self.alphanumColor = alphanumColor
        self.alphanum = alphanum


class Payload:
    def __init__(self, dock, shape, shapeColor, alphanumColor, alphanum):
        self.dock = dock
        self.shape = shape
        self.shapeColor = shapeColor
        self.alphanumColor = alphanumColor
        self.alphanum = alphanum


def compare(payload, target):
    error1 = ["RED", "ORANGE", "YELLOW"]
    error2 = ["WHITE", "GRAY"]
    error3 = ["PURPLE", "GRAY"]
    error4 = ["BROWN", "ORANGE"]
    arr1 = ['I', 'L']
    arr4 = ['M', 'E', 'K', 'H', '3']
    arr6 = ['9']
    arrC = ['U']
    arrG = ['C']
    arrJ = ['1', 'U', 'L']
    arrK = ['V']
    arrM = ['W', 'N']
    arrO = ['0']
    arrQ = ['D', '0']
    arrS = ['5']
    arrT = ['1']
    arrV = ['U']

    score = 0;
    if payload.shape == target.shape:
        score += 1

    if payload.shapeColor == target.shapeColor:
        score += 1
    elif any(target.shapeColor == match for match in error1) and any(payload.shapeColor == match for match in error1):
        score += 0.5
    elif any(target.shapeColor == match for match in error2) and any(payload.shapeColor == match for match in error2):
        score += 0.5
    elif any(target.shapeColor == match for match in error3) and any(payload.shapeColor == match for match in error3):
        score += 0.5
    elif any(target.shapeColor == match for match in error4) and any(payload.shapeColor == match for match in error4):
        score += 0.5
    else:
        if payload.shapeColor == target.alphanumColor or payload.alphanumColor == target.shapeColor:
            score += 0.5
        elif any(target.shapeColor == match for match in error1) and any(
                payload.alphanumColor == match for match in error1):
            score += 0.5
        elif any(target.shapeColor == match for match in error2) and any(
                payload.alphanumColor == match for match in error2):
            score += 0.5
        elif any(target.shapeColor == match for match in error3) and any(
                payload.alphanumColor == match for match in error3):
            score += 0.5
        elif any(target.shapeColor == match for match in error4) and any(
                payload.alphanumColor == match for match in error4):
            score += 0.5

    if payload.alphanumColor == target.alphanumColor:
        score += 1
    elif any(target.alphanumColor == match for match in error1) and any(
            payload.alphanumColor == match for match in error1):
        score += 0.5
    elif any(target.alphanumColor == match for match in error2) and any(
            payload.alphanumColor == match for match in error2):
        score += 0.5
    elif any(target.alphanumColor == match for match in error3) and any(
            payload.alphanumColor == match for match in error3):
        score += 0.5
    elif any(target.alphanumColor == match for match in error4) and any(
            payload.alphanumColor == match for match in error4):
        score += 0.5
    else:
        if payload.shapeColor == target.alphanumColor or payload.alphanumColor == target.shapeColor:
            score += 0.5
        elif any(target.alphanumColor == match for match in error1) and any(
                payload.shapeColor == match for match in error1):
            score += 0.5
        elif any(target.alphanumColor == match for match in error2) and any(
                payload.shapeColor == match for match in error2):
            score += 0.5
        elif any(target.alphanumColor == match for match in error3) and any(
                payload.shapeColor == match for match in error3):
            score += 0.5
        elif any(target.alphanumColor == match for match in error4) and any(
                payload.shapeColor == match for match in error4):
            score += 0.5

    if payload.alphanum == target.alphanum:
        score += 1
    elif any(char == payload.alphanum for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == '1' and any(char in arr1 for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == '4' and any(char in arr4 for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == '6' and any(char in arr6 for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'C' and any(char in arrC for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'G' and any(char in arrG for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'J' and any(char in arrJ for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'K' and any(char in arrK for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'M' and any(char in arrM for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'O' and any(char in arrO for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'Q' and any(char in arrQ for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'S' and any(char in arrS for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'T' and any(char in arrT for char in target.alphanum):
        score += 0.5
    elif payload.alphanum == 'V' and any(char in arrV for char in target.alphanum):
        score += 0.5

    return score


# targets = []
# targets.append(Target('mbruh', 10, 9, 'no', 'mbrah', 'y'))
# targets.append(Target('mbruh', 9, 8, 'no', 'mbrah', 'no'))
# targets.append(Target('mbruh', 9, 9, 'no', 'mbrah', 'z'))
# targets.append(Target('mbruh', 9, 8, 'no', 'mbrah', '8'))
# targets.append(Target('mbruh', 9, 9, 'no', 'mbrah', '20'))

# payloads = []
# payloads.append(Payload(1, 'mbruh','no', 'mbrah', 'no'))
# payloads.append(Payload(2, 'mbruh', 'no', 'mbrah', 'y'))
# payloads.append(Payload(3, 'mbruh','no', 'mbrah', '8'))
# payloads.append(Payload(4, 'mbruh', 'no', 'mbrah', 'z'))
# payloads.append(Payload(5, 'mbruh','no', 'mbrah', 'z'))


# def calculate_dist(drone_lat, drone_lon, target_lat, target_lon):
#    dLat = (target_lat-drone_lat) * math.pi / 180
#    dLon = (target_lon-drone_lon)*math.pi/180
#    lat1 = drone_lat * math.pi / 180
#    lat2 = target_lat * math.pi / 180
#    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
#    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#    return c

# test_targets = [{'latitude': 1, 'longitude': 1}, {'latitude': 3, 'longitude': 3}, {'latitude': 2, 'longitude': 2}, {'latitude': 5, 'longitude': 5}, {'latitude': 4, 'longitude': 4}]

# def sort_targets(targets, drone_lat, drone_lon):
#    sorted_targets = []
#    target_order = [];
#    for i in range(len(targets)):
#        target_lat = targets[i]['latitude']
#        target_lon = targets[i]['longitude']
#        target_distance = calculate_dist(drone_lat, drone_lon, target_lat, target_lon);
#        target_order.append([target_distance, i])
#    target_order.sort()
#    for order in target_order:
#        index = order[1]
#        sorted_targets.append(targets[index])
#
#    return sorted_targets

# print(targets)
# print(sort_targets(test_targets, 6, 6))


def order_payloads(payloads, targets):
    payload_order = []
    target_scores = []
    hasConflicts = False
    unassigned_targets = []
    unassigned_payloads = [0, 1, 2, 3]  # removed 4 (or 5th element) for testing purposes.
    ordered_payloads = []

    # For each target, compare to all the payloads, generate a similarity score for each payload
    for target in targets:
        payload_scores = []
        for payload in payloads:
            payload_score = compare(payload, target)
            payload_scores.append(payload_score)
        target_scores.append(payload_scores)
    # Take the highest payload score's index for each target
    print("target scores: ", target_scores)
    print("payload scores: ", payload_scores)
    for payload_scores in target_scores:
        payload_order.append(payload_scores.index(max(payload_scores)))

    for index in payload_order:
        if payload_order.count(index) > 1:
            hasConflicts = True
        else:
            hasConflicts = False

    if hasConflicts:
        for i in range(len(payload_order)):
            if payload_order.count(payload_order[i]) != 1:
                unassigned_targets.append(i)
            if payload_order.count(payload_order[i]) == 1:
                unassigned_payloads.remove(payload_order[i])
            for j in range(len(unassigned_targets)):
                payload_order[unassigned_targets[j]] = unassigned_payloads[j]
        for payload_index in payload_order:
            ordered_payloads.append(payloads[payload_index])
    else:
        for payload_index in payload_order:
            ordered_payloads.append(payloads[payload_index])
    return ordered_payloads
# TODO Create random number gen to assign payload info

# Payload 1 Info (The Givens)
dock1 = 0
shape1 = "SEMICIRCLE"
shapeColor1 = "PURPLE"
alphanumColor1 = "BROWN"
alphanum1 = "4"

# Payload 2 Info
dock2 = 1
shape2 = "TRIANGLE"
shapeColor2 = "BLUE"
alphanumColor2 = "ORANGE"
alphanum2 = "M"

# Payload 3 Info
dock3 = 2
shape3 = "STAR"
shapeColor3 = "WHITE"
alphanumColor3 = "RED"
alphanum3 = "Q"

# Payload 4 Info
dock4 = 3
shape4 = "PENTAGON"
shapeColor4 = "YELLOW"
alphanumColor4 = "GREEN"
alphanum4 = "C"

# Payload 5 Info
dock5 = 4
shape5 = ""
shapeColor5 = ""
alphanumColor5 = ""
alphanum5 = ""


def printObjectValues(objectList):
    return f'Dock: {objectList[i].dock}, Shape:{objectList[i].shape}, Shape Color: {objectList[i].shapeColor}, Alphnum Color: {objectList[i].alphanumColor}, Alphnum: {objectList[i].alphanum}'


def matchCheck(objectList1, objectList2):
    print(f'Shape Matched: {objectList1[i].shape == objectList2[i].shape}')
    print(f'Shape Color Matched: {objectList1[i].shapeColor == objectList2[i].shapeColor}')
    print(f'Alphnum Color Matched: {objectList1[i].alphanumColor == objectList2[i].alphanumColor}')
    print(f'Alphnum Matched: {objectList1[i].alphanum == objectList2[i].alphanum}\n')


# TODO Create random a gen for "detected" target attributes, run through comparison/test cases n amount of times.

targets = []
targets.append(Target('RECTANGLE', 10, 9, 'BLUE', 'YELLOW', 'D'))
targets.append(Target('SEMICIRCLE', 10, 9, 'BROWN', 'ORANGE', '3'))
targets.append(Target('CIRCLE', 10, 9, 'WHITE', 'PURPLE', 'K'))
targets.append(Target('SQUARE', 10, 9, 'PURPLE', 'ORANGE', '7',))


payloads = []
payloads.append(Payload(0, 'SEMICIRCLE', 'BROWN', 'ORANGE', '3'))
payloads.append(Payload(1, 'SQUARE', 'WHITE', 'ORANGE', '7'))
payloads.append(Payload(2, 'CIRCLE', 'PURPLE', 'PURPLE', 'K'))
payloads.append(Payload(3, 'RECTANGLE', 'BLUE', 'YELLOW', 'D'))

ordered_loads = order_payloads(payloads, targets)


#for i in range(len(ordered_loads)):
#    print("Given: ", printObjectValues(payloads))
#    print("Ordered: ", printObjectValues(ordered_loads), "\n")
#    matchCheck(ordered_loads, targets)


print(ordered_loads)
for load in ordered_loads:
    print(load.shape)
    print(load.shapeColor)
    print(load.alphanumColor)
    print(load.alphanum)
    print(load.dock)

'''
for item in range(len(targets)):
    print(payloads[item],ordered_loads[item])
    print(compare(payloads[item],ordered_loads[item]))
print("")
'''