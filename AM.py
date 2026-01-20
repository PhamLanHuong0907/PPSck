import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# --- CẤU HÌNH HIỂN THỊ SỐ (QUAN TRỌNG) ---
# suppress=True: Tắt chế độ in khoa học (e-05)
# precision=6: Mặc định in 6 số sau dấu phẩy
# formatter: Đảm bảo mọi số float đều được format dạng thập phân
np.set_printoptions(suppress=True, precision=6, floatmode='fixed')

def get_adams_coefficients(order, method='AB'):
    """
    Tính hệ số cho phương pháp Adams-Bashforth (AB) hoặc Adams-Moulton (AM)
    dựa trên tích phân đa thức Lagrange.
    """
    t = sp.symbols('t')
    # Chuẩn hóa bước nhảy h=1. Đoạn tích phân từ 0 đến 1
    
    if method == 'AB':
        points = [-i for i in range(order)]
        target_range = (0, 1) 
    else: # AM
        points = [1] + [-i for i in range(order - 1)]
        target_range = (0, 1)

    t_sym = sp.symbols('t')
    coeffs = []
    
    # Xây dựng đa thức Lagrange và tích phân
    for i in range(len(points)):
        L = 1
        for j in range(len(points)):
            if i != j:
                L *= (t_sym - points[j]) / (points[i] - points[j])
        
        integral = sp.integrate(L, (t_sym, target_range[0], target_range[1]))
        coeffs.append(float(integral))
        
    return coeffs

def rk4_step(f, t, y, h):
    """Giải một bước bằng RK4 để khởi tạo giá trị."""
    k1 = h * f(t, y)
    k2 = h * f(t + 0.5*h, y + 0.5*k1)
    k3 = h * f(t + 0.5*h, y + 0.5*k2)
    k4 = h * f(t + h, y + k3)
    return y + (k1 + 2*k2 + 2*k3 + k4) / 6.0

def solve_adams_predictor_corrector(funcs, y0, t_span, h, order):
    """
    Giải hệ PTVP bằng phương pháp AB-AM (Dự báo - Hiệu chỉnh).
    """
    t0, tf = t_span
    n_steps = int((tf - t0) / h) + 1
    t_vals = np.linspace(t0, tf, n_steps)
    
    dim = len(y0)
    y_vals = np.zeros((n_steps, dim))
    y_vals[0] = y0
    
    # 1. Khởi tạo (Initialization) bằng RK4
    print(f"--- Đang khởi tạo {order-1} bước đầu bằng RK4 ---")
    for i in range(order - 1):
        y_vals[i+1] = rk4_step(funcs, t_vals[i], y_vals[i], h)
        
    ab_coeffs = get_adams_coefficients(order, 'AB') 
    am_coeffs = get_adams_coefficients(order, 'AM')
    
    # 2. Vòng lặp chính (Predictor - Corrector)
    print(f"--- Bắt đầu vòng lặp AB{order}-AM{order} ---")
    
    f_history = np.zeros((n_steps, dim))
    for i in range(order):
        f_history[i] = funcs(t_vals[i], y_vals[i])
        
    for i in range(order - 1, n_steps - 1):
        # --- PREDICTOR (Dự báo) ---
        y_pred = y_vals[i].copy()
        for j in range(order):
            y_pred += h * ab_coeffs[j] * f_history[i-j]
            
        f_next_pred = funcs(t_vals[i+1], y_pred)
        
        # --- CORRECTOR (Hiệu chỉnh) ---
        y_corr = y_vals[i].copy()
        
        term_future = am_coeffs[0] * f_next_pred
        term_past = np.zeros(dim)
        for j in range(1, order): 
            term_past += am_coeffs[j] * f_history[i - (j-1)]
            
        y_corr += h * (term_future + term_past)
        
        y_vals[i+1] = y_corr
        f_history[i+1] = funcs(t_vals[i+1], y_corr)
        
    return t_vals, y_vals

# --- CÁC HÀM XỬ LÝ NHẬP LIỆU ---

def parse_functions(func_strs):
    """Chuyển chuỗi nhập vào thành hàm Python thực thi được."""
    def f(t, Y):
        # Thêm các hằng số/hàm toán học phổ biến vào context
        vars_dict = {'t': t, 'e': np.e, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'pi': np.pi, 'sqrt': np.sqrt}
        variable_names = ['x', 'y', 'z', 'u', 'v', 'w']
        for idx, val in enumerate(Y):
            if idx < len(variable_names):
                vars_dict[variable_names[idx]] = val
        
        res = []
        for s in func_strs:
            try:
                res.append(eval(s, {}, vars_dict)) 
            except Exception as e:
                print(f"Lỗi khi tính hàm '{s}': {e}")
                return np.zeros(len(Y))
        return np.array(res)
    return f

def main():
    print("=== CHƯƠNG TRÌNH GIẢI PTVP BẰNG ADAMS-BASHFORTH-MOULTON (AB-AM) ===")
    print("Hỗ trợ giải hệ phương trình và tự động sinh công thức mọi bậc.")
    
    print("\n--- Chọn chế độ ---")
    print("1. Nhập thủ công (Dạng tổng quát)")
    print("2. Chạy bài mẫu: Câu 2 (Hệ Lotka-Volterra mở rộng)")
    print("3. Chạy bài mẫu: Câu 33a (Đơn giản)")
    
    choice = input("Lựa chọn của bạn (1/2/3): ")
    
    if choice == '1':
        dim = int(input("Nhập số lượng phương trình (biến): "))
        func_strs = []
        print(f"Nhập các hàm f_i(t, x, y, ...) vế phải. Dùng x, y, z cho các biến phụ thuộc.")
        for i in range(dim):
            s = input(f"f_{i+1} = ")
            func_strs.append(s)
            
        y0_strs = input(f"Nhập giá trị ban đầu (cách nhau bởi dấu phẩy, vd: 0.8, 0.3): ")
        y0 = np.array([float(v) for v in y0_strs.split(',')])
        
        t_start = float(input("Thời điểm bắt đầu t0: "))
        t_end = float(input("Thời điểm kết thúc t_end: "))
        h = float(input("Bước nhảy h: "))
        order = int(input("Bậc của phương pháp (s), ví dụ 3 hoặc 4: "))
        
        funcs = parse_functions(func_strs)
        t_span = (t_start, t_end)
        
    elif choice == '2': 
        print("\n--- Đang thiết lập bài toán Câu 2 ---")
        k_val = float(input("Nhập giá trị k cho beta (beta = k * 0.01): "))
        beta = k_val * 0.01
        alpha = 0.2
        gamma = 0.6
        delta = 0.45
        
        f1 = f"x*(1-x)*(x-{beta}) - {alpha}*x*y"
        f2 = f"{gamma}*x*y - {delta}*y"
        
        func_strs = [f1, f2]
        funcs = parse_functions(func_strs)
        y0 = np.array([0.8, 0.3])
        t_span = (0, 100)
        h = 0.01 
        print(f"Hệ PT:\n  dx/dt = {f1}\n  dy/dt = {f2}")
        # Numpy giờ sẽ in y0 dạng số thường nhờ cấu hình ở đầu file
        print(f"y0 = {y0}, t thuộc {t_span}, h={h:.6f}")
        
        order_in = input("Nhập bậc s (nhấn Enter để dùng AB4-AM4 hoặc 3): ")
        order = int(order_in) if order_in else 3

    elif choice == '3': 
        func_strs = ["-2*x"] 
        print("Bài toán: y' = -2y (Biến trong code là x).")
        funcs = parse_functions(func_strs)
        y0 = np.array([1.0])
        t_span = (0, 1.0)
        h = 0.1
        order = 3
        
    else:
        print("Lựa chọn không hợp lệ.")
        return

    # GIẢI
    t_res, y_res = solve_adams_predictor_corrector(funcs, y0, t_span, h, order)
    
    # KẾT QUẢ
    print(f"\n--- KẾT QUẢ (In toàn bộ hoặc 20 dòng cuối) ---")
    vars_name = ['x', 'y', 'z', 'u', 'v']
    header = "t\t" + "\t".join([f"{vars_name[i]}" for i in range(len(y0))])
    print(header)
    
    # In kết quả, dùng .6f để ép kiểu số thập phân
    # Nếu danh sách quá dài, có thể chỉ in phần đầu và cuối
    limit_print = 20
    start_idx = 0 if len(t_res) < limit_print else len(t_res) - limit_print
    
    if start_idx > 0:
        print("... (đã ẩn các dòng đầu) ...")

    for i in range(start_idx, len(t_res)):
        # Ép kiểu float hiển thị 6 chữ số thập phân, không e
        t_str = f"{t_res[i]:.6f}"
        vals_str = "\t".join([f"{val:.6f}" for val in y_res[i]])
        print(f"{t_str}\t{vals_str}")

    # VẼ ĐỒ THỊ
    plt.figure(figsize=(10, 6))
    for i in range(len(y0)):
        plt.plot(t_res, y_res[:, i], label=f'Biến {vars_name[i]}')
    
    if choice == '2':
        plt.figure(figsize=(6, 6))
        plt.plot(y_res[:, 0], y_res[:, 1])
        plt.title("Đồ thị pha (x, y)")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        
    plt.title(f"Giải nghiệm bằng AB{order}-AM{order}")
    plt.xlabel("t")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()