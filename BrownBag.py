import random
class Node:
    def __init__(self, name):
        self.name = name
        self.nameList = []
        self.bool = []
    
    def addName(self, obj):
        self.nameList.append(obj)
        self.bool.append("0")

    def setNameList(self,list):
        self.nameList = list

    def hungOutBefore(self,name):
        i = self.nameList.index(name)
        if self.bool[i] == 1:
            return True
        else:
            return False

    def hungOut(self,name):
        i = self.nameList.index(name)
        if(self.hungOutBefore(name)):
            print("The pair has already hung out before")
        else:
            self.bool[i] = 1 #this means that the person has hung out with the person being inputted

    def hungOut2(self,name1,name2):
        i = self.nameList.index(name1)
        j = self.nameList.index(name2)
        if self.hungOutBefore(name1) and self.hungOutBefore(name2):
            print("A pair has already hung out before")
        else:
            self.bool[i] = 1 #this means that the person has hung out with the person being inputted
            self.bool[j] = 1

def getPersonInList(nodeList, name):
    #wrose
    for person in nodeList:
        if person.name == name:
            return person

#as the method says, this transfers all the items in the file to be able to use in the code later following how BrownBag.txt looks
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

def codeToFile(file, nameNodeList):
    f = open(file, "w")
    for x in nameNodeList:
        f.write(x.name + "\n")
        f.write(", ".join(x.nameList))
        f.write("\n")
        f.write(", ".join(map(str,x.bool)))
        f.write("\n\n")
    f.close()

nodeList = list()
drawList = list()
f = open("namesList.txt","r")
file = f.readlines()
f.close()

#this adds the names from the name list file into a list for the code to go through
for x in file:
    name = Node(x.strip("\n"))
    drawList.append(x.strip("\n"))
    nodeList.append(name)

#once the names are added into the lists, the node list then has a list of the names other than themselves
#also has a list of boolean values to determine if they have hung out with each other
for x in nodeList:
        for y in file:
            if y.strip("\n") != x.name.strip("\n"):
                x.addName(y.strip("\n"))

yn = input ("Is this the same list of names? \nThis modifies the BrownBag file and losing whatever list you had before if it's a new list (Y/N) ")
if yn.lower() == "n":
    f = open("BrownBag.txt", "w")
    #this writes each section into the file (each section is each object from list)
    for x in nodeList:
        f.write(x.name + "\n")
        f.write(", ".join(x.nameList))
        f.write("\n")
        f.write(", ".join(x.bool))
        f.write("\n\n")
    f.close()
else:
    fileToCode("BrownBag.txt", nodeList)

#both persons need to go to node and their nameList to find name then set the index of bool = 1
#this pairs them up regardless of they hung out or not
a = 0
ranInt = random.randrange(1,int(len(drawList)/2))
while a < int(len(nodeList)/2):
    a += 1
    person1 = random.choice(drawList)
    person1Node = getPersonInList(nodeList, person1)
    if person1 in drawList:
        drawList.remove(person1)

    #this randomly chooses a second person
    while True:
        person2 = random.choice(drawList)
        person2Node = getPersonInList(nodeList, person2)
        if not person1Node.hungOutBefore(person2) and not person2Node.hungOutBefore(person1):
            drawList.remove(person2)
            print(a, end = ": ")
            print(person1Node.name, end = ": ")

            #this chooses a third person for a random group as long as the amount of people is odd
            if a == ranInt and len(nodeList) % 2 == 1:
                print(person2, end =", ")
                while True:
                    person3 = random.choice(drawList)
                    person3Node = getPersonInList(nodeList, person3)
                    if not person1Node.hungOutBefore(person3) and not person2Node.hungOutBefore(person3) and not person3Node.hungOutBefore(person1) and not person3Node.hungOutBefore(person2):
                        drawList.remove(person3)
                        person1Node.hungOut(person3)
                        person2Node.hungOut(person3)
                        person3Node.hungOut2(person1,person2)
                        break
                print(person3)
            else:
                print(person2)
            break
    
    person1Node.hungOut(person2)
    person2Node.hungOut(person1)
    if(len(drawList) <= 0):
        break

#this code to file will always be at the end to modify the file
codeToFile("BrownBag.txt", nodeList)
