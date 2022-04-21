import tkinter as tk
from tkinter import Frame, ttk, messagebox
import pyzbar.pyzbar as pyzbar
from datetime import date, datetime
import cv2
import time

class Firstpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        border = tk.LabelFrame(self, text='login', bg='white', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand='yes', padx=150, pady=150)

        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='white')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width=30, bd=5)
        T1.place(x=180, y=20)

        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='white')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width=30, show='*', bd=5)
        T2.place(x=180, y=80)

        def verify():
            try:
                with open("Credential.txt", "r") as f:
                    info = f.readlines()
                    a = 0  # this variable is used to switch between the pages...
                    for i in info:
                        u, p = i.split(",")  # username, password
                        if u.strip() == T1.get() and p.strip() == T2.get():
                            controller.show_frame(Secondpage)
                            a = 1
                            break
                    if a == 0:
                        messagebox.showinfo("Error!", "Please provide correct username and password")                        
            except:
                messagebox.showinfo("Error!!", "Please provide correct username and password")

        B1 = tk.Button(border, text="submit", font=("Arial", 15), command=verify)
        B1.place(x=320, y=115)

        def register():
            window = tk.Tk()
            window.title("Register")
            window.resizable(0, 0)
            window.configure(bg='white')
            la1 = tk.Label(window, text="Username", font=("Arial", 15), bg="white")
            la1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=200, y=10)
            la2 = tk.Label(window, text="Password", font=("Arial", 15), bg="white")
            la2.place(x=10, y=50)
            t2 = tk.Entry(window, width=30, show='*', bd=5)
            t2.place(x=200, y=50)
            la3 = tk.Label(window, text="Confirm Password", font=("Arial", 15), bg="white")
            la3.place(x=10, y=100)
            t3 = tk.Entry(window, width=30, show='*', bd=5)
            t3.place(x=200, y=100)

            def check():
                if t1.get() != "" or t2.get() != "" or t3.get() != "":
                    if t2.get() == t3.get():
                        with open("Credential.txt", "a") as f:
                            f.write(t1.get() + ',' + t2.get() + "\n")
                            messagebox.showinfo("Welcome", "You are registered successfully...!!")
                    else:
                        messagebox.showinfo("Error", "Your passwords didn't match")
                else:
                    messagebox.showinfo("Error", "Please enter all the fields")

            b1 = tk.Button(window, text="Sign in", font=("Arial", 15), bg='white', command=check)
            b1.place(x=170, y=150)

            window.geometry('500x200')
            window.mainloop()

        B2 = tk.Button(self, text="Register", bg="white", font=('Arial', 15), command=register)
        B2.place(x=650, y=20)


class Secondpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        year = tk.StringVar()
        branch = tk.StringVar()
        sec = tk.StringVar()
        period = tk.StringVar()

        #  Label of the window

        title = tk.Label(self, text="Automatic Attendance System ", bd=10, relief=tk.GROOVE,
                         font=("times new roman", 40),
                         bg="lavender", fg="black")
        title.pack(side=tk.TOP, fill=tk.X)

        Manage_Frame = Frame(self, bg="lavender")
        Manage_Frame.place(x=0, y=80, width=480, height=530)

        ttk.Label(self, text="Year", background="lavender", foreground="black", font=("Times New Roman", 15)).place(
            x=100,
            y=150)

        #  Combo box for the Year

        combo_search = ttk.Combobox(self, textvariable=year, width=10, font=("times new roman", 13), state='readonly')
        combo_search['values'] = ('1', '2', '3', '4')
        combo_search.place(x=250, y=150)

        ttk.Label(self, text="Branch", background="lavender", foreground="black", font=("Times New Roman", 15)).place(
            x=100,
            y=200)

        #  Combo box for the Departments
        combo_search = ttk.Combobox(self, textvariable=branch, width=10, font=("times new roman", 13),
                                    state='readonly')
        combo_search['values'] = ("CSE", "ECE", "CIVIL", "MECHANICAL")
        combo_search.place(x=250, y=200)

        ttk.Label(self, text="Section", background="lavender", foreground="black",
                  font=("Times New Roman", 15)).place(x=100,
                                                      y=250)

        #  Combo boc for the sections

        combo_search = ttk.Combobox(self, textvariable=sec, width=10, font=("times new roman", 13), state='readonly')
        combo_search['values'] = ('A', 'B', 'C', 'D')
        combo_search.place(x=250, y=250)

        ttk.Label(self, text="Period", background="lavender", foreground="black", font=("Times New Roman", 15)).place(
            x=100,
            y=300)

        #  Combo box for the periods

        combo_search = ttk.Combobox(self, textvariable=period, width=10, font=("times new roman", 13),
                                    state='readonly')
        combo_search['values'] = ('1', '2', '3', '4', '5', '6', '7')
        combo_search.place(x=250, y=300)

        def check():
            if year.get() and branch.get() and period.get() and sec.get():
                self.destroy()
                open_cam()
            else:
                messagebox.showwarning("Warning", "All fields required!!")

        Manage_Frame = Frame(self, bg="lavender")
        Manage_Frame.place(x=480, y=80, width=450, height=530)

        def open_cam():
            cap = cv2.VideoCapture(0)
            names = []
            today = date.today()
            d = today.strftime("%b-%d-%Y")

            fob = open(d + '.xls', 'w+')
            fob.write("Reg No." + '\t')
            fob.write("Class & Sec" + '\t')
            fob.write("Year" + '\t')
            fob.write("Period" + '\t')
            fob.write("In Time" + '\n')

            def enterData(z):
                if z in names:
                    pass
                else:
                    it = datetime.now()
                    names.append(z)
                    z = ''.join(str(z))
                    in_time = it.strftime("%H:%M:%S")
                    fob.write(
                        z + '\t' + branch.get() + '-' + sec.get() + '\t' + year.get() + '\t' + period.get() + '\t' +
                        in_time + '\n')
                return names

            print('Reading...')

            def checkData(data):
                if data in names:
                    print('Already Present')
                else:
                    print('\n' + str(len(names) + 1) + '\n' + 'present...')
                    enterData(data)

            while True:
                _, frame = cap.read()
                decodedObjects = pyzbar.decode(frame)
                for obj in decodedObjects:
                    checkData(obj.data)
                    time.sleep(1)

                cv2.imshow("Frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            fob.close()

        Button = tk.Button(self, text="Submit", font=("Arial", 15), command=lambda: check())
        Button.place(x=200, y=350)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for i in (Firstpage, Secondpage):
            frame = i(window, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(Firstpage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Attendance system")


app = Application()
app.maxsize(800, 500)
app.mainloop()
