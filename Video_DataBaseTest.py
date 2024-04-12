import tkinter as tk
from pyzbar.pyzbar import decode
from PIL import Image,ImageTk
from tkinter import messagebox
import cv2 as cv
import sys
import threading
import numpy as np
import time
import pypyodbc as odbc
import pyodbc
import traceback




root = tk.Tk()
root.geometry('800x600')
root.title('Video')



#---Video Captured
camera = cv.VideoCapture(0)
frame_video = tk.Frame(root,width=600,height=400,borderwidth=2,relief='solid')
frame_video.pack_propagate(False)  
frame_video.pack()
handle_frame_img = tk.Label(frame_video,image='')
data = 'xx'
data1=''
last_data = ''
conn = ""
ktra = 0
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-9Q5LPOB\SQLEXPRESS'
DATABASE_NAME = 'QLBH_N01_SV'

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
def capturedVideo():
    global handle_frame_img
    global data, last_data
    global conn
    # print("KQ: ", data)
    status,frame = camera.read()
    if status == False:
        message = messagebox.showerror("Lỗi","Camera của bay bị hỏng à")
        sys.exit()
    else:
        rgb_type_arr = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        info = decode(rgb_type_arr)
        # print(info)
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
            print(directionOfQrCode)
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
            point_text = (int(point_C[0]-((dimensionofQrCode.width)/2)),int(point_C[1]-15))
            # print(point_text)
            #Lấy dữ liệu, chuyển dữ liệu gốc về dạng UTF-8
            data = DecodedObject.data.decode('utf-8')
            frame_text = cv.putText(frame_drew,text=data,fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(0,255,0),org=point_text,thickness=2)
            image = Image.fromarray(frame_text)
            image = image.resize((600,400))
            destImage = ImageTk.PhotoImage(image=image)
            handle_frame_img.configure(
                image=destImage
            )
            handle_frame_img.image = destImage
                #Loop after 20ms
            handle_frame_img.pack()
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
            handle_frame_img.pack()
            handle_frame_img.after(20,capturedVideo)

    if last_data != data:
        plit_data = list(data.split(","))
        ldt = [' Raspberry_PI_4_B', ' Raspberry_PI_4_B', ' Raspberry_PI_4_B']
        sql_query = "INSERT INTO LuuKho (MaHang, TenHang, TrangThai) VALUES (?,?,?)"
        
        # sql_query = f"INSERT INTO HangHoaLuuKho (MaHang,TenHang,TrangThai) VALUES ({0},{1},{2})".format(plit_data[0],plit_data[1],plit_data[2])
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query,plit_data)
        except Exception as e:
            print(f"Lỗi chèn dữ liệu: {e}")
            traceback.print_exc()
        else:
            print("Thêm dữ liệu vào DataBase thành công")
            cursor.commit()   
        last_data = data 
            
   
#---Button
def handleStatus():
    global t1
    print(f'Sleeping in 10 second...')
    time.sleep(10)
    # print('Done Sleeping...')
    print ('Done Sleeping')
    t1.join()

def connetDataBase():
    global t2
    global ktra 
    


def checkDataBase():
    global ktra
    global data
    if ktra == 1:
        print("Đang kiểm tra")
    

def insert_data(data):
    plit_data = data.split(",")
    column_values = ", ".join(plit_data)
    sql_query = f"INSERT INTO HangHoaLuuKho (MaHang, TenHang, TrangThai) VALUES ({column_values})"
    # sql_query = f"INSERT INTO HangHoaLuuKho (MaHang,TenHang,TrangThai) VALUES ({0},{1},{2})".format(plit_data[0],plit_data[1],plit_data[2])
    try:
    
        cursor = conn.cursor()
        cursor.execute(sql_query)
    except:
                print("Lỗi chèn dữ liệu vào DataBase")
    else:
        print("Thêm dữ liệu vào DataBase thành công")
        cursor.commit()
    

t1 = threading.Thread(target=handleStatus)
t2 = threading.Thread(target=connetDataBase)
button = tk.Button(
    root,
    text='Bấm thử xem',
    # command=t2.start
    
)
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-9Q5LPOB\SQLEXPRESS'
DATABASE_NAME = 'QLBH_N01_SV'

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

button.pack()
capturedVideo()
# insert_data()
root.mainloop()



