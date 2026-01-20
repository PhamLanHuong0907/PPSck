import numpy as np
import math

def trapezoidal_table_with_runge(X, Y, g_func=None):
    """
    Tính tích phân Hình thang và sai số Runge từ bảng dữ liệu.
    
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
    print("PHƯƠNG PHÁP HÌNH THANG TRÊN BẢNG DỮ LIỆU (CÓ SAI SỐ RUNGE)")
    print("="*80)
    print(f"Số khoảng chia n = {n}")
    print(f"Bước nhảy gốc h = {h}")
    
    # --- KIỂM TRA ĐIỀU KIỆN RUNGE ---
    # Để tạo lưới thưa (bước 2h), n phải chẵn.
    if n % 2 != 0:
        print("\n[CẢNH BÁO]")
        print(f"n = {n} là số LẺ.")
        print("-> Chỉ tính được I_h. KHÔNG tính được sai số Runge (vì không chia đôi lưới được).")
        can_calc_runge = False
    else:
        can_calc_runge = True

    # =================================================================
    # BƯỚC 1: TÍNH I_h TRÊN LƯỚI MỊN (Bước h)
    # =================================================================
    print(f"\n1. TÍNH I_h (Trên toàn bộ lưới n={n}):")
    print(f"   Công thức: h/2 * [y0 + yn + 2*(y1 + ... + yn-1)]")
    print("-" * 80)
    print(f"{'i':<4} | {'xi':<10} | {'yi':<10} | {'G(xi,yi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 80)
    
    sum_weighted_fine = 0.0
    
    for i in range(n + 1):
        val = g_func(X[i], Y[i])
        
        # Xác định hệ số: Đầu/Cuối là 1, Giữa là 2
        if i == 0 or i == n:
            weight = 1
        else:
            weight = 2
            
        term = weight * val
        sum_weighted_fine += term
        
        print(f"{i:<4} | {X[i]:<10.4f} | {Y[i]:<10.4f} | {val:<12.4f} | {weight:<6} | {term:<12.4f}")
        
    print("-" * 80)
    # Công thức: (h/2) * Tổng trọng số
    I_h = (h / 2) * sum_weighted_fine
    
    print(f"Tổng thành phần S_fine = {sum_weighted_fine:.6f}")
    print(f"=> I_h ≈ (h/2) * S_fine = ({h}/2) * {sum_weighted_fine:.6f} = {I_h:.8f}")

    if not can_calc_runge:
        return I_h, None

    # =================================================================
    # BƯỚC 2: TÍNH I_2h TRÊN LƯỚI THƯA (Bước 2h)
    # =================================================================
    print(f"\n2. TÍNH I_2h (Trên lưới thưa, chỉ lấy điểm chẵn):")
    print(f"   Bước nhảy mới: H = 2h = {2*h}")
    print(f"   Các điểm sử dụng: 0, 2, 4 ... {n}")
    print("-" * 80)
    print(f"{'i':<4} | {'xi':<10} | {'G(xi,yi)':<12} | {'Hệ số':<6} | {'Thành phần':<12}")
    print("-" * 80)
    
    sum_weighted_coarse = 0.0
    
    # Duyệt bước nhảy 2: 0, 2, 4... n
    for i in range(0, n + 1, 2):
        val = g_func(X[i], Y[i])
        
        # Xác định hệ số cho lưới thưa
        # Đầu (0) và Cuối (n) vẫn là 1
        # Các điểm ở giữa lưới thưa (2, 4, ... n-2) là 2
        if i == 0 or i == n:
            weight = 1
        else:
            weight = 2
            
        term = weight * val
        sum_weighted_coarse += term
        
        print(f"{i:<4} | {X[i]:<10.4f} | {val:<12.4f} | {weight:<6} | {term:<12.4f}")
        
    print("-" * 80)
    # Công thức: (2h / 2) * Tổng = h * Tổng
    I_2h = (2 * h / 2) * sum_weighted_coarse
    
    print(f"Tổng thành phần S_coarse = {sum_weighted_coarse:.6f}")
    print(f"=> I_2h ≈ (2h/2) * S_coarse = {h} * {sum_weighted_coarse:.6f} = {I_2h:.8f}")

    # =================================================================
    # BƯỚC 3: ĐÁNH GIÁ SAI SỐ RUNGE
    # =================================================================
    # Phương pháp Hình thang có bậc chính xác p=2 -> Chia cho 2^2 - 1 = 3
    sai_so = abs(I_h - I_2h) / 3
    I_best = I_h + sai_so 
    
    print(f"\n3. ĐÁNH GIÁ SAI SỐ (Runge p=2 cho Hình thang):")
    print(f"   Delta = |I_h - I_2h| / 3")
    print(f"   Delta = |{I_h:.6f} - {I_2h:.6f}| / 3")
    print(f"   Delta ≈ {sai_so:.8f}")
    
    print(f"\n=> KẾT QUẢ CUỐI CÙNG (I + Delta):")
    print(f"   I ≈ {I_best:.8f}")
    
    return I_best, sai_so

# =================================================================
# MAIN - VÍ DỤ ÁP DỤNG
# =================================================================
if __name__ == "__main__":
    # GIẢ SỬ ĐỀ BÀI (Giống ảnh cuối bạn gửi): 
    # Tính Integral [ x*f(x) + sqrt(x) ] dx trên [0, 4]
    
    # 1. Tạo dữ liệu mẫu (n=4 để chẵn -> tính được Runge)
    # Các điểm: 0, 1, 2, 3, 4
    X_data = np.array([2,
2.127,
2.254,
2.381,
2.508,
2.635,
2.762,
2.889,
3.016,
3.143,
3.27,
3.397,
3.524,
3.651,
3.778,
3.905,
4.032,
4.159,
4.286,
4.413,
4.54,
4.667,
4.794,
4.92099999999999,
5.04799999999999,
5.17499999999999,
5.30199999999999,
5.42899999999999,
5.55599999999999,
5.68299999999999,
5.80999999999999,
5.93699999999999,
6.06399999999999,
6.19099999999999,
6.31799999999999,
6.44499999999999,
6.57199999999999,
6.69899999999999,
6.82599999999999,
6.95299999999999,
7.07999999999999,
7.20699999999999,
7.33399999999999,
7.46099999999999,
7.58799999999999,
7.71499999999999,
7.84199999999999,
7.96899999999999,
8.09599999999999,
8.22299999999999,
8.34999999999999,
8.47699999999999,
8.60399999999999,
8.73099999999999,
8.85799999999999,
8.98499999999999,
9.11199999999999,
9.239,
9.366,
9.493,
9.62,
9.747,
9.874,
10.001,
10.128
]) 
    Y_data = np.array([1.91933,
1.47912,
1.0654,
0.68632,
0.34951,
0.06141,
-0.17236,
-0.34745,
-0.46072,
-0.51017,
-0.4952,
-0.41652,
-0.2761,
-0.07702,
0.17621,
0.47814,
0.8221,
1.20055,
1.60526,
2.02706,
2.4566,
2.88369,
3.29844,
3.69048,
4.04966,
4.36618,
4.63064,
4.83418,
4.96876,
5.02692,
5.0026,
4.89047,
4.68641,
4.38754,
3.99246,
3.50072,
2.91342,
2.23269,
1.46217,
0.60659,
-0.32824,
-1.33544,
-2.4074,
-3.5355,
-4.71049,
-5.92288,
-7.16253,
-8.41927,
-9.6829,
-10.94336,
-12.1908,
-13.41621,
-14.61062,
-15.7663,
-16.8762,
-17.93426,
-18.93567,
-19.87649,
-20.75433,
-21.56782,
-22.31714,
-23.0036,
-23.6298,
-24.1996,
-24.71799
]) # f(x) giả định
    
    # 2. Định nghĩa hàm dưới dấu tích phân G(x, y)
    def ham_phuc_tap(x, y):
        # Ví dụ: g(x) = x*f(x) + sqrt(x)
        # return x * y + math.sqrt(x)
        return y

    # 3. Gọi hàm tính toán
    trapezoidal_table_with_runge(X_data, Y_data, g_func=ham_phuc_tap)