import numpy as np
import math

def giai_noi_suy_gauss_full_dao_ham_fix(x_nodes, y_nodes, x_val):
    """
    Giải bài toán nội suy Gauss 1 & 2:
    - Bảng sai phân chuẩn.
    - Đa thức P(t).
    - Tính f(x), f'(x).
    (Đã fix lỗi kiểu dữ liệu h)
    """
    n = len(x_nodes)
    
    # --- 0. KIỂM TRA ĐIỀU KIỆN ---
    if n % 2 == 0:
        print("❌ LỖI: Số mốc nội suy phải là số LẺ để có tâm chính xác.")
        return

    mid = n // 2
    x0 = float(x_nodes[mid])
    # [FIX] Ép kiểu float cho h ngay từ đầu để tránh lỗi chuỗi
    h = float(x_nodes[1] - x_nodes[0])
    t_val = (x_val - x0) / h
    
    print("\n" + "="*95)
    print(f"{'GIẢI NỘI SUY TRUNG TÂM (GAUSS 1 & GAUSS 2) + ĐẠO HÀM':^95}")
    print("="*95)
    print(f"1. THÔNG SỐ CƠ BẢN:")
    print(f"   - Số mốc n = {n}")
    print(f"   - Mốc trung tâm x0 = {x0} (index {mid})")
    print(f"   - Bước nhảy h = {h}")
    print(f"   - Biến đổi t = ({x_val} - {x0}) / {h} = {t_val:.6f}")

    # --- 1. TÍNH BẢNG SAI PHÂN ---
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    # --- 2. IN BẢNG SAI PHÂN (DẠNG HÌNH THOI) ---
    print("\n" + "-"*40 + " 2. BẢNG SAI PHÂN TRUNG TÂM " + "-"*40)
    headers = ["i", "x", "y"] + [f"D^{k}y" for k in range(1, min(n, 6))]
    cw = 12
    print(f"{headers[0]:<6}{headers[1]:<{cw}}" + "".join([f"{h:^{cw}}" for h in headers[2:]]))
    print("-" * (6 + cw + cw*(len(headers)-2)))

    for row_display in range(2 * n - 1):
        line_str = ""
        if row_display % 2 == 0:
            real_i = row_display // 2
            rel_i = real_i - mid
            line_str += f"{rel_i:<6}{x_nodes[real_i]:<{cw}.2f}"
            for j in range(n):
                if j >= 6: break
                if j % 2 == 0:
                    data_idx = real_i - (j // 2)
                    if 0 <= data_idx < n - j:
                        val = delta[data_idx][j]
                        line_str += f"{val:^{cw}.4f}"
                    else: line_str += f"{'':^{cw}}"
                else: line_str += f"{'':^{cw}}"
        else:
            upper_i = row_display // 2
            line_str += f"{'':<6}{'':<{cw}}"
            for j in range(n):
                if j >= 6: break
                if j % 2 != 0:
                    data_idx = upper_i - ((j - 1) // 2)
                    if 0 <= data_idx < n - j:
                        val = delta[data_idx][j]
                        line_str += f"{val:^{cw}.4f}"
                    else: line_str += f"{'':^{cw}}"
                else: line_str += f"{'':^{cw}}"
        print(line_str)

    # --- HÀM TÍNH TOÁN ---
    def print_calculation_steps(method_name):
        print(f"\n" + "="*95)
        print(f" 3. {method_name.upper()} ".center(95, "="))
        
        print(f"{'k':<4} | {'Hệ số (Delta)':<15} | {'Nhân tử (t)':<25} | {'Giá trị thêm':<15} | {'Tổng P_k(t)':<15}")
        print("-" * 90)
        
        current_sum = delta[mid][0]
        
        # Đa thức
        P_poly = np.poly1d([delta[mid][0]])
        prod_poly = np.poly1d([1.0])
        t_var = np.poly1d([1.0, 0.0])
        
        print(f"{'0':<4} | {'y0':<15} | {'1':<25} | {current_sum:<15.6f} | {current_sum:<15.6f}")
        
        term_prod_val = 1.0
        
        for k in range(1, n):
            row_idx = 0
            factor_val = 0
            factor_str = ""
            factor_poly = None
            
            if method_name == "Gauss 1":
                row_idx = mid - (k // 2)
                if k % 2 != 0: 
                    f = (k - 1) // 2
                    factor_val = t_val + f
                    factor_str = f"(t+{f})" if f != 0 else "t"
                    factor_poly = t_var + f
                else:
                    f = k // 2
                    factor_val = t_val - f
                    factor_str = f"(t-{f})"
                    factor_poly = t_var - f
            elif method_name == "Gauss 2":
                row_idx = mid - ((k + 1) // 2)
                if k == 1:
                    factor_val = t_val
                    factor_str = "t"
                    factor_poly = t_var
                elif k % 2 == 0:
                    f = k // 2
                    factor_val = t_val + f
                    factor_str = f"(t+{f})"
                    factor_poly = t_var + f
                else:
                    f = (k - 1) // 2
                    factor_val = t_val - f
                    factor_str = f"(t-{f})"
                    factor_poly = t_var - f

            if row_idx < 0: break
            
            diff = delta[row_idx][k]
            term_prod_val *= factor_val
            term_val = (diff / math.factorial(k)) * term_prod_val
            current_sum += term_val
            
            prod_poly = prod_poly * factor_poly
            term_poly = (diff / math.factorial(k)) * prod_poly
            P_poly = P_poly + term_poly
            
            print(f"{k:<4} | {diff:<15.6f} | {factor_str:<25} | {term_val:<15.6f} | {current_sum:<15.6f}")
            
        print("-" * 90)
        
        # --- KẾT QUẢ ĐA THỨC & ĐẠO HÀM ---
        print(f"🔹 Đa thức nội suy P(t):")
        print(P_poly)
        print(f"\n🔹 Kết quả tính toán:")
        print(f"   f({x_val}) ≈ P({t_val:.4f}) = {current_sum:.6f}")
        
        # Đạo hàm
        P_deriv = np.polyder(P_poly)
        val_deriv = float(P_deriv(t_val)) # [FIX] Ép kiểu float cho giá trị đạo hàm
        
        # [FIX] Đảm bảo h là float khi chia
        f_prime = (1.0 / float(h)) * val_deriv
        
        print(f"   P'({t_val:.4f}) = {val_deriv:.6f}")
        # Dùng {h} trong f-string chỉ để hiển thị
        print(f"   f'({x_val}) = (1/{h}) * P'(t) = {val_deriv:.6f} / {h}")
        print(f"   => f'({x_val}) ≈ {f_prime:.6f}")

    # --- 3. CHẠY ---
    print_calculation_steps("Gauss 1")
    print_calculation_steps("Gauss 2")

# ==============================================================================
# NHẬP DỮ LIỆU CỦA BẠN
# ==============================================================================
# Dữ liệu từ ảnh bài tập của bạn (image_f85fc3.png)
x_input = np.array([1.45, 1.50, 1.55, 1.60, 1.65])
y_input = np.array([1.1432, 1.1855, 1.2292, 1.2741, 1.3205])
x_can_tinh = 1.52

giai_noi_suy_gauss_full_dao_ham_fix(x_input, y_input, x_can_tinh)