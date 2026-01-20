import sys

def tinh_gia_tri_horner(coeffs, c):
    """
    Tính giá trị của đa thức P(x) tại điểm x = c bằng sơ đồ Horner.
    (Dựa theo thuật toán a) trong ảnh bạn cung cấp)
    (ĐÃ CẬP NHẬT ĐỂ IN RA TỪNG BƯỚC)

    Tham số:
    coeffs (list): Danh sách các hệ số A = [a_n, a_n-1, ..., a_0]
                   (LƯU Ý: hệ số bậc cao nhất A[0] = a_n ở ĐẦU danh sách).
    c (float or int): Điểm cần tính giá trị P(c).

    Trả về:
    float or int: Giá trị P(c), hoặc None nếu input không hợp lệ.
    """
    
    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    print(f"  A (mảng hệ số) = {coeffs}")
    print(f"  c (điểm cần tính) = {c}")
    
    # "n: Bậc của đa thức"
    # (len(coeffs) là n + 1)
    n = len(coeffs) - 1
    print(f"  n (bậc đa thức) = len(A) - 1 = {n}")

    # --- 2. Kiểm tra điều kiện input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    
    # "Bậc của đa thức n >= 0"
    print(f"  Kiểm tra n >= 0:")
    if n < 0: # Tương đương danh sách rỗng
        print(f"    Lỗi: n = {n}. Bậc đa thức phải >= 0 (danh sách hệ số không rỗng).")
        return None
    print(f"    -> n = {n} >= 0. Hợp lệ.")
    
    # "Mảng A phải có đúng n + 1 phần tử"
    print(f"  Kiểm tra mảng A có n + 1 phần tử:")
    # Điều này luôn đúng vì n được định nghĩa là len(coeffs) - 1
    print(f"    -> Hợp lệ (A có {len(coeffs)} phần tử, n + 1 = {n+1}).")

    # --- 3. Thiết lập điều kiện dừng ---
    # (Bước này trong ảnh chỉ mang tính mô tả)
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Phương pháp là một vòng lặp for với số lần lặp n = {n} đã biết trước.")
    print(f"  Do đó, không cần thiết lập điều kiện dừng đặc biệt.")

    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Khởi tạo P = a_n (phần tử A[0])
    P = coeffs[0]
    print(f"  [4.1] Khởi tạo P = a_n = A[0] = {P}")
    
    # Bước 4.2: Thiết lập vòng lặp for i chạy từ 1 đến n
    print(f"  [4.2] Thiết lập vòng lặp for i chạy từ 1 đến n={n}")
    
    for i in range(1, n + 1):
        print(f"    --- i = {i} ---")
        
        # Lưu giá trị P cũ để in ra cho rõ ràng
        P_old = P
        a_i = coeffs[i]
        
        # Bước 4.3 (Trong vòng lặp): Cập nhật P = a_i + P * c
        P = a_i + P_old * c
        
        print(f"    [4.3] Cập nhật P = a_i + P_truoc * c")
        print(f"          P = A[{i}] + P * c")
        print(f"          P = {a_i} + {P_old} * {c}")
        print(f"          P = {a_i} + {P_old * c}")
        print(f"          => P = {P}")
        
    # Bước 4.4: Sau vòng lặp, P là giá trị cuối cùng
    print(f"  [4.4] Sau vòng lặp, P = {P} là giá trị cuối cùng.")

    # --- 5. Xác định output ---
    print(f"[Bước 5] Xác định output:")
    print(f"  Giá trị P({c}) = {P}")
    
    return P

# --------------------------------------------------------------------
# PHẦN "FILE ỨNG DỤNG" ĐỂ CHẠY THỬ THUẬT TOÁN
# (Đã cập nhật để gọn gàng hơn)
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG THUẬT TOÁN HORNER TÍNH GIÁ TRỊ P(c) ---")
    
    # --- Ví dụ 1: ---
    # Xét đa thức: P(x) = 3x^3 - 2x^2 + 0x - 5
    # n = 3
    # A = [a_3, a_2, a_1, a_0] = [3, -2, 0, -5]
    he_so_A = [3, -2, 0, -5]
    
    # Tính giá trị tại c = 2
    diem_c = 2
    
    print(f"\n--- Ví dụ 1 ---")
    print(f"Đa thức có hệ số: {he_so_A}")
    print(f"Tính giá trị tại c = {diem_c}")
    
    # Gọi hàm (Hàm sẽ tự in các bước 1-5)
    gia_tri_P = tinh_gia_tri_horner(he_so_A, diem_c)
    
    if gia_tri_P is not None:
        # Bước 5 đã in kết quả, ta chỉ cần in dòng kiểm tra
        print(f"(Kiểm tra: Kết quả mong đợi là 11)")

    # --- Ví dụ 2: ---
    # Xét đa thức bậc 0: P(x) = 5
    # n = 0
    # A = [5]
    he_so_A_2 = [5]
    diem_c_2 = 100 # P(100) vẫn phải bằng 5
    
    print(f"\n--- Ví dụ 2 ---")
    print(f"Đa thức có hệ số: {he_so_A_2}")
    print(f"Tính giá trị tại c = {diem_c_2}")
    
    gia_tri_P_2 = tinh_gia_tri_horner(he_so_A_2, diem_c_2)
    if gia_tri_P_2 is not None:
        print(f"(Kiểm tra: Kết quả mong đợi là 5)")

    # --- Ví dụ 3: Input không hợp lệ ---
    print(f"\n--- Ví dụ 3 ---")
    print("Thử với danh sách hệ số rỗng:")
    # Hàm sẽ tự in lỗi ở Bước 2
    tinh_gia_tri_horner([], 3)