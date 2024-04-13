#Ví dụ này sẽ chỉ ra cách viết chương trình theo hướng OOP
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import cv2 as cv
import sys
class myApp(tk.Tk):
    def __init__(self,title,dimension):
        super().__init__()
        #Tạo debug Input
        if isinstance(dimension,tuple) == False:
           raise ValueError("Wrong Input")
        else:
            self.height = dimension[1]
            self.width = dimension[0]
            #Thiết lập giao diện
            self.title(title)
            self.geometry(f'{dimension[0]}x{dimension[1]}')
            self.resizable(False,False)
            #-Chia làm 2 frame : 1 frame sẽ có show camera và frame còn lại chứa các tab
            
            #Camera
            self.frame_camera = tk.Frame(self,borderwidth=2,width=dimension[0],height=dimension[1]/2,relief="solid")
            self.frame_camera.pack_propagate(False)
            self.frame_camera.pack()
            self.label_camera = tk.Label(self.frame_camera,image="")
            self.label_camera.pack()
            
            #Frame chứa notebook và các tab
            self.frame_notebook = tk.Frame(self,borderwidth=2,width=dimension[0],height=dimension[1]/2,relief="solid")
            self.frame_notebook.pack()
            self.frame_notebook.pack_propagate(False)
            self.myNotebook = ttk.Notebook(self.frame_notebook)
            self.myNotebook.pack()
            
            #Các tab
            self.tab1 = Tab1(self,(dimension[0],dimension[1]/2))
            self.tab2 = Tab2(self,(dimension[0],dimension[1]/2))
            self.myNotebook.add(self.tab1,text="Tab1")
            self.myNotebook.add(self.tab2,text="Tab2")
            
            #Thiết lập các thuộc tính
            self.camera = cv.VideoCapture(0)
    def cameraLoop(self):
        status,frame = self.camera.read()
        if status == False:
            message = messagebox.showerror("Error","Please check your camera")
            sys.exit()
        else:
            #Chuyển về chuẩn màu RGB
            frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            #Chuyển về format Image của PIL
            image = Image.fromarray(frame)
            image = image.resize((int(self.width),int(self.height/2)))
            img_tkFormat = ImageTk.PhotoImage(image=image)
            self.label_camera.configure(
                image = img_tkFormat
            )
            self.label_camera.image = img_tkFormat
            #Call after 20ms. Link : https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
            
            self.after(20,self.cameraLoop)
            
class baseLayout_Tab(tk.Frame):
    def __init__(self,parent,dimension):
        super().__init__(parent,width=dimension[0],height=dimension[1])
        if isinstance(dimension,tuple) == False:
           raise ValueError("Wrong Input")
        else:
            self.pack_propagate(False)
            self.text = ""
            self.text_label = tk.Label(self,text=self.text)
            self.text_label.pack()

class Tab1(baseLayout_Tab):
    def __init__(self,parent,dimension):
        #Kế thừa hàm khởi tạo
        super().__init__(parent,dimension)
        self.text = "Hoang"
        #Configure text inside label
        self.text_label.configure(
            text = self.text
        )

class Tab2(baseLayout_Tab):
    def __init__(self,parent,dimension):
        #Kế thừa hàm khởi tạo
        super().__init__(parent,dimension)
        self.text = "Bla"
        #Configure text inside label
        self.text_label.configure(
            text = self.text
        )
        self.button = tk.Button(
            self,
            text="Bấm đi",
            command=self.handleFunction
        )
        self.button.pack()
    def handleFunction(self):
        message = messagebox.showinfo("Thông tin","Bạn đã nhấn nút ấn")

if __name__ == "__main__":
    app = myApp("Hoang",(800,600))
    app.after(20,app.cameraLoop)
    app.mainloop()
        
v
