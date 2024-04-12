import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pypyodbc as odbc
import pyodbc
import sys
import cv2

root = tk.Tk()
root.geometry("800x800")

# Thay đổi các thông số kết nối dựa trên cấu hình của bạn

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

    # Kết nối đến SQL Server

    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    # sql_query = "INSERT INTO Sv (Ma_sinh_vien,Ho_va_ten,Lop,Tuoi) VALUES (201614668,'thanhNguyen','29a',18)"
    sql_query = "DELETE FROM Sv WHERE Tuoi=23;"
   
    
    # Thực hiện một số thao tác, ví dụ: lấy dữ liệu từ một bảng;'
    # thực hiện câu lệnh
    cursor.execute(sql_query) 
    # rowcount = cursor.rowcount
     # lưu dữ liệu vào
    cursor.commit() 
    # Lấy tất cả các dòng từ kết quả truy vấn
    # if rowcount > 0:
    #     messagebox.showinfo("Thành công", "Thêm bản ghi thành công!")
    # else:
    #     messagebox.showerror("Lỗi", "Thêm bản ghi thất bại!")
    # In kết quả

    # rows = cursor.fetchall()
    # for row in rows:
    #     print(rows)


    # df = pd.read_sql('Select * From Sv',connection)
    # print(df.to_string())
except Exception as e:
    print(f"Error: {e}")


root.mainloop()