import tkinter as ttk
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter import scrolledtext
import BrownBag  as brownBag

class introWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Introductory")

        #sets dimensions of the window being created
        self.root.geometry('1200x400')

        mes = "Hello\nWelcome to my program\nIn this program you will be:\n1: Inputting names\n2: Determing whether you want the pairs or not.\nThe program pairs up everyone in the list.\nThey will never be paired up with each other in the future if using the same list"
        self.introText = ttk.Label(self.root,text=mes,font=('Arial',24))
        self.introText.place(relx=.5, x=-(self.introText.winfo_reqwidth()/2))

        #the button to move on to the next window
        self.continueButton = ttk.Button(self.root,text="Continue", command=lambda:[self.root.destroy(),self.nextWindow()])
        self.continueButton.place(relx=.5, x=-(self.continueButton.winfo_reqwidth()/2),
                                y=self.introText.winfo_reqheight()+5)

        self.quitButton = ttk.Button(self.root,text="Quit", command=quit)
        self.quitButton.place(relx=.5, x=-(self.continueButton.winfo_reqwidth()/2)+(self.quitButton.winfo_reqwidth()/2)-4,
                                y=self.introText.winfo_reqheight()+self.continueButton.winfo_reqheight()+5)
        
        self.root.mainloop()
    
    def nextWindow(self):
        introWindow2()

class introWindow2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("List of Names")
        self.root.geometry('400x400')

        #read the namelist file to display for the user
        f = open("namesList.txt","r")
        nameFile = f.readlines()
        f.close()

        self.text = scrolledtext.ScrolledText(self.root,height=len(nameFile),width=25)
        for x in nameFile:
            self.text.insert('end', x)
        self.text.config(state='disabled')
        self.text.place(relx=.5, anchor='n')

        self.useListLabel = ttk.Label(self.root,text="Use the same list from the previous use?")
        self.useListLabel.place(relx=.5, x=-(self.text.winfo_reqwidth()/2)-12,
                                y=self.text.winfo_reqheight())

        self.yesButton = ttk.Button(self.root,text="Yes", command=lambda:[self.root.destroy(),self.outputWindow()])
        self.yesButton.place(relx=.5,x=-(self.text.winfo_reqwidth()/4),
                             y=self.text.winfo_reqheight()+self.useListLabel.winfo_reqheight())

        self.noButton = ttk.Button(self.root,text="No", command=lambda:[self.root.destroy(),inputWindow()])
        self.noButton.place(relx=.5,x=-(self.text.winfo_reqwidth()/4)+(self.yesButton.winfo_reqwidth()),
                            y=self.text.winfo_reqheight()+self.useListLabel.winfo_reqheight())
        
        self.root.mainloop()
    
    def nextWindow(self):
        inputWindow()
    
    def outputWindow(self):
        brownBag.fileToCode("BrownBag.txt", brownBag.nodeList)
        outputWindow()
    
class inputWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Input Window")
        self.root.geometry('400x400')

        self.instrLabel = tk.Label(self.root, text="When inputting a new list of names, each line is a name")
        self.instrLabel.place(relx=.5,x=-self.instrLabel.winfo_reqwidth()/2)

        self.inputText = scrolledtext.ScrolledText(self.root,height=10,width=25)
        self.inputText.place(relx=.5,x=-(self.inputText.winfo_reqwidth()/2),
                            y=self.instrLabel.winfo_reqheight())
        self.inputText.config(state='normal')

        self.doneButton = ttk.Button(self.root,text="Done",command=lambda:self.confirmation())
        self.doneButton.place(relx=.5,x=-(self.doneButton.winfo_reqwidth()/2),
                              y=self.inputText.winfo_reqheight()+self.instrLabel.winfo_reqheight())

        self.root.mainloop()
    
    def getInput(self):
        nameListFile = open("namesList.txt","w")

        val = self.inputText.get("1.0",'end-1c')
        print(val)
        nameListFile.write(val)
        print("Retrieving Done")

        nameListFile.close()

    def confirmation(self):
        answer = askyesno(title="Confirmation",message="Are you sure this list is correct?")
        if answer:
            self.getInput()
            self.root.destroy()
            outputWindow()

class outputWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pairs")
        self.root.geometry("800x600")

        brownBag.pairUp()
        self.pairsLabel = tk.Label(self.root, text=brownBag.returnPairing(brownBag.pairings),width=50,justify='left',font=('Arial',32))
        self.pairsLabel.place(relx=.5, x = -self.pairsLabel.winfo_reqwidth()/2)

        self.confirmationLabely = self.pairsLabel.winfo_reqheight()+10
        self.confirmationLabel = tk.Label(self.root, text="Are these pairings fine?",font=('Arial',32))
        self.confirmationLabel.place(relx=.5, x = -self.confirmationLabel.winfo_reqwidth()/2,
                                    y = self.confirmationLabely)
 
        self.noButton = tk.Button(self.root, text = "No", command=lambda:[self.redoPairings()],font=('Arial',24),anchor='c')
        self.noButton.place(relx=.5,x=+self.noButton.winfo_reqwidth()/2,
                            y=self.confirmationLabel.winfo_reqheight()+self.confirmationLabely)

        self.yesButton = tk.Button(self.root, text = "Yes",command=lambda:[self.finishPairings()],font=('Arial',24),anchor='c')
        self.yesButton.place(relx=.5,x=-self.yesButton.winfo_reqwidth()/2 - self.noButton.winfo_reqwidth(),
                            y=self.confirmationLabel.winfo_reqheight()+self.confirmationLabely)
            
    def redoPairings(self):
        brownBag.createDrawList("namesList.txt",brownBag.drawList)
        brownBag.pairings = []
        brownBag.pairUp()

        self.pairsLabel = tk.Label(self.root, text=brownBag.returnPairing(brownBag.pairings),width=50,justify='left',font=('Arial',32))
        self.pairsLabel.place(relx=.5, x = -self.pairsLabel.winfo_reqwidth()/2)

        self.root.update()
    
    def finishPairings(self):
        self.root.destroy()
        for rowIndex in range(0, len(brownBag.pairings)):
                brownBag.pairings[rowIndex][0].hungOut(brownBag.pairings[rowIndex][1])
                if len(brownBag.pairings[rowIndex]) > 2:
                    brownBag.pairings[rowIndex][0].hungOut(brownBag.pairings[rowIndex][2])
                    brownBag.pairings[rowIndex][1].hungOut(brownBag.pairings[rowIndex][2])

        brownBag.codeToFile("BrownBag.txt", brownBag.nodeList)

if __name__ == "__main__":
    introWindow()
