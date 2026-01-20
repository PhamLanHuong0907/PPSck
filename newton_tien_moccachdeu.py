import numpy as np
import math

def solve_newton_forward_equidistant(x_nodes, y_nodes, x_val):
    """
    Giải bài toán nội suy Newton tiến với mốc cách đều.
    Input:
        x_nodes: Mảng các mốc x (cách đều).
        y_nodes: Mảng các giá trị y tương ứng.
        x_val: Giá trị x cần tính.
    """
    n = len(x_nodes)
    
    # Kiểm tra tính cách đều
    h = x_nodes[1] - x_nodes[0]
    # (Có thể thêm code kiểm tra sai số h nếu cần thiết)
    
    # --- BƯỚC 1: TÍNH BẢNG SAI PHÂN (FORWARD DIFFERENCE TABLE) ---
    # delta[i][j] là sai phân cấp j tại mốc i
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    
    # Tính sai phân: Delta_k = Delta_{k-1}(sau) - Delta_{k-1}(trước)
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    # --- IN BẢNG ---
    print("\n" + "="*70)
    print(f"{'NỘI SUY NEWTON TIẾN (MỐC CÁCH ĐỀU)':^70}")
    print("="*70 + "\n")
    
    print(f"Bước biến đổi: h = {h}")
    t_val = (x_val - x_nodes[0]) / h
    print(f"Tại x = {x_val} => t = (x - x0)/h = ({x_val} - {x_nodes[0]})/{h} = {t_val:.5f}\n")
    
    print(f"1. BẢNG SAI PHÂN (Forward Difference Table):")
    print("-" * 75)
    headers = ["x", "y", "Delta y"] + [f"D^{k} y" for k in range(2, n)]
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

    # --- BƯỚC 2: CÔNG THỨC ĐA THỨC ---
    # Hệ số cơ bản: a_k = Delta^k y0 / k!
    # P(t) = y0 + (Dy0/1!)t + (D^2y0/2!)t(t-1) + ...
    
    print(f"2. ĐA THỨC NỘI SUY P(t):")
    # Lấy hàng đầu tiên (delta[0]) làm các hệ số sai phân
    diffs = delta[0]
    
    poly_str = f"P(t) = {diffs[0]:.4f}"
    for k in range(1, n):
        fact_k = math.factorial(k)
        coeff = diffs[k] / fact_k
        
        sign = " + " if coeff >= 0 else " - "
        val_display = abs(coeff)
        
        term_str = f"{sign}{val_display:.4f}"
        # Tạo chuỗi t(t-1)...
        var_part = "t"
        for m in range(1, k):
            var_part += f"(t-{m})"
            
        term_str += var_part
        
        if k % 2 == 0:
             poly_str += "\n          " + term_str
        else:
             poly_str += term_str
             
    print(f"   Công thức:\n          {poly_str}\n")

    # --- BƯỚC 3: TÍNH GIÁ TRỊ VÀ ĐẠO HÀM ---
    print(f"3. TÍNH TOÁN TẠI t = {t_val:.5f} (tương ứng x = {x_val}):")
    
    # a) Tính f(x) ~ P(t)
    # Áp dụng trực tiếp công thức tổng sigma
    f_res = diffs[0]
    
    # Biến lưu tích t(t-1)...(t-k+1)
    t_term = 1 
    
    for k in range(1, n):
        t_term = t_term * (t_val - (k - 1))
        term_val = (diffs[k] / math.factorial(k)) * t_term
        f_res += term_val
        
    print(f"   ➢ Giá trị hàm số:  f({x_val}) ≈ {f_res:.5f}")
    
    # b) Tính đạo hàm f'(x)
    # f'(x) = (1/h) * P'(t)
    # P(t) = Sum [ (Delta^k y0 / k!) * Product_{j=0}^{k-1}(t-j) ]
    # Đạo hàm Product bằng quy tắc đạo hàm tích: Sum các tích con bỏ 1 phần tử
    
    p_prime_t = 0 # Đạo hàm theo biến t
    
    for k in range(1, n):
        coeff = diffs[k] / math.factorial(k)
        
        # Tính đạo hàm của cụm t(t-1)...(t-k+1) tại giá trị t_val
        term_deriv = 0
        
        # Cụm này có k phần tử: (t-0), (t-1), ..., (t-(k-1))
        # Đạo hàm là tổng của k số hạng, mỗi số hạng là tích của k-1 phần tử còn lại
        for m in range(k): # m là chỉ số phần tử bị bỏ đi (đạo hàm = 1)
            sub_prod = 1
            for j in range(k):
                if j != m:
                    sub_prod *= (t_val - j)
            term_deriv += sub_prod
            
        p_prime_t += coeff * term_deriv
        
    # Chuyển về đạo hàm theo x: f'(x) = P'(t) * (1/h)
    f_prime_x = p_prime_t * (1.0 / h)
    
    print(f"   ➢ Giá trị đạo hàm: f'({x_val}) ≈ {f_prime_x:.5f}")
    print(f"     (Lưu ý: f'(x) = P'(t) * 1/h = {p_prime_t:.5f} * {1/h:.2f})")
    print("\n" + "="*70)

# --- VÍ DỤ CHẠY THỬ (Dựa trên slide trang 13 hoặc dữ liệu mẫu) ---
# Ví dụ: Cho bảng dữ liệu cách đều h=0.2
# x: 1.2, 1.4, 1.6
# y: ...
x_data = [1.2, 1.4, 1.6, 1.8]
y_data = [2.0, 2.8, 3.9, 5.2] # Dữ liệu giả định để test
x_calc = 1.5

solve_newton_forward_equidistant(x_data, y_data, x_calc)