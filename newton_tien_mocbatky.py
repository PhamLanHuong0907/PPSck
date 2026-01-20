import numpy as np

def solve_and_print_newton(x_nodes, y_nodes, x_val):
    """
    Hàm giải bài toán nội suy Newton và in ra các bước trình bày.
    """
    n = len(x_nodes)
    
    # --- BƯỚC 1: TÍNH VÀ IN BẢNG TỶ SAI PHÂN ---
    # Tạo bảng lưu trữ: Cột 0 là x, Cột 1 là y, Cột 2 trở đi là sai phân
    table = np.zeros((n, n + 1))
    table[:, 0] = x_nodes
    table[:, 1] = y_nodes
    
    # Tính toán các cột tỷ sai phân
    # Công thức: f[xi...xk] = (f[xi+1...xk] - f[xi...xk-1]) / (xk - xi)
    for j in range(2, n + 1): # j là chỉ số cột (2 -> n)
        for i in range(n - j + 1):
            numerator = table[i+1][j-1] - table[i][j-1]
            denominator = table[i+j-1][0] - table[i][0]
            table[i][j] = numerator / denominator

    print("\n" + "="*60)
    print(f"{'GIẢI BÀI TOÁN NỘI SUY NEWTON':^60}")
    print("="*60 + "\n")
    
    print(f"1. BẢNG TỶ SAI PHÂN (Divided Difference Table):")
    print("-" * 65)
    # Tạo header: x  y  SD_1  SD_2 ...
    headers = ["x", "y"] + [f"SD Cấp {k}" for k in range(1, n)]
    header_str = "".join([f"{h:<12}" for h in headers])
    print(header_str)
    print("-" * 65)
    
    # In từng hàng của bảng
    for i in range(n):
        row_str = ""
        for j in range(n + 1):
            val = table[i][j]
            # Chỉ in các giá trị hợp lệ trong bảng tam giác, còn lại in khoảng trắng
            if i < n - (j - 1): 
                row_str += f"{val:<12.4f}" # Định dạng 4 chữ số thập phân
            else:
                row_str += f"{'':<12}"
        print(row_str)
    print("-" * 65 + "\n")

    # --- BƯỚC 2: XÁC ĐỊNH ĐA THỨC ---
    # Các hệ số nằm ở hàng đầu tiên của các cột sai phân (table[0][1] -> table[0][n])
    coeffs = table[0, 1:] 
    
    print(f"2. ĐA THỨC NỘI SUY NEWTON P(x):")
    print(f"   Các hệ số tìm được: {list(np.round(coeffs, 5))}")
    
    # Tạo chuỗi công thức đa thức để in ra
    poly_str = f"P(x) = {coeffs[0]:.4f}"
    for i in range(1, n):
        sign = " + " if coeffs[i] >= 0 else " - "
        val = abs(coeffs[i])
        term = f"{sign}{val:.4f}"
        # Thêm các nhân tử (x - x0)(x - x1)...
        for k in range(i):
            term += f"(x - {x_nodes[k]})"
        # Xuống dòng nếu công thức quá dài
        if i % 2 == 0: 
            poly_str += "\n          " + term
        else:
            poly_str += term
            
    print(f"   Công thức:\n          {poly_str}\n")

    # --- BƯỚC 3: TÍNH GIÁ TRỊ VÀ ĐẠO HÀM TẠI x = x_val ---
    print(f"3. TÍNH TOÁN TẠI x = {x_val}:")
    
    # a) Tính f(x) bằng lược đồ Horner (nhân dồn)
    p_val = coeffs[n-1]
    for k in range(n-2, -1, -1):
        p_val = coeffs[k] + (x_val - x_nodes[k]) * p_val
    print(f"   ➢ Giá trị hàm số:  f({x_val}) ≈ {p_val:.5f}")
    
    # b) Tính đạo hàm f'(x)
    # P'(x) = Tổng các đạo hàm thành phần.
    # Đạo hàm của a_i * (x-x0)...(x-xi-1) là a_i * [Tổng các tích con khi bỏ 1 phần tử]
    f_prime = 0
    for i in range(1, n):
        term_deriv = 0
        for k in range(i): # k là vị trí nhân tử bị đạo hàm thành 1
            prod_sub = 1
            for j in range(i):
                if j != k:
                    prod_sub *= (x_val - x_nodes[j])
            term_deriv += prod_sub
        f_prime += coeffs[i] * term_deriv
        
    print(f"   ➢ Giá trị đạo hàm: f'({x_val}) ≈ {f_prime:.5f}")
    print("\n" + "="*60)

# --- PHẦN NHẬP DỮ LIỆU CỦA BẠN ---
# Ví dụ: Mốc (1, 2), (2, 7), (3, 5) và tính tại x = 2.5
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 7.0, 5.0]
x_calc = 2.5

# Gọi hàm
solve_and_print_newton(x_data, y_data, x_calc)