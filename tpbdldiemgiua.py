import numpy as np
import math

def midpoint_table_with_runge(X, Y, g_func=None):
    """
    Tính tích phân Điểm giữa và sai số Runge từ bảng dữ liệu.
    
    Tham số:
    - X, Y: Mảng dữ liệu đầu vào.
    - g_func: Hàm biến đổi G(x, y). Nếu None, mặc định là y.
              Dùng để giải các bài toán tích phân hàm hợp.
    """
    n = len(X) - 1
    h = X[1] - X[0]
    
    # Hàm mặc định nếu không truyền g_func
    if g_func is None:
        def g_func(x, y): return y

    print("\n" + "="*70)
    print("PHƯƠNG PHÁP ĐIỂM GIỮA TRÊN BẢNG DỮ LIỆU (CÓ SAI SỐ RUNGE)")
    print("="*70)
    print(f"Số khoảng chia n = {n}")
    print(f"Bước nhảy gốc h = {h}")
    
    # --- KIỂM TRA ĐIỀU KIỆN ---
    if n % 4 != 0:
        print("\n[CẢNH BÁO QUAN TRỌNG]")
        print(f"n = {n} không chia hết cho 4.")
        print("-> Chỉ có thể tính giá trị gần đúng I, KHÔNG thể tính sai số Runge.")
        print("-> Lý do: Lưới thưa cần gộp 4 khoảng h thành 1 khoảng lớn.")
        can_calc_runge = False
    else:
        can_calc_runge = True

    # =================================================================
    # BƯỚC 1: TÍNH I_h TRÊN LƯỚI MỊN (Độ rộng 2h)
    # =================================================================
    print(f"\n1. TÍNH I_h (Trên toàn bộ lưới):")
    print(f"   - Gộp các đoạn [xi, xi+2] có độ rộng 2h = {2*h}")
    print(f"   - Điểm giữa là các chỉ số LẺ: 1, 3, 5... {n-1}")
    print("-" * 70)
    print(f"{'i (giữa)':<10} | {'xi':<12} | {'yi':<12} | {'Val = G(xi,yi)':<15}")
    print("-" * 70)
    
    sum_fine = 0.0
    # Duyệt các chỉ số lẻ: 1, 3, 5 ...
    for i in range(1, n, 2):
        val = g_func(X[i], Y[i])
        sum_fine += val
        print(f"{i:<10} | {X[i]:<12.4f} | {Y[i]:<12.4f} | {val:<15.6f}")
        
    print("-" * 70)
    I_h = 2 * h * sum_fine
    print(f"Tổng S_fine = {sum_fine:.6f}")
    print(f"=> I_h ≈ 2h * S_fine = {2*h:.4f} * {sum_fine:.6f} = {I_h:.8f}")

    if not can_calc_runge:
        return I_h, None

    # =================================================================
    # BƯỚC 2: TÍNH I_2h TRÊN LƯỚI THƯA (Độ rộng 4h)
    # =================================================================
    print(f"\n2. TÍNH I_2h (Trên lưới thưa - Để đánh giá sai số):")
    print(f"   - Gộp các đoạn lớn [xi, xi+4] có độ rộng 4h = {4*h}")
    print(f"   - Điểm giữa mới là các chỉ số: 2, 6, 10... {n-2}")
    print("-" * 70)
    print(f"{'i (giữa)':<10} | {'xi':<12} | {'yi':<12} | {'Val = G(xi,yi)':<15}")
    print("-" * 70)
    
    sum_coarse = 0.0
    # Duyệt các chỉ số: 2, 6, 10 ... (Bước nhảy là 4)
    for i in range(2, n, 4):
        val = g_func(X[i], Y[i])
        sum_coarse += val
        print(f"{i:<10} | {X[i]:<12.4f} | {Y[i]:<12.4f} | {val:<15.6f}")
        
    print("-" * 70)
    I_2h = 4 * h * sum_coarse
    print(f"Tổng S_coarse = {sum_coarse:.6f}")
    print(f"=> I_2h ≈ 4h * S_coarse = {4*h:.4f} * {sum_coarse:.6f} = {I_2h:.8f}")

    # =================================================================
    # BƯỚC 3: ĐÁNH GIÁ SAI SỐ RUNGE
    # =================================================================
    # Phương pháp điểm giữa có bậc chính xác p=2 -> Chia cho 2^2 - 1 = 3
    sai_so = abs(I_h - I_2h) / 3
    I_best = I_h + sai_so # Hoặc I_h + (Ih - I2h)/3 (Công thức Extrapolation)
    
    print(f"\n3. ĐÁNH GIÁ SAI SỐ (Nguyên lý Runge p=2):")
    print(f"   Delta = |I_h - I_2h| / (2^2 - 1)")
    print(f"   Delta = |{I_h:.6f} - {I_2h:.6f}| / 3")
    print(f"   Delta ≈ {sai_so:.8f}")
    
    print(f"\n=> KẾT QUẢ CUỐI CÙNG (Đã bù sai số):")
    print(f"   I ≈ {I_best:.8f}")
    
    return I_best, sai_so

# =================================================================
# MAIN - VÍ DỤ ÁP DỤNG
# =================================================================
if __name__ == "__main__":
    # GIẢ SỬ ĐỀ BÀI: 
    # Cho bảng dữ liệu của hàm f(x) = x^2 trên đoạn [0, 4]
    # Cần tính tích phân: Integral [ x*f(x) + sqrt(x) ] dx
    
    # 1. Tạo dữ liệu mẫu (n=8 để chia hết cho 4 -> tính được Runge)
    # Các điểm: 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0
    X_data = np.linspace(0, 4, 9) 
    Y_data = X_data**2 # f(x)
    
    # 2. Định nghĩa hàm dưới dấu tích phân G(x, y)
    def ham_de_bai(x, y):
        # y ở đây chính là f(x) từ bảng
        return x * y + math.sqrt(x)

    # 3. Gọi hàm tính toán
    midpoint_table_with_runge(X_data, Y_data, g_func=ham_de_bai)