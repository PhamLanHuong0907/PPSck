import numpy as np
import math

def newton_cotes_table_data(X, Y, n_order, g_func=None):
    """
    Tính tích phân Newton-Cotes bậc n (4, 5, 6) từ bảng dữ liệu.
    Sử dụng hệ số nguyên chuẩn SGK.
    
    Tham số:
    - X, Y: Mảng dữ liệu đầu vào.
    - n_order: Bậc của phương pháp (4: Boole, 5, 6: Weddle).
    - g_func: Hàm biến đổi G(x, y). Nếu None, mặc định là y.
    """
    num_points = len(X)
    actual_n = num_points - 1
    h = X[1] - X[0]
    
    # Hàm mặc định nếu không truyền g_func
    if g_func is None:
        def g_func(x, y): return y

    print("\n" + "="*85)
    print(f"PHƯƠNG PHÁP NEWTON-COTES (BẬC n={n_order}) TRÊN BẢNG DỮ LIỆU")
    print("="*85)
    
    # 1. KHO TÀNG HỆ SỐ (TRA CỨU)
    # Cấu trúc: {n: (Mẫu_số_chung_N, [Danh_sách_hệ_số_nguyên_H])}
    COEFFS_DICT = {
        4: (90,  [7, 32, 12, 32, 7]),                   # Boole's Rule
        5: (288, [19, 75, 50, 50, 75, 19]),             # n=5
        6: (840, [41, 216, 27, 272, 27, 216, 41])       # Weddle's Rule
    }

    # 2. KIỂM TRA ĐẦU VÀO
    if n_order not in COEFFS_DICT:
        print(f"Lỗi: Code này chỉ hỗ trợ n = 4, 5, 6. Bạn nhập n = {n_order}.")
        return None
        
    if actual_n != n_order:
        print(f"[CẢNH BÁO] Số khoảng dữ liệu thực tế ({actual_n}) KHÁC với bậc n yêu cầu ({n_order}).")
        print(f"-> Code sẽ chỉ lấy {n_order+1} điểm đầu tiên để tính minh họa.")
        # Cắt ngắn dữ liệu cho đúng n đoạn
        X = X[:n_order+1]
        Y = Y[:n_order+1]
    
    # Lấy hệ số tương ứng
    mau_so_N, he_so_H = COEFFS_DICT[n_order]

    print(f"Số khoảng chia n = {n_order}")
    print(f"Bước nhảy h = {h}")
    print(f"Mẫu số chung N = {mau_so_N}")
    print(f"Bộ hệ số nguyên H = {he_so_H}")
    
    # =================================================================
    # BƯỚC TÍNH TOÁN VÀ LẬP BẢNG
    # =================================================================
    print("-" * 85)
    print(f"{'i':<4} | {'xi':<10} | {'G(xi,yi)':<12} | {'Hi (Hệ số)':<10} | {'Hi * G':<15}")
    print("-" * 85)
    
    sum_weighted = 0.0
    
    for i in range(n_order + 1):
        # Tính giá trị hàm (có thể là f(x) hoặc công thức phức tạp)
        val = g_func(X[i], Y[i])
        
        # Lấy hệ số nguyên
        hi = he_so_H[i]
        
        # Tính thành phần
        term = hi * val
        sum_weighted += term
        
        print(f"{i:<4} | {X[i]:<10.4f} | {val:<12.4f} | {hi:<10} | {term:<15.4f}")
        
    print("-" * 85)
    
    # =================================================================
    # TÍNH KẾT QUẢ CUỐI CÙNG
    # Công thức SGK: I = (b - a) * (1/N) * Tổng_trọng_số
    # Hoặc: I = n*h * (1/N) * Tổng
    # =================================================================
    
    b_minus_a = X[-1] - X[0]
    I = b_minus_a * (1 / mau_so_N) * sum_weighted
    
    print(f"Tổng trọng số S = {sum_weighted:.6f}")
    print(f"Chiều dài đoạn [a, b] = {b_minus_a:.4f}")
    print(f"\nCông thức: I ≈ ((b-a) / N) * S")
    print(f"Kết quả:  I ≈ ({b_minus_a:.4f} / {mau_so_N}) * {sum_weighted:.6f}")
    print(f"          I ≈ {I:.8f}")
    
    return I

# =================================================================
# MAIN - VÍ DỤ ÁP DỤNG
# =================================================================
if __name__ == "__main__":
    # --- VÍ DỤ 1: n=6 (Giống Thí dụ 1 trong sách) ---
    # Hàm f(x) = 1/(1+x) trên [0, 1]
    
    # Tạo dữ liệu giả định (7 điểm cho n=6)
    X6 = np.linspace(0, 1, 7) 
    Y6 = 1 / (1 + X6)
    
    # Gọi hàm tính toán
    newton_cotes_table_data(X6, Y6, n_order=6)
    
    
    # --- VÍ DỤ 2: BÀI TOÁN PHỨC TẠP (n=4) ---
    # Tính Integral [ x*f(x) + sqrt(x) ] dx trên [0, 4]
    
    print("\n\n" + " "*20 + "--- VÍ DỤ BÀI TOÁN PHỨC TẠP (n=4) ---")
    
    # Tạo dữ liệu (5 điểm cho n=4)
    X4 = np.linspace(0, 4, 5) # 0, 1, 2, 3, 4
    Y4 = X4**2                # f(x) giả định
    
    # Định nghĩa hàm biến đổi G(x, y)
    def ham_phuc_tap(x, y):
        return x * y + math.sqrt(x)
        
    newton_cotes_table_data(X4, Y4, n_order=4, g_func=ham_phuc_tap)