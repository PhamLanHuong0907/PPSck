import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp

# --- CẤU HÌNH HIỂN THỊ SỐ ---
# suppress=True: Tắt chế độ in khoa học (e-05)
# precision=6: Mặc định in 6 số sau dấu phẩy cho mảng numpy
# floatmode='fixed': Cố định định dạng
np.set_printoptions(suppress=True, precision=6, floatmode='fixed')

# --- KHỐI 1: LÝ THUYẾT ỔN ĐỊNH & KIỂM TRA ---

def check_stability_theoretical(method, h, lam):
    """
    Kiểm tra tính ổn định dựa trên z = h * lambda
    Theo định nghĩa miền ổn định tuyệt đối.
    """
    z = h * lam
    if method == 'euler_hien':
        # Ổn định nếu |1 + z| < 1 
        is_stable = abs(1 + z) < 1
        condition_str = "|1 + z| < 1 (Hình tròn đơn vị tâm -1)"
    elif method == 'euler_an':
        # Ổn định nếu |1/(1-z)| < 1 <=> |1 - z| > 1
        is_stable = abs(1 - z) > 1
        condition_str = "|1 - z| > 1 (Bên ngoài hình tròn tâm 1)"
    elif method == 'hinh_thang':
        # Ổn định nếu |(2+z)/(2-z)| < 1 <=> Re(z) < 0 (A-stable)
        is_stable = z.real < 0
        condition_str = "Re(z) < 0 (Nửa mặt phẳng trái)"
    else:
        return False, "Không xác định", 0
    
    return is_stable, condition_str, abs(1+z) if method=='euler_hien' else 0

def plot_stability_regions():
    """
    Vẽ minh họa miền ổn định trên mặt phẳng phức cho các phương pháp.
    """
    x = np.linspace(-3, 3, 400)
    y = np.linspace(-3, 3, 400)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    plt.figure(figsize=(12, 4))
    
    # 1. Euler Hiện: |1+z| < 1
    plt.subplot(1, 3, 1)
    region_hien = np.abs(1 + Z)
    plt.contourf(X, Y, region_hien, levels=[0, 1], colors=['#a8e6cf'], alpha=0.7)
    plt.contour(X, Y, region_hien, levels=[1], colors='g')
    plt.title("Euler Hiện (Forward)\n$|1+z|<1$ ")
    plt.grid(True)
    plt.axhline(0, color='black', lw=1); plt.axvline(0, color='black', lw=1)
    plt.gca().set_aspect('equal')

    # 2. Euler Ẩn: |1-z| > 1
    plt.subplot(1, 3, 2)
    region_an = np.abs(1 - Z)
    # Tô màu phần lớn hơn 1 (đảo ngược logic contourf để tô phần ngoài)
    plt.contourf(X, Y, region_an, levels=[0, 1], colors=['white'], alpha=1) # Che phần trong
    plt.imshow([[0,0],[0,0]], extent=(-3,3,-3,3), cmap='Blues', alpha=0.3) # Nền xanh
    plt.contour(X, Y, region_an, levels=[1], colors='b') # Biên
    # Vẽ lại hình tròn trắng đè lên
    circle = plt.Circle((1, 0), 1, color='white', fill=True)
    plt.gca().add_patch(circle)
    plt.title("Euler Ẩn (Backward)\n$|1-z|>1$")
    plt.grid(True)
    plt.axhline(0, color='black', lw=1); plt.axvline(0, color='black', lw=1)
    plt.gca().set_aspect('equal')

    # 3. Hình Thang: Re(z) < 0
    plt.subplot(1, 3, 3)
    plt.fill_between([-3, 0], -3, 3, color='#ffccbc', alpha=0.7)
    plt.axvline(0, color='r')
    plt.title("Hình Thang (Trapezoidal)\n$Re(z)<0$ (A-stable)")
    plt.grid(True)
    plt.axhline(0, color='black', lw=1); plt.axvline(0, color='black', lw=1)
    plt.xlim(-3, 3); plt.ylim(-3, 3)
    plt.gca().set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

# --- KHỐI 2: THUẬT TOÁN GIẢI (SOLVERS) ---

def solve_ode_core(method, f_func, t_span, y0, h):
    """
    Hàm giải chính (Kernel).
    Trả về (ts, ys)
    """
    t0, t_end = t_span
    N = int(np.ceil((t_end - t0) / h))
    ts = np.linspace(t0, t0 + N*h, N+1)
    dim = len(y0)
    ys = np.zeros((N+1, dim))
    ys[0] = y0
    
    for i in range(N):
        t_curr = ts[i]
        y_curr = ys[i]
        t_next = ts[i+1]
        
        if method == 'euler_hien':
            ys[i+1] = y_curr + h * f_func(t_curr, y_curr)
            
        elif method == 'euler_an':
            def equation(y_next):
                return y_next - y_curr - h * f_func(t_next, y_next)
            ys[i+1] = fsolve(equation, y_curr)
            
        elif method == 'hinh_thang':
            def equation(y_next):
                return y_next - y_curr - (h/2) * (f_func(t_curr, y_curr) + f_func(t_next, y_next))
            ys[i+1] = fsolve(equation, y_curr)
            
    return ts, ys

# --- KHỐI 3: PHÂN TÍCH SAI SỐ VÀ CẤP HỘI TỤ ---

def analyze_convergence(method, f_func, t_span, y0, h_base):
    """
    Phân tích sai số và cấp hội tụ bằng cách chạy với h, h/2, h/4.
    """
    print(f"\n>> PHÂN TÍCH HỘI TỤ: {method.upper()}")
    
    # 1. Tạo nghiệm tham chiếu (Exact Reference)
    sol_ref = solve_ivp(f_func, t_span, y0, method='RK45', rtol=1e-10, atol=1e-10)
    
    # Hàm nội suy nghiệm chính xác
    def get_exact(t):
        from scipy.interpolate import interp1d
        if not hasattr(analyze_convergence, "interpolator"):
            analyze_convergence.interpolator = interp1d(sol_ref.t, sol_ref.y, kind='cubic', fill_value="extrapolate")
        return analyze_convergence.interpolator(t).T

    steps = [h_base, h_base/2, h_base/4]
    
    # Căn chỉnh tiêu đề bảng
    print(f"{'h':<12} | {'Sai số Max (Global)':<25} | {'Cấp hội tụ (p)':<20}")
    print("-" * 65)
    
    prev_error = None
    
    for h in steps:
        ts, ys = solve_ode_core(method, f_func, t_span, y0, h)
        
        # Tính sai số
        y_exact_vals = np.array([get_exact(t) for t in ts]).reshape(len(ts), len(y0))
        max_err = np.max(np.abs(y_exact_vals - ys))
        
        order_str = "N/A"
        if prev_error is not None and max_err > 0:
            p = np.log2(prev_error / max_err)
            order_str = f"{p:.4f}"
            
        # --- SỬA ĐỔI QUAN TRỌNG ---
        # Sử dụng .10f thay vì .6e để hiện số thập phân đầy đủ
        # Nếu sai số cực nhỏ (< 1e-10), nó có thể hiện 0.0000000000
        print(f"{h:<12.6f} | {max_err:<25.10f} | {order_str:<20}")
        prev_error = max_err

    return

# --- KHỐI GIAO DIỆN ---

def get_user_input():
    print("="*60)
    print("CHƯƠNG TRÌNH GIẢI PTVP & PHÂN TÍCH EULER")
    print("="*60)
    
    print("Nhập bài toán (Ví dụ y' = y - t^2 + 1, y(0)=0.5)")
    print("Lưu ý: dùng cú pháp Python (np.sin, np.exp, t, y[0]...)")
    prob_type = input("Chọn loại (1: Hệ PT / 2: PT cấp cao): ")
    
    equations = []
    y0_vals = []
    
    if prob_type == '1':
        dim = int(input("Số chiều (số phương trình): "))
        for i in range(dim):
            eq = input(f"y[{i}]' = ")
            val = float(input(f"y[{i}](t0) = "))
            equations.append(eq)
            y0_vals.append(val)
    else:
        order = int(input("Cấp phương trình: "))
        for i in range(order - 1):
            equations.append(f"y[{i+1}]")
            val = float(input(f"y^({i})(t0) = "))
            y0_vals.append(val)
        last_eq = input(f"y^({order}) (vế phải) = ")
        val_last = float(input(f"y^({order-1})(t0) = "))
        equations.append(last_eq)
        y0_vals.append(val_last)
        
    t0 = float(input("t0: "))
    t_end = float(input("t_end: "))
    h = float(input("Bước h: "))
    
    def system_func(t, y):
        derivs = []
        for eq in equations:
            d = eval(eq, {"np": np, "t": t, "y": y})
            derivs.append(d)
        return np.array(derivs)

    return system_func, (t0, t_end), np.array(y0_vals), h

def main():
    f_func, t_span, y0, h = get_user_input()
    
    print("\nChọn chế độ:")
    print("1. Chạy giải và vẽ đồ thị thông thường")
    print("2. Phân tích chuyên sâu (Sai số, Hội tụ, Ổn định)")
    mode = input("Lựa chọn (1/2): ")
    
    methods = ['euler_hien', 'euler_an', 'hinh_thang']
    
    if mode == '2':
        # 1. Vẽ miền ổn định
        print("\n[INFO] Đang vẽ miền ổn định tuyệt đối trên mặt phẳng phức...")
        plot_stability_regions()
        
        # 2. Kiểm tra lambda
        print("\n--- KIỂM TRA ỔN ĐỊNH VỚI LAMBDA CỤ THỂ ---")
        try:
            lam_real = float(input("Nhập ước lượng trị riêng (Lambda) của bài toán (Phần thực): "))
            for m in methods:
                stable, cond, val = check_stability_theoretical(m, h, complex(lam_real, 0))
                status = "ỔN ĐỊNH" if stable else "KHÔNG ỔN ĐỊNH"
                print(f"[{m.upper()}]: {status}. Điều kiện: {cond}")
        except:
            print("Bỏ qua kiểm tra lambda cụ thể.")

        # 3. Phân tích hội tụ
        print("\n--- PHÂN TÍCH SAI SỐ & TỐC ĐỘ HỘI TỤ ---")
        for m in methods:
            analyze_convergence(m, f_func, t_span, y0, h)
            
    else:
        # Chạy thường
        plt.figure(figsize=(10, 6))
        for m in methods:
            ts, ys = solve_ode_core(m, f_func, t_span, y0, h)
            plt.plot(ts, ys[:, 0], label=f'{m}', marker='.')
            
            # In kết quả cuối cùng - Numpy global settings sẽ lo phần định dạng
            print(f"[{m}] y_end = {ys[-1]}")
            
        plt.legend()
        plt.grid()
        plt.title(f"Giải PTVP với h={h:.6f}")
        plt.show()

if __name__ == "__main__":
    main()