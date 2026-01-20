import numpy as np
import pandas as pd

def giai_lagrange_dang_thuong(x_nodes, y_nodes, x_cal=None):
    n = len(x_nodes)
    print("\n" + "="*80)
    print(f"{'GIẢI NỘI SUY LAGRANGE - PHƯƠNG PHÁP CÁC THƯƠNG':^80}")
    print("="*80)
    print(f"Số mốc nội suy: {n}")
    print(f"X: {x_nodes}")
    print(f"Y: {y_nodes}")

    # --- BƯỚC 1: BẢNG TÍCH (Tính hệ số của đa thức W_n+1) ---
    print("\n" + "-"*40 + " BƯỚC 1: BẢNG TÍCH (Đa thức W) " + "-"*40)
    # W(x) = (x-x0)(x-x1)...(x-xn)
    # Hàm np.poly trả về hệ số của đa thức có các nghiệm là x_nodes
    # Hệ số được sắp xếp từ bậc cao nhất xuống thấp nhất (x^n, x^n-1, ..., x^0)
    w_coeffs = np.poly(x_nodes)
    
    # In ra dạng đa thức W(x)
    w_str = "W(x) = "
    deg_w = len(w_coeffs) - 1
    for i, c in enumerate(w_coeffs):
        pow_val = deg_w - i
        sign = " + " if c >= 0 else " - "
        if i == 0: sign = ""
        if pow_val == 0: w_str += f"{sign}{abs(c):.4f}"
        elif pow_val == 1: w_str += f"{sign}{abs(c):.4f}x"
        else: w_str += f"{sign}{abs(c):.4f}x^{pow_val}"
    
    print("Hệ số của W(x) (từ bậc cao -> thấp):")
    print(np.round(w_coeffs, 4))
    print(f"\nCông thức khai triển:\n{w_str}")

    # --- BƯỚC 2: BẢNG THƯƠNG (Ma trận A - Chia Horner) ---
    print("\n" + "-"*40 + " BƯỚC 2: BẢNG THƯƠNG (Ma trận A) " + "-"*40)
    print("Thực hiện phép chia Horner: Q_i(x) = W(x) / (x - x_i)")
    
    # Ma trận A lưu các hệ số thương. 
    # Kích thước n dòng (mỗi dòng là 1 mốc x_i), n cột (hệ số từ bậc n-1 đến 0)
    # Lưu ý: w_coeffs có n+1 phần tử. Khi chia cho (x-xi) sẽ còn n phần tử.
    matrix_A = np.zeros((n, n))
    
    # In tiêu đề bảng
    headers = [f"x^{n-1-i}" for i in range(n)]
    print(f"{'x_i':<8} | " + "".join([f"{h:<12}" for h in headers]))
    print("-" * (10 + 12*n))
    
    # Tính toán từng dòng bằng lược đồ Horner
    for i in range(n):
        root = x_nodes[i]
        # Lược đồ Horner:
        # b_0 = a_0
        # b_k = a_k + b_{k-1} * root
        
        # w_coeffs[0] là hệ số bậc cao nhất (luôn là 1)
        current_val = w_coeffs[0]
        matrix_A[i][0] = current_val
        
        # Tính các hệ số tiếp theo
        for j in range(1, n):
            current_val = w_coeffs[j] + current_val * root
            matrix_A[i][j] = current_val
            
        # In dòng ra màn hình
        row_str = f"{root:<8.2f} | " + "".join([f"{val:<12.4f}" for val in matrix_A[i]])
        print(row_str)

    # --- BƯỚC 3: TÍNH TRỌNG SỐ C_i VÀ D_i ---
    print("\n" + "-"*40 + " BƯỚC 3: TÍNH HỆ SỐ C_i " + "-"*40)
    # D_i = đạo hàm W'(x_i) = tích các (xi - xj)
    # C_i = y_i / D_i
    
    D_arr = np.zeros(n)
    C_arr = np.zeros(n)
    
    print(f"{'i':<4} | {'x_i':<8} | {'y_i':<8} | {'D_i (Mẫu số)':<15} | {'C_i (Trọng số)':<15}")
    print("-" * 60)
    
    for i in range(n):
        # Tính D_i
        p_prod = 1.0
        for j in range(n):
            if i != j:
                p_prod *= (x_nodes[i] - x_nodes[j])
        D_arr[i] = p_prod
        C_arr[i] = y_nodes[i] / p_prod
        print(f"{i:<4} | {x_nodes[i]:<8.2f} | {y_nodes[i]:<8.4f} | {D_arr[i]:<15.4f} | {C_arr[i]:<15.6f}")

    # --- BƯỚC 4: TỔNG HỢP ĐA THỨC ---
    print("\n" + "-"*40 + " BƯỚC 4: ĐA THỨC NỘI SUY P(x) " + "-"*40)
    print("P(x) = Sum( C_i * Row_i_of_A )")
    
    # Nhân trọng số C_i vào từng hàng của ma trận A rồi cộng dọc xuống
    # P_coeffs = [Sum(C0*A00, C1*A10...), Sum(C0*A01, ...), ...]
    final_coeffs = np.zeros(n)
    
    for j in range(n): # Duyệt theo cột (bậc của x)
        col_sum = 0
        for i in range(n): # Duyệt theo hàng (các mốc)
            col_sum += C_arr[i] * matrix_A[i][j]
        final_coeffs[j] = col_sum
        
    print("Các hệ số tìm được (từ bậc cao nhất):")
    print(np.round(final_coeffs, 6))
    
    # Viết công thức đẹp
    poly_final = f"P(x) ="
    deg_p = n - 1
    for i, c in enumerate(final_coeffs):
        pow_val = deg_p - i
        # Xử lý dấu
        sign = " + " if c >= 0 else " - "
        if i == 0 and c >= 0: sign = " "
        elif i == 0 and c < 0: sign = "-"
        
        val = abs(c)
        if val < 1e-9: continue # Bỏ qua hệ số 0
        
        if pow_val == 0: poly_final += f"{sign}{val:.5f}"
        elif pow_val == 1: poly_final += f"{sign}{val:.5f}x"
        else: poly_final += f"{sign}{val:.5f}x^{pow_val}"
        
    print(f"\nKẾT QUẢ CUỐI CÙNG:")
    print(poly_final)
    
    # --- BƯỚC 5: TÍNH GIÁ TRỊ (NẾU CÓ) ---
    if x_cal is not None:
        print(f"\n" + "-"*40 + f" TÍNH GIÁ TRỊ TẠI x = {x_cal} " + "-"*40)
        # Horner cho đa thức kết quả
        res = final_coeffs[0]
        for i in range(1, n):
            res = res * x_cal + final_coeffs[i]
        print(f"P({x_cal}) = {res:.6f}")

# =================================================================
# CHẠY THỬ VỚI DỮ LIỆU CỦA BẠN
# =================================================================
# Dữ liệu từ hình ảnh image_f77a8c.png (Bài giải mẫu trong vở)
# x: 2.1, 2.2, 2.4, 2.5, 2.7, 2.8
# y: 3.178, 3.452, 3.597, 4.132, 4.376, 4.954 (Nhìn ảnh hơi mờ nên mình lấy xấp xỉ)

x_data = np.array([2.1, 2.2, 2.4, 2.5, 2.7, 2.8])
y_data = np.array([3.178, 3.452, 3.597, 4.132, 4.376, 4.954])
x_tinh = 2.5

giai_lagrange_dang_thuong(x_data, y_data, x_tinh)