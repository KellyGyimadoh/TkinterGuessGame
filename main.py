from tkinter import *
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
import mysql.connector
from tkinter import END, IntVar, messagebox
import random
import sqlite3
try:
   # Connect to SQLite database (creates the file if it doesn't exist)
    mydb = sqlite3.connect('magicdb.sqlite3')  # Database will be in the same folder as your script
    cursor = mydb.cursor()
    print("SQLite connection successful")

    # Example of creating a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS game (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL DEFAULT 0
                      )''')
    mydb.commit()
except sqlite3.Error as e:
    print(f"Error connecting to SQLite: {e}")
# Global variables to keep track of guesses and score
user=""
gameGuesses = 4
Gamescore = 0
magicNumber = random.randint(1, 100)
Gameanswer=0
magicLevel=0
window= Tk() #instantiate instant of window
window.geometry("600x800")
window.title("Magic Guess Game")
window.config(bg="#f55714")


#window.config(background="white")
#window.iconphoto(True,icon)
#label
#db
def displayLeaderBoard():
    for widget in window.winfo_children():
        widget.pack_forget()  # Hide all widgets in the main window
    leaderBoardFrame.pack(fill="both", expand=True)  # Show the game frame
    try:
        mycursor=mydb.cursor()
        query="SELECT id,name, score FROM game"
        mycursor.execute(query)
        records=mycursor.fetchall()
        if not records:
            messagebox.showerror("Error", "No match found")
            return 
                # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)
        count=0
        for record in records:
            count+=1
            tree.insert('',END,text=record[0], values=(count,record[1],record[2],))
            
    except mysql.connector.Error as e:
            messagebox.showerror("Error",f"error :{e}")
    finally:
        mycursor.fetchall()
def quitGame():
    response = messagebox.askquestion("Quit Game?", "Do you want to quit?")
    if response == 'yes':
        window.destroy()
def showScoreBoard():   
    for widget in window.winfo_children():
        widget.pack_forget()  # Hide all widgets in the main window
    scoreFrame.pack(fill="both", expand=True)  # Show the game frame
def goToHomePage():
    # Hide the current game frame
    gameFrame.pack_forget()
    scoreFrame.pack_forget()
    leaderBoardFrame.pack_forget()
    
    # Show the main content (home page)
    mainlabel.pack()
    extralabel.pack(pady=15)
    usernamelabel.pack(pady=15)
    name_entry.pack(pady=10)
    start_button.pack(pady=15)

def generateMagicNumber():
    return random.randint(1,100)
def updateUserLabel():
    userlabel.config(text=f"Magician: {user}")  
def checkAnswer():
    """Check the user's answer against the magic number."""
    global gameGuesses, Gamescore, magicNumber,user,magicLevel

    """Check the user's answer against the magic number."""
    userAnswer = answerEntry.get()

    # Validate input
    if userAnswer == "":
        messagebox.showerror("Error", "Please enter a number")
        return  # Exit the function early if there's an error

    if not userAnswer.isdigit():
        messagebox.showerror("Error", "Please enter a valid number")
        return  # Exit the function early if there's an error

    userAnswer = int(userAnswer)  # Convert userAnswer to an integer for comparison

    # Check the user's guess
    if userAnswer > magicNumber:
        gameGuesses -= 1
        messagebox.showwarning("Getting there", f"The number you gave is more than the magic number..you have {gameGuesses} guesses left")
    elif userAnswer < magicNumber:
        gameGuesses -= 1
        messagebox.showwarning("Getting there", f"The number you gave is less than the magic number ..you have {gameGuesses} guesses left")
    elif userAnswer == magicNumber:
        Gamescore += 5
        magicLevel+=1
        
        messagebox.showinfo("Success", f"You won! Guess is {userAnswer} correct! Magic number is {magicNumber}..Your score is {Gamescore}")
        try:
            if user!="":
                mycursor=mydb.cursor()
                query="UPDATE game SET score= ? WHERE name= ?"
                val=(Gamescore,user)
                mycursor.execute(query,val)
                mydb.commit()
        except mysql.connector.Error as e:
            print(f"error :{e}")
            

        # Optionally reset the game here or provide a way to start over
         # Prompt to continue or reset
        if messagebox.askyesno("Continue", "Do you want to continue playing?"):
            gameGuesses = 5  # Reset guesses
            magicNumber = generateMagicNumber()  # Generate new magic number
            totalguessLabel.config(text=f"Guesses Left: {gameGuesses}")
            scorelabel.config(text=f"Score: {Gamescore}")
        else:
            startNewFrame()


   # Check if the user has run out of guesses
    if gameGuesses > 0:
        totalguessLabel.config(text=f"Guesses Left: {gameGuesses}")  # Update guesses left
    else:
        if messagebox.askretrycancel("Out of guesses", f"Magic Number is {magicNumber}.Dont give up! Do you want to play again?"):
            gameGuesses = 5  # Reset guesses for the new game
            magicNumber = generateMagicNumber()  # Generate a new magic number
            Gamescore = 0  # Reset score
            answerEntry.delete(0, END)  # Clear the entry
            totalguessLabel.config(text=f"Guesses Left: {gameGuesses}")
            scorelabel.config(text=f"Score: {Gamescore}")
        else:
            showScoreBoard()
            

def startNewFrame():
    """Raise the game frame to show the game content."""
    for widget in window.winfo_children():
        widget.pack_forget()  # Hide all widgets in the main window
    gameFrame.pack(fill="both", expand=True)  # Show the game frame


def startgame():
    global user
    username=name_entry.get()
    if(username==""):
        messagebox.showerror("Error","Please fill your name")
    elif(len(username) >=6):
        messagebox.showerror("Error","Please Enter name up to 5 characters")
    elif (searchUser(username)):
        user=username
        messagebox.showinfo("Success","Ready to Become the best magician ")
        updateUserLabel()
        startNewFrame()
    else:
        try:
            mycursor=mydb.cursor()
            query="INSERT INTO game (name) values(?)"
            val=(username,)
            mycursor.execute(query,val)
            mydb.commit()
            user=username
            messagebox.showinfo("Success","Ready to Become the best magician ")
            updateUserLabel()
            startNewFrame()

        except mysql.connector.Error as e:
            messagebox.showerror("Error",f"error adding user.. try again...:{e}")
def searchUser(userName):
        global user
        try:
            mycursor=mydb.cursor()
            query="SELECT name FROM game WHERE name=?"
            val=(userName,)
            mycursor.execute(query,val)
            record=mycursor.fetchone()
            
            if(record):
                user=record[0]
                return True
            else:
                return False

        except mysql.connector.Error as e:
            messagebox.showerror("Error",f"error adding user.. try again...:{e}")
            return False
        
        

mainlabel= Label(window,text="Realm Of Numbers",font=('Arial',40,'bold'),
             fg='yellow',bg='black',relief=RAISED,bd=10,padx=20,
             pady=20,compound='bottom')
mainlabel.pack()
extralabel= Label(window,text="Be a Magician! Guess the correct number",font=('Verdana',10,'bold'),
             fg='yellow',bg='black',relief=RAISED,bd=10,padx=20,
             pady=20,compound='bottom')
extralabel.pack(pady=15)
usernamelabel= Label(window,text="Enter Username",font=('Verdana',20,'bold'),
             fg='yellow',bg='black',relief=RAISED,bd=10,padx=20,
             pady=20,compound='bottom')
usernamelabel.pack(pady=15)
name_entry=Entry(window,font=('Verdana',40),bg="black", fg="yellow",)
name_entry.pack(pady=10)
# Ensure the cursor matches the text color
name_entry.configure(insertbackground='yellow')  # Change the insertion cursor color

start_button=Button(window,text="START GAME",font=("Verdana",30),bg="yellow",
                    activebackground="yellow",fg="red",activeforeground="red",command=startgame)
start_button.pack(pady=15)

board_button=Button(window,text="LEADERBOARD",font=("Verdana",30),bg="blue",
                    activebackground="yellow",fg="red",activeforeground="red",command=displayLeaderBoard)
board_button.pack(pady=15)




# Create the new game frame
gameFrame =Frame(window, bg="lightblue")


               # Add content to the game frame
game_label =Label(gameFrame, text="""🧙🧙Welcome to the Game!Welcome to the mysterious realm of numbers,
                    a land where numbers hold magical powers. The ancient numberian 
                    soccer has hidden a powerful number deep within the enchanted forest,
                    legend has it that whoever can guess this secret 
                    number will unlock unimaginable treasures and untold knowledge.🧹🧹🧹""", font=('Verdana', 13), bg="#b6f23f",fg="#f03316")
game_label.grid(row=0,column=1,columnspan=5,pady=30,padx=200)

userlabel=Label(gameFrame,text=f"🧝Magician:",font=("Verdana", 15))
userlabel.grid(row=3,column=1,padx=100)

magiclabel=Label(gameFrame,text=f"🔥🔥Magic Level: {magicLevel}",font=("Verdana", 15))
magiclabel.grid(row=3,column=2,padx=100)

scorelabel=Label(gameFrame,text=f"Score: {Gamescore}",font=("Verdana", 15))
scorelabel.grid(row=3,column=3,padx=100)

totalguessLabel=Label(gameFrame,text=f"Guesses Left: {gameGuesses}",font=("Verdana", 15))
totalguessLabel.grid(row=3,column=6,padx=10)

questionFrame=Frame(gameFrame,bg="#a1cc64")
questionFrame.grid(row=5,column=1,columnspan=7,padx=40,pady=100)

questionLabel=Label(questionFrame,bg="yellow",text="Guess the number?",font=("Verdana",20))
questionLabel.pack()

answerEntry= Entry(questionFrame,font=("Verdana",20),bg="black",fg="yellow")
answerEntry.pack(pady=20)
answerEntry.configure(insertbackground='yellow')


# Quit button to return to the starting page
myMagicNumber=generateMagicNumber()
answerButton=Button(questionFrame,text="Submit Guess",font=("verdana",20),bg="#c5cc64",
                    activebackground="#c5cc64",command=checkAnswer)
answerButton.pack(pady=10)
quit_button = Button(gameFrame, text="Quit Game", font=("Verdana", 20), command=quitGame)
quit_button.grid(row=10,column=2)

#create score board
scoreFrame=Frame(window,bg="yellow")
byeLabel=Label(scoreFrame,text=f"ARBACADABRA!!🪄🪄🧝🧝 THANKS FOR PLAYING",font=("Verdana",25),bg="#64cc77")
byeLabel.pack(pady=10)
yourScore=Label(scoreFrame,text=f"Your Score is {Gamescore}",font=("Verdana",25),bg="#e3a66d")
yourScore.pack(pady=10)

home_button = Button(scoreFrame, text="Back To Home", font=("Verdana", 20), command=goToHomePage, bg="black",fg="White")
home_button.pack(pady=10)

exit_button = Button(scoreFrame, text="Quit Game", font=("Verdana", 20), command=quitGame, bg="black",fg="White")
exit_button.pack(pady=10)

# Bind the Return key to the entry widget to also start the new frame
name_entry.bind('<Return>', lambda event: startNewFrame())
#table
leaderBoardFrame=Frame(window,bg="#95f04f")
titlelabel=Label(leaderBoardFrame,text=f"MAGICIANS ASSEMBLED!!🪄🪄🧝🧝",font=("Verdana",25),bg="#64cc77")
titlelabel.grid(row=0,column=1, padx=200)

tablecolumns = ('No','UserName','Score',)

       # Create Treeview
tree =Treeview(leaderBoardFrame, columns=tablecolumns, show='headings')
        # Create a hidden 'id' column
tree.column("#0", width=0, stretch=NO)  # This hides the 'id' column
tree.heading('No', text='No')
tree.heading('UserName', text='UserName')
tree.heading('Score', text='Score')

tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Add a scroll bar
scrollbar =Scrollbar(leaderBoardFrame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=2, sticky='ns')

back_button = Button(leaderBoardFrame, text="Back To Home", font=("Verdana", 20), command=goToHomePage, bg="black",fg="White")
back_button.grid(row=3,column=1,padx=200)


window.mainloop()