import tkinter as tk
from PIL import Image, ImageTk
import cv2
from tkinter import ttk
import datetime
import numpy as np
from pyzbar.pyzbar import decode
from tkinter import messagebox
import cv2 as cv
import sys
import pyodbc as odbc
import traceback
import pandas as pd
import sys
import threading

data = 'xx'
data1=''
last_data = ''
conn = ""
ktra = 0
ktratable = ''
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-9Q5LPOB\SQLEXPRESS'
DATABASE_NAME = 'QLLK_NCKH'
directionOfQrCode = ''
connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes
"""   

try:
    print("Đang kết nối với server ....")
    conn = odbc.connect(connection_string)
except:
    print("Kiểm tra lại cách kết nối nhaa")
    exit() #Thoát khỏi chương trình
else:
    print("Kết nối thành công!")

root = tk.Tk()
root.title("Chia cửa sổ thành 3 phần bằng nhau")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Tính toán kích thước của cửa sổ
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

frame_width = window_width // 3  # Kích thước mỗi frame
frame_height = window_height

# Tạo 3 frame conn
frame1 = tk.Frame(root, width=frame_width, height=frame_height, bg="black")
frame1.pack_propagate(False)
frame1.grid(row=0, column=0)

frame2 = tk.Frame(root, width=frame_width*2, height=frame_height, bg="pink")
frame2.pack_propagate(False)
frame2.grid(row=0, column=1)

frame2.grid_rowconfigure(0,weight=4)
frame2.grid_rowconfigure(1,weight=6)
frame2.grid_rowconfigure(0,weight=4)

frame2_1 = tk.Frame(frame2, width=frame_width*2, height=frame_height*(4/14), bg="red")
frame2_1.pack_propagate(False)
frame2_1.grid(row=0, column=0)

frame2_2 = tk.Frame(frame2, width=frame_width*2, height=frame_height*(6/14), bg="brown")
frame2_2.pack_propagate(False)
frame2_2.grid(row=1, column=0)

frame2_3 = tk.Frame(frame2, width=frame_width*2, height=frame_height*(4/14), bg="pink")
frame2_3.pack_propagate(False)
frame2_3.grid(row=2, column=0)

class LayOut(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)
        self.conn = conn
        self.master = master
        self.width=width
        self.height=height
        self.colums_table = ("0","1", "2","3","4","5","6","7")
        self.table = ttk.Treeview(self,columns=self.colums_table)
        self.table.heading("0", text="Mã hàng")
        self.table.heading("#0", text="STT")
        self.table.heading("1", text="Tên hàng")
        self.table.heading("2", text="Xuất xứ")
        self.table.heading("3", text="Giá nhập")
        self.table.heading("4", text="Giá xuất")
        self.table.heading("5", text="Số lượng")
        self.table.heading("6", text="Khu Vực")
        self.table.heading("7", text=None)
        self.table.column("#0", width=100)
        self.table.column("6",width=150)
        self.table.pack()
        self.table_name = ""
    def insertData(self,data):
        self.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time = str(self.current_time)
        # time= tuple(time)
        # data=list(data)
        data=tuple(data)
        data = data + (self.time,)
        # data.append(time)
        sql_query = f"INSERT INTO Bang_{self.table_name}_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuong{self.table_name},KhuVuc,ThoiGian{self.table_name}) VALUES (?,?,?,?,?,?,?,?)"      
        print(sql_query)
        print(f'{data}', type(data))
        print(self.time)
        print(type(table))
        # print(type(current_time))
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query,data)
        except Exception as e:
            print(f"Lỗi chèn dữ liệu: {e}")
            traceback.print_exc()
        else:
            print(f"Thêm dữ liệu vào Bang_{table}_Kho thành công")
            cursor.commit()   
            

class NotebookTongKho(LayOut):
    def __init__(self, master,width,height):
        super().__init__(master, width, height)
        


class NotebookNhapKho(LayOut):
    def __init__(self, master, width, height):
        self.data=data
        super().__init__(master, width, height)
        self.table.heading("5",text="Số lượng nhập hàng")
        self.table.heading("7",text="Thời gian nhập hàng")
        self.table_name = "Nhap"
    # def insertData(self, data):
    #     super().insertData()

# object = NotebookNhapKho("",100,100,"Bla")
# object.insertData       
        


class NotebookXuatKho(LayOut):
    def __init__(self, master, width, height):
        super().__init__(master, width, height)
        self.data=data
        self.table.heading("5", text="Số lượng xuất hàng")
        self.table.heading("7",text="Thời gian xuất hàng")



class MainApplication(tk.Frame):
    def __init__(self, master, frame_width, frame_height):
        super().__init__(master, width=frame_width, height=frame_height)
        self.master = master
        self.pack(fill='both', expand=True)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab1 = NotebookTongKho(self.notebook, width=frame_width, height=frame_height)
        self.tab2 = NotebookNhapKho(self.notebook, width=frame_width, height=frame_height)
        self.tab3 = NotebookXuatKho(self.notebook, width=frame_width, height=frame_height)

        self.notebook.add(self.tab1, text="Bảng tổng kho")
        self.notebook.add(self.tab2, text="Bảng nhập kho")
        self.notebook.add(self.tab3, text="Bảng xuất kho")


def insertData(data,table):
    global conn
    global current_time
    time = str(current_time)
    # time= tuple(time)
    # data=list(data)
    data=tuple(data)

    data = data + (time,)
    # data.append(time)
    sql_query = f"INSERT INTO Bang_{table}_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuong{table},KhuVuc,ThoiGian{table}) VALUES (?,?,?,?,?,?,?,?)"      
    print(sql_query)
    print(f'{data}', type(data))
    print(time)
    print(type(table))
    # print(type(current_time))
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query,data)
    except Exception as e:
        print(f"Lỗi chèn dữ liệu: {e}")
        traceback.print_exc()
    else:
        print(f"Thêm dữ liệu vào Bang_{table}_Kho thành công")
        cursor.commit()   
app = MainApplication(frame2_2,frame_width=frame_width*2, frame_height=frame_height*(6/14))


























# notebook = ttk.Notebook(frame2_2)
# notebook.pack_propagate(False)
# notebook.pack(expand=False)

# notebook_2_NhapKho = tk.Frame(notebook, width=frame_width*2, height=frame_height*(6/14))
# notebook_2_NhapKho.pack_propagate(False)
# notebook_2_XuatKho = tk.Frame(notebook, width=frame_width*2, height=frame_height*(6/14))
# notebook_2_XuatKho.pack_propagate(False)


# notebook.add(notebook_2_XuatKho,text="Bảng xuất kho")
# notebook.add(notebook_2_NhapKho,text="Bảng nhập kho")



# bA = tk.Button(master=notebook_2_NhapKho,text="xcv").pack(side='left')

# bas = tk.Button(master=notebook_2_XuatKho,text="123").pack(expand=False)













##################################ComboBox############################################################################################


colum_TongKho = ("0","1", "2","3","4","5","6")
colum_XuatKho = ("0","1", "2","3","4","5","6","7")
colum_NhapKho = ("0","1", "2","3","4","5","6","7")

nameTable = ttk.Label(frame2,text="Bảng Tổng Kho",width=12)
# nameTable.place(x=0,y=330,width=100)

table = ttk.Treeview(frame2, columns=colum_TongKho)
table.heading("#0", text="STT")
table.heading("0", text="Mã hàng")
table.heading("1", text="Tên hàng")
table.heading("2", text="Xuất xứ")
table.heading("3", text="Giá nhập")
table.heading("4", text="Giá xuất")
table.heading("5", text="Số lượng")
table.heading("6", text="Khu Vực")

table.column("#0", width=100)
table.column("6",widt=150)

def ExportElxs():
    global conn
    global nameTableData
    name_table = str(nameTableData.get())
    kq = pd.read_sql(f'SELECT * FROM Bang_{name_table}_Kho',conn)
    df = pd.DataFrame(kq)
    df.to_excel('test1.xlsx',sheet_name='kq1')
    # print(name_table)

def on_btXuatExcel():
    excel = threading.Thread(target=ExportElxs)
    excel.start()

btXuatExcel = tk.Button(
    master=frame2,
    text='Xuất file excel',
    command=on_btXuatExcel                   
    )
    # .place(x=10,y=700)

##############################################################################################################################



handle_frame_img = tk.Label(frame1,image='',width=frame_width,height=400)
handle_frame_img.place(x=0,y=400)
# camera = cv2.VideoCapture(0)

counter = 1
# def add_data():
# # Lấy ngày/giờ hiện tại
#     global counter
#     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     # Thêm dữ liệu mới vào bảng
#     table.insert("", "end", text=str(counter), values=(f"Mã hàng {data[1]}","Nội dung {data[0]}","Ngày/Giờ{current_time}"))
#     counter += 1

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_dataBase_to_TreeView(data):
    global counter
    global current_time
    # Lấy ngày/giờ hiện tại
    # Thêm dữ liệu mới vào bảng
    print(data)
    data = list(data.split(","))
    print(len(data))
    #print(data[1])
    #ao = data[0]
    if len(data) >= 3:
        print(data[1])
        table.insert("", "end", text=str(counter), values=(data[0],data[1],data[2], current_time))
        # table.insert("", "end", text=str(counter), values=(f"Nội dung ", current_time))
        counter +=1   


def insertData(data,table):
    global conn
    global current_time
    time = str(current_time)
    # time= tuple(time)
    # data=list(data)
    data=tuple(data)
    data = data + (time,)
    # data.append(time)
    sql_query = f"INSERT INTO Bang_{table}_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuong{table},KhuVuc,ThoiGian{table}) VALUES (?,?,?,?,?,?,?,?)"      
    print(sql_query)
    print(f'{data}', type(data))
    print(time)
    print(type(table))
    # print(type(current_time))
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query,data)
    except Exception as e:
        print(f"Lỗi chèn dữ liệu: {e}")
        traceback.print_exc()
    else:
        print(f"Thêm dữ liệu vào Bang_{table}_Kho thành công")
        cursor.commit()   

#Hàm lấy dữ liệu từ database
# data_select = []
def selectData(data):
    # global data_select
    sql_query = f"SELECT * FROM Bang_Tong_Kho Where MaHang = {data}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        #Lấy dữ liệu từ database
        row = cursor.fetchone()
    except Exception as e:
        print(f"Lỗi lấy dữ liệu: {e}")
        traceback.print_exc()
    else:
        # Kiểm tra xem có dữ liệu được trả về không
        if row is not None:
        # Chuyển đổi dữ liệu thành list và gán vào biến
            data_select = [element for element in row]
            print('Truy vấn dữ liệu thành công')
    return tuple(data_select)




root.mainloop()
# camera.release()


       