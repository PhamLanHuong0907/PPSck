import math

# ==========================================
# 1. KHAI BÁO HÀM SỐ VÀ ĐẠO HÀM
# ==========================================
def ham_f(x):
    """Hàm số cần tính: f(x) = e^(-x^2)"""
    return math.exp(-x**2)

def dao_ham_cap_2(x):
    """
    Trả về |f''(x)| để tìm M2.
    f(x) = e^(-x^2) -> f''(x) = (4x^2 - 2) * e^(-x^2)
    """
    return abs((4*x**2 - 2) * math.exp(-x**2))

# ==========================================
# 2. CÁC HÀM TIỆN ÍCH (HELPER)
# ==========================================
def tim_M2_tu_dong(a, b, step_check=1000):
    """Quét mẫu để tìm Max |f''(x)| trên [a, b]"""
    max_val = 0
    h_scan = (b - a) / step_check
    for i in range(step_check + 1):
        val = dao_ham_cap_2(a + i * h_scan)
        if val > max_val:
            max_val = val
    return max_val

def in_dong_bang(i, x, y, he_so, thanh_phan):
    """Hàm hỗ trợ in 1 dòng của bảng cho thẳng hàng"""
    print(f"{i:<6} | {x:<12.6f} | {y:<12.6f} | {he_so:<6} | {thanh_phan:<12.6f}")

# ==========================================
# 3. THUẬT TOÁN HÌNH THANG (TỰ ĐỘNG TÌM n)
# ==========================================
def giai_bai_toan_hinh_thang(a, b, epsilon, manual_M2=None):
    print("\n" + "="*60)
    print(" GIẢI BÀI TOÁN TÍCH PHÂN - PHƯƠNG PHÁP HÌNH THANG")
    print("="*60)
    
    # --- BƯỚC 1: XÁC ĐỊNH M2 ---
    if manual_M2 is not None:
        M2 = manual_M2
        print(f"1. Đánh giá đạo hàm cấp 2 (Nhập tay): M2 = {M2}")
    else:
        M2_raw = tim_M2_tu_dong(a, b)
        M2 = math.ceil(M2_raw) # Làm tròn lên cho an toàn giống tính tay
        print(f"1. Đánh giá đạo hàm cấp 2 (Tự động):")
        print(f"   Max thực tế ≈ {M2_raw:.6f} -> Chọn M2 = {M2}")

    # --- BƯỚC 2: TÍNH n ---
    # Công thức sai số: |Rn| <= (M2 * (b-a)^3) / (12 * n^2) <= epsilon
    # => n >= sqrt( (M2 * (b-a)^3) / (12 * epsilon) )
    tu_so = M2 * ((b - a)**3)
    mau_so = 12 * epsilon
    n_min = math.sqrt(tu_so / mau_so)
    n = math.ceil(n_min)
    
    print(f"2. Xác định số đoạn chia n:")
    print(f"   Áp dụng: n >= sqrt( {M2}*{b-a}^3 / 12*{epsilon} )")
    print(f"   => n >= {n_min:.4f}")
    print(f"   => CHỌN n = {n}")

    # --- BƯỚC 3: TÍNH bƯỚC NHẢY h ---
    h = (b - a) / n
    print(f"3. Bước nhảy h = ({b}-{a})/{n} = {h:.8f}")

    # --- BƯỚC 4: LẬP BẢNG TÍNH ---
    print("\n4. Bảng tính chi tiết (Rút gọn):")
    print("-" * 60)
    print(f"{'i':<6} | {'xi':<12} | {'yi = f(xi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 60)

    S = 0 # Tổng các thành phần
    
    # Biến đếm để điều khiển việc in bảng (chỉ in 3 dòng đầu và 3 dòng cuối)
    limit_print = 3 
    
    for i in range(n + 1):
        xi = a + i * h
        yi = ham_f(xi)
        
        # Xác định hệ số (Hình thang: đầu cuối là 1, giữa là 2)
        if i == 0 or i == n:
            he_so = 1
        else:
            he_so = 2
            
        term = he_so * yi
        S += term
        
        # Logic in rút gọn
        if i < limit_print:
            in_dong_bang(i, xi, yi, he_so, term)
        elif i == limit_print:
            print(f"{'...':<6} | {'...':<12} | {'...':<12} | {'...':<6} | {'...':<12}")
        elif i > n - limit_print:
            in_dong_bang(i, xi, yi, he_so, term)

    print("-" * 60)
    print(f"Tổng S (đã nhân hệ số) = {S:.8f}")

    # --- BƯỚC 5: KẾT QUẢ ---
    I = (h / 2) * S
    print("\n5. Kết quả cuối cùng:")
    print(f"   I ≈ (h/2) * S")
    print(f"   I ≈ ({h:.8f}/2) * {S:.8f}")
    print(f"   I ≈ {I:.8f}")
    
    # Kiểm tra sai số thực tế (nếu biết giá trị đúng)
    # Tích phân e^-x^2 từ 0->2 là (sqrt(pi)/2 * erf(2))
    I_exact = 0.8820813907
    error = abs(I - I_exact)
    print(f"\n[Kiểm tra] Giá trị thực: {I_exact:.10f}")
    print(f"[Kiểm tra] Sai số thực  : {error:.10f} ", end="")
    if error < epsilon:
        print("(ĐẠT YÊU CẦU ✅)")
    else:
        print("(KHÔNG ĐẠT ❌)")

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    # Đề bài: Tính tích phân e^-x^2 trên [0, 2] sai số 10^-5
    # Trường hợp bài tập cho sẵn M2 = 2 thì truyền tham số manual_M2=2
    giai_bai_toan_hinh_thang(a=0, b=2, epsilon=1e-5, manual_M2=2)