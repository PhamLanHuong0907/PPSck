import numpy as np
import pandas as pd

def find_best_fit_model(x_in, y_in):
    """
    Tự động thử nhiều mô hình hàm số và tìm ra mô hình có sai số nhỏ nhất.
    """
    x = np.array(x_in, dtype=float)
    y = np.array(y_in, dtype=float)
    n = len(x)
    
    results = [] # Danh sách lưu kết quả các mô hình
    
    print(f"--- ĐANG PHÂN TÍCH DỮ LIỆU (n={n} điểm) ---\n")

    # --- MODEL 1: TUYẾN TÍNH (LINEAR) y = ax + b ---
    # Phi = [x, 1]
    Phi_lin = np.column_stack((x, np.ones(n)))
    try:
        w = np.linalg.solve(Phi_lin.T @ Phi_lin, Phi_lin.T @ y)
        a, b = w
        y_pred = a*x + b
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        results.append({
            'Loại hàm': 'Tuyến tính (y = ax + b)',
            'RMSE': rmse,
            'Tham số': f'a={a:.4f}, b={b:.4f}',
            'Công thức': f'y = {a:.4f}x + {b:.4f}'
        })
    except: pass

    # --- MODEL 2: BẬC 2 (QUADRATIC) y = ax^2 + bx + c ---
    # Phi = [x^2, x, 1]
    Phi_quad = np.column_stack((x**2, x, np.ones(n)))
    try:
        w = np.linalg.solve(Phi_quad.T @ Phi_quad, Phi_quad.T @ y)
        a, b, c = w
        y_pred = a*x**2 + b*x + c
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        results.append({
            'Loại hàm': 'Bậc 2 (y = ax^2 + bx + c)',
            'RMSE': rmse,
            'Tham số': f'a={a:.4f}, b={b:.4f}, c={c:.4f}',
            'Công thức': f'y = {a:.4f}x^2 + {b:.4f}x + {c:.4f}'
        })
    except: pass

    # --- MODEL 3: NGHỊCH ĐẢO (INVERSE) y = ax + b/x ---
    # Phi = [x, 1/x] (Lưu ý x phải != 0)
    if not np.any(x == 0):
        Phi_inv = np.column_stack((x, 1/x))
        try:
            w = np.linalg.solve(Phi_inv.T @ Phi_inv, Phi_inv.T @ y)
            a, b = w
            y_pred = a*x + b/x
            rmse = np.sqrt(np.mean((y - y_pred)**2))
            results.append({
                'Loại hàm': 'Nghịch đảo (y = ax + b/x)',
                'RMSE': rmse,
                'Tham số': f'a={a:.4f}, b={b:.4f}',
                'Công thức': f'y = {a:.4f}x + {b:.4f}/x'
            })
        except: pass

    # --- MODEL 4: HÀM MŨ (EXPONENTIAL) y = ae^(bx) ---
    # Tuyến tính hóa: ln(y+ky) = ln(a) + bx
    # Xử lý âm cho y
    ky = 0
    if np.min(y) <= 0: ky = 1.0 - np.min(y)
    y_shift = y + ky
    
    Phi_exp = np.column_stack((x, np.ones(n)))
    try:
        w = np.linalg.solve(Phi_exp.T @ Phi_exp, Phi_exp.T @ np.log(y_shift))
        b, ln_a = w
        a = np.exp(ln_a)
        y_pred = a * np.exp(b*x) - ky
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        
        sign_k = f" - {ky:.4f}" if ky > 0 else ""
        results.append({
            'Loại hàm': 'Hàm Mũ (y = ae^bx)',
            'RMSE': rmse,
            'Tham số': f'a={a:.4f}, b={b:.4f}, k={ky}',
            'Công thức': f'y = {a:.4f}e^({b:.4f}x){sign_k}'
        })
    except: pass

    # --- MODEL 5: HÀM LŨY THỪA (POWER) y = ax^b ---
    # Tuyến tính hóa: ln(y+ky) = ln(a) + b*ln(x+kx)
    # Xử lý âm cho cả x và y
    kx = 0
    if np.min(x) <= 0: kx = 1.0 - np.min(x)
    x_shift = x + kx
    
    # ky đã tính ở trên
    
    Phi_pow = np.column_stack((np.ones(n), np.log(x_shift)))
    try:
        w = np.linalg.solve(Phi_pow.T @ Phi_pow, Phi_pow.T @ np.log(y_shift))
        ln_a, b = w
        a = np.exp(ln_a)
        y_pred = a * np.power(x_shift, b) - ky
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        
        str_x = "x" if kx==0 else f"(x+{kx})"
        sign_k = f" - {ky:.4f}" if ky > 0 else ""
        results.append({
            'Loại hàm': 'Lũy thừa (y = ax^b)',
            'RMSE': rmse,
            'Tham số': f'a={a:.4f}, b={b:.4f}',
            'Công thức': f'y = {a:.4f}{str_x}^{b:.4f}{sign_k}'
        })
    except: pass

    # --- TỔNG HỢP VÀ XẾP HẠNG ---
    df_results = pd.DataFrame(results)
    # Sắp xếp theo RMSE tăng dần (Sai số càng nhỏ càng tốt)
    df_results = df_results.sort_values(by='RMSE').reset_index(drop=True)
    
    print("BẢNG XẾP HẠNG CÁC MÔ HÌNH (TỪ TỐT NHẤT ĐẾN TỆ NHẤT):")
    print("-" * 100)
    # In đẹp
    print(df_results[['Loại hàm', 'RMSE', 'Công thức']].to_string(index=False))
    print("-" * 100)
    
    best_model = df_results.iloc[0]
    print(f"\n✅ KHUYẾN NGHỊ: Dữ liệu này phù hợp nhất với {best_model['Loại hàm']}")
    print(f"   với sai số RMSE = {best_model['RMSE']:.6f}")

# ==========================================
# VÍ DỤ SỬ DỤNG
# ==========================================

# Ví dụ 1: Dữ liệu có dáng Parabol (Bậc 2)
print(">>> VÍ DỤ 1: TEST VỚI DỮ LIỆU DẠNG PARABOL")
x1 = [0, 1, 2, 3, 4, 5]
y1 = [2.1, 3.5, 8.2, 16.5, 27.8, 41.5] # Xấp xỉ y = 1.5x^2 + 2
find_best_fit_model(x1, y1)

print("\n" + "="*50 + "\n")

# Ví dụ 2: Dữ liệu có dáng Mũ (Exponential)
print(">>> VÍ DỤ 2: TEST VỚI DỮ LIỆU DẠNG MŨ")
x2 = [1, 2, 3, 4, 5]
y2 = [2.7, 7.4, 20.1, 54.6, 148.4] # Xấp xỉ y = e^x
find_best_fit_model(x2, y2)