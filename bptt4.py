import numpy as np
import pandas as pd

def solve_power_law_full_matrices(x_in, y_in):
    """
    Giải bài toán: y = a * x^b
    (Có xử lý dữ liệu âm/bằng 0 cho cả x và y bằng cách tịnh tiến)
    """
    x = np.array(x_in, dtype=float)
    y = np.array(y_in, dtype=float)
    n = len(x)
    
    print(f"=== GIẢI BÀI TOÁN: y = a * x^b (n={n}) ===")
    
    # --- BƯỚC 1: XỬ LÝ DỮ LIỆU (DATA PRE-PROCESSING) ---
    print("\n" + "="*60)
    print("BƯỚC 1: XỬ LÝ DỮ LIỆU (Tịnh tiến để thỏa mãn điều kiện Logarit)")
    print("-" * 60)
    
    # 1.1 Xử lý x (x phải > 0 mới tính được ln(x))
    min_x = np.min(x)
    kx = 0.0
    if min_x <= 0:
        kx = 1.0 - min_x
        print(f"-> Phát hiện x <= 0. Tịnh tiến x một lượng kx = {kx:.4f}")
    else:
        print("-> Dữ liệu x dương, kx = 0.")

    # 1.2 Xử lý y (y phải > 0 mới tính được ln(y))
    min_y = np.min(y)
    ky = 0.0
    if min_y <= 0:
        ky = 1.0 - min_y
        print(f"-> Phát hiện y <= 0. Tịnh tiến y một lượng ky = {ky:.4f}")
    else:
        print("-> Dữ liệu y dương, ky = 0.")

    # Áp dụng tịnh tiến
    x_shifted = x + kx
    y_shifted = y + ky
    
    # Tính Logarit
    X_log = np.log(x_shifted) # ln(x')
    Y_log = np.log(y_shifted) # ln(y')
    
    # In bảng chi tiết
    df_data = pd.DataFrame({
        'x_goc': x,
        'x_shift': x_shifted,
        'ln(x_shift) [X]': X_log,
        '|': ['|']*n, # Cột ngăn cách
        'y_goc': y,
        'y_shift': y_shifted,
        'ln(y_shift) [Y]': Y_log
    })
    print(df_data.to_string(index=False, float_format=lambda x: "{:.4f}".format(x) if isinstance(x, (float, int)) else x))

    # --- BƯỚC 2: MA TRẬN THIẾT KẾ PHI ---
    print("\n" + "="*60)
    print("BƯỚC 2: XÂY DỰNG MA TRẬN THIẾT KẾ (PHI)")
    print("-" * 60)
    print("Mô hình tuyến tính: Y = A + b*X")
    print(" - Cột 1: 1 (Hệ số tự do A = ln a)")
    print(" - Cột 2: ln(x_shift) (Hệ số mũ b)")
    
    col_1 = np.ones(n)
    col_2 = X_log
    
    Phi = np.column_stack((col_1, col_2))
    
    # In ma trận Phi
    df_phi = pd.DataFrame(Phi, columns=['1 (ln a)', 'ln(x) (b)'])
    print(df_phi.to_string(index=False, float_format=lambda x: "{:.4f}".format(x)))

    # --- BƯỚC 3: HỆ PHƯƠNG TRÌNH CHUẨN ---
    print("\n" + "="*60)
    print("BƯỚC 3: TÍNH TOÁN MA TRẬN TRUNG GIAN")
    print("-" * 60)
    
    M = Phi.T @ Phi       # Ma trận Gram
    V = Phi.T @ Y_log     # Véc-tơ vế phải
    
    print("a) Ma trận Gram (M = Phi^T . Phi): kích thước 2x2")
    print(M)
    
    print("\nb) Véc-tơ vế phải (V = Phi^T . Y_log): kích thước 2x1")
    print(V)

    # --- BƯỚC 4: GIẢI VÀ KẾT LUẬN ---
    print("\n" + "="*60)
    print("BƯỚC 4: KẾT QUẢ CUỐI CÙNG")
    print("-" * 60)
    
    try:
        # Giải hệ M * w = V
        w = np.linalg.solve(M, V)
        A_param, b_param = w
        
        # Khôi phục a từ A
        a_param = np.exp(A_param)
        
        print(f"Nghiệm vector w (ln a, b): {w}")
        print(f"-> Tham số A (ln a) = {A_param:.6f} => a = {a_param:.6f}")
        print(f"-> Tham số b (mũ)   = {b_param:.6f}")
        print(f"-> Tịnh tiến kx={kx}, ky={ky}")
        
        # Tạo chuỗi hàm số
        str_x = "x" if kx == 0 else f"(x + {kx:.4f})"
        str_ky = "" if ky == 0 else f"- {ky:.4f}"
        
        print(f"\n=> HÀM THỰC NGHIỆM: y = {a_param:.4f} * {str_x}^{b_param:.4f} {str_ky}")
        
        # Đánh giá sai số RMSE
        # y_pred = a * (x+kx)^b - ky
        y_pred = a_param * np.power(x_shifted, b_param) - ky
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        print(f"   Sai số RMSE      : {rmse:.6f}")

    except np.linalg.LinAlgError:
        print("LỖI: Ma trận suy biến, không thể giải.")

# --- CHẠY THỬ VỚI DỮ LIỆU PHỨC TẠP (CÓ ÂM) ---
# Dữ liệu giả lập hàm y = 2 * (x+3)^0.5 - 5
# x có giá trị âm, y có giá trị âm
x_test = [-2.0, -1.0, 0.0, 1.0, 2.0, 5.0]
y_test = [-3.0, -2.17, -1.53, -1.0, -0.52, 0.66] 

solve_power_law_full_matrices(x_test, y_test)