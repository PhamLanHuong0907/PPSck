import sys

def chia_horner(coeffs, c):
    """
    Thực hiện phép chia đa thức P(x) cho (x - c) bằng sơ đồ Horner.
    Trả về các hệ số của đa thức thương Q(x) và số dư R.
    (Dựa trên thuật toán (b) trong ảnh)
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT TỪNG BƯỚC)

    Tham số:
    coeffs (list): Danh sách các hệ số A = [a_n, a_n-1, ..., a_0]
                   (Hệ số bậc cao nhất A[0] = a_n ở ĐẦU danh sách).
    c (float or int): Giá trị từ biểu thức chia (x - c).

    Trả về:
    tuple: (B_coeffs, R)
           B_coeffs (list): Danh sách hệ số của thương Q(x)
                            [b_{n-1}, b_{n-2}, ..., b_0]
           R (float or int): Số dư của phép chia (chính là P(c))
           Hoặc (None, None) nếu input không hợp lệ.
    """
    
    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    print(f"  A (mảng hệ số) = {coeffs}")
    print(f"  c (giá trị chia) = {c}")
    
    # "n: Bậc của đa thức"
    n = len(coeffs) - 1
    print(f"  n (bậc đa thức) = len(A) - 1 = {n}")

    # --- 2. Kiểm tra điều kiện input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    
    # "Bậc của đa thức n >= 1"
    print(f"  Kiểm tra n >= 1:")
    if n < 1:
        print(f"    Lỗi: Bậc của đa thức phải >= 1 (để chia). Đa thức này có bậc {n}.")
        return None, None
    print(f"    -> n = {n} >= 1. Hợp lệ.")
    
    # "Mảng A phải có đúng n + 1 phần tử"
    print(f"  Kiểm tra mảng A có n + 1 phần tử:")
    print(f"    -> Hợp lệ (A có {len(coeffs)} phần tử, n + 1 = {n+1}).")

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Phương pháp là một vòng lặp for. Không cần điều kiện dừng đặc biệt.")

    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")

    # Bước 4.1: Khởi tạo mảng B
    B_coeffs = []
    print(f"  [4.1] Khởi tạo mảng B để lưu {n} hệ số của Q(x): B = {B_coeffs}")

    # Bước 4.2: Gán b_{n-1} = a_n
    # (Hệ số đầu tiên của Q(x) bằng hệ số đầu tiên của P(x))
    b_prev = coeffs[0]
    B_coeffs.append(b_prev)
    print(f"  [4.2] Gán b_{n-1} = a_n = A[0]")
    print(f"        -> b_{n-1} (hệ số đầu tiên của Q) = {b_prev}")
    print(f"        -> Lưu vào B. B hiện tại = {B_coeffs}")
    
    # Bước 4.3: Thiết lập vòng lặp for i chạy từ 1 đến n-1
    # (Code lặp từ i=1 đến n-1. Tổng cộng n-1 lần lặp)
    print(f"  [4.3] Thiết lập vòng lặp for i chạy từ 1 đến n-1 (tức là i từ 1 đến {n-1})")

    # Bước 4.4 (Trong vòng lặp): Tính các hệ số thương
    # Vòng lặp này sẽ tính b_{n-2}, b_{n-3}, ..., b_0
    for i in range(1, n):
        print(f"    --- i = {i} (Tính hệ số b_{n-1-i}) ---")
        
        # Lấy hệ số a_{n-i} (chính là coeffs[i])
        a_i = coeffs[i]
        
        # Công thức đúng: b_current = a_i + b_previous * c
        b_current = a_i + b_prev * c
        
        print(f"    [4.4] Tính hệ số thương tiếp theo:")
        print(f"          Công thức: b_moi = a_hi_tai + b_truoc * c")
        print(f"          (Tương ứng: b_{n-1-i} = a_{n-i} + b_{n-i} * c)")
        print(f"          b_moi = A[i] + b_truoc * c")
        print(f"          b_moi = {a_i} + {b_prev} * {c}")
        print(f"          b_moi = {a_i} + {b_prev * c}")
        print(f"          => b_moi = {b_current}")
        
        # Lưu kết quả b_{n-1-i} vào mảng B
        B_coeffs.append(b_current)
        print(f"          -> Lưu kết quả vào B. B hiện tại = {B_coeffs}")
        
        # Cập nhật b_prev (b_truoc) cho vòng lặp tiếp theo
        b_prev = b_current
        
    print("    --- Kết thúc vòng lặp ---")

    # Bước 4.5: Tính số dư R
    # Công thức đúng: R = a_0 + b_0 * c
    # a_0 là phần tử cuối cùng của coeffs (coeffs[n])
    # b_0 là phần tử cuối cùng ta vừa tính (hiện đang lưu trong b_prev)
    a_0 = coeffs[n]
    R = a_0 + b_prev * c
    
    print(f"  [4.5] Tính số dư R:")
    print(f"        Công thức: R = a_0 + b_0 * c")
    print(f"        (Trong code: R = A[n] + b_prev * c)")
    print(f"        R = {a_0} + {b_prev} * {c}")
    print(f"        R = {a_0} + {b_prev * c}")
    print(f"        => R = {R}")
    
    # 5. Xác định output
    print(f"[Bước 5] Xác định output:")
    print(f"  Mảng B (hệ số Q(x)) = {B_coeffs}")
    print(f"  Giá trị R (số dư) = {R}")
    
    return B_coeffs, R

# --------------------------------------------------------------------
# PHẦN "FILE ỨNG DỤNG" ĐỂ CHẠY THỬ THUẬT TOÁN
# (Đã cập nhật để gọn gàng hơn)
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("--- ỨNG DỤNG THUẬT TOÁN CHIA HORNER ---")
    
    # --- Ví dụ 1: ---
    he_so_A = [3, -2, 0, -5]
    diem_c = 2
    
    print(f"\n--- Ví dụ 1 ---")
    print(f"Đa thức P(x) có hệ số: {he_so_A}")
    print(f"Chia cho (x - {diem_c})")
    
    # Gọi hàm (Hàm sẽ tự in các bước 1-5)
    B, R = chia_horner(he_so_A, diem_c)
    

    # --- Ví dụ 2: ---
    he_so_A_2 = [1, 0, -4]
    diem_c_2 = -2
    
    print(f"\n--- Ví dụ 2 ---")
    print(f"Đa thức P(x) có hệ số: {he_so_A_2}")
    print(f"Chia cho (x - ({diem_c_2}))")
    
    # Gọi hàm (Hàm sẽ tự in các bước 1-5)
    B_2, R_2 = chia_horner(he_so_A_2, diem_c_2)