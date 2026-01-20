import numpy as np

def giai_noi_suy_ham_nguoc_chi_tiet(x_data, y_data, y_target, so_moc):
    """
    Giải và in chi tiết bài toán nội suy ngược (PP Hàm ngược).
    Input:
        x_data: Mảng giá trị x (nghiệm cần tìm).
        y_data: Mảng giá trị y (biến số của hàm ngược).
        y_target: Giá trị y_ban (y ngang) cần tìm x.
        so_moc: Số lượng mốc nội suy (k+1).
    """
    
    print("\n" + "="*70)
    print(f"{'GIẢI BÀI TOÁN NỘI SUY NGƯỢC (PHƯƠNG PHÁP HÀM NGƯỢC)':^70}")
    print("="*70 + "\n")
    
    print(f"Yêu cầu: Tìm x sao cho f(x) = {y_target}")
    print(f"Dữ liệu đầu vào: {len(x_data)} điểm. Số mốc sử dụng: {so_moc}")

    # --- BƯỚC 1: CHỌN MỐC TỐI ƯU ---
    print(f"\n" + "-"*30 + " BƯỚC 1: CHỌN MỐC TỐI ƯU " + "-"*30)
    # Tính khoảng cách từ các y_data đến y_target
    distances = np.abs(y_data - y_target)
    
    # Lấy chỉ số của k mốc gần nhất
    sorted_indices_by_dist = np.argsort(distances)
    selected_indices = sorted_indices_by_dist[:so_moc]
    
    # Sắp xếp lại theo giá trị y tăng dần để bảng tỷ sai phân đẹp và dễ tính
    # (Lưu ý: Với Newton mốc bất kỳ thì không bắt buộc, nhưng nên làm để dễ theo dõi)
    selected_indices = sorted(selected_indices, key=lambda i: y_data[i])
    
    # Trích xuất dữ liệu con
    # QUAN TRỌNG: Đảo vai trò -> y làm Mốc (Nodes), x làm Giá trị (Values)
    nodes_y = y_data[selected_indices]  # Đây là 'x' trong công thức Newton
    values_x = x_data[selected_indices] # Đây là 'y' trong công thức Newton
    
    print(f"Chọn {so_moc} điểm có giá trị y gần {y_target} nhất:")
    print(f"{'Index':<10} | {'y (Mốc)':<12} | {'x (Giá trị)':<12} | {'Khoảng cách':<12}")
    print("-" * 55)
    for i in range(so_moc):
        idx = selected_indices[i]
        dist = abs(y_data[idx] - y_target)
        print(f"{idx:<10} | {nodes_y[i]:<12.4f} | {values_x[i]:<12.4f} | {dist:<12.4f}")
        
    # --- BƯỚC 2: TÍNH BẢNG TỶ SAI PHÂN ---
    print(f"\n" + "-"*30 + " BƯỚC 2: BẢNG TỶ SAI PHÂN (Biến y) " + "-"*30)
    # Bảng tỷ sai phân g[...]
    # Cột 0 là nodes_y, Cột 1 là values_x, Cột 2 trở đi là sai phân
    n = so_moc
    table = np.zeros((n, n + 1))
    table[:, 0] = nodes_y
    table[:, 1] = values_x
    
    # Tính toán
    for j in range(2, n + 1): # Cột sai phân cấp j-1
        for i in range(n - j + 1):
            numerator = table[i+1][j-1] - table[i][j-1]
            denominator = table[i+j-1][0] - table[i][0] # Chia cho hiệu mốc (y)
            table[i][j] = numerator / denominator

    # In bảng
    headers = ["y_k", "x_k"] + [f"SD Cấp {k}" for k in range(1, n)]
    header_str = "".join([f"{h:<12}" for h in headers])
    print(header_str)
    print("-" * (12 * (n+1)))
    
    for i in range(n):
        row_str = ""
        for j in range(n + 1):
            val = table[i][j]
            if i < n - (j - 1):
                row_str += f"{val:<12.5f}"
            else:
                row_str += f"{'':<12}"
        print(row_str)

    # --- BƯỚC 3: XÂY DỰNG ĐA THỨC ---
    print(f"\n" + "-"*30 + " BƯỚC 3: ĐA THỨC NỘI SUY P(y) " + "-"*30)
    # Hệ số là hàng chéo trên cùng: table[0][1], table[0][2]...
    coeffs = table[0, 1:]
    
    print(f"Các hệ số Newton (a_i): {list(np.round(coeffs, 6))}")
    
    # Tạo chuỗi công thức
    poly_str = f"x ≈ P(y) = {coeffs[0]:.5f}"
    for i in range(1, n):
        sign = " + " if coeffs[i] >= 0 else " - "
        val = abs(coeffs[i])
        term = f"{sign}{val:.5f}"
        for k in range(i):
            term += f"(y - {nodes_y[k]:.4f})"
            
        # Ngắt dòng nếu dài
        if len(poly_str.split('\n')[-1]) > 60:
             poly_str += "\n           " + term
        else:
             poly_str += term
             
    print("Công thức đa thức nội suy hàm ngược:")
    print(f"           {poly_str}")

    # --- BƯỚC 4: TÍNH GIÁ TRỊ ---
    print(f"\n" + "-"*30 + f" BƯỚC 4: TÍNH TẠI y = {y_target} " + "-"*30)
    
    # Tính bằng Horner
    res = coeffs[n-1]
    details_str = f"Bat dau: {coeffs[n-1]:.6f}"
    
    for k in range(n-2, -1, -1):
        res = coeffs[k] + (y_target - nodes_y[k]) * res
        
    print(f"Thay y = {y_target} vào đa thức P(y):")
    print(f" -> Kết quả xấp xỉ: x ≈ {res:.6f}")
    
    return res

# ==============================================================================
# PHẦN NHẬP DỮ LIỆU CỦA BẠN (Thay đổi phần này)
# ==============================================================================

# Dữ liệu mẫu (Lấy từ ví dụ trong tài liệu 17_NoisuyNguoc.pdf)
# X: 1.2, 1.4, ...
# Y: 4.02, 3.98, ...
x_input = np.array([1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8])
y_input = np.array([4.02, 3.98, 4.23, 3.67, 2.99, 1.24, 0.87, 2.08, 4.54])

# Giá trị cần tìm nghiệm
y_can_tim = 1.0  # Ví dụ: Tìm x để y = 1.0

# Số mốc muốn dùng (Ví dụ dùng 4 mốc -> Đa thức bậc 3)
so_moc_noi_suy = 4

# GỌI HÀM
giai_noi_suy_ham_nguoc_chi_tiet(x_input, y_input, y_can_tim, so_moc_noi_suy)