import math

def tinh_dao_ham_tai_x(target_x, X, Y, p, hien_thi_chi_tiet=True):
    """
    Hàm đa năng: Tính đạo hàm tại target_x.
    - Tự động chọn cửa sổ nội suy.
    - Tự động phát hiện trùng mốc để dùng công thức tối ưu.
    - In ra bảng chi tiết các thành phần w_j, y_j nếu cần (phục vụ báo cáo).
    """
    n = len(X)
    
    # 1. Tìm vị trí mốc gần nhất để làm tâm
    closest_idx = 0
    min_dist = float('inf')
    for i in range(n):
        dist = abs(X[i] - target_x)
        if dist < min_dist:
            min_dist = dist
            closest_idx = i
            
    # 2. Xác định cửa sổ [start, end]
    start = closest_idx - (p // 2)
    if start < 0: start = 0
    if start + p >= n: start = n - 1 - p
    end = start + p
    
    window_X = X[start : end+1]
    window_Y = Y[start : end+1]
    
    if hien_thi_chi_tiet:
        print(f"\n*> Đang tính f'({target_x}):")
        print(f"   - Chọn cửa sổ nội suy: {window_X}")
        print(f"   - Bảng tính các thành phần (Formula Terms):")
        print(f"     {'xj':<10} | {'yj':<10} | {'wj (Trọng số)':<15} | {'wj * yj':<15}")
        print("     " + "-"*56)

    # 3. Kiểm tra trùng mốc
    trung_moc_idx = -1
    for k in range(len(window_X)):
        if abs(window_X[k] - target_x) < 1e-12:
            trung_moc_idx = k
            break
            
    f_prime = 0.0
    
    # 4. Tính toán từng số hạng
    for j in range(len(window_X)):
        xj = window_X[j]
        yj = window_Y[j]
        w_j = 0.0
        
        # --- TÍNH TRỌNG SỐ w_j ---
        if trung_moc_idx != -1:
            # === TRƯỜNG HỢP: TẠI MỐC (Dùng công thức nút) ===
            xi = window_X[trung_moc_idx]
            if j == trung_moc_idx:
                for m in range(len(window_X)):
                    if m != j: w_j += 1.0 / (xi - window_X[m])
            else:
                product = 1.0
                for m in range(len(window_X)):
                    if m != j and m != trung_moc_idx:
                        product *= (xi - window_X[m]) / (xj - window_X[m])
                w_j = (1.0 / (xj - xi)) * product
        else:
            # === TRƯỜNG HỢP: ĐIỂM BẤT KỲ (Dùng công thức tổng quát) ===
            Lj_val = 1.0
            for m in range(len(window_X)):
                if m != j:
                    Lj_val *= (target_x - window_X[m]) / (xj - window_X[m])
            
            sum_inv = 0.0
            for k in range(len(window_X)):
                if k != j:
                    sum_inv += 1.0 / (target_x - window_X[k])
            
            w_j = Lj_val * sum_inv

        # --- CỘNG DỒN VÀ IN KẾT QUẢ ---
        term = w_j * yj
        f_prime += term
        
        if hien_thi_chi_tiet:
            print(f"     {xj:<10} | {yj:<10.5f} | {w_j:<15.5f} | {term:<15.5f}")

    if hien_thi_chi_tiet:
        print("     " + "-"*56)
        print(f"   -> Tổng cộng f'({target_x}) ≈ {f_prime:.6f}")
        
    return f_prime

# --- CHƯƠNG TRÌNH CHÍNH (MAIN) ---
if __name__ == "__main__":
    # Dữ liệu mẫu (Data từ câu 19)
    # Bạn hãy copy đủ list dữ liệu vào đây nhé
    X_input = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    Y_input = [1.888, 2.040, 2.183, 2.317, 2.440, 2.552, 2.655, 2.746, 2.827, 2.898, 2.959]

    p_degree = 3 # Bậc 3 (4 điểm)
    
    # === BÀI TOÁN 1: TÍNH TOÀN BỘ BẢNG (IN DẠNG TỔNG HỢP) ===
    print(f"=== BÀI TOÁN 1: TÍNH ĐẠO HÀM TẠI MỌI ĐIỂM TRONG BẢNG ===")
    print(f"{'x':<10} | {'f\'(x) gan dung':<15}")
    print("-" * 30)
    
    results = []
    for x_val in X_input:
        # Tắt chi tiết (False) để chỉ lấy kết quả cuối cho bảng tổng hợp
        val = tinh_dao_ham_tai_x(x_val, X_input, Y_input, p_degree, hien_thi_chi_tiet=False)
        results.append(val)
        print(f"{x_val:<10} | {val:.6f}")
        
    print("\n" + "="*60 + "\n")
    
    # === BÀI TOÁN 2: TÍNH TẠI ĐIỂM BẤT KỲ (CÓ CHI TIẾT) ===
    print(f"=== BÀI TOÁN 2: TÍNH CHI TIẾT TẠI ĐIỂM BẤT KỲ (VÍ DỤ x = 1.15) ===")
    x_bat_ky = 1.15
    tinh_dao_ham_tai_x(x_bat_ky, X_input, Y_input, p_degree, hien_thi_chi_tiet=True)
    
    print("\n" + "="*60 + "\n")

    # === BÀI TOÁN 3: KIỂM TRA LẠI TẠI MỘT MỐC CÓ SẴN (CÓ CHI TIẾT) ===
    print(f"=== BÀI TOÁN 3: TÍNH CHI TIẾT TẠI MỘT MỐC NỘI SUY (VÍ DỤ x = 1.2) ===")
    # Chọn một điểm có trong X_input để kiểm tra logic "Trùng mốc"
    x_moc = 1.2 
    tinh_dao_ham_tai_x(x_moc, X_input, Y_input, p_degree, hien_thi_chi_tiet=True)