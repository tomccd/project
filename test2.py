import pyodbc as odbc
import pandas as pd
import sys

# Thiết lập kết nối với SQL Server
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



# try:
#     df = pd.read_sql('SELECT * FROM Bang_Tong_Kho',conn)
# except:
#     print("Kiểm tra lại bảng liên kết")
# else:
#     print(df['MaHang'].values)
# # Tạo một cursor từ kết nối
# cursor = conn.cursor()

# # Thực thi câu lệnh SQL để lấy dữ liệu
# cursor.execute("SELECT * FROM Bang_Tong_Kho WHERE MaHang = 001")

# # Lấy dữ liệu từ câu lệnh SQL
# row = cursor.fetchone()

# # Kiểm tra xem có dữ liệu được trả về không
# if row is not None:
#     # Chuyển đổi dữ liệu thành list và gán vào biến
#     data = [element for element in row]
# else:
#     data = []

# if data[0] in df['MaHang'].values:
#     print("Exis")
# a = df['MaHang'].values



data_tuple = ('002', 'Cookie', 'Holland', '130$', '190$', 6, 'Food', '2024-04-07 10:07:59')
# Biến đổi tuple thành một chuỗi dữ liệu có thể chèn được
# Biến đổi tuple thành một chuỗi dữ liệu có thể chèn được
data_to_insert = ','.join([f"'{value}'" if isinstance(value, str) else str(value) for value in data_tuple])

print(data_to_insert, data_tuple)
print(type(data_to_insert), type(data_tuple))

sql_query = f"INSERT INTO Bang_Nhap_Kho (MaHang,TenHang,XuatXu,GiaNhap,GiaBan,SoLuongNhap,KhuVuc,ThoiGianNhap) VALUES (?,?,?,?,?,?,?,?)"
try:
    cursor = conn.cursor()
    # Thực thi câu lệnh SQL
    cursor.execute(sql_query,data_tuple)
    conn.commit()  # Bạn cần commit ở connection, không phải ở cursor
    print(f"Thêm dữ liệu vào Bang_Nhap_Kho thành công")
except Exception as e:
    print(f"Lỗi chèn dữ liệu: {e}")
finally:
    cursor.close()





# Lưu các thay đổi vào cơ sở dữ liệu
    conn.commit()




# # print(type(a))
# print(type(data))

# # In dữ liệu
# print(data)
# print(data[0])


