from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import filedialog
import json

class App:

    def __init__(self,root):
        self.univ_font_heading = "Poppins 30 bold"
        self.univ_font_para = "Poppins 17 bold"

        self.root = root
        self.config(self.root)
        # self.login_frame(self.root)
        self.add_first_page(self.root)

    # This is to config the root window
    def config(self,root):
        root.title("Chat Application")
        root.config(bg="white")
        root.geometry("600x520")

    # def login_frame(self,root):
    #     self.frame = ttk.Frame(self.root,)
    #     self.frame.pack(anchor="center")
    #     self.add_first_page(self.frame)

    def add_first_page(self,frame):
        #  adding the heading Chat Application
        heading_label = ttk.Label(self.root,text="Chat Application",background="white",foreground="purple",font=self.univ_font_heading)
        heading_label.place(x=120,y=40,relwidth=1.0)

        # Adding the entry and label to ask for name of the user
        label_name = ttk.Label(self.root,text="Nickname : ",background="white",font=self.univ_font_para)
        label_name.place(x=60,y=150,relwidth=0.5)
        self.entry_name = ttk.Entry(self.root,foreground="black",font=self.univ_font_para,width=20)
        self.entry_name.place(x=220,y=150,relwidth=0.5)

        # Entry for the password
        label_name = ttk.Label(self.root,text="Password : ",background="white",font=self.univ_font_para)
        label_name.place(x=60,y=250,relwidth=0.5)
        self.entry_pass = ttk.Entry(self.root,foreground="black",show="*",font=self.univ_font_para,width=20)
        self.entry_pass.place(x=220,y=250,relwidth=0.5)

        # Button
        btn_submit = ttk.Button(self.root,text="Submit",command=self.submit)
        btn_submit.place(x=250,y=380)

        # Button
        btn_submit = ttk.Button(self.root,text="Quit",command=self.root.destroy)
        btn_submit.place(x=250,y=420)

    def submit(self):
        cbool = messagebox.askquestion("Confirm","Please Confirm The Details");
        if cbool == "yes":
            object_user = {
            "nickname" : self.entry_name.get(),
            "password" : self.entry_pass.get()
            }
            with open("user_data.json","ab+") as f:
                f.seek(0,2)                                #Go to the end of file
                if f.tell() == 0 :                         #Check if file is empty
                    f.write(json.dumps([object_user]).encode())  #If empty, write an array
                else :
                    f.seek(-1,2)
                    f.truncate()                           #Remove the last character, open the array
                    f.write(' , '.encode())                #Write the separator
                    f.write(json.dumps(object_user).encode())    #Dump the dictionary
                    f.write(']'.encode())
                    self.entry_name.delete(0,"end")
                    self.entry_name.insert(0, "")
                    self.entry_pass.delete(0,"end")
                    self.entry_pass.insert(0, "")
                    self.root.destroy()
                    self.chat = Chat_page(object_user["nickname"])

        else :
            pass
        print("able to submit")

class Chat_page:
    def __init__(self,person_name):
        self.root = ThemedTk(theme="arc")
        self.root.config(bg="white")
        self.root.title(f"Chat :: {person_name}")
        self.root.geometry("800x650")

        self.root.mainloop()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    App(root)
    root.mainloop()
