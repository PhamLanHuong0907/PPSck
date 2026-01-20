import numpy as np
import math

def giai_bessel_da_thuc_dao_ham_fix(x_nodes, y_nodes, x_val):
    """
    Giải Bessel, in bảng chi tiết, xuất đa thức P(t) và tính đạo hàm f'(x).
    (Đã fix lỗi numpy.ndarray not callable)
    """
    n = len(x_nodes)
    
    # --- 1. CHUẨN BỊ ---
    idx0 = -1
    for i in range(n - 1):
        if x_nodes[i] <= x_val <= x_nodes[i+1]:
            idx0 = i
            break
    if idx0 == -1: idx0 = n // 2 - 1 if n % 2 == 0 else n // 2

    x0 = x_nodes[idx0]
    h = x_nodes[1] - x_nodes[0]
    t_val = (x_val - x0) / h
    
    print("\n" + "="*95)
    print(f"{'GIẢI NỘI SUY BESSEL & TÍNH ĐẠO HÀM':^95}")
    print("="*95)
    print(f"1. THÔNG SỐ:")
    print(f"   - Khoảng trung tâm: [{x0}, {x_nodes[idx0+1]}]")
    print(f"   - Bước nhảy h = {h}")
    print(f"   - Biến đổi t = (x - {x0}) / {h}")
    print(f"   - Tại x = {x_val} => t = {t_val:.6f}")

    # --- 2. TÍNH & IN BẢNG SAI PHÂN ---
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    print("\n" + "-"*40 + " 2. BẢNG SAI PHÂN TRUNG TÂM " + "-"*40)
    headers = ["i", "x", "y"] + [f"D^{k}y" for k in range(1, min(n, 6))]
    cw = 12
    print(f"{headers[0]:<6}{headers[1]:<{cw}}" + "".join([f"{h:^{cw}}" for h in headers[2:]]))
    print("-" * (6 + cw + cw*(len(headers)-2)))

    for row_display in range(2 * n - 1):
        line_str = ""
        if row_display % 2 == 0: 
            real_i = row_display // 2
            rel_i = real_i - idx0
            line_str += f"{rel_i:<6}{x_nodes[real_i]:<{cw}.2f}"
            for j in range(n):
                if j >= 6: break
                if j % 2 == 0:
                    data_idx = real_i - (j // 2)
                    if 0 <= data_idx < n - j:
                        line_str += f"{delta[data_idx][j]:^{cw}.4f}"
                    else: line_str += f"{'':^{cw}}"
                else: line_str += f"{'':^{cw}}"
        else:
            line_str += f"{'':<6}{'':<{cw}}"
            upper_i = row_display // 2
            for j in range(n):
                if j >= 6: break
                if j % 2 != 0:
                    data_idx = upper_i - ((j - 1) // 2)
                    if 0 <= data_idx < n - j:
                        line_str += f"{delta[data_idx][j]:^{cw}.4f}"
                    else: line_str += f"{'':^{cw}}"
                else: line_str += f"{'':^{cw}}"
        print(line_str)

    # --- 3. XÂY DỰNG ĐA THỨC & TÍNH TOÁN ---
    print(f"\n" + "="*95)
    print(f" 3. XÂY DỰNG ĐA THỨC NỘI SUY P(t) ".center(95, "="))
    
    val_y0 = delta[idx0][0]
    val_y1 = delta[idx0+1][0]
    
    # [FIX] Đảm bảo P_t luôn là object poly1d
    P_t = np.poly1d([(val_y0 + val_y1) / 2])
    
    poly_accum_even = np.poly1d([1.0]) 
    t_poly = np.poly1d([1.0, 0.0]) # t + 0

    print(f"{'k':<4} | {'Hệ số':<15} | {'Nhân tử (Biểu thức)':<35} | {'Giá trị tại t':<15}")
    print("-" * 90)
    print(f"{'0':<4} | {P_t[0]:<15.5f} | {'1':<35} | {P_t(t_val):<15.5f}")

    for k in range(1, n):
        term_poly = None
        coeff = 0.0
        factor_desc = ""

        if k % 2 != 0: 
            # --- CẤP LẺ ---
            m = (k + 1) // 2
            row_idx = idx0 - (m - 1)
            if row_idx < 0: break
            
            # [FIX] Ép kiểu float chuẩn Python để tránh lỗi numpy
            coeff = float(delta[row_idx][k])
            
            current_factor_poly = poly_accum_even * (t_poly - 0.5)
            
            # Tính toán hệ số nhân
            scalar_multiplier = coeff / math.factorial(k)
            term_poly = current_factor_poly * scalar_multiplier
            
            if k==1: factor_desc = "(t - 0.5)"
            else: factor_desc = f"[t...(t-{m-1})] * (t - 0.5)"

        else:
            # --- CẤP CHẴN ---
            m = k // 2
            row_u = idx0 - m
            row_l = idx0 - m + 1
            if row_u < 0: break
            
            # [FIX] Ép kiểu float
            val1 = float(delta[row_u][k])
            val2 = float(delta[row_l][k])
            coeff = (val1 + val2) / 2.0
            
            poly_accum_even = poly_accum_even * (t_poly + (m - 1)) * (t_poly - m)
            current_factor_poly = poly_accum_even
            
            scalar_multiplier = coeff / math.factorial(k)
            term_poly = current_factor_poly * scalar_multiplier
            
            if k==2: factor_desc = "t(t - 1)"
            else: factor_desc = f"t(t-1)...(t+{m-1})(t-{m})"

        # [FIX QUAN TRỌNG] Kiểm tra nếu term_poly bị biến thành ndarray thì ép lại về poly1d
        if isinstance(term_poly, np.ndarray):
             # Nếu là mảng 0-d (scalar array), lấy giá trị rồi nhân lại
             if term_poly.ndim == 0:
                 term_poly = current_factor_poly * float(term_poly)
             else:
                 # Nếu là mảng hệ số, tạo lại poly1d từ hệ số đó
                 term_poly = np.poly1d(term_poly)

        # Cộng vào đa thức tổng
        P_t = P_t + term_poly
        
        # Gọi hàm tính giá trị (lúc này term_poly chắc chắn là poly1d nên gọi được)
        val_at_t = term_poly(t_val)
        print(f"{k:<4} | {coeff:<15.5f} | {factor_desc:<35} | {val_at_t:<15.5f}")

    # --- 4. KẾT QUẢ ĐA THỨC ---
    print("\n" + "-"*40 + " 4. KẾT QUẢ ĐA THỨC P(t) " + "-"*40)
    print("Đa thức nội suy P(t):")
    print(P_t)

    # --- 5. TÍNH GIÁ TRỊ f(x) ---
    fx_approx = P_t(t_val)
    print(f"\n>>> GIÁ TRỊ HÀM SỐ: f({x_val}) ≈ {fx_approx:.6f}")

    # --- 6. TÍNH ĐẠO HÀM f'(x) ---
    print("\n" + "-"*40 + " 5. TÍNH ĐẠO HÀM f'(x) " + "-"*40)
    P_prime_t = np.polyder(P_t)
    print("Đạo hàm theo t: P'(t) =")
    print(P_prime_t)
    
    val_P_prime = P_prime_t(t_val)
    f_prime_x = (1 / h) * val_P_prime
    
    print(f"\nTại x = {x_val} (t = {t_val:.6f}):")
    print(f"   P'({t_val:.6f}) = {val_P_prime:.6f}")
    print(f"   f'({x_val}) = (1/{h}) * {val_P_prime:.6f} ≈ {f_prime_x:.6f}")

# ==============================================================================
# NHẬP DỮ LIỆU CỦA BẠN
# ==============================================================================
x_input = np.array([1.4, 1.5, 1.6, 1.7])
y_input = np.array([1.1855, 1.2292, 1.2741, 1.3205])
x_can_tinh = 1.55 

giai_bessel_da_thuc_dao_ham_fix(x_input, y_input, x_can_tinh)