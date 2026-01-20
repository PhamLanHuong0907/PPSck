import sympy # type: ignore

def horner_k_derivative(coeffs, x0, k):
    """
    Tính đạo hàm cấp 1 đến k của đa thức P tại điểm x0 bằng sơ đồ Horner.
    (ĐÃ SỬA LỖI BIẾN 'n' TRONG HÀM print_matrix)
    
    :param coeffs: List các hệ số của P, bắt đầu từ bậc cao nhất (ví dụ: [a_n, a_n-1, ..., a_0])
    :param x0: Điểm cần tính đạo hàm (có thể là số hoặc biến symbolic)
    :param k: Bậc đạo hàm cao nhất cần tính (ví dụ: k=2 nghĩa là tính P', P'')
    :return: Dict chứa các giá trị P(x0), P'(x0), P''(x0), ...
    """
    
    # --- 1. Xác định input ---
    print(f"\n--- Bắt đầu thuật toán Horner (bảng) tính đạo hàm cấp 0 đến {k} tại c = {x0} ---")
    print(f"[Bước 1] Xác định input:")
    P_coeffs = [sympy.sympify(c) for c in coeffs]
    n = len(P_coeffs) - 1
    print(f"  A (mảng hệ số) = {P_coeffs}")
    print(f"  n (bậc đa thức) = {n}")
    print(f"  c (điểm cần tính) = {x0}")
    print(f"  k (bậc đạo hàm cao nhất) = {k}")

    # --- 2. Kiểm tra điều kiện input ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    print(f"  Kiểm tra n >= k >= 0:")
    if k > n:
        print(f"    Lỗi: Đa thức chỉ có bậc {n}, không thể tính đạo hàm cấp {k}.")
        return {}
    if k < 0:
        print(f"    Lỗi: Bậc đạo hàm k={k} phải >= 0.")
        return {}
    print(f"    -> Hợp lệ (n={n}, k={k}).")
    
    print(f"  Kiểm tra A có n+1 phần tử:")
    print(f"    -> Hợp lệ (A có {len(P_coeffs)} phần tử, n+1 = {n+1}).")

    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Thuật toán sẽ lặp (k+1) = {k+1} lần (tương ứng j=0 đến k).")
    print(f"  Không cần điều kiện dừng đặc biệt.")

    # --- 4. Thực hiện tính toán ---
    print(f"[Bước 4] Thực hiện tính toán:")

    # Bước 4.1: Khởi tạo mảng hệ số làm việc B = A
    # (Code dùng bảng 'a' 2 chiều, a[0] là hàng đầu tiên)
    # Khởi tạo ma trận (k+2) hàng (0 đến k+1) và (n+1) cột (0 đến n)
    a = [[sympy.sympify(0) for _ in range(n + 1)] for _ in range(k + 2)]
    a[0] = P_coeffs.copy()
    print(f"  [4.1] Khởi tạo mảng hệ số làm việc (hàng a[0] = A):")
    print(f"    a[0] = {a[0]}")
    print(f"    Đa thức gốc Q_0(x) (từ a[0]):")
    print_polynomial(a[0])
    
    # === YÊU CẦU 1: HIỆN MA TRẬN BAN ĐẦU ===
    print(f"  [4.1.b] Ma trận (bảng) ban đầu (chỉ có hàng i=0):")
    # In ma trận (k+1 hàng, n+1 cột)
    print_matrix(a, k + 1, n, title=f"Ma trận ban đầu (a[0] = A, còn lại = 0)")
    # ======================================

    # Bước 4.2: Khởi tạo mảng 'R_list' (code dùng dict 'results')
    results = {}
    R_list_print = [] # Dùng để in theo thuật toán ảnh
    print(f"  [4.2] Khởi tạo danh sách lưu kết quả (results = {{}})")

    # Bước 4.3: Thiết lập vòng lặp ngoài (j chạy từ 0 đến k)
    # (Code dùng i chạy từ 1 đến k+1, tương đương j = i-1)
    print(f"  [4.3] Bắt đầu vòng lặp ngoài (j = 0 đến k={k}):")
    
    # Phải lặp k+1 lần (i=1...k+1)
    for i in range(1, k + 2):
        # j_image là chỉ số 0, 1, ..., k (bậc đạo hàm)
        j_image = i - 1 
        print(f"    --- Vòng lặp j = {j_image} (code i = {i}) ---")
        
        # Bước 4.4 (Trong vòng lặp): Áp dụng thuật toán (b)
        print(f"    [4.4] Áp dụng thuật toán chia Horner (b):")
        print(f"          (Chia đa thức Q_{j_image}(x) từ hàng a[{i-1}])")
        print(f"          (Lưu kết quả Q_{j_image+1}(x) vào hàng a[{i}])")
        
        # Bắt đầu lặp Horner cho hàng mới
        a[i][0] = a[i-1][0]
        print(f"          Hệ số đầu: a[{i}][0] = a[{i-1}][0] = {a[i][0]}")

        # Vòng lặp Horner (thuật toán (b))
        # j_code là chỉ số cột (1, 2, ...)
        # (Số cột tính toán cho hàng i là (n - i + 2) cột)
        for j_code in range(1, n - i + 2):
            a[i][j_code] = a[i-1][j_code] + a[i][j_code-1] * x0
            print(f"          Tính: a[{i}][{j_code}] = a[{i-1}][{j_code}] + a[{i}][{j_code-1}] * {x0} = {sympy.simplify(a[i][j_code])}")

        # "Lưu số dư R_j vào 'R_list[j]'"
        remainder_index = n - i + 1
        remainder = a[i][remainder_index]
        R_list_print.append(remainder)
        R_list_str = [str(sympy.simplify(r)) for r in R_list_print]

        print(f"          -> Phép chia hoàn tất.")
        print(f"          Lưu số dư R_{j_image} = a[{i}][{remainder_index}] = {remainder}")
        print(f"          (R_list tạm thời = {R_list_str})")

        # === YÊU CẦU 2: HIỆN MA TRẬN SAU KHI CẬP NHẬT HÀNG i ===
        print(f"          -> Trạng thái ma trận (bảng) sau bước j = {j_image}:")
        print_matrix(a, k + 1, n, title=f"Ma trận sau khi tính hàng i={i}")
        # ======================================================
        
        # Bước 4.6 (cho bậc j): Tính j!
        j_fact = sympy.factorial(j_image)
        
        # Bước 4.7 (cho bậc j): Tính kết quả P^(j)(c) = R_j * j!
        result_val = sympy.simplify(remainder * j_fact)
        
        print(f"    [4.6 & 4.7] Tính giá trị đạo hàm cấp j={j_image}:")
        print(f"          Value_{j_image} = R_{j_image} * (j!)")
        print(f"          Value_{j_image} = {remainder} * {j_fact} = {result_val}")
        
        if j_image == 0:
            key_name = "P(x0)"
            results[key_name] = result_val
        else:
            key_name = f"P_k{j_image}(x0)"
            results[key_name] = result_val
        
        print(f"    --- Kết thúc vòng lặp j = {j_image} ---")
        
    print(f"  --- Kết thúc vòng lặp ngoài ---")
    
    # ===
    # Phần này mô phỏng các bước 4.5, 4.6, 4.7 trong ảnh
    # (chỉ tính cho giá trị k cuối cùng)
    # ===
    
    print(f"\n  [Bước 4.5, 4.6, 4.7] (Tính toán theo ảnh CHỈ cho bậc k={k}):")
    
    # Bước 4.5: Lấy số dư cuối cùng R_k
    R_k = R_list_print[k] # R_list[k] là R_k (vì j=0..k)
    print(f"    [4.5] Lấy số dư (ứng với j=k): R_k = {R_k}")
    
    # Bước 4.6: Tính k!
    k_fact = sympy.factorial(k)
    print(f"    [4.6] Tính k!: {k}! = {k_fact}")
    
    # Bước 4.7: Tính kết quả cuối cùng
    Value = sympy.simplify(R_k * k_fact)
    print(f"    [4.7] Tính kết quả cuối cùng: Value = R_k * k! = {Value}")


    # --- 5. Xác định output ---
    print(f"[Bước 5] Xác định output (cho P^({k})(c) theo ảnh):")
    print(f"  Giá trị P^({k})(c) = {Value}")
    
    print("\n(Output đầy đủ của hàm (từ 0 đến k) trả về dict 'results')")
    print("--- Kết thúc ---")
    return results

def print_polynomial(coeffs):
    """Hàm tiện ích để in đa thức từ hệ số symbolic."""
    x = sympy.symbols('x')
    n = len(coeffs) - 1
    P_str = []
    for i in range(n + 1):
        term = coeffs[i]
        power = n - i
        if term != 0:
            if power == 0:
                P_str.append(f"({term})")
            elif power == 1:
                P_str.append(f"({term}*x)")
            else:
                P_str.append(f"({term}*x**{power})")
    
    print("    P(x) = " + " + ".join(P_str))

# === HÀM TIỆN ÍCH ĐỂ IN MA TRẬN (ĐÃ SỬA LỖI) ===
def print_matrix(matrix, max_i, max_j, title="Trạng thái ma trận:"):
    """
    Hàm tiện ích để in ma trận (bảng) Horner 2D.
    matrix: ma trận 'a'
    max_i: số hàng để in (k+1)
    max_j: số cột để in (n)
    """
    print(f"\n    {title}")
    
    # Tạo tiêu đề cột (j = 0...n)
    col_width = 12 # Tăng độ rộng cột để chứa biểu thức symbolic
    header_cols = []
    for j in range(max_j + 1):
        header_cols.append(f"j={j:<{col_width-2}}")
    print(f"      | {' | '.join(header_cols)}")
    print("-" * (len(header_cols) * (col_width + 2) + 6))

    # In từng hàng (i = 0...k+1)
    for i in range(max_i + 1):
        row_cells = []
        for j in range(max_j + 1):
            cell_val = matrix[i][j]
            
            # Rút gọn và chuyển sang chuỗi, giới hạn độ rộng
            # Nếu giá trị là 0, chỉ in '0' thay vì '0.0000...'
            if cell_val == 0:
                 cell_str = "0"
            else:
                 cell_str = str(sympy.simplify(cell_val))
                 
            # Căn trái và giới hạn độ rộng
            cell_str = f"{cell_str:<{col_width}}"
            
            # === DÒNG ĐÃ SỬA ===
            # (Thay 'n' bằng 'max_j' vì n không tồn tại trong scope này)
            # Hàng 'i' có (max_j - i + 2) phần tử được tính toán (từ cột 0 đến max_j-i+1)
            if j >= (max_j - i + 2) and i > 0:
                 cell_str = f"{'.':<{col_width}}" # Dấu chấm cho ô ngoài phạm vi
            # ==================
                 
            row_cells.append(cell_str)
        
        print(f"i={i:<2}   | {' | '.join(row_cells)}")
    print("") # Thêm một dòng trống
# ==============================