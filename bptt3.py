import numpy as np
import pandas as pd

def solve_exp_quadratic_full_matrices(x_in, y_in):
    """
    Giải bài toán tìm hàm: y = a * e^(bx + cx^2)
    (Tự động xử lý dữ liệu âm bằng cách tịnh tiến y + k)
    Hiển thị đầy đủ các ma trận trung gian.
    """
    # Chuyển đổi dữ liệu sang numpy array
    x = np.array(x_in, dtype=float)
    y = np.array(y_in, dtype=float)
    n = len(x)
    
    print(f"=== GIẢI BÀI TOÁN BÌNH PHƯƠNG TỐI THIỂU (n={n}) ===")
    print("Mô hình: y = a * e^(bx + cx^2) [- k]")
    
    # --- BƯỚC 1: XỬ LÝ DỮ LIỆU (DATA PRE-PROCESSING) ---
    print("\n" + "="*50)
    print("BƯỚC 1: XỬ LÝ DỮ LIỆU & TUYẾN TÍNH HÓA")
    print("-" * 50)
    
    min_val = np.min(y)
    k_shift = 0.0
    
    # Kiểm tra và tính k
    if min_val <= 0:
        k_shift = 1.0 - min_val
        print(f"-> Phát hiện dữ liệu y <= 0 (min={min_val}).")
        print(f"-> Tịnh tiến y một lượng k = {k_shift:.4f} để đảm bảo ln(y+k) xác định.")
    else:
        print("-> Dữ liệu y dương, k = 0.")

    y_shifted = y + k_shift
    Y_log = np.log(y_shifted)
    
    # In bảng dữ liệu chi tiết
    df_data = pd.DataFrame({
        'x': x,
        'y_goc': y,
        'y_shift (y+k)': y_shifted,
        'ln(y_shift) [Y lớn]': Y_log
    })
    print(df_data.to_string(index=False, float_format=lambda x: "{:.4f}".format(x)))

    # --- BƯỚC 2: TẠO MA TRẬN THIẾT KẾ PHI ---
    print("\n" + "="*50)
    print("BƯỚC 2: MA TRẬN THIẾT KẾ (MATRIX PHI)")
    print("-" * 50)
    
    # Hàm tuyến tính hóa: ln(y) = c*x^2 + b*x + ln(a)
    # Thứ tự cột: [x^2, x, 1] tương ứng với tham số [c, b, ln(a)]
    col_x2 = x**2
    col_x = x
    col_1 = np.ones(n)
    
    Phi = np.column_stack((col_x2, col_x, col_1))
    
    # In ma trận Phi có dán nhãn cột
    df_phi = pd.DataFrame(Phi, columns=['x^2 (c)', 'x (b)', '1 (ln a)'])
    print(df_phi.to_string(index=False, float_format=lambda x: "{:.4f}".format(x)))

    # --- BƯỚC 3: HỆ PHƯƠNG TRÌNH CHUẨN (NORMAL EQUATIONS) ---
    print("\n" + "="*50)
    print("BƯỚC 3: HỆ PHƯƠNG TRÌNH ĐẠI SỐ (Ma * w = V)")
    print("-" * 50)
    
    # Tính M = Phi.T * Phi
    M = Phi.T @ Phi
    
    # Tính V = Phi.T * Y_log
    V = Phi.T @ Y_log
    
    print("a) Ma trận Gram (M = Phi^T . Phi): kích thước 3x3")
    print(M)
    
    print("\nb) Véc-tơ vế phải (V = Phi^T . Y_log): kích thước 3x1")
    print(V)

    # --- BƯỚC 4: GIẢI HỆ VÀ KẾT QUẢ ---
    print("\n" + "="*50)
    print("BƯỚC 4: GIẢI HỆ VÀ KẾT LUẬN")
    print("-" * 50)
    
    try:
        # Giải hệ phương trình
        w = np.linalg.solve(M, V)
        c_param, b_param, A_param = w
        
        print(f"Nghiệm vector w (c, b, ln a): {w}")
        
        # Chuyển đổi về tham số gốc
        a_param = np.exp(A_param)
        
        print(f"\n-> Tham số a (e^A) = {a_param:.6f}")
        print(f"-> Tham số b       = {b_param:.6f}")
        print(f"-> Tham số c       = {c_param:.6f}")
        print(f"-> Tham số k       = {k_shift:.6f}")
        
        # In phương trình dạng text
        sign_k = f"- {k_shift:.4f}" if k_shift > 0 else ""
        print(f"\n=> HÀM TÌM ĐƯỢC: y = {a_param:.4f}.e^({b_param:.4f}x + {c_param:.4f}x^2) {sign_k}")
        
        # Đánh giá sai số
        y_pred = a_param * np.exp(b_param * x + c_param * x**2) - k_shift
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        print(f"   Sai số RMSE     : {rmse:.6f}")
        
    except np.linalg.LinAlgError:
        print("LỖI: Ma trận suy biến, không thể giải hệ phương trình.")

# --- DỮ LIỆU TEST ---
# Dữ liệu mẫu (bao gồm số âm để test tính năng tịnh tiến)
x_sample = [-2.0, -1.0, 0.0, 1.0, 2.0]
y_sample = [17.0, 6.0, 2.0, -0.5, -1.0] 

solve_exp_quadratic_full_matrices(x_sample, y_sample)