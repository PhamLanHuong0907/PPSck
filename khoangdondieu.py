import sympy
import sys

def _sign(x):
    """
    Hàm hỗ trợ (private) để lấy dấu của một số.
    (Tương ứng với hàm sign() trong thuật toán)
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def tim_khoang_don_dieu(X_input, Y_input, verbose=False):
    """
    Xác định các khoảng đơn điệu [X[i], X[j]] dựa trên giá trị Y.
    (Theo thuật toán trong ảnh)

    :param X_input: Mảng các mốc (có thể là số hoặc biểu thức)
    :param Y_input: Mảng các giá trị (PHẢI LÀ SỐ)
    :param verbose: Nếu True, sẽ in ra các bước thực hiện
    :return: Danh sách các khoảng (MonotonicIntervals)
    """
    
    # --- 1. & 2. Xác định và Kiểm tra input ---
    try:
        # X có thể là symbolic
        X = [sympy.sympify(val) for val in X_input] 
        # Y phải là số
        Y = [sympy.sympify(val) for val in Y_input]
    except sympy.SympifyError as e:
        print(f"Lỗi: Input không hợp lệ, không thể chuyển đổi. '{e}'", file=sys.stderr)
        return []
        
    if len(X) != len(Y):
        print("Lỗi: Mảng X và Y không cùng kích thước.", file=sys.stderr)
        return []
    
    n = len(X) - 1 # n là chỉ số cuối cùng (n+1 điểm)
    if n < 1: # Cần ít nhất 2 điểm (X[0], X[1])
        print("Lỗi: Cần ít nhất 2 điểm (n >= 1).", file=sys.stderr)
        return []

    # Kiểm tra Y có phải là số không
    for i, y_val in enumerate(Y):
        if not y_val.is_number:
            print(f"Lỗi: Y[{i}] ({y_val}) phải là một số.", file=sys.stderr)
            return []

    if verbose:
        print("\n--- Bắt đầu thuật toán tìm khoảng đơn điệu ---")

    # --- 4. Thực hiện tính toán ---
    
    # Bước 4.1: Khởi tạo
    MonotonicIntervals = []
    
    # Bước 4.2: Khởi tạo start_idx
    start_idx = 0
    
    # Bước 4.3: Tính sign_prev
    diff_0 = Y[1] - Y[0]
    sign_prev = _sign(diff_0)
    
    if verbose:
        print(f"Bước 4.1-4.2: Khởi tạo: MonotonicIntervals = [], start_idx = 0")
        print(f"Bước 4.3: (Y[1]-Y[0]) = {diff_0}. Gán sign_prev = {sign_prev}")

    # Bước 4.4: Thiết lập vòng lặp for i chạy từ 1 đến n - 1
    if verbose:
        print(f"Bước 4.4-4.6: Bắt đầu vòng lặp (i từ 1 đến {n-1}):")
        
    for i in range(1, n): # Vòng lặp i = 1, 2, ..., n-1
        
        # Bước 4.5 (Trong vòng lặp):
        diff_curr = Y[i+1] - Y[i]
        sign_curr = _sign(diff_curr)
        
        if verbose:
            print(f"  i = {i}:")
            print(f"    Bước 4.5: (Y[{i+1}]-Y[{i}]) = {diff_curr}. Gán sign_curr = {sign_curr}")

        # Bước 4.6 (Trong vòng lặp):
        if (sign_curr != sign_prev) and (sign_curr != 0):
            if verbose:
                print(f"    Bước 4.6: Đổi dấu! (sign_curr={sign_curr} != sign_prev={sign_prev}) và sign_curr != 0.")
            
            # * Thêm khoảng
            interval = [X_input[start_idx], X_input[i]]
            MonotonicIntervals.append(interval)
            
            # * Cập nhật
            start_idx = i
            sign_prev = sign_curr
            
            if verbose:
                print(f"      * Thêm khoảng: {interval}")
                print(f"      * Cập nhật: start_idx = {i}, sign_prev = {sign_curr}")
        else:
            if verbose:
                if sign_curr == sign_prev:
                    print(f"    Bước 4.6: Cùng dấu (tiếp tục).")
                elif sign_curr == 0:
                    print(f"    Bước 4.6: Đoạn bằng (bỏ qua, giữ sign_prev={sign_prev}).")
                        
    # Bước 4.7 (Sau vòng lặp):
    if verbose:
        print(f"Bước 4.7: (Sau vòng lặp) Thêm khoảng cuối cùng.")
    
    last_interval = [X_input[start_idx], X_input[n]] # X[n] là mốc cuối cùng
    MonotonicIntervals.append(last_interval)
    
    if verbose:
        print(f"    * Thêm khoảng: {last_interval}")

    # --- 5. Xác định output ---
    if verbose:
        print("--- Hoàn tất thuật toán ---")
    return MonotonicIntervals