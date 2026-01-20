import numpy as np

def solve_least_squares_show_matrices(x, y):
    """
    Giải bài toán bình phương tối thiểu cho hàm: y = a*x + b/x
    Hiển thị chi tiết các ma trận Phi, M, và véc-tơ b.
    """
    # Chuyển đổi sang numpy array để dễ tính toán
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    
    # Lọc bỏ các giá trị x = 0 (nếu có)
    if np.any(x == 0):
        print("Cảnh báo: Loại bỏ các điểm x = 0.")
        valid = x != 0
        x = x[valid]
        y = y[valid]

    n = len(x)
    print(f"Số lượng điểm dữ liệu n = {n}")

    # --- BƯỚC 1: XÂY DỰNG MA TRẬN THIẾT KẾ PHI ---
    # Hàm cơ sở 1: phi1(x) = x
    # Hàm cơ sở 2: phi2(x) = 1/x
    col1 = x
    col2 = 1 / x
    
    # Ghép 2 cột lại thành ma trận Phi (n dòng, 2 cột)
    Phi = np.column_stack((col1, col2))
    
    print("\n" + "="*40)
    print("1. MA TRẬN THIẾT KẾ (PHI) - Kích thước {}x2".format(n))
    print("Cột 1 là x, Cột 2 là 1/x")
    print("-" * 40)
    print(Phi)

    # --- BƯỚC 2: THIẾT LẬP HỆ PHƯƠNG TRÌNH CHUẨN ---
    # Tính Ma trận Gram: M = Phi^T * Phi
    M = Phi.T @ Phi  # Dấu @ là phép nhân ma trận trong Python
    
    # Tính Véc-tơ vế phải: b = Phi^T * Y
    vector_b = Phi.T @ y

    print("\n" + "="*40)
    print("2. MA TRẬN GRAM (M = Phi^T * Phi)")
    print("-" * 40)
    print(M)
    
    print("\n" + "="*40)
    print("3. VÉC-TƠ VẾ PHẢI (b = Phi^T * Y)")
    print("-" * 40)
    print(vector_b)

    # --- BƯỚC 3: GIẢI HỆ PHƯƠNG TRÌNH M * a = b ---
    try:
        # Giải hệ phương trình tuyến tính
        coeffs = np.linalg.solve(M, vector_b)
        a = coeffs[0]
        b_param = coeffs[1] # Đặt tên b_param để không nhầm với vector_b
        
        print("\n" + "="*40)
        print("KẾT QUẢ NGHIỆM:")
        print(f"a = {a:.6f}")
        print(f"b = {b_param:.6f}")
        
        sign = "+" if b_param >= 0 else "-"
        print(f"\n=> Hàm thực nghiệm: y = {a:.4f}x {sign} {abs(b_param):.4f}/x")
        
    except np.linalg.LinAlgError:
        print("\nLỗi: Ma trận suy biến, không thể giải.")

# --- CHẠY THỬ VỚI DỮ LIỆU ---
# Bạn thay dữ liệu của bạn vào đây
x_data = [1.0, 2.0, 3.0, 4.0, -2.0]
y_data = [7.1, 6.4, 7.8, 9.2, -6.6]

solve_least_squares_show_matrices(x_data, y_data)