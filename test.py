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

##################################ComboBox############################################################################################


colum_TongKho = ("0","1", "2","3","4","5","6")
colum_XuatKho = ("0","1", "2","3","4","5","6","7")
colum_NhapKho = ("0","1", "2","3","4","5","6","7")

nameTable = ttk.Label(frame2,text="Bảng Tổng Kho",width=12,)
nameTable.place(x=0,y=330,width=100)

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

table.pack(fill="both",padx=0,pady=350)

nameTableData = tk.StringVar()

def setup_table(name, time_label = None):
    table.delete(*table.get_children())
    nameTable.config(text=name)
    table.config(columns=colum_NhapKho)
    table.heading("#0", text="STT")
    table.heading("0", text="Mã hàng")
    table.heading("1", text="Tên hàng")
    table.heading("2", text="Xuất xứ")
    table.heading("3", text="Giá nhập")
    table.heading("4", text="Giá xuất")
    table.heading("5", text="Số lượng")
    table.heading("6", text="Khu Vực")
    table.heading("7", text=time_label)
    table.column("#0", width=100)
    table.column("6", width=150)
    table.pack(fill="both", padx=0, pady=350)

def nhapKho():
    setup_table("Bảng nhập kho", "Thời gian nhập")

def xuatKho():
    setup_table("Bảng xuất kho", "Thời gian xuất")

def tongKho():
    setup_table("Bảng tổng kho")

#RadioButton NhapKho
r = ttk.Radiobutton(
        frame2,
        text="Nhập kho",
        value="Nhap",
        variable=nameTableData,
        command=nhapKho
    ).place(x=20,y=550)
#RadioButton XuatKho
r1 = ttk.Radiobutton(
        frame2,
        text="Xuất kho",
        value="Xuat",
        variable=nameTableData,
        command=xuatKho
    ).place(x=20,y=600)
#RadioButton TongKho
r2 = ttk.Radiobutton(
        frame2,
        text="Tổng kho",
        value="Tong",
        variable=nameTableData,
        command=tongKho
    ).place(x=20,y=650)

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
    ).place(x=10,y=700)

##############################################################################################################################



handle_frame_img = tk.Label(frame1,image='',width=frame_width,height=400)
handle_frame_img.place(x=0,y=400)
camera = cv2.VideoCapture(0)

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


def capturedVideo():
    global handle_frame_img
    global data, last_data
    global conn, directionOfQrCode
    global nameTableData
    global ktratable
    MaHang= list()
    # data_frame = list()
    status,frame = camera.read()
    if status == False:
        message = messagebox.showerror("Lỗi","Camera của bay bị hỏng à")
        sys.exit()
    else:
        rgb_type_arr = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        info = decode(rgb_type_arr)
        #Nếu trong info có Class Decode được tạo thì sẽ lấy dữ liệu
        if len(info)>0:
            DecodedObject = info[0]
            # print(DecodedObject)
            GeometryOfQrCode = DecodedObject.polygon
            #--Hướng của mã QR Code dựa trên 3 đỉnh
            # có 4 trường hợp:
            # 1 .LEFT, 2. RIGHT, 3. UP, 4. DOWN
            directionOfQrCode = DecodedObject.orientation
            dimensionofQrCode = DecodedObject.rect
            # print(directionOfQrCode)
            # print(DirectionOfQrCode)
            #Vẽ đa giác ABCD bằng tọa độ các đỉnh
            point_A = [GeometryOfQrCode[0].x,GeometryOfQrCode[0].y]
            point_B = [GeometryOfQrCode[1].x,GeometryOfQrCode[1].y]
            point_C = [GeometryOfQrCode[2].x,GeometryOfQrCode[2].y]
            point_D = [GeometryOfQrCode[3].x,GeometryOfQrCode[3].y]
            
            pts = np.array([point_A,point_B,point_C,point_D],dtype=np.int32)
            #Mỗi không gian chứa 2 điểm, do đó cần reshape
            pts = pts.reshape((-1,1,2))
            #Vẽ đa giác trên frame
            frame_drew = cv.polylines(rgb_type_arr,[pts],True,color=(0,255,0),thickness=2)
            # print(point_C)
            # print(point_D)
            #Vị trí chữ dựa trên chiều của mã QR
            point_text = (int(point_C[0]-((dimensionofQrCode.width)/1)),int(point_C[1]-30))
            # print(point_text)
            #Lấy dữ liệu, chuyển dữ liệu gốc về dạng UTF-8
            data = DecodedObject.data.decode('utf-8')
            data_frame = list(data.split(","))
            data_frame = list(data_frame)
            df = pd.read_sql('SELECT * FROM Bang_Tong_Kho',conn)
            if data_frame[0] in df['MaHang'].values:
                frame_text = cv.putText(frame_drew,text=f'Ma:{data_frame[0]},In Stock',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(0,255,0),org=point_text,thickness=2)
                # if ktratable != nameTableData.get():
                #     name = nameTableData.get()
                #     print(name)
                #     ktratable = nameTableData.get()
                #kiểm tra không trùng lặp dữ liệu
                if last_data != data_frame[0]:
                    # insertData(data,name)
                    # print(directionOfQrCode)
                    # add_dataBase_to_TreeView(data)
                    #Biến lưu giá trị truy vấn từ CSDL
                    data_temp = selectData(data_frame[0])
                    name_table = str(nameTableData.get()) #Biến lấy giá trị tên của bảng cần chèn
                    insertData(data_temp,name_table)
                    print(data_temp)
                    print(type(name_table))
                    last_data = data_frame[0]    

            else:
                frame_text = cv.putText(frame_drew,text=f'Ma:{data_frame[0]},Out of Stock',fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(255,0,0),org=point_text,thickness=2)
            image = Image.fromarray(frame_text)
            image = image.resize((600,400))
            destImage = ImageTk.PhotoImage(image=image)
            handle_frame_img.configure(
                image=destImage
            )
            handle_frame_img.image = destImage
                #Loop after 20ms
            handle_frame_img.place(x=0,y=400)
            handle_frame_img.after(20,capturedVideo)
        else:
            image = Image.fromarray(rgb_type_arr)
            image = image.resize((600,400))
            destImage = ImageTk.PhotoImage(image=image)
            handle_frame_img.configure(
                image=destImage
            )
            handle_frame_img.image = destImage
                #Loop after 20ms
            handle_frame_img.place(x=0,y=400)
            handle_frame_img.after(20,capturedVideo)

            
    # print(type(MaHang))
    # print(type(data_frame))

    # print(MaHang)
    # print(data_frame)

    # if ktratable != nameTableData.get():
    #     name = nameTableData.get()
    #     print(name)
    #     ktratable = nameTableData.get()
    #     #kiểm tra không trùng lặp dữ liệu
    #     if last_data != data & data_frame[0]:
    #         # insertData(data,name)
    #         # print(directionOfQrCode)
    #         # add_dataBase_to_TreeView(data)
    #         selectData(data)
    #         last_data = data
    
    
#Hoàng đã ở đây nè    
capturedVideo()
root.mainloop()
camera.release()


       
