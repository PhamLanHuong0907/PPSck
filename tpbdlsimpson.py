import numpy as np
import math

def simpson_table_with_runge(X, Y, g_func=None):
    """
    Tính tích phân Simpson 1/3 và sai số Runge từ bảng dữ liệu.
    
    Tham số:
    - X, Y: Mảng dữ liệu đầu vào.
    - g_func: Hàm biến đổi G(x, y). Nếu None, mặc định là y.
    """
    n = len(X) - 1
    h = X[1] - X[0]
    
    # Hàm mặc định nếu không truyền g_func
    if g_func is None:
        def g_func(x, y): return y

    print("\n" + "="*80)
    print("PHƯƠNG PHÁP SIMPSON 1/3 TRÊN BẢNG DỮ LIỆU (CÓ SAI SỐ RUNGE)")
    print("="*80)
    print(f"Số khoảng chia n = {n}")
    print(f"Bước nhảy gốc h = {h}")
    
    # --- KIỂM TRA ĐIỀU KIỆN ---
    # 1. Để tính Simpson thường: n phải CHẴN.
    if n % 2 != 0:
        print("\n[LỖI NGHIÊM TRỌNG]")
        print(f"n = {n} là số LẺ -> Không thể dùng Simpson 1/3.")
        return None, None

    # 2. Để tính sai số Runge: n phải CHIA HẾT CHO 4.
    # Lý do: Lưới thưa có n/2 khoảng. Để Simpson chạy được trên lưới thưa thì n/2 phải chẵn => n chia hết 4.
    if n % 4 != 0:
        print("\n[CẢNH BÁO]")
        print(f"n = {n} chia hết cho 2 nhưng KHÔNG chia hết cho 4.")
        print("-> Tính được I_h nhưng KHÔNG tính được sai số Runge (lưới thưa bị lẻ).")
        can_calc_runge = False
    else:
        can_calc_runge = True

    # =================================================================
    # BƯỚC 1: TÍNH I_h TRÊN LƯỚI MỊN (Bước h)
    # =================================================================
    print(f"\n1. TÍNH I_h (Trên toàn bộ lưới n={n}):")
    print(f"   Công thức: h/3 * [y0 + yn + 4*(Lẻ) + 2*(Chẵn)]")
    print("-" * 80)
    print(f"{'i':<4} | {'xi':<10} | {'G(xi,yi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 80)
    
    sum_weighted_fine = 0.0
    
    for i in range(n + 1):
        val = g_func(X[i], Y[i])
        
        # Xác định hệ số Simpson chuẩn: 1 - 4 - 2 - 4 ... - 1
        if i == 0 or i == n:
            weight = 1
        elif i % 2 != 0: # Chỉ số lẻ
            weight = 4
        else:            # Chỉ số chẵn
            weight = 2
            
        term = weight * val
        sum_weighted_fine += term
        
        print(f"{i:<4} | {X[i]:<10.4f} | {val:<12.4f} | {weight:<6} | {term:<12.4f}")
        
    print("-" * 80)
    # Công thức: (h/3) * Tổng trọng số
    I_h = (h / 3) * sum_weighted_fine
    
    print(f"Tổng thành phần S_fine = {sum_weighted_fine:.6f}")
    print(f"=> I_h ≈ (h/3) * S_fine = ({h}/3) * {sum_weighted_fine:.6f} = {I_h:.8f}")

    if not can_calc_runge:
        return I_h, None

    # =================================================================
    # BƯỚC 2: TÍNH I_2h TRÊN LƯỚI THƯA (Bước 2h)
    # =================================================================
    print(f"\n2. TÍNH I_2h (Trên lưới thưa, chỉ lấy điểm chẵn của lưới cũ):")
    print(f"   Bước nhảy mới: H = 2h = {2*h}")
    print(f"   Các điểm sử dụng (Index cũ): 0, 2, 4, 6... {n}")
    print("-" * 80)
    print(f"{'i_cu':<6} | {'xi':<10} | {'G(xi,yi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 80)
    
    sum_weighted_coarse = 0.0
    
    # Duyệt lưới thưa: Index cũ nhảy cóc 2 đơn vị (0, 2, 4...)
    # Gọi j là index mới trên lưới thưa: j = 0, 1, 2... tương ứng với i = 0, 2, 4...
    # Số khoảng chia mới n_new = n / 2
    
    for i in range(0, n + 1, 2):
        val = g_func(X[i], Y[i])
        
        # Logic tính hệ số trên lưới thưa:
        # i=0 (Đầu) -> 1
        # i=n (Cuối) -> 1
        # Các điểm giữa:
        # Nếu i chia hết cho 4 (0, 4, 8...) -> Đóng vai trò điểm CHẴN trên lưới mới -> 2
        # Nếu i chia 4 dư 2 (2, 6, 10...)  -> Đóng vai trò điểm LẺ trên lưới mới  -> 4
        
        if i == 0 or i == n:
            weight = 1
        elif i % 4 != 0: # Ví dụ 2, 6, 10... (Lẻ trong lưới mới)
            weight = 4
        else:            # Ví dụ 4, 8, 12... (Chẵn trong lưới mới)
            weight = 2
            
        term = weight * val
        sum_weighted_coarse += term
        
        print(f"{i:<6} | {X[i]:<10.4f} | {val:<12.4f} | {weight:<6} | {term:<12.4f}")
        
    print("-" * 80)
    # Công thức: (2h / 3) * Tổng
    I_2h = (2 * h / 3) * sum_weighted_coarse
    
    print(f"Tổng thành phần S_coarse = {sum_weighted_coarse:.6f}")
    print(f"=> I_2h ≈ (2h/3) * S_coarse = {2*h/3:.4f} * {sum_weighted_coarse:.6f} = {I_2h:.8f}")

    # =================================================================
    # BƯỚC 3: ĐÁNH GIÁ SAI SỐ RUNGE
    # =================================================================
    # Phương pháp Simpson có bậc chính xác p=4 -> Chia cho 2^4 - 1 = 15
    sai_so = abs(I_h - I_2h) / 15
    I_best = I_h + sai_so 
    
    print(f"\n3. ĐÁNH GIÁ SAI SỐ (Runge p=4 cho Simpson):")
    print(f"   Delta = |I_h - I_2h| / 15")
    print(f"   Delta = |{I_h:.6f} - {I_2h:.6f}| / 15")
    print(f"   Delta ≈ {sai_so:.8f}")
    
    print(f"\n=> KẾT QUẢ CUỐI CÙNG (I + Delta):")
    print(f"   I ≈ {I_best:.8f}")
    
    return I_best, sai_so

# =================================================================
# MAIN - VÍ DỤ ÁP DỤNG
# =================================================================
if __name__ == "__main__":
    # GIẢ SỬ ĐỀ BÀI: 
    # Tính Integral [ x*f(x) + sqrt(x) ] dx trên [0, 4]
    
    # 1. Tạo dữ liệu mẫu (n=8 để chia hết cho 4 -> tính được Runge)
    # Các điểm: 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0
    X_data = np.linspace(0, 4, 9) 
    Y_data = X_data**2 # f(x) giả định
    
    # 2. Định nghĩa hàm dưới dấu tích phân G(x, y)
    def ham_phuc_tap(x, y):
        return x * y + math.sqrt(x)

    # 3. Gọi hàm tính toán
    simpson_table_with_runge(X_data, Y_data, g_func=ham_phuc_tap)