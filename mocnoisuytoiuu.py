import math

def tim_moc_noi_suy_toi_uu(n, a, b):
    """
    Hàm tính n mốc nội suy tối ưu (mốc Chebyshev) trên khoảng [a, b]
    dựa trên thuật toán bạn đã cung cấp.
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT TỪNG BƯỚC)

    Tham số:
    n (int): Số lượng mốc nội suy cần tìm (n >= 1).
    a (float): Mút trái của khoảng nội suy.
    b (float): Mút phải của khoảng nội suy (phải thỏa mãn a < b).

    Trả về:
    list: Danh sách chứa n mốc nội suy, đã được sắp xếp tăng dần,
          hoặc None nếu input không hợp lệ.
    """
    
    # --- 1. Xác định input ---
    print(f"\n[Bước 1] Xác định input: n = {n}, a = {a}, b = {b}")

    # --- 2. Kiểm tra điều kiện của input ---
    print("[Bước 2] Kiểm tra điều kiện input...")
    if not isinstance(n, int) or n < 1:
        print(f"  Lỗi: n (số mốc) phải là số nguyên >= 1. Nhận được: {n}")
        return None
    
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        print(f"  Lỗi: a và b phải là số thực. Nhận được: a={a}, b={b}")
        return None

    if a >= b:
        print(f"  Lỗi: Khoảng nội suy không hợp lệ. Phải là a < b. Nhận được: a={a}, b={b}")
        return None
    
    print(f"  -> Input hợp lệ (n={n}, a={a}, b={b}).")

    # --- 3. Thiết lập tính toán ---
    # Khởi tạo một danh sách (mảng) rỗng, đặt tên là X
    X = []
    print(f"[Bước 3] Thiết lập tính toán: Khởi tạo danh sách X = {X}")

    # --- 4. Thực hiện tính toán (vòng lặp for i từ 0 đến n-1) ---
    print(f"[Bước 4] Thực hiện vòng lặp for i từ 0 đến {n-1}:")
    
    for i in range(n):
        print(f"  --- i = {i} ---")
        
        # Bước 4a: Tính mốc Chebyshev chuẩn hóa t_i trên đoạn [-1, 1]
        # (Sử dụng công thức ngược (n-1-i) như trong code gốc
        #  để khớp với mô tả "theo thứ tự ngược" trong ảnh,
        #  giúp đảm bảo mốc_noi_suy cuối cùng tăng dần)
        
        # Công thức tính t_i
        numerator_term = (2 * (n - 1 - i) + 1)
        numerator = numerator_term * math.pi
        denominator = (2 * n)
        t = math.cos(numerator / denominator)
        
        print(f"    [4a] Tính mốc t_{i} (chuẩn hóa trên [-1, 1]):")
        print(f"         Công thức: t = cos( (2*(n-1-i) + 1)*pi / (2*n) )")
        print(f"         Với n={n}, i={i}:")
        print(f"         t = cos( (2*({n}-1-{i}) + 1)*pi / (2*{n}) )")
        print(f"         t = cos( ({numerator_term})*pi / {denominator} )")
        print(f"         t = cos( {numerator / denominator:.6f} rad )")
        print(f"         => t = {t:.6f}")
        
        # Bước 4b: Ánh xạ mốc t_i từ [-1, 1] về đoạn [a, b]
        term1 = (a + b) / 2
        term2 = (b - a) / 2
        x = term1 + term2 * t
        
        print(f"    [4b] Ánh xạ mốc x_{i} về [{a}, {b}]:")
        print(f"         Công thức: x = (a+b)/2 + (b-a)/2 * t")
        print(f"         Với a={a}, b={b}, t={t:.6f}:")
        print(f"         x = ({a}+{b})/2 + ({b}-{a})/2 * {t:.6f}")
        print(f"         x = {term1} + {term2} * {t:.6f}")
        print(f"         => x = {x:.6f}")
        
        # Bước 4c: Lưu kết quả
        X.append(x)
        print(f"    [4c] Lưu kết quả:")
        print(f"         Thêm x = {x:.6f} vào danh sách X.")
        
        # In danh sách X hiện tại với các giá trị đã được định dạng
        formatted_X_so_far = [f"{val:.6f}" for val in X]
        print(f"         -> X hiện tại = {formatted_X_so_far}")
    
    print("  --- Kết thúc vòng lặp ---")

    # --- 5. Xác định output ---
    print(f"[Bước 5] Xác định output: Trả về danh sách X.")
    
    # In X với định dạng floats cuối cùng
    formatted_X_final = [f"{val:.6f}" for val in X]
    print(f"  -> Output cuối cùng: {formatted_X_final}")
    
    return X