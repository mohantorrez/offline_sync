import Tkinter as tk
import tkMessageBox
import json
import requests
from urllib import urlopen
import os.path
import threading
import ast

class app(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.master.title("App")
        self.windows = []
        self.home()

    def home(self):
        self.frame=tk.Frame(self)
        self.frame.grid()
        self.newbutton=tk.Button(self)
        self.offline_upload()
        self.row=0
        url = "http://localhost/spritle/api.php?action=get_users";
        check = self.connected_to_internet()
        if(check):
            r = requests.get(url)
            j = r.json()
            open('post.json', 'w+')
            with open('post.json','w+') as f:
                json.dump(j,f)
        else:
            json_data=open("post.json").read()

            j = json.loads(json_data)

        self.E1 = tk.Label(self.frame, text="Title")
        self.E1.grid(row=self.row, column=0)
        self.E1 = tk.Label(self.frame, text="Author")
        self.E1.grid(row=self.row, column=1)
        self.E1 = tk.Label(self.frame, text="Body")
        self.E1.grid(row=self.row, column=2)

       # j = [[0 for x in range(5)] for x in range(5)] 
        # j[0]['title'] = "asdg"
        # j[0]['author'] = "asdg"
        # j[0]['body'] = "asdg"
        for val in j:
            self.row += 1
            self.T1 = tk.Label(self.frame, text=val['title'])
            self.T1.grid(row=self.row, column=0)
            self.A1 = tk.Label(self.frame, text=val['author'])
            self.A1.grid(row=self.row, column=1)
            self.B1 = tk.Label(self.frame, text=val['body'])
            self.B1.grid(row=self.row, column=2)
            editButton = tk.Button(self.frame, text="Edit", fg="White", bg="#0094FF", 
                                      font=("Grobold", 10),command = lambda no=val['id'],title=val['title'],author=val['author'],body=val['body']: self.new_window(no,title,author,body))
            editButton.grid(row=self.row,column=3)
            deletebutton = tk.Button(self.frame, text="Delete", fg="White", bg="#0094FF", 
                                      font=("Grobold", 10),command = lambda no=val['id']: self.insert(no,type="delete"))
            deletebutton.grid(row=self.row,column=4)
        #     editButton.pack()
        # newButton = tk.Button(self, text="New Post", fg="White", bg="#0094FF",
        #                              font=("Grobold", 10),command =  lambda:self.new_window)
        # newButton.grid(row = self.row + 1, column = 2)
        self.newbutton.destroy()
        self.newbutton = tk.Button(self.frame,text="New Post",command=self.new_window)
        self.newbutton.grid(row = self.row+1)

    def new_window(self,id='',title='',author='',body=''):
        self.new = tk.Toplevel(self)
        self.new.title("Function")
        self.L1 = tk.Label(self.new, text="Title")
        self.L1.grid()
        self.E1 = tk.Entry(self.new, bd =5)
        self.E1.grid()
        #E1.insert(0,title)

        self.L2 = tk.Label(self.new, text="Author")
        self.L2.grid( )
        self.E2 = tk.Entry(self.new, bd =5)
        self.E2.grid()
        #E2.insert(0,author)

        self.L3 = tk.Label(self.new, text="Body")
        self.L3.grid( )
        self.E3 = tk.Entry(self.new, bd =5)
        self.E3.grid()
        self.E1.insert(0,title)
        self.E2.insert(0,author)
        self.E3.insert(0,body)

        self.new.update_button = tk.Button(self.new, text="Submit", fg="White", bg="#0094FF", 
                                       font=("Grobold", 10),command = lambda no=id: self.insert(no))
        self.new.update_button.grid()
        # if(id != ''):
        #     self.new.E1.insert(0,title)
        #     self.new.E2.insert(0,author)
        #     self.new.E3.insert(0,body)
        #     self.new.update_button = tk.Button(self.new, text="Update", fg="White", bg="#0094FF", 
        #                               font=("Grobold", 10),command = lambda no=id,title=title,author=author,body=body: self.insert(no,title,author,body))
        #     self.new.update_button.grid()
        # else:
        #     self.new.submit = tk.Button(self.new, text="Insert", fg="White", bg="#0094FF",
        #                 font=("Grobold", 10),command =lambda id='',title=self.new.E1.get(),author=self.new.E2.get(),body=self.new.E3.get() :self.insert(id,title,author,body))
        #     self.new.submit.grid()
        self.windows.append(self.new)

    def insert(self, id='', type='', title='', author='', body=''):
        if(type == '' and title == '' and author == ''):
            title = self.E1.get()
            author = self.E2.get()
            body = self.E3.get()
            data = {
            "id" : id,
            "author": author,
            "body" : body,
            "title" : title,
            "type" : type
            }
        else:
            data = {
            "id" : id,
            "type" : type
            }
        data_json = json.dumps(data)
        print data_json
        #data = ast.literal_eval(data)
        #print data_json
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = 'http://localhost/spritle/api.php?action=insert_list&data_json='
        check = self.connected_to_internet()
        if(check):
            r = requests.post(url+data_json ,headers=headers )
            if (r.status_code == 200):
                tkMessageBox.showinfo("Result","success")
                if(type != 'delete'):
                    self.new.destroy()
                self.frame.destroy()
                self.home()
        else:
            tkMessageBox.showinfo('Result','No Connection Stored for later upload')
            with open('offline_post.json', 'r+') as f:
                new = json.load(f)
                new.append(data)
                f.seek(0)
                json.dump(new, f)
                f.truncate()
            if(type != 'delete'):
                    self.new.destroy()
            self.frame.destroy()
            self.home()

        
    def offline_upload(self):
        json_data=open("offline_post.json",'r+')
        j = json.load(json_data)
        if(j != ""):
            for val in j:
                data_json = json.dumps(val)
                url = 'http://localhost/spritle/api.php?action=insert_list&data_json='
                check = self.connected_to_internet()
                if(check):
                    r = requests.post(url+data_json)


            
    def connected_to_internet(self, timeout=5):
        try:
            #t = threading.Timer(3, self.connected_to_internet())
            #t.start()
            url = 'http://localhost/spritle/api.php?action=insert_list&data_json='
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            print("No internet connection available.")
            return False


app = app() 
app.grid() 

app.mainloop()
