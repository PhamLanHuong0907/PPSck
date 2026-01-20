import numpy as np

def solve_least_squares_quadratic_cos(x_in, y_in):
    """
    Giải bài toán bình phương tối thiểu cho hàm: y = a*x^2 + b*cos(x) + c
    """
    # 1. Chuyển đổi dữ liệu sang dạng mảng NumPy
    x = np.array(x_in, dtype=float)
    y = np.array(y_in, dtype=float)
    n = len(x)
    
    print(f"--- GIẢI BÀI TOÁN: y = ax^2 + b*cos(x) + c (với n={n}) ---")

    # 2. XÂY DỰNG MA TRẬN THIẾT KẾ PHI (Kích thước n x 3)
    # Cột 1: x^2 (tương ứng tham số a)
    col_1 = x**2
    
    # Cột 2: cos(x) (tương ứng tham số b)
    # Lưu ý: x phải ở đơn vị radian. Nếu đề cho độ thì phải đổi sang radian: np.deg2rad(x)
    col_2 = np.cos(x)
    
    # Cột 3: Số 1 (tương ứng tham số c - hằng số)
    col_3 = np.ones(n)
    
    # Ghép 3 cột lại
    Phi = np.column_stack((col_1, col_2, col_3))
    
    print("\n1. Ma trận thiết kế Phi (5 dòng đầu):")
    print(Phi[:5]) 
    if n > 5: print("...")

    # 3. THIẾT LẬP HỆ PHƯƠNG TRÌNH CHUẨN
    # Ma trận Gram: M = Phi^T * Phi
    M = Phi.T @ Phi
    
    # Véc-tơ vế phải: V = Phi^T * y
    V = Phi.T @ y

    print("\n2. Ma trận Gram M (3x3):")
    print(M)
    print("\n3. Véc-tơ vế phải V:")
    print(V)

    # 4. GIẢI HỆ PHƯƠNG TRÌNH M * params = V
    try:
        # params sẽ chứa [a, b, c] theo thứ tự cột của Phi
        params = np.linalg.solve(M, V)
        a, b, c = params
        
        print("\n" + "="*40)
        print("KẾT QUẢ TÌM ĐƯỢC:")
        print(f"a = {a:.6f}")
        print(f"b = {b:.6f}")
        print(f"c = {c:.6f}")
        
        # In phương trình hoàn chỉnh
        def fmt_sign(val): return f"+ {val:.4f}" if val >= 0 else f"- {abs(val):.4f}"
        print(f"\n=> Hàm thực nghiệm: y = {a:.4f}x^2 {fmt_sign(b)}cos(x) {fmt_sign(c)}")
        print("="*40)
        
        # 5. ĐÁNH GIÁ SAI SỐ
        y_pred = a * x**2 + b * np.cos(x) + c
        residuals = y - y_pred
        rmse = np.sqrt(np.mean(residuals**2))
        print(f"\nSai số trung bình phương (RMSE): {rmse:.6f}")
        
    except np.linalg.LinAlgError:
        print("\nLỗi: Ma trận suy biến, không thể giải hệ phương trình.")

# --- CHẠY THỬ VỚI DỮ LIỆU GIẢ LẬP ---
# (Bạn thay dữ liệu thật từ file của bạn vào đây)
# Tạo dữ liệu mẫu khớp với hàm y = 1.5x^2 - 2cos(x) + 3
x_dummy = np.linspace(-2, 2, 6) # 6 điểm từ -2 đến 2
y_dummy = 1.5 * x_dummy**2 - 2 * np.cos(x_dummy) + 3
# Thêm chút nhiễu để giống thực nghiệm
y_dummy += np.array([0.1, -0.05, 0.02, 0.1, -0.1, 0.05])

solve_least_squares_quadratic_cos(x_dummy, y_dummy)