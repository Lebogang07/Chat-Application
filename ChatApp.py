from tkinter import *
from tkinter import messagebox
from datetime import datetime

with open("Contact List.txt", "r") as file:
    contact_name = [line.strip() for line in file if line.strip()]
    
messages = {contact: [] for contact in contact_name} ##Create a message history dictionary for each contact

def NewUser_Window():
    new_user = Tk() ##Creates a new window
    new_user.title("New user registration")
    new_user.geometry("320x320")  ##Size of the new window 
    
    TextLabel = Label(new_user, text="Create a new user account", font=('Arial',10, 'bold')).grid(row=0, column = 0, columnspan=2)
    
    NewLabel = Label(new_user, text="Username:", width=20).grid(row=1, column=0, pady=5)
    NewEntry = Entry(new_user).grid(row=1, column=1, pady=5)  ##Username input

    NewPassword = Label(new_user, text="Password:").grid(row=2, column=0, pady=5)
    NewPassword = Entry(new_user, show="*").grid(row=2, column=1, pady=5) ## Password entry
    
    AddButton = Button(new_user, text = "Add", command=new_user.destroy).grid(row=3, columnspan=2, pady=10) ##Adds the new user to existing users
    



def Group():
    group = Tk() ##Creates a new group chat window
    group.title("Group Chat")
    group.geometry("330x330")
    
    names = Label(group, text="Group", anchor="w")
    names.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="W")

    backButton = Button(group, text="Back", command=group.destroy).grid(row=0, column=1, pady=5, padx=1, sticky="e") ##Back button that closes the initial open window

    chat_display = Text(group,width = 39, height= 15)
    chat_display.grid(row=1, column=0, columnspan=2, padx=5, pady=5) ##Display conversation
    inputText = Text(group, width=30, height=2)
    inputText.grid(row=2, column=0, padx=5, pady=5) ##Area to send text messages
    
    chat_display.tag_configure("time_right", justify="right", rmargin=5) ##Aligns the time to the right of the text
    
    def send_message():
        msg = inputText.get("1.0", END).strip() ##Content from inputText area is stored in a variable 
        if not msg:
            return
        time_sent = datetime.now().strftime("%H:%M") ##Gets the current system time formated in hours and minutes
        
        chat_display.config(state=NORMAL) ##Allows the insertion of text into the display
        chat_display.insert(END, f"You: {msg}\n")
        chat_display.insert(END, f"{time_sent}\n", "time_right") ##Inserts the time the message was sent 
        chat_display.config(state=DISABLED) ##For read-only purposes 
        
        inputText.delete("1.0", END) ##Clears the inputText widget 


    sendButton = Button(group, text="Send", command=send_message).grid(row=2, column=1, padx=5, pady=5)
    


def CreateGroupChat():
    groupWindow = Tk() ##Creates a new window to create a group chat
    groupWindow.title("Creating Group Chat")
    groupWindow.geometry("320x320")
    
    label = Label(groupWindow, text="Add members to the group: ").grid(row=0, column=0)
    

    check_vars = [] ##An array to store the list of contacts
    row_number = 1

    try:
        with open("Contact List.txt", "r") as file: ##Reads information from the text file and adds it to the array 
            for line in file:
                contact = line.strip()
                var = IntVar()
                check_vars.append((contact, var))
                Checkbutton(groupWindow, text=contact, variable=var).grid(row=row_number, column=0, sticky="w", padx=10, pady=2) ##Creates a check button to slecet multiple members 
                row_number += 1 

    except FileNotFoundError:
        Label(groupWindow, text="Contact list not found.").grid(row=1, column=0, padx=10, pady=10) ##Message that appears when the file is empty
        
    button = Button(groupWindow, text="Add Members", command = Group).grid(row=row_number, column=0, columnspan=2) ##This button adds the selected members to a group and opens the group chat window 
    backButton = Button(groupWindow, text="Back", command=groupWindow.destroy).grid(row=row_number, column=1, pady=10, padx=1, sticky="e")
    
def Contacts_Window():
    
    def New_Chat(): ##A method to start a coversation with the selected contact
        selection = ContactList.curselection() 
        if not selection:
            messagebox.showinfo("No selection", "Please select a contact to chat with.") ##Message appears when no contact is selected
            return
        
        index = selection[0]  ##Assigns the selected item to a variable 
        contact_name = ContactList.get(index)
        
        new_chat = Tk() ##Creates a new window where the communication occurs 
        new_chat.title("Chat Window")
        new_chat.geometry("330x330")
        
        name_label = Label(new_chat, text=contact_name, font=("Arial", 12), anchor="w") ##Displays the name of the selected contact 
        name_label.grid(row=0,column=0, columnspan=2, sticky="w",padx=5, pady=5)
        
        backButton = Button(new_chat, text="Back", command=new_chat.destroy).grid(row=0, column=1, sticky="e", pady=10, padx=1)
        
        chat_display = Text(new_chat,width = 39, height= 15)
        chat_display.grid(row=1, column=0, columnspan=2, padx=5, pady=5) ##Display conversation 
        
        def display_chat(contact_name):
            
            chat_display.config(state=NORMAL)
            chat_display.delete(1.0, END)
            
            chat_display.tag_configure("time_right", justify="right")
            
            for sender, msg, time in messages[contact_name]:
                chat_display.insert(END, f"{sender}: {msg}\n")
                chat_display.insert(END, f"{time}\n", "time_right")
            chat_display.config(state=DISABLED)

        
        inputText = Text(new_chat, width=30, height=2)
        inputText.grid(row=2, column=0, padx=5, pady=5)
        
        def send_message():
            msg = inputText.get("1.0", END).strip()
            if not msg:
                return
            time_sent = datetime.now().strftime("%H:%M")
            messages[contact_name].append(("You", msg, time_sent))
            display_chat(contact_name)
            inputText.delete(1.0, END)
        
        sendButton = Button(new_chat, text="Send", command=send_message).grid(row=2, column=1, padx=5, pady=5)
        
        display_chat(contact_name)
        
        
        
    ContactWindow = Tk() ##Creates a new window to display contacts
    ContactWindow.title("Contact List")
    ContactWindow.geometry("320x320")
    
    ContactsLable = Label(ContactWindow, text="Contacts").grid(row=0, column=0, padx=5)
    ContactList = Listbox(ContactWindow, width=30) ##Creates a list box where contacts will be listed 
    ContactList.grid(row=1, column=0, pady=5, columnspan=2)
    
    ## The code below is for retrieving the contact list from the text file.(I created a text file just to test the funcionality)
    ##Marnus will modify this accordingly 
    try:
        with open("Contact List.txt", "r") as file: ##Reads information from the "Contact List" file
            for line in file:
                ContactList.insert(END, line.strip()) ##Writes the information to the list box 
    except FileNotFoundError:
        ContactList.insert(END, "No contacts found.") ## Returns the meaasge when the file is empty 
    
   
    NewChatButton = Button(ContactWindow, text="New Chat", width=12, command = New_Chat).grid(row=2,column=0, pady=10, padx=2) ##Button to start coversation with the selected contact in a new window 

    GroupChatButtom = Button(ContactWindow, text="Create Group Chat", width=13, command=CreateGroupChat).grid(row=2, column=1, pady=10, padx=2) #Button to create a group chat
            
    backButton = Button(ContactWindow, text="Back", command=ContactWindow.destroy).grid(row=2, column=3, pady=10, padx=40)


window = Tk() ##Creates the main window 

window.geometry("420x420")
window.title("Login Window")

TitleLable = Label(window, text="Enter your login details ", font = ('Arial',10, 'bold')).grid(row=0, column = 0, columnspan=2)

UsernameLabel = Label(window, text="Username:", width=20).grid(row=1, column=0, pady=5)
UserNameEntry = Entry(window).grid(row=1, column=1, pady=5)  ##Username input

PasswordLabel = Label(window, text="Password:").grid(row=2, column=0, pady=5)
PasswordEntry = Entry(window, show="*").grid(row=2, column=1, pady=5) ##Password input 

checkFrame = Frame(window)
checkFrame.grid(row=3, column=0, columnspan=2, pady=5)

useDefaultLabel = Label(checkFrame, text="Use default server")
useDefaultLabel.pack(side=LEFT)

checkButton = Checkbutton(checkFrame)
checkButton.pack(side=RIGHT)

buttonConnect = Button(window, text="Connect", command=Contacts_Window).grid(row=6,column=0, pady=10) ##Connects the user to their server

buttonNewUser = Button(window, text="New User", command=NewUser_Window).grid(row=6, column=1, pady=10) ##Allows new users to create an account to login 

window.mainloop()
