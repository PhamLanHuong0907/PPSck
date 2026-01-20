import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from fractions import Fraction
import math

# --- CẤU HÌNH HIỂN THỊ ---
# suppress=True: Tắt chế độ in khoa học (e-05) của numpy
# precision=6: Lấy 6 chữ số thập phân
np.set_printoptions(suppress=True, precision=6, floatmode='fixed')

class RungeKuttaSolver:
    def __init__(self, s):
        self.s = s
        self.A = np.zeros((s, s))
        self.b = np.zeros(s)
        self.c = np.zeros(s)
        self.method_name = f"RK{s}"

    def _frac(self, val):
        """Helper: Chuyển float sang chuỗi phân số tối giản"""
        if abs(val) < 1e-9: return "0"
        if abs(val - 1.0) < 1e-9: return "1"
        return str(Fraction(val).limit_denominator(1000))

    def _fmt_float(self, val):
        """Helper: Định dạng số thập phân, không dùng e (ví dụ: 0.000123)"""
        # :.6f nghĩa là lấy 6 số sau dấu phẩy. Bạn có thể tăng lên .8f hoặc .10f nếu cần chính xác hơn
        return f"{val:.6f}"

    def derive_tableau(self, input_alphas=None):
        """Xây dựng bảng Butcher"""
        print("\n" + "="*60)
        print(f"   QUY TRÌNH XÂY DỰNG CÔNG THỨC RK{self.s} (LỜI GIẢI CHI TIẾT)")
        print("="*60)

        # --- TRƯỜNG HỢP s = 2 ---
        if self.s == 2:
            c2 = input_alphas[0] if input_alphas else 1.0
            print(f">> Input: Chọn alpha_2 (c2) = {self._frac(c2)}")
            print("\n1. Hệ phương trình ràng buộc (Order Conditions s=2):")
            print("   (1) r1 + r2 = 1;  (2) r2 * c2 = 1/2;  (3) b11 = c2")
            
            if c2 == 0: return False
            r2 = 1.0 / (2.0 * c2)
            r1 = 1.0 - r2
            b11 = c2
            
            print("\n2. Giải hệ phương trình:")
            print(f"   r2 = {self._frac(r2)}; r1 = {self._frac(r1)}; b11 = {self._frac(b11)}")
            
            self.c = np.array([0, c2]); self.b = np.array([r1, r2])
            self.A = np.array([[0, 0], [b11, 0]])
            self.method_name = f"RK2 (alpha={self._frac(c2)})"

        # --- TRƯỜNG HỢP s = 3 ---
        elif self.s == 3:
            if not input_alphas or len(input_alphas) < 2: return False
            c2, c3 = input_alphas
            det = c2 * c3**2 - c3 * c2**2
            if abs(det) < 1e-9: return False

            r2 = (0.5 * c3**2 - (1/3) * c3) / det
            r3 = ((1/3) * c2 - 0.5 * c2**2) / det
            r1 = 1.0 - r2 - r3
            b22 = 1.0 / (6.0 * r3 * c2) if abs(r3*c2) > 1e-9 else 0
            b21 = c3 - b22
            b11 = c2
            
            self.c = np.array([0, c2, c3]); self.b = np.array([r1, r2, r3])
            self.A = np.array([[0,0,0], [b11,0,0], [b21,b22,0]])
            self.method_name = "Generic RK3"

        # --- TRƯỜNG HỢP s = 4 ---
        elif self.s == 4:
            if input_alphas and input_alphas[0] == '3/8':
                self.c = np.array([0, 1/3, 2/3, 1])
                self.b = np.array([1/8, 3/8, 3/8, 1/8])
                self.A = np.array([[0,0,0,0], [1/3,0,0,0], [-1/3,1,0,0], [1,-1,1,0]])
                self.method_name = "RK4 (3/8 Rule)"
            else:
                self.c = np.array([0, 0.5, 0.5, 1])
                self.b = np.array([1/6, 1/3, 1/3, 1/6])
                self.A = np.array([[0,0,0,0], [0.5,0,0,0], [0,0.5,0,0], [0,0,1,0]])
                self.method_name = "Classic RK4"
            print(f">> Sử dụng bảng Butcher chuẩn của {self.method_name}")
        return True

    def print_formula_structure(self):
        """In công thức lý thuyết tổng quát"""
        print(f"\n[CÔNG THỨC TỔNG QUÁT - {self.method_name}]")
        print("-" * 40)
        for i in range(self.s):
            args = "y_n"
            terms = [f"{self._frac(self.A[i][j])}k_{j+1}" for j in range(i) if abs(self.A[i][j]) > 1e-9]
            if terms: args += " + h*(" + " + ".join(terms) + ")"
            time_arg = "t_n"
            if abs(self.c[i]) > 1e-9: time_arg += f" + {self._frac(self.c[i])}h"
            print(f"  k_{i+1} = f( {time_arg},  {args} )")
        terms_b = [f"{self._frac(self.b[i])}k_{i+1}" for i in range(self.s) if abs(self.b[i]) > 1e-9]
        print(f"  y_(n+1) = y_n + h * ({' + '.join(terms_b)})")

    def print_applied_formula(self, expressions, h_val):
        print(f"\n" + "="*60)
        print(f"   CÔNG THỨC ÁP DỤNG CỤ THỂ (h = {self._fmt_float(h_val)})")
        print("="*60)

        t_sym = sp.symbols('t_n')
        num_vars = len(expressions)
        
        if num_vars == 1:
            state_syms = [sp.symbols('y_n')]
        else:
            var_names = ['x_n', 'y_n', 'z_n', 'w_n'][:num_vars]
            state_syms = [sp.symbols(name) for name in var_names]

        # Parse hàm f
        funcs_expr = []
        for expr_str in expressions:
            clean_str = expr_str.replace('^', '**').replace('np.', '')
            try:
                parsed = sp.sympify(clean_str)
            except:
                print(f"Lỗi: Không thể đọc biểu thức '{expr_str}'")
                return

            subs_map = {sp.symbols('t'): t_sym}
            if num_vars == 1:
                subs_map[sp.symbols('y')] = state_syms[0]
                subs_map[sp.symbols('x')] = state_syms[0] 
            else:
                var_chars = ['x', 'y', 'z', 'w']
                for i in range(num_vars):
                    subs_map[sp.symbols(var_chars[i])] = state_syms[i]
            
            funcs_expr.append(parsed.subs(subs_map))

        # Tính toán symbolical
        for i in range(self.s):
            print(f"\n--- Bước {i+1} (Tính k_{i+1}) ---")
            t_arg = t_sym + self.c[i] * h_val
            
            current_state_args = []
            for var_idx in range(num_vars):
                shift = 0
                for j in range(i): 
                    val_a = self.A[i][j]
                    if abs(val_a) > 1e-9:
                        k_name = f"k{j+1}" if num_vars == 1 else f"k{j+1}_{['x','y','z'][var_idx]}"
                        k_sym = sp.symbols(k_name)
                        shift += val_a * h_val * k_sym
                current_state_args.append(state_syms[var_idx] + shift)

            for func_idx, func_expr in enumerate(funcs_expr):
                subs_dict = {t_sym: t_arg}
                for v_idx, v_sym in enumerate(state_syms):
                    subs_dict[v_sym] = current_state_args[v_idx]
                
                final_expr = func_expr.subs(subs_dict)
                suffix = "" if num_vars == 1 else f"_{['x','y','z'][func_idx]}"
                expr_str = str(final_expr).replace('**', '^')
                print(f"  k_{i+1}{suffix} = {expr_str}")

        print(f"\n--- Kết quả (Tính y_{{n+1}}) ---")
        for var_idx in range(num_vars):
            sum_b = 0
            for i in range(self.s):
                if abs(self.b[i]) > 1e-9:
                    k_name = f"k{i+1}" if num_vars == 1 else f"k{i+1}_{['x','y','z'][var_idx]}"
                    k_sym = sp.symbols(k_name)
                    sum_b += self.b[i] * k_sym
            
            y_next_expr = state_syms[var_idx] + h_val * sum_b
            var_out = ['x','y','z'][var_idx] if num_vars > 1 else 'y'
            print(f"  {var_out}_(n+1) = {str(y_next_expr).replace('**', '^')}")

    def analyze_stability(self):
        print("\n[PHÂN TÍCH ỔN ĐỊNH & HỘI TỤ]")
        print("-" * 50)
        p = self.s
        print(f"1. Cấp chính xác (Order): p = {p}")
        print(f"   - Sai số cụt cục bộ: O(h^{p+1})")
        print(f"   - Sai số toàn cục: O(h^{p})")
        
        sum_b = np.sum(self.b)
        # Sử dụng _fmt_float cho sum_b
        print(f"2. Kiểm tra tính nhất quán: Tổng b_i = {self._fmt_float(sum_b)} -> {'Đạt' if abs(sum_b-1)<1e-9 else 'Không đạt'}")
        
        rz_str = "1 + z"
        for i in range(2, self.s + 1):
            rz_str += f" + z^{i}/{math.factorial(i)}"
            
        print(f"3. Đa thức ổn định R(z):")
        print(f"   R(z) = {rz_str}")

    def get_stability_function_value(self, z):
        I = np.eye(self.s)
        ones = np.ones(self.s)
        try:
            M = I - z * self.A
            inv_vec = np.linalg.solve(M, ones)
            val = 1 + z * np.dot(self.b, inv_vec)
            return val
        except np.linalg.LinAlgError:
            return np.inf

    def plot_stability_region(self, test_points=[]):
        x = np.linspace(-5, 2, 400)
        y = np.linspace(-4, 4, 400)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        R_abs = np.zeros_like(Z, dtype=float)
        rows, cols = Z.shape
        
        is_explicit = np.allclose(np.triu(self.A), 0)
        if is_explicit:
            coeffs = [1.0]
            curr = np.ones(self.s)
            for k in range(self.s + 1):
                val = np.dot(self.b, curr)
                if k > 0: coeffs.append(val)
                curr = np.dot(self.A, curr)
                if np.allclose(curr, 0): break
            
            poly_val = np.zeros_like(Z, dtype=complex)
            for i, c in enumerate(coeffs):
                if i==0: poly_val += 1
                else: poly_val += c * (Z**i)
            R_abs = np.abs(poly_val)
        else:
            for r in range(rows):
                for c in range(cols):
                    R_abs[r, c] = abs(self.get_stability_function_value(Z[r, c]))

        plt.figure(figsize=(8, 6))
        plt.contourf(X, Y, R_abs, levels=[0, 1], colors=['#99ccff'], alpha=0.6)
        plt.contour(X, Y, R_abs, levels=[1], colors='blue', linewidths=2)
        
        plt.axhline(0, color='black', lw=1)
        plt.axvline(0, color='black', lw=1)

        if test_points:
            print(f"\n[KIỂM TRA ỔN ĐỊNH VỚI CÁC ĐIỂM TEST]")
            # Định dạng tiêu đề
            print(f"{'Điểm z':<20} | {'|R(z)|':<15} | {'Trạng thái'}")
            print("-" * 55)
            
            for pt in test_points:
                z = complex(pt)
                val = self.get_stability_function_value(z)
                abs_val = abs(val)
                is_stable = abs_val <= 1.0 + 1e-9
                
                status = "ỔN ĐỊNH" if is_stable else "KHÔNG ỔN ĐỊNH"
                # Sửa định dạng in tại đây:
                # z.real:g -> z.real:.4f (số thực 4 chữ số)
                z_str = f"{z.real:.4f}{z.imag:+.4f}j"
                print(f"{z_str:<20} | {abs_val:<15.6f} | {status}")
                
                color = 'green' if is_stable else 'red'
                marker = 'o' if is_stable else 'x'
                plt.plot(z.real, z.imag, marker=marker, color=color, markersize=8, markeredgewidth=2, 
                         label=f"z={z_str} ({status})")

        plt.title(f'Miền ổn định - {self.method_name}')
        plt.xlabel('Re(z)')
        plt.ylabel('Im(z)')
        plt.grid(True, linestyle='--')
        if test_points:
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def check_step_stability(self, f, t, y, h):
        y = np.array(y, dtype=float).flatten()
        n = len(y)
        J = np.zeros((n, n))
        f_val = np.array(f(t, y)).flatten()
        
        epsilon = 1e-6
        for i in range(n):
            y_perturbed = y.copy()
            y_perturbed[i] += epsilon
            f_perturbed = np.array(f(t, y_perturbed)).flatten()
            J[:, i] = (f_perturbed - f_val) / epsilon
            
        try:
            eigenvalues = np.linalg.eigvals(J)
        except:
            return False, "Lỗi linalg"

        all_stable = True
        max_R = 0
        
        for lam in eigenvalues:
            z = lam * h
            R_val = abs(self.get_stability_function_value(z))
            if R_val > max_R: max_R = R_val
            if R_val > 1.0 + 1e-4:
                all_stable = False
        
        return all_stable, max_R

    def solve(self, f, t_span, y0, h):
        t0, tf = t_span
        n_steps = int(np.ceil((tf - t0) / h - 1e-9))
        t = t0; y = np.array(y0, dtype=float)
        ts = [t]; ys = [y]
        
        print(f"\n[BẢNG SỐ LIỆU] Chạy từ t={t0} đến {tf}, h={h}")
        print(f"{'t':<12} | {'y':<30}")
        
        # --- SỬA ĐỔI: In dòng đầu tiên với định dạng fix float ---
        y_str = "[" + ", ".join([self._fmt_float(val) for val in y.flatten()]) + "]"
        print(f"{t:<12.6f} | {y_str}")
        
        for step in range(n_steps):
            try:
                k = np.zeros((self.s, len(y)))
                for i in range(self.s):
                    sum_ak = np.zeros_like(y)
                    for j in range(i): sum_ak += self.A[i, j] * k[j]
                    
                    val = f(t + self.c[i]*h, y + h*sum_ak)
                    if np.any(np.isinf(val)) or np.any(np.isnan(val)) or np.any(np.abs(val) > 1e100):
                        raise OverflowError("Giá trị đạo hàm quá lớn")
                    k[i] = val
                
                sum_bk = np.zeros_like(y)
                for i in range(self.s): sum_bk += self.b[i] * k[i]
                
                y_new = y + h * sum_bk
                
                if np.any(np.isinf(y_new)) or np.any(np.isnan(y_new)) or np.any(np.abs(y_new) > 1e100):
                    raise OverflowError("Nghiệm bùng nổ ra vô cùng")
                    
                y = y_new
                t += h
                ts.append(t); ys.append(y)
                
                # --- SỬA ĐỔI: In trong vòng lặp với định dạng fix float ---
                if len(ts) < 20 or step % (n_steps//20) == 0:
                     y_str = "[" + ", ".join([self._fmt_float(val) for val in y.flatten()]) + "]"
                     print(f"{t:<12.6f} | {y_str}")
                      
            except (OverflowError, RuntimeWarning) as e:
                print(f"\n[DỪNG SỚM] Phát hiện tràn số tại t={self._fmt_float(t)}. Phương trình có nghiệm tiến tới vô cùng.")
                print(f"Lý do: {e}")
                break
            
        return np.array(ts), np.array(ys)