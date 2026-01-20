import sympy
import sys

def tim_khoang_cach_ly(X_input, Y_input, y_bar_input, verbose=False):
    """
    Xác định các khoảng [X[i], X[i+1]] mà giá trị y_bar nằm
    giữa Y[i] và Y[i+1], dựa trên thuật toán trong ảnh.
    (ĐÃ CẬP NHẬT ĐỂ IN CHI TIẾT CÁC BƯỚC)

    :param X_input: Mảng các mốc (có thể là số hoặc biểu thức)
    :param Y_input: Mảng các giá trị (PHẢI LÀ SỐ)
    :param y_bar_input: Giá trị y cần tìm (PHẢI LÀ SỐ)
    :param verbose: Nếu True, sẽ in ra các bước thực hiện
    :return: Danh sách các khoảng (Intervals)
    """
    
    # --- 1. Xác định input ---
    try:
        # X có thể là symbolic
        X = [sympy.sympify(val) for val in X_input] 
        # Y và y_bar phải là số để so sánh
        Y = [sympy.sympify(val) for val in Y_input]
        y_bar = sympy.sympify(y_bar_input)
    except sympy.SympifyError as e:
        if verbose: print(f"[Bước 1] Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        else: print(f"Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return []
        
    n = len(X) - 1 # n là BẬC (theo ảnh là n+1 điểm)
    
    if verbose:
        print("\n--- Bắt đầu thuật toán tìm khoảng cách ly ---")
        print(f"[Bước 1] Xác định input:")
        print(f"  X (Mảng) = {X_input} (n+1 = {n+1} điểm)")
        print(f"  Y (Mảng) = {Y_input}")
        print(f"  y_bar (Giá trị) = {y_bar_input}")
        print(f"  n (Bậc) = {n}")

    # --- 2. Kiểm tra điều kiện input ---
    if verbose: print(f"[Bước 2] Kiểm tra điều kiện input:")
    
    if len(X) != len(Y):
        if verbose: print(f"  Lỗi: Mảng X ({len(X)}) và Y ({len(Y)}) không cùng kích thước.", file=sys.stderr)
        else: print("Lỗi: Mảng X và Y không cùng kích thước.", file=sys.stderr)
        return []
    if verbose: print(f"  -> Kích thước X và Y bằng nhau (n+1 = {n+1}). (Hợp lệ)")
    
    if n < 1:
        if verbose: print(f"  Lỗi: Cần ít nhất 2 điểm (n >= 1). Nhận được n = {n}.", file=sys.stderr)
        else: print("Lỗi: Cần ít nhất 2 điểm (n >= 1).", file=sys.stderr)
        return []
    if verbose: print(f"  -> n = {n} >= 1. (Hợp lệ)")

    # Kiểm tra Y và y_bar có phải là số không
    if not y_bar.is_number:
        if verbose: print(f"  Lỗi: y_bar ({y_bar}) phải là một số.", file=sys.stderr)
        else: print(f"Lỗi: y_bar ({y_bar}) phải là một số.", file=sys.stderr)
        return []
    if verbose: print(f"  -> y_bar là số. (Hợp lệ)")
    
    for i, y_val in enumerate(Y):
        if not y_val.is_number:
            if verbose: print(f"  Lỗi: Y[{i}] ({y_val}) phải là một số.", file=sys.stderr)
            else: print(f"Lỗi: Y[{i}] ({y_val}) phải là một số.", file=sys.stderr)
            return []
    if verbose: print(f"  -> Y là mảng số. (Hợp lệ)")

    # --- 3. Thiết lập điều kiện dừng ---
    if verbose:
        print(f"[Bước 3] Thiết lập điều kiện dừng:")
        print(f"  Không cần thiết lập (vòng lặp for xác định).")

    # --- 4. Thực hiện tính toán ---
    if verbose: print(f"[Bước 4] Thực hiện tính toán:")
    
    # Bước 4.1: Khởi tạo danh sách rỗng
    if verbose: print(f"  [4.1] Khởi tạo danh sách rỗng Intervals = []")
    Intervals = []
    
    # Bước 4.2: Thiết lập vòng lặp for i chạy từ 0 đến n - 1
    if verbose: print(f"  [4.2] Thiết lập vòng lặp for i chạy từ 0 đến {n-1}:")
    
    for i in range(n): # (range(n) chạy từ 0 đến n-1)
        
        y_i = Y[i]
        y_i_plus_1 = Y[i+1]
        
        if verbose:
            print(f"    --- i = {i} ---")
            print(f"      Khoảng X: [{X_input[i]}, {X_input[i+1]}]")
            print(f"      Khoảng Y: [{y_i}, {y_i_plus_1}]")

        # Bước 4.3 (Trong vòng lặp): Kiểm tra
        check = (y_i - y_bar) * (y_i_plus_1 - y_bar)
        
        if verbose:
            print(f"      [4.3] Check = (Y[{i}] - y_bar) * (Y[{i+1}] - y_bar)")
            print(f"            = ({y_i} - {y_bar}) * ({y_i_plus_1} - {y_bar})")
            print(f"            = {y_i - y_bar} * {y_i_plus_1 - y_bar} = {check}")

        # Bước 4.4 (Trong vòng lặp): Nếu check <= 0
        if check <= 0:
            khoang = [X_input[i], X_input[i+1]]
            Intervals.append(khoang)
            if verbose:
                print(f"      [4.4] Kết quả: check <= 0. Thêm khoảng {khoang}")
        else:
            if verbose:
                print(f"      [4.4] Kết quả: check > 0. Bỏ qua khoảng.")

    if verbose: print("    --- Kết thúc vòng lặp ---")

    # --- 5. Xác định output ---
    if verbose:
        print(f"[Bước 5] Xác định output:")
        print(f"  Danh sách Intervals: {Intervals}")
        print("--- Hoàn tất thuật toán ---")
        
    return Intervals