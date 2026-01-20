import numpy as np

def tim_moc_bat_ky_toi_uu(x_data, y_data, x_target, k_moc):
    """
    Chọn k mốc bất kỳ gần x_target nhất.
    Không yêu cầu các mốc phải liền kề nhau trong bảng gốc.
    """
    # 1. Tính khoảng cách từ tất cả các điểm đến x_target
    distances = np.abs(x_data - x_target)
    
    # 2. Lấy chỉ số (index) của k điểm có khoảng cách nhỏ nhất
    # argsort trả về index từ bé đến lớn
    nearest_indices = np.argsort(distances)[:k_moc]
    
    # 3. Sắp xếp lại index tăng dần để đảm bảo x0 < x1 < ... < xk
    # (Quan trọng: Nội suy Newton yêu cầu mốc phải sắp xếp theo thứ tự)
    nearest_indices = np.sort(nearest_indices)
    
    # 4. Trích xuất dữ liệu
    x_out = x_data[nearest_indices]
    y_out = y_data[nearest_indices]
    
    return x_out, y_out

def tim_moc_cach_deu_toi_uu(x_data, y_data, x_target, k_moc):
    """
    Chọn k mốc CÁCH ĐỀU (liên tiếp) sao cho x_target nằm giữa.
    Bắt buộc phải lấy một đoạn liền mạch [i, i+k] từ dữ liệu gốc.
    """
    n_total = len(x_data)
    
    # 1. Tìm vị trí của điểm trong data gần x_target nhất
    distances = np.abs(x_data - x_target)
    idx_nearest = np.argmin(distances)
    
    # 2. Xác định cửa sổ trượt (window) sao cho idx_nearest nằm giữa
    # Bán kính về mỗi bên
    radius = k_moc // 2
    
    start_idx = idx_nearest - radius
    end_idx = start_idx + k_moc
    
    # 3. Xử lý trường hợp cửa sổ bị trượt ra ngoài biên mảng
    if start_idx < 0:
        # Nếu bị trào ra bên trái, đẩy cửa sổ về 0
        diff = 0 - start_idx
        start_idx += diff
        end_idx += diff
        
    if end_idx > n_total:
        # Nếu bị trào ra bên phải, đẩy cửa sổ lùi lại
        diff = end_idx - n_total
        start_idx -= diff
        end_idx -= diff
        
    # Đảm bảo index không âm (phòng trường hợp k_moc > n_total)
    start_idx = max(0, start_idx)
    end_idx = min(n_total, end_idx)
    
    # 4. Trích xuất
    x_out = x_data[start_idx:end_idx]
    y_out = y_data[start_idx:end_idx]
    
    # Kiểm tra nhanh xem có thực sự cách đều không (sai số nhỏ cho phép)
    diffs = np.diff(x_out)
    if not np.allclose(diffs, diffs[0], atol=1e-5):
        print("CẢNH BÁO: Các mốc trích xuất KHÔNG cách đều (dữ liệu gốc có thể bị lỗi).")
        
    return x_out, y_out

# =======================================================
# VÍ DỤ CHẠY THỬ
# =======================================================

# Giả sử bảng dữ liệu gốc (10 điểm)
# Lưu ý: Data này cách đều h=0.2
x_full = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8])
y_full = np.sin(x_full) 

x_val = 1.9  # Điểm cần tính
so_moc = 5   # Số mốc cần lấy

print(f"Dữ liệu gốc: {x_full}")
print(f"Cần tính tại x = {x_val} với {so_moc} mốc.\n")

# --- TEST 1: CHỌN MỐC BẤT KỲ ---
print("-" * 30)
print("1. CHỌN MỐC BẤT KỲ (Arbitrary)")
x_batky, y_batky = tim_moc_bat_ky_toi_uu(x_full, y_full, x_val, so_moc)
print(f"Các mốc chọn được: {x_batky}")
# Giải thích: Nó sẽ nhặt từng điểm gần nhất, không quan tâm thứ tự gốc, 
# sau đó sắp xếp lại. (Kết quả thường giống cách đều nếu data gốc tốt)

# --- TEST 2: CHỌN MỐC CÁCH ĐỀU ---
print("-" * 30)
print("2. CHỌN MỐC CÁCH ĐỀU (Equidistant)")
x_cachdeu, y_cachdeu = tim_moc_cach_deu_toi_uu(x_full, y_full, x_val, so_moc)
print(f"Các mốc chọn được: {x_cachdeu}")
h_step = x_cachdeu[1] - x_cachdeu[0]
print(f"Bước nhảy h = {h_step:.2f}")

# --- SAU ĐÓ BẠN NÉM VÀO HÀM GIẢI ---
# Ví dụ: solve_newton_forward_equidistant(x_cachdeu, y_cachdeu, x_val)