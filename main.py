import numpy as np
import matplotlib.pyplot as plt
from RungeKutta import RungeKuttaSolver
from problems import get_problem

def plot_solutions(solver, ts, ys, f=None, h=None):
    """
    Vẽ đồ thị và tô màu các điểm dựa trên tính ổn định.
    Màu xanh (Green): Nằm trong miền ổn định.
    Màu đỏ (Red): Nằm ngoài miền ổn định.
    """
    plt.figure(figsize=(12, 7))
    num_vars = ys.shape[1]
    labels = ['x', 'y', 'z', 'w'] if num_vars <= 4 else [f'y_{i}' for i in range(num_vars)]
    
    # 1. Vẽ đường nối (Line plot) mờ hơn một chút để làm nền
    colors_line = ['b', 'orange', 'g', 'm'] # Màu xanh dương, cam, xanh lá, tím
    for i in range(num_vars):
        plt.plot(ts, ys[:, i], '-', color=colors_line[i%len(colors_line)], 
                 alpha=0.4, label=f'{labels[i]}(t) (Đường nối)')

    # 2. Vẽ các điểm (Scatter) với màu sắc dựa trên tính ổn định
    if f is not None and h is not None:
        print("\n>> Đang phân tích ổn định từng điểm trên đồ thị (vui lòng chờ)...")
        stable_points_x = []
        stable_points_y = []
        unstable_points_x = []
        unstable_points_y = []
        
        # Duyệt qua từng bước thời gian
        for i, t_val in enumerate(ts):
            y_val = ys[i]
            # Gọi hàm kiểm tra từ solver (Bạn phải chắc chắn đã thêm hàm này vào RungeKutta.py)
            try:
                is_stable, r_val = solver.check_step_stability(f, t_val, y_val, h)
                
                # Lưu tọa độ để vẽ (gom tất cả biến y vào chung để hiển thị trạng thái hệ thống)
                for var_idx in range(num_vars):
                    if is_stable:
                        stable_points_x.append(t_val)
                        stable_points_y.append(y_val[var_idx])
                    else:
                        unstable_points_x.append(t_val)
                        unstable_points_y.append(y_val[var_idx])
            except AttributeError:
                print("Cảnh báo: Hàm 'check_step_stability' chưa có trong RungeKuttaSolver.")
                break

        # Vẽ điểm ỔN ĐỊNH (Xanh lá)
        if stable_points_x:
            plt.scatter(stable_points_x, stable_points_y, c='green', s=20, zorder=5, 
                        label='Ổn định (|R(z)| ≤ 1)')
        
        # Vẽ điểm KHÔNG ỔN ĐỊNH (Đỏ)
        if unstable_points_x:
            plt.scatter(unstable_points_x, unstable_points_y, c='red', s=30, zorder=6, marker='x',
                        label='Mất ổn định (|R(z)| > 1)')
    else:
        # Fallback nếu không truyền f, h
        for i in range(num_vars):
            plt.plot(ts, ys[:, i], 'o', markersize=4)

    plt.title(f'Phân tích Ổn định - {solver.method_name} (h={h})')
    plt.xlabel('Thời gian t')
    plt.ylabel('Giá trị')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

def main():
    while True:
        print("\n" + "="*60)
        print(" CHƯƠNG TRÌNH PHÂN TÍCH & XÂY DỰNG RUNGE-KUTTA (RK)")
        print("="*60)
        
        # BƯỚC 1: CHỌN SỐ NẤC
        try:
            s_input = input(">> BƯỚC 1: Nhập số nấc s (2, 3, 4) [q để thoát]: ").strip()
            if s_input.lower() == 'q': break
            s = int(s_input)
            if s not in [2, 3, 4]:
                print("Lỗi: Hiện tại chỉ hỗ trợ s = 2, 3, 4.")
                continue
        except ValueError:
            continue

        solver = RungeKuttaSolver(s)

        # BƯỚC 2: CHỌN DẠNG INPUT (MODE)
        print("\n>> BƯỚC 2: Chọn chế độ input")
        print("   [1] Tự xây dựng công thức (Nhập alpha/c -> Hiện công thức -> Giải)")
        print("   [2] Sử dụng công thức chuẩn (Classic, Heun...) -> Giải PT")
        mode = input("   Lựa chọn (1/2): ").strip()

        # --- XỬ LÝ MODE 1: XÂY DỰNG ---
        if mode == '1':
            alphas = []
            print(f"\n   [DẠNG 1] Xây dựng RK{s} từ tham số alpha (c)")
            try:
                # 1. Nhập tham số alpha
                if s == 2:
                    val = float(input("   Nhập alpha_2 (c2) [Gợi ý: 0.5, 1.0, 0.75]: "))
                    alphas = [val]
                elif s == 3:
                    print("   Nhập alpha_2, alpha_3 [Gợi ý: (0.5, 1.0) hoặc (1/3, 2/3)]")
                    v2 = float(input("   c2: "))
                    v3 = float(input("   c3: "))
                    alphas = [v2, v3]
                
                # 2. Tính bảng Butcher & In lời giải
                success = solver.derive_tableau(alphas)
                if not success: continue
                
                # 3. In công thức tổng quát
                solver.print_formula_structure()
            
                if input(">> Vẽ biểu đồ miền ổn định? (y/n): ").lower() == 'y': 
                    solver.plot_stability_region()
                if input("\n>> Khảo sát tính hội tụ? (y/n): ").lower() == 'y':
                    solver.analyze_stability()
            except ValueError:
                print("Lỗi nhập số liệu.")
        
        # --- XỬ LÝ MODE 2: GIẢI PHƯƠNG TRÌNH ---
        elif mode == '2':
            # 1. Chọn phương pháp chuẩn
            print(f"\n   [DẠNG 2] Chọn phương pháp RK{s} chuẩn:")
            alphas = []
            if s == 2:
                print("   a. Heun Method (alpha = 1)")
                print("   b. Midpoint Method (alpha = 1/2)")
                print("   c. Ralston Method (alpha = 3/4)")
                ch = input("   Chọn (a/b/c): ").lower()
                if ch == 'a': alphas = [1.0]
                elif ch == 'b': alphas = [0.5]
                elif ch == 'c': alphas = [0.75]
                else: alphas = [1.0]
            elif s == 3:
                print("   a. Heun RK3 (c=[1/3, 2/3])")
                print("   b. Kutta RK3 (c=[1/2, 1])")
                ch = input("   Chọn (a/b): ").lower()
                if ch == 'a': alphas = [1/3, 2/3]
                else: alphas = [0.5, 1.0]
            elif s == 4:
                print("   a. Classic RK4")
                print("   b. RK4 3/8 Rule")
                ch = input("   Chọn (a/b): ").lower()
                if ch == 'b': alphas = ['3/8'] 
                else: alphas = [] 

            # 2. Tạo bảng Butcher
            solver.derive_tableau(alphas)

            # 3. Nhập bài toán
            print("\n>> Nhập thông tin bài toán vi phân:")
            print("   Nhập 'custom' hoặc ID bài đã lưu (ví dụ 'bai1')")
            pid_input = input("   Lựa chọn: ").strip()
            if not pid_input: pid_input = 'custom'

            data = get_problem(pid_input)
            if data:
                f, t_span, y0, h, expressions, _ = data
                
                # 4. [QUAN TRỌNG] In cả 2 loại công thức
                solver.print_formula_structure()          # Công thức lý thuyết
                solver.print_applied_formula(expressions, h) # Công thức thay số
                
                # 5. Giải và vẽ đồ thị
                ts, ys = solver.solve(f, t_span, y0, h)
                
                print("\n   [BẢNG KẾT QUẢ TÓM TẮT]")
                print(f"   {'t':<10} | {'y (vector)':<30}")
                step_log = max(1, len(ts)//10)
                for i in range(0, len(ts), step_log):
                    print(f"   {ts[i]:<10.4f} | {str(ys[i])}")
                
                # --- ĐÂY LÀ DÒNG QUAN TRỌNG ĐÃ SỬA ---
                # Truyền thêm f và h vào để hàm vẽ biết cách tính ổn định
                plot_solutions(solver, ts, ys, f=f, h=h)
                
                if input("\n>> Xem miền ổn định? (y/n): ").lower() == 'y':
                    solver.plot_stability_region()
                if input("\n>> Khảo sát tính hội tụ? (y/n): ").lower() == 'y':
                    solver.analyze_stability()
if __name__ == "__main__":
    main()