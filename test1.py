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
import pypyodbc as odbc
import traceback

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

##############################################################################################################################


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
counter = 1
def nhapKho():
    global counter
    counter = 1
    table.delete(*table.get_children())
    nameTable.config(text="Bảng nhập kho")
    table.config(columns=colum_NhapKho)
    table.heading("#0", text="STT")
    table.heading("0", text="Mã hàng")
    table.heading("1", text="Tên hàng")
    table.heading("2", text="Xuất xứ")
    table.heading("3", text="Giá nhập")
    table.heading("4", text="Giá xuất")
    table.heading("5", text="Số lượng")
    table.heading("6", text="Khu Vực")
    table.heading("7", text="Thời gian nhập")
    table.column("#0", width=150)
    table.column("6",widt=150)
    table.pack(fill="both",padx=0,pady=350)

def xuatKho():
    table.delete(*table.get_children())
    global counter
    counter = 1
    nameTable.config(text="Bảng xuất kho")
    table.config(columns=colum_NhapKho)
    table.heading("#0", text="STT")
    table.heading("0", text="Mã hàng")
    table.heading("1", text="Tên hàng")
    table.heading("2", text="Xuất xứ")
    table.heading("3", text="Giá nhập")
    table.heading("4", text="Giá xuất")
    table.heading("5", text="Số lượng")
    table.heading("6", text="Khu Vực")
    table.heading("7", text="Thời gian xuất")
    table.column("#0", width=150)
    table.column("6",widt=150)
    table.pack(fill="both",padx=0,pady=350)

def tongKho():
    table.delete(*table.get_children())
    global counter
    counter = 1
    nameTable.config(text="Bảng tổng kho")
    table.config(columns=colum_NhapKho)
    table.heading("#0", text="STT")
    table.heading("0", text="Mã hàng")
    table.heading("1", text="Tên hàng")
    table.heading("2", text="Xuất xứ")
    table.heading("3", text="Giá nhập")
    table.heading("4", text="Giá xuất")
    table.heading("5", text="Số lượng")
    table.heading("6", text="Khu Vực")
    table.column("#0", width=150)
    table.column("6",widt=150)
    table.pack(fill="both",padx=0,pady=350)

agreement = tk.StringVar()
r = ttk.Radiobutton(
        frame2,
        text="Nhập kho",
        value="1",
        variable=agreement,
        command=nhapKho
    ).place(x=20,y=550)

r1 = ttk.Radiobutton(
        frame2,
        text="Xuất kho",
        value="2",
        variable=agreement,
        command=xuatKho
    ).place(x=20,y=600)
r2 = ttk.Radiobutton(
        frame2,
        text="Tổng kho",
        value="3",
        variable=agreement,
        command=tongKho
    ).place(x=20,y=650)



##############################################################################################################################
def add_data():
# Lấy ngày/giờ hiện tại
    global counter
    # global agreement
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Thêm dữ liệu mới vào bảng
    table.insert("", "end", text=str(counter), values=(f"Mã hàng$$","Nội dung $$",current_time))
    counter += 1
    print(agreement.get())










tk.Button(frame2,text="xx",
          command=add_data).place(x=0,y=700)















root.mainloop()
