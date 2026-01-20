import numpy as np
import math

def giai_stirling_full_dao_ham(x_nodes, y_nodes, x_val):
    """
    Giải nội suy Stirling:
    - Bảng sai phân chuẩn.
    - Xây dựng đa thức P(t).
    - Tính f(x) và đạo hàm f'(x).
    """
    n = len(x_nodes)
    
    # --- 0. KIỂM TRA ĐIỀU KIỆN ---
    if n % 2 == 0:
        print("❌ LỖI: Số mốc nội suy phải là số LẺ để có tâm chính xác.")
        return

    mid = n // 2
    x0 = float(x_nodes[mid])
    # [FIX] Ép kiểu float cho h để tránh lỗi phép chia sau này
    h = float(x_nodes[1] - x_nodes[0])
    t_val = (x_val - x0) / h
    
    print("\n" + "="*95)
    print(f"{'GIẢI NỘI SUY STIRLING + ĐA THỨC & ĐẠO HÀM':^95}")
    print("="*95)
    print(f"1. THÔNG SỐ:")
    print(f"   - Số mốc n = {n}. Tâm x0 = {x0} (index {mid})")
    print(f"   - Bước nhảy h = {h}")
    print(f"   - Biến đổi t = ({x_val} - {x0}) / {h} = {t_val:.6f}")
    if abs(t_val) > 0.25:
        print("   ⚠️ Lưu ý: Stirling hội tụ tốt nhất khi |t| <= 0.25")

    # --- 1. TÍNH BẢNG SAI PHÂN ---
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    # --- 2. IN BẢNG SAI PHÂN DẠNG HÌNH THOI ---
    print("\n" + "-"*40 + " 2. BẢNG SAI PHÂN TRUNG TÂM " + "-"*40)
    headers = ["i", "x", "y"] + [f"D^{k}y" for k in range(1, min(n, 6))]
    cw = 12
    
    header_str = f"{headers[0]:<6}{headers[1]:<{cw}}"
    for head in headers[2:]: header_str += f"{head:^{cw}}"
    print(header_str)
    print("-" * len(header_str))

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

    # --- 3. TÍNH TOÁN STIRLING & ĐA THỨC ---
    print(f"\n" + "="*95)
    print(f" 3. QUÁ TRÌNH TÍNH TOÁN & XÂY DỰNG ĐA THỨC ".center(95, "="))
    print(f"{'k':<4} | {'Hệ số (TB/Gốc)':<20} | {'Nhân tử t':<25} | {'Giá trị thêm':<15} | {'Tổng P_k(t)':<15}")
    print("-" * 90)

    # -- Khởi tạo cho tính toán số --
    current_sum = delta[mid][0] # y0
    prod_temp = 1.0 
    
    # -- Khởi tạo cho Đa thức --
    # P(t) bắt đầu bằng hằng số y0
    P_poly = np.poly1d([float(delta[mid][0])])
    # Biến t: 1*t + 0
    t_poly = np.poly1d([1.0, 0.0])
    # Tích lũy nhân tử đa thức (t^2 - 1^2)...
    prod_poly_accum = np.poly1d([1.0])

    print(f"{'0':<4} | {'y0':<20} | {'1':<25} | {current_sum:<15.6f} | {current_sum:<15.6f}")

    for k in range(1, n):
        term_val = 0
        coeff_val = 0
        factor_str = ""
        factor_val = 0
        
        # Biến lưu đa thức nhân tử của bước hiện tại
        current_factor_poly = None 

        # --- SỐ HẠNG LẺ (2m-1) ---
        if k % 2 != 0:
            m = (k + 1) // 2
            idx_up = mid - m
            idx_down = mid - m + 1
            if idx_up < 0: break
            
            # Hệ số: Trung bình cộng
            val1 = float(delta[idx_down][k])
            val2 = float(delta[idx_up][k])
            coeff_val = (val1 + val2) / 2.0
            
            # Nhân tử số: t * prod_temp
            factor_val = t_val * prod_temp
            
            # Nhân tử Đa thức: t * prod_poly_accum
            current_factor_poly = t_poly * prod_poly_accum
            
            if m == 1: factor_str = "t"
            else: factor_str = f"t(t^2-1^2)...(t^2-{m-1}^2)"

        # --- SỐ HẠNG CHẴN (2m) ---
        else:
            m = k // 2
            idx = mid - m
            if idx < 0: break
            
            # Hệ số: Giá trị gốc
            coeff_val = float(delta[idx][k])
            
            # Nhân tử số: t^2 * prod_temp
            factor_val = (t_val**2) * prod_temp
            
            # Nhân tử Đa thức: t^2 * prod_poly_accum
            current_factor_poly = (t_poly**2) * prod_poly_accum
            
            # Cập nhật tích lũy cho vòng sau (chỉ cập nhật sau bước chẵn)
            # Nhân thêm (t^2 - m^2)
            prod_temp *= (t_val**2 - m**2)
            prod_poly_accum = prod_poly_accum * (t_poly**2 - float(m**2))
            
            if m == 1: factor_str = "t^2"
            else: factor_str = f"t^2(t^2-1^2)...(t^2-{m-1}^2)"

        # --- TÍNH TOÁN CỘNG DỒN ---
        # 1. Tính giá trị số
        term_val = (coeff_val / math.factorial(k)) * factor_val
        current_sum += term_val
        
        # 2. Tính đa thức (quan trọng: ép kiểu float cho hệ số để tránh lỗi numpy)
        scalar_coeff = coeff_val / math.factorial(k)
        term_poly = current_factor_poly * scalar_coeff
        
        # Kiểm tra an toàn: nếu term_poly bị biến thành mảng số (ndarray), ép lại thành poly1d
        if isinstance(term_poly, np.ndarray):
            term_poly = np.poly1d(term_poly)
            
        P_poly = P_poly + term_poly

        print(f"{k:<4} | {coeff_val:<20.6f} | {factor_str:<25} | {term_val:<15.6f} | {current_sum:<15.6f}")

    print("-" * 90)
    
    # --- 4. KẾT QUẢ ---
    print(f"\n🔹 Đa thức nội suy Stirling P(t):")
    print(P_poly)
    
    print(f"\n🔹 Kết quả tính toán:")
    print(f"   f({x_val}) ≈ P({t_val:.4f}) = {current_sum:.6f}")

    # --- 5. TÍNH ĐẠO HÀM ---
    # P'(t)
    P_deriv = np.polyder(P_poly)
    # Giá trị P'(t)
    val_deriv = float(P_deriv(t_val))
    # f'(x) = (1/h) * P'(t)
    f_prime = (1.0 / h) * val_deriv
    
    print(f"\n🔹 Đạo hàm f'(x):")
    print(f"   P'({t_val:.4f}) = {val_deriv:.6f}")
    print(f"   f'({x_val}) = (1/{h}) * {val_deriv:.6f} ≈ {f_prime:.6f}")

# ==============================================================================
# NHẬP DỮ LIỆU CỦA BẠN
# ==============================================================================
# Dữ liệu mẫu (Thay số bài tập của bạn vào đây)
x_input = np.array([1.45, 1.50, 1.55, 1.60, 1.65])
y_input = np.array([1.1432, 1.1855, 1.2292, 1.2741, 1.3205])
x_can_tinh = 1.52

giai_stirling_full_dao_ham(x_input, y_input, x_can_tinh)