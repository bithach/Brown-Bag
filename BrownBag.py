import random
import PersonNode

def getPersonInNodeList(nodeList, name):
    for person in nodeList:
        if person.name == name:
            return person

def newNameList(fileName,nodeList):
    f = open(fileName, "w")
    #this writes each section into the file (each section is each object from list)
    for x in nodeList:
        f.write(x.name + "\n")
        f.write(", ".join(x.nameList))
        f.write("\n")
        f.write(", ".join(x.bool))
        f.write("\n\n")
    f.close()

def createDrawList(filename,drawList):
    f = open(filename,"r")
    file = f.readlines()
    f.close()

    for x in file:
        drawList.append(x.strip("\n"))

#as the method says, this transfers all the items in the file (specifically for the BrownBag file) to be able to use in the code later following how BrownBag.txt looks
def fileToCode(file, nameNodeList):
    f = open(file, "r")
    a = 0
    for line in f:
        if(nameNodeList[a].name == line.strip("\n")):
            #this changes the name list of the persons name
            nameList = next(f).strip("\n").split(", ")
            nameNodeList[a].nameList = nameList

            #this is to change the boolean list 
            boolList = next(f).strip("\n").split(", ")
            nameNodeList[a].bool = list(map(int, boolList))
            #skips empty line 
            next(f)
        a+=1

#goes through the list of name nodes that contain the name, the name list and the boolean list and writes them into the text file
def codeToFile(file, nameNodeList):
    f = open(file, "w")
    for x in nameNodeList:
        f.write(x.name + "\n")
        f.write(", ".join(x.nameList))
        f.write("\n")
        f.write(", ".join(map(str,x.bool)))
        f.write("\n\n")
    f.close()

def printPairings(pairingList):
    a = 0
    for row in pairingList:
        a += 1
        print(a, end = ": ")
        for col in row:
            print(col.name, end = " ")
        print()

def returnPairing(pairingList):
    pairings = ""
    a = 0
    for row in pairingList:
        a += 1
        pairings += str(a) + ": "
        for col in row:
            pairings += col.name + ", "
        pairings = pairings[:-2]
        pairings += "\n"
    return pairings[:-1]

#both persons need to go to node and their nameList to find name then set the index of bool = 1
def pairUp():
    a = 0
    ranInt = random.randrange(1,int(len(drawList)/2))
    while a < int(len(nodeList)/2):
        a+=1
        person1 = random.choice(drawList)
        person1Node = getPersonInNodeList(nodeList, person1)
        if person1 in drawList:
            pairings.append([person1Node])
            drawList.remove(person1)
        
        b = 0
        #this randomly chooses a second person
        while True:
            person2 = random.choice(drawList)
            person2Node = getPersonInNodeList(nodeList, person2)
            if not person1Node.hungOutBefore(person2Node) and not person2Node.hungOutBefore(person1Node):
                pairings[a-1].append(person2Node)
                drawList.remove(person2)

                #this chooses a third person for a random group as long as the amount of people is odd
                #also the 3rd person goes into a random group
                if a == ranInt and len(nodeList) % 2 == 1:
                    while True:
                        person3 = random.choice(drawList)
                        person3Node = getPersonInNodeList(nodeList, person3)
                        if not person1Node.hungOutBefore(person3Node) and not person3Node.hungOutBefore(person1Node) and not person2Node.hungOutBefore(person3Node) and not person3Node.hungOutBefore(person2Node):
                            pairings[a-1].append(person3Node) 
                            drawList.remove(person3)
                            break
                break

            #prevents infinite looping problems (case where the remaining people have hung out with each other already)
            #make remaining people pair up
            b+=1
            if b > len(drawList):
                pairings[a-1].append(person2Node)
                drawList.remove(person2)
                break

        if(len(drawList) <= 0):
            break

#-----------Variables--------------------
pairings = []
nodeList = list()
drawList = list()
#----------------------------------------

f = open("namesList.txt","r")
nameFile = f.readlines() #list of names from file
f.close()

#this adds the names from the name list file into a list for the code to go through
for x in nameFile:
    name = PersonNode.Person(x.strip("\n"))
    drawList.append(x.strip("\n"))
    nodeList.append(name)

#once the names are added into the lists, the node list then has a list of the names other than themselves
#also has a list of boolean values to determine if they have hung out with each other
#This has a runtime of O(N^2) - goes through the len(nodeList) then len(nodeList)-1 -> O(N(N-1))
for x in nodeList:
    for y in nameFile:
        if y.strip("\n") != x.name.strip("\n"):
            x.addName(y.strip("\n"))

if __name__ == "__main__":

    yn = input ("Is this the same list of names? \nThis modifies the BrownBag file and losing whatever list you had before if it's a new list (Y/N) ")
    if yn.lower() == "n":
        #this writes each section into the file (each section is each object from list)
        newNameList("BrownBag.txt",nodeList)
    else:
        fileToCode("BrownBag.txt", nodeList)

    while True:
        pairings = []
        pairUp()
        printPairings(pairings)
        yn = input("Are these pairings fine? (Y/N) ")
        if yn.lower() == "y":
            for rowIndex in range(0, len(pairings)):
                pairings[rowIndex][0].hungOut(pairings[rowIndex][1])
                if len(pairings[rowIndex]) > 2:
                    pairings[rowIndex][0].hungOut(pairings[rowIndex][2])
                    pairings[rowIndex][1].hungOut(pairings[rowIndex][2])
            codeToFile("BrownBag.txt", nodeList)
            break
        else:
            createDrawList("namesList.txt",drawList)
    #this code to file will always be at the end to modify the file