import math

# ==========================================
# 1. KHAI BÁO HÀM SỐ VÀ ĐẠO HÀM
# ==========================================
def ham_f(x):
    """Hàm số cần tính: f(x) = e^(-x^2)"""
    return math.exp(-x**2)

def dao_ham_cap_4(x):
    """
    Trả về |f''''(x)| để tìm M4.
    f(x) = e^(-x^2)
    f''''(x) = (16x^4 - 48x^2 + 12) * e^(-x^2)
    """
    term = 16*x**4 - 48*x**2 + 12
    return abs(term * math.exp(-x**2))

# ==========================================
# 2. CÁC HÀM TIỆN ÍCH
# ==========================================
def tim_M4_tu_dong(a, b, step_check=1000):
    """Quét mẫu để tìm Max |f''''(x)| trên [a, b]"""
    max_val = 0
    h_scan = (b - a) / step_check
    for i in range(step_check + 1):
        val = dao_ham_cap_4(a + i * h_scan)
        if val > max_val:
            max_val = val
    return max_val

def in_dong_bang(i, x, y, he_so, thanh_phan):
    """Hàm in 1 dòng bảng ngay ngắn"""
    print(f"{i:<6} | {x:<12.6f} | {y:<12.6f} | {he_so:<6} | {thanh_phan:<12.6f}")

# ==========================================
# 3. THUẬT TOÁN SIMPSON (TỰ ĐỘNG TÌM n)
# ==========================================
def giai_bai_toan_simpson(a, b, epsilon, manual_M4=None):
    print("\n" + "="*65)
    print(" GIẢI BÀI TOÁN TÍCH PHÂN - PHƯƠNG PHÁP SIMPSON 1/3")
    print("="*65)
    
    # --- BƯỚC 1: XÁC ĐỊNH M4 ---
    if manual_M4 is not None:
        M4 = manual_M4
        print(f"1. Đánh giá đạo hàm cấp 4 (Nhập tay): M4 = {M4}")
    else:
        M4_raw = tim_M4_tu_dong(a, b)
        M4 = math.ceil(M4_raw) # Làm tròn lên giống tính tay
        print(f"1. Đánh giá đạo hàm cấp 4 (Tự động):")
        print(f"   Max thực tế ≈ {M4_raw:.6f} -> Chọn M4 = {M4}")

    # --- BƯỚC 2: TÍNH n ---
    # Sai số Simpson: |Rn| <= (M4 * (b-a)^5) / (180 * n^4)
    # => n >= căn_bậc_4( (M4 * (b-a)^5) / (180 * epsilon) )
    tu_so = M4 * ((b - a)**5)
    mau_so = 180 * epsilon
    n_min = (tu_so / mau_so)**0.25
    
    n = math.ceil(n_min)
    
    # Quan trọng: Simpson bắt buộc n chẵn
    if n % 2 != 0:
        n += 1
        note = "(Làm tròn lên số chẵn)"
    else:
        note = "(Đã chẵn)"
        
    print(f"2. Xác định số đoạn chia n:")
    print(f"   Áp dụng: n >= 4_sqrt( {M4}*(b-a)^5 / 180*{epsilon} )")
    print(f"   => n min >= {n_min:.4f}")
    print(f"   => CHỌN n = {n} {note}")

    # --- BƯỚC 3: TÍNH h ---
    h = (b - a) / n
    print(f"3. Bước nhảy h = ({b}-{a})/{n} = {h:.8f}")

    # --- BƯỚC 4: LẬP BẢNG TÍNH ---
    print("\n4. Bảng tính chi tiết (Rút gọn):")
    print("-" * 65)
    print(f"{'i':<6} | {'xi':<12} | {'yi = f(xi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 65)

    S = 0 
    limit_print = 3 # Chỉ in 3 dòng đầu/cuối nếu bảng quá dài
    
    for i in range(n + 1):
        xi = a + i * h
        yi = ham_f(xi)
        
        # --- XÁC ĐỊNH HỆ SỐ SIMPSON (QUAN TRỌNG) ---
        # Quy luật: 1 (đầu) - 4 (lẻ) - 2 (chẵn) - ... - 4 (lẻ) - 1 (cuối)
        if i == 0 or i == n:
            he_so = 1
        elif i % 2 != 0: # Chỉ số lẻ
            he_so = 4
        else:            # Chỉ số chẵn
            he_so = 2
            
        term = he_so * yi
        S += term
        
        # In bảng rút gọn
        if i < limit_print:
            in_dong_bang(i, xi, yi, he_so, term)
        elif i == limit_print:
             print(f"{'...':<6} | {'...':<12} | {'...':<12} | {'...':<6} | {'...':<12}")
        elif i > n - limit_print:
            in_dong_bang(i, xi, yi, he_so, term)

    print("-" * 65)
    print(f"Tổng S (đã nhân hệ số) = {S:.8f}")

    # --- BƯỚC 5: KẾT QUẢ ---
    I = (h / 3) * S
    print("\n5. Kết quả cuối cùng:")
    print(f"   I ≈ (h/3) * S")
    print(f"   I ≈ ({h:.8f}/3) * {S:.8f}")
    print(f"   I ≈ {I:.9f}")
    
    # Kiểm tra sai số
    I_exact = 0.8820813907
    error = abs(I - I_exact)
    print(f"\n[Kiểm tra] Giá trị thực: {I_exact:.10f}")
    print(f"[Kiểm tra] Sai số thực  : {error:.10f} ", end="")
    if error < epsilon:
        print("(ĐẠT ✅)")
    else:
        print("(KHÔNG ĐẠT ❌)")

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    # Đề bài: Tính tích phân e^-x^2 trên [0, 2] sai số 10^-5
    # Nếu đề bài cho M4 = 12 thì nhập manual_M4=12
    giai_bai_toan_simpson(a=0, b=2, epsilon=1e-5, manual_M4=12)