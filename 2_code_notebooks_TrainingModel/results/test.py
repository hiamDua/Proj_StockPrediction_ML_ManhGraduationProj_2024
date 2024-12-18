import pandas as pd
import glob

# Đường dẫn tới các tệp .txt
file_paths = glob.glob("*.txt")  # Tìm tất cả các file .txt trong thư mục hiện tại

# Khởi tạo danh sách lưu dữ liệu
data = []

# Hàm đọc file và trích xuất dữ liệu
def extract_metrics(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        print(f"Processing file: {file_path}")  # Debugging line
        stock_name = file_path.split("/")[-1].split("_")[0]
        
        model = None
        test_r2, test_rmse, test_mape = None, None, None
        
        for line in lines:
            print(f"Line: {line.strip()}")  # Debugging line
            if "Model:" in line:
                model = line.split(":")[1].strip()
            if "TEST SET METRICS:" in line:  # Start collecting metrics after this line
                continue
            if "R2:" in line and model:  # Collect metrics only if model is defined
                test_r2 = float(line.split(":")[1].strip())
            if "RMSE:" in line and model:
                test_rmse = float(line.split(":")[1].strip())
            if "MAPE%:" in line and model:
                test_mape = float(line.split(":")[1].strip().replace('%', '').strip())  # Remove '%' before conversion
            
            # If all metrics are collected, append to data
            if model and test_r2 is not None and test_rmse is not None and test_mape is not None:
                data.append([stock_name, model, test_r2, test_rmse, test_mape])
                # Reset metrics for the next model
                model, test_r2, test_rmse, test_mape = None, None, None, None

# Đọc dữ liệu từ tất cả các file
for file_path in file_paths:
    extract_metrics(file_path)

# Tạo DataFrame
columns = ["Cổ phiếu", "Mô hình", "Test R²", "Test RMSE", "Test MAPE%"]
df = pd.DataFrame(data, columns=columns)

# Thêm cột Nhận xét
def generate_comments(row):
    if row["Test R²"] < 0:
        return "Mô hình không hiệu quả trên dữ liệu kiểm tra."
    elif row["Test MAPE%"] < 5:
        return "Hiệu suất tốt với MAPE thấp và R² cao."
    else:
        return "Hiệu suất khá nhưng cần cải thiện độ chính xác."

df["Nhận xét"] = df.apply(generate_comments, axis=1)

# Xuất bảng ra file CSV hoặc hiển thị
df.to_csv("output_metrics.csv", index=False)
print(df)
