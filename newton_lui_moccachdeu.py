import numpy as np
import math

def solve_newton_backward_equidistant(x_nodes, y_nodes, x_val):
    """
    Giải bài toán nội suy Newton LÙI với mốc CÁCH ĐỀU.
    Input:
        x_nodes: Mảng các mốc x (cách đều).
        y_nodes: Mảng các giá trị y tương ứng.
        x_val: Giá trị x cần tính.
    """
    n = len(x_nodes)
    
    # Kiểm tra khoảng cách h
    h = x_nodes[1] - x_nodes[0]
    
    # --- BƯỚC 1: TÍNH BẢNG SAI PHÂN (DIFFERENCE TABLE) ---
    # Bảng này tính giống hệt Newton tiến
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    # --- IN BẢNG ---
    print("\n" + "="*70)
    print(f"{'NỘI SUY NEWTON LÙI (MỐC CÁCH ĐỀU)':^70}")
    print("="*70 + "\n")
    
    # Mốc cuối cùng x_n
    x_n = x_nodes[n-1]
    
    print(f"Bước biến đổi: h = {h}, Mốc cuối x_n = {x_n}")
    t_val = (x_val - x_n) / h
    print(f"Tại x = {x_val} => t = (x - x_n)/h = ({x_val} - {x_n})/{h} = {t_val:.5f}\n")
    
    print(f"1. BẢNG SAI PHÂN (Difference Table):")
    print("-" * 75)
    headers = ["x", "y", "Nab y"] + [f"D^{k} y" for k in range(2, n)] # Nabla (Sai phân lùi)
    header_str = "".join([f"{h:<12}" for h in headers])
    print(header_str)
    print("-" * 75)
    
    for i in range(n):
        row_str = f"{x_nodes[i]:<12.4f}"
        for j in range(n):
            val = delta[i][j]
            if i < n - j:
                row_str += f"{val:<12.4f}"
            else:
                row_str += f"{'':<12}"
        print(row_str)
    print("-" * 75 + "\n")

    # --- BƯỚC 2: XÁC ĐỊNH HỆ SỐ LÙI ---
    # Lấy các phần tử ở cạnh dưới của bảng (đường chéo đi lên từ y_n)
    # y_n nằm ở delta[n-1][0]
    # Nabla y_n nằm ở delta[n-2][1]
    # Nabla^k y_n nằm ở delta[n-1-k][k]
    
    backward_diffs = []
    for k in range(n):
        row_idx = n - 1 - k
        col_idx = k
        backward_diffs.append(delta[row_idx][col_idx])
        
    print(f"2. ĐA THỨC NỘI SUY P(t):")
    print(f"   Các sai phân lùi (Nabla^k y_n): {list(np.round(backward_diffs, 5))}")
    
    # Tạo chuỗi công thức: P(t) = y_n + t*Dy + t(t+1)/2!*D^2y...
    poly_str = f"P(t) = {backward_diffs[0]:.4f}"
    
    for k in range(1, n):
        fact_k = math.factorial(k)
        coeff = backward_diffs[k] / fact_k
        
        sign = " + " if coeff >= 0 else " - "
        val_display = abs(coeff)
        
        term_str = f"{sign}{val_display:.4f}"
        
        # Tạo chuỗi t(t+1)...(t+k-1)
        var_part = "t"
        for m in range(1, k):
            var_part += f"(t+{m})" # Điểm khác biệt: Dấu cộng
            
        term_str += var_part
        
        if k % 2 == 0:
             poly_str += "\n          " + term_str
        else:
             poly_str += term_str
             
    print(f"   Công thức:\n          {poly_str}\n")

    # --- BƯỚC 3: TÍNH GIÁ TRỊ VÀ ĐẠO HÀM ---
    print(f"3. TÍNH TOÁN TẠI t = {t_val:.5f} (tương ứng x = {x_val}):")
    
    # a) Tính f(x)
    f_res = backward_diffs[0]
    t_term = 1 
    
    for k in range(1, n):
        # Nhân thêm (t + (k-1)) vào tích lũy. 
        # k=1: nhân t
        # k=2: nhân (t+1)
        t_term = t_term * (t_val + (k - 1))
        
        term_val = (backward_diffs[k] / math.factorial(k)) * t_term
        f_res += term_val
        
    print(f"   ➢ Giá trị hàm số:  f({x_val}) ≈ {f_res:.5f}")
    
    # b) Tính đạo hàm f'(x)
    # f'(x) = (1/h) * P'(t)
    # P(t) chứa các cụm t(t+1)...(t+k-1)
    
    p_prime_t = 0
    
    for k in range(1, n):
        coeff = backward_diffs[k] / math.factorial(k)
        
        # Đạo hàm của cụm tích k phần tử: t, (t+1), ..., (t+k-1)
        # Tập hợp các phần tử trong tích:
        factors = [t_val + m for m in range(k)]
        
        # Đạo hàm tích = Tổng các tích con (bỏ 1 phần tử)
        term_deriv = 0
        for m in range(k): # m là vị trí bị bỏ
            sub_prod = 1
            for j in range(k):
                if j != m:
                    sub_prod *= factors[j]
            term_deriv += sub_prod
            
        p_prime_t += coeff * term_deriv
        
    f_prime_x = p_prime_t * (1.0 / h)
    
    print(f"   ➢ Giá trị đạo hàm: f'({x_val}) ≈ {f_prime_x:.5f}")
    print(f"     (f'(x) = P'(t)/h = {p_prime_t:.5f} / {h})")
    print("\n" + "="*70)

# --- VÍ DỤ CHẠY THỬ ---
# Dữ liệu từ ảnh (1.2, 3.172), (1.3, 3.695)...
# Giả sử ta muốn tính tại x gần cuối bảng (ví dụ 1.75) để dùng Newton lùi hiệu quả
x_data = [1.2, 1.3, 1.4, 1.5]
y_data = [3.172, 3.695, 4.250, 4.890] # Dữ liệu giả định
x_calc = 1.45

solve_newton_backward_equidistant(x_data, y_data, x_calc)