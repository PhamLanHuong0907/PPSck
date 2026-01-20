import math
import sympy  # Import thư viện symbolic
import sys    # Dùng để in lỗi

def trich_xuat_diem_phu_hop(all_x_data_input, all_y_data_input, x_input, k):
    """
    Trích xuất k điểm nội suy phù hợp theo thuật toán trong ảnh.
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    :param all_x_data_input: Mảng X (dạng list các số hoặc string biểu thức)
    :param all_y_data_input: Mảng Y (dạng list, sẽ được sao chép)
    :param x_input: Điểm cần tính (số hoặc string biểu thức)
    :param k: Số lượng điểm cần trích xuất (1 <= k <= n+1)
    :return: (X_new, Y_new) là các mảng con, hoặc (None, None) nếu thất bại
    """

    print(f"\n--- Bắt đầu trích xuất {k} điểm cho x = {x_input} ---")

    # --- 1. Xác định input ---
    print(f"[Bước 1] Xác định input:")
    try:
        # Chuyển đổi X và x_input sang SymPy để xử lý
        all_x_data = [sympy.sympify(val) for val in all_x_data_input]
        x = sympy.sympify(x_input)
    except sympy.SympifyError as e:
        print(f"  Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return None, None
        
    n = len(all_x_data) - 1 
    print(f"  X (Mảng) = {all_x_data_input}")
    print(f"  Y (Mảng) = {all_y_data_input}")
    print(f"  n (Bậc) = {n} (có {n+1} điểm)")
    print(f"  k (Số điểm) = {k}")
    print(f"  x (Điểm) = {x}")

    # --- 2. Kiểm tra điều kiện ---
    print(f"[Bước 2] Kiểm tra điều kiện input:")
    if n < 0:
        print("  Lỗi: Dữ liệu rỗng.")
        return None, None
        
    print(f"  Kiểm tra k >= 1 và k <= n+1:")
    if not (k >= 1 and k <= n + 1):
        print(f"    Lỗi: Số điểm k={k} không hợp lệ. Phải là 1 <= k <= {n+1}.")
        return None, None
    print(f"    -> k={k} hợp lệ.")
    
    print(f"  Kiểm tra X và Y cùng kích thước:")
    if len(all_x_data) != len(all_y_data_input):
        print(f"    Lỗi: Mảng X ({len(all_x_data)}) và Y ({len(all_y_data_input)}) không cùng kích thước.")
        return None, None
    print(f"    -> Kích thước {n+1} hợp lệ.")
        
    # --- 3. Thiết lập điều kiện dừng ---
    print(f"[Bước 3] Thiết lập điều kiện dừng:")
    print(f"  Không cần thiết lập (tính toán trực tiếp).")

    print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Tính bước nhảy h (dùng SymPy)
    print(f"  [4.1] Tính bước nhảy h (kiểm tra cách đều):")
    if n > 0:
        h = sympy.simplify(all_x_data[1] - all_x_data[0])
        print(f"    h = X[1] - X[0] = {all_x_data[1]} - {all_x_data[0]} = {h}")
        
        # (Kiểm tra toàn bộ mảng X xem có cách đều không)
        for i in range(2, n + 1):
            h_i = sympy.simplify(all_x_data[i] - all_x_data[i-1])
            
            is_close = False
            # Nếu cả 2 đều là số, dùng math.isclose để so sánh
            if h.is_number and h_i.is_number:
                is_close = math.isclose(float(h), float(h_i), rel_tol=1e-9)
            # Nếu là biểu thức, dùng so sánh symbolic
            else:
                is_close = (sympy.simplify(h_i - h) == 0)

            if not is_close:
                print(f"    Lỗi: Mốc không cách đều. Khoảng h_i={h_i} (tại X[{i}]) != h={h}", file=sys.stderr)
                return None, None
        print(f"    -> Các mốc cách đều h = {h}.")
            
    else:
        h = 1
        print(f"    n=0, đặt h = 1.")
        
    # Bước 4.2: Tìm chỉ số j của mốc x_j nằm gần x nhất
    print(f"  [4.2] Tìm chỉ số j (mốc x_j gần x nhất):")
    
    # * Tính j' = (x - x_0) / h
    j_prime = sympy.simplify((x - all_x_data[0]) / h)
    print(f"    Tính j' = (x - X[0]) / h = ({x} - {all_x_data[0]}) / {h} = {j_prime}")
    
    # * KIỂM TRA: j_prime phải là một SỐ
    if not j_prime.is_number:
        print(f"    Lỗi: Không thể xác định chỉ số 'j' từ input symbolic.")
        print(f"    -> j' = {j_prime} (là biểu thức). Dừng lại.")
        return None, None

    # * Làm tròn j = round(j')
    j_float = float(j_prime)
    j = round(j_float)
    print(f"    Làm tròn j = round({j_float:.4f}) = {j}")
    
    # * Hiệu chỉnh j để đảm bảo j nằm trong [0, n]
    j_old = j
    j = max(0, min(n, j))
    j = int(j) 
    print(f"    Hiệu chỉnh j = max(0, min(n, j)) = max(0, min({n}, {j_old})) = {j}")
    print(f"    -> Chỉ số gần nhất j = {j} (tương ứng x[{j}] = {all_x_data_input[j]})")

    # Bước 4.3: Xác định chỉ số bắt đầu start_idx
    print(f"  [4.3] Xác định chỉ số bắt đầu start_idx:")
    k_minus_1_div_2 = (k - 1) // 2
    start_idx = j - k_minus_1_div_2
    print(f"    start_idx = j - (k - 1)//2 = {j} - ({k} - 1)//2 = {j} - {k_minus_1_div_2} = {start_idx}")
    
    # Bước 4.4: Hiệu chỉnh start_idx
    print(f"  [4.4] Hiệu chỉnh start_idx để đảm bảo k điểm nằm trong [0, {n}]:")
    start_idx_old = start_idx
    
    if start_idx < 0:
        start_idx = 0
        print(f"    Phát hiện start_idx ({start_idx_old}) < 0. Gán start_idx = 0.")
    
    # (Chỉ số cuối cùng của mảng con là start_idx + k - 1)
    if start_idx + k - 1 > n:
        start_idx = n - k + 1
        print(f"    Phát hiện start_idx + k - 1 ({start_idx_old + k - 1}) > n ({n}). Gán start_idx = n - k + 1 = {start_idx}.")
    
    if start_idx == start_idx_old:
        print(f"    start_idx = {start_idx} (không cần hiệu chỉnh).")
        
    start_idx = int(start_idx)
    print(f"    -> Chỉ số bắt đầu cuối cùng: {start_idx} (sẽ lấy từ X[{start_idx}] đến X[{start_idx + k - 1}])")

    # Bước 4.5: Khởi tạo hai mảng mới (kích thước k)
    print(f"  [4.5] Khởi tạo X_new, Y_new (kích thước k={k})")
    X_new = [None] * k 
    Y_new = [None] * k 
    
    # Bước 4.6 & 4.7: Sao chép k điểm
    print(f"  [4.6 & 4.7] Thiết lập vòng lặp i = 0 đến {k-1} và sao chép dữ liệu:")
    # Trả về giá trị GỐC (dạng string/số) thay vì đối tượng SymPy
    for i in range(k):
        idx = start_idx + i
        X_new[i] = all_x_data_input[idx]
        Y_new[i] = all_y_data_input[idx]
        print(f"    i = {i}: X_new[{i}] = X[{idx}] = {X_new[i]}; Y_new[{i}] = Y[{idx}] = {Y_new[i]}")

    # --- 5. Xác định output ---
    print(f"[Bước 5] Xác định output:")
    print(f"  X_new = {X_new}")
    print(f"  Y_new = {Y_new}")
    print("--- Hoàn tất trích xuất ---")
    
    return X_new, Y_new