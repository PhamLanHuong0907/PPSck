import numpy as np

def solve_newton_backward_arbitrary(x_nodes, y_nodes, x_val):
    """
    Giải bài toán nội suy Newton LÙI với mốc BẤT KỲ.
    Sử dụng bảng tỷ sai phân nhưng lấy hệ số từ dưới lên.
    """
    n = len(x_nodes)
    
    # --- BƯỚC 1: TÍNH BẢNG TỶ SAI PHÂN ---
    # Vẫn tính bảng như bình thường (giống Newton tiến)
    # table[i][j] = f[x_i, ..., x_{i+j}]
    table = np.zeros((n, n + 1))
    table[:, 0] = x_nodes
    table[:, 1] = y_nodes
    
    for j in range(2, n + 1): # j là chỉ số cột (cấp tỷ sai phân)
        for i in range(n - j + 1):
            numerator = table[i+1][j-1] - table[i][j-1]
            denominator = table[i+j-1][0] - table[i][0]
            table[i][j] = numerator / denominator

    print("\n" + "="*70)
    print(f"{'NỘI SUY NEWTON LÙI (MỐC BẤT KỲ)':^70}")
    print("="*70 + "\n")
    
    print(f"1. BẢNG TỶ SAI PHÂN (Divided Difference Table):")
    print("-" * 75)
    headers = ["x", "y"] + [f"SD Cấp {k}" for k in range(1, n)]
    header_str = "".join([f"{h:<12}" for h in headers])
    print(header_str)
    print("-" * 75)
    
    for i in range(n):
        row_str = ""
        for j in range(n + 1):
            val = table[i][j]
            if i < n - (j - 1): 
                row_str += f"{val:<12.4f}"
            else:
                row_str += f"{'':<12}"
        print(row_str)
    print("-" * 75 + "\n")

    # --- BƯỚC 2: XÁC ĐỊNH HỆ SỐ LÙI ---
    # Newton lùi dùng các hệ số kết thúc tại x_n: f[x_n], f[x_{n-1}, x_n], f[x_{n-2}, x_{n-1}, x_n]...
    # Trong bảng table[i][j], các giá trị này nằm ở: table[n-1][1] (y_n), table[n-2][2], table[n-3][3]...
    # Lưu ý: Cột 1 là y. Hệ số a_k tương ứng với cột k+1 trong bảng code của mình.
    
    backward_coeffs = []
    # a0 = y_n -> table[n-1][1]
    # a1 = f[x_{n-1}, x_n] -> table[n-2][2]
    # ak = table[n-1-k][k+1]
    
    for k in range(n):
        # Lấy phần tử cuối cùng của mỗi cột sai phân hợp lệ
        # Cột trong table là k+1 (vì cột 0 là x)
        row_idx = n - 1 - k
        col_idx = k + 1
        backward_coeffs.append(table[row_idx][col_idx])
        
    print(f"2. ĐA THỨC NỘI SUY NEWTON LÙI P(x):")
    print(f"   Các hệ số (từ a0 đến a_{n-1}): {list(np.round(backward_coeffs, 5))}")
    
    poly_str = f"P(x) = {backward_coeffs[0]:.4f}"
    for i in range(1, n):
        sign = " + " if backward_coeffs[i] >= 0 else " - "
        val = abs(backward_coeffs[i])
        term = f"{sign}{val:.4f}"
        
        # Nhân tử lùi: (x - x_n)(x - x_{n-1})...
        # Lưu ý: x_nodes trong code là 0-indexed. Phần tử cuối là x_nodes[n-1]
        for k in range(i):
            # Với số hạng thứ i (hệ số a_i), ta nhân với (x - x_n), (x - x_{n-1})... (x - x_{n-i+1})
            node_idx = n - 1 - k
            term += f"(x - {x_nodes[node_idx]})"
            
        if i % 2 == 0: 
            poly_str += "\n          " + term
        else:
            poly_str += term
            
    print(f"   Công thức:\n          {poly_str}\n")

    # --- BƯỚC 3: TÍNH GIÁ TRỊ VÀ ĐẠO HÀM ---
    print(f"3. TÍNH TOÁN TẠI x = {x_val}:")
    
    # a) Tính f(x)
    f_res = backward_coeffs[0]
    term_val = 1
    
    for i in range(1, n):
        # Nhân thêm (x - x_{n-i}) vào tích lũy
        # i=1: nhân (x - x_n)
        # i=2: nhân (x - x_{n-1})
        current_node = x_nodes[n - i]
        term_val *= (x_val - current_node)
        
        f_res += backward_coeffs[i] * term_val
        
    print(f"   ➢ Giá trị hàm số:  f({x_val}) ≈ {f_res:.5f}")
    
    # b) Tính đạo hàm f'(x)
    # P(x) = a0 + a1(x-xn) + a2(x-xn)(x-xn-1) + ...
    # Đạo hàm của term thứ i: a_i * [(x-xn)...(x-xn-i+1)]'
    
    f_prime = 0
    for i in range(1, n):
        term_deriv = 0
        # Cụm tích có i phần tử: x_n, x_{n-1}, ..., x_{n-i+1}
        # Tập hợp các mốc trong cụm tích này:
        current_nodes_set = [x_nodes[n - 1 - k] for k in range(i)]
        
        # Đạo hàm tích: Tổng các tích con khi bỏ 1 phần tử
        for k in range(i): # k là vị trí phần tử bị bỏ
            sub_prod = 1
            for j in range(i):
                if j != k:
                    sub_prod *= (x_val - current_nodes_set[j])
            term_deriv += sub_prod
            
        f_prime += backward_coeffs[i] * term_deriv
        
    print(f"   ➢ Giá trị đạo hàm: f'({x_val}) ≈ {f_prime:.5f}")
    print("\n" + "="*70)

# --- DỮ LIỆU CHẠY THỬ ---
# Dùng lại dữ liệu mẫu nhưng sắp xếp để thấy rõ tính chất lùi
# x: 1, 2, 3 -> x_n là 3
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 7.0, 5.0]
x_calc = 2.5

solve_newton_backward_arbitrary(x_data, y_data, x_calc)