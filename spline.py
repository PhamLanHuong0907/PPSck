import numpy as np
import matplotlib.pyplot as plt

class SplineMasterSolver:
    def __init__(self, x, y):
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.n = len(x)
        
        # --- BƯỚC 1: CHUẨN BỊ DỮ LIỆU ---
        print(f"\n{'='*30} BƯỚC 1: CHUẨN BỊ SỐ LIỆU {'='*30}")
        # Sắp xếp
        sorted_idx = np.argsort(self.x)
        self.x = self.x[sorted_idx]
        self.y = self.y[sorted_idx]
        
        print(f"1. Bảng dữ liệu đã sắp xếp:")
        print(f"   X: {self.x}")
        print(f"   Y: {self.y}")
        
        # Tính h
        self.h = np.diff(self.x)
        print(f"2. Các bước nhảy h_k:")
        for k, val in enumerate(self.h):
            print(f"   h_{k} = {self.x[k+1]} - {self.x[k]} = {val:.4f}")

    def solve_linear(self):
        """Spline Tuyến tính (Cấp 1)"""
        print(f"\n{'='*30} LỜI GIẢI SPLINE CẤP 1 (Linear) {'='*30}")
        print("Dạng hàm: S_k(x) = a_k * x + b_k")
        
        coeffs = []
        for k in range(self.n - 1):
            print(f"\n--- Đoạn {k+1}: [{self.x[k]}, {self.x[k+1]}] ---")
            # a = (y1-y0)/h
            a = (self.y[k+1] - self.y[k]) / self.h[k]
            # b = y0 - a*x0
            b = self.y[k] - a * self.x[k]
            
            print(f"   a_{k} = ({self.y[k+1]} - {self.y[k]}) / {self.h[k]:.4f} = {a:.4f}")
            print(f"   b_{k} = {self.y[k]} - ({a:.4f} * {self.x[k]}) = {b:.4f}")
            print(f"   => PT: y = {a:.4f}x + {b:.4f}")
            coeffs.append((a, b))
        return coeffs

    def solve_quadratic(self, m0=None):
        """Spline Cấp 2 (Quadratic)"""
        print(f"\n{'='*30} LỜI GIẢI SPLINE CẤP 2 (Quadratic) {'='*30}")
        print("Dạng hàm: S_k(x) = a_k x^2 + b_k x + c_k")
        
        # Tính m (đạo hàm bậc 1)
        m = np.zeros(self.n)
        
        # Điều kiện biên
        if m0 is None:
            m[0] = (self.y[1] - self.y[0]) / self.h[0] # Xấp xỉ
            print(f"   (Chọn biên m_0 xấp xỉ sai phân: {m[0]:.4f})")
        else:
            m[0] = m0
            print(f"   (Biên đề bài: m_0 = S'(0) = {m[0]})")
            
        print("\n1. Tính các đạo hàm m_k tại nút (Công thức truy hồi):")
        for k in range(self.n - 1):
            term = 2 * (self.y[k+1] - self.y[k]) / self.h[k]
            m[k+1] = -m[k] + term
            print(f"   m_{k+1} = -m_{k} + 2*(y_{k+1}-y_{k})/h_{k}")
            print(f"        = -({m[k]:.4f}) + {term:.4f} = {m[k+1]:.4f}")
            
        print("\n2. Tính hệ số đa thức:")
        coeffs = []
        for k in range(self.n - 1):
            print(f"\n--- Đoạn {k+1}: [{self.x[k]}, {self.x[k+1]}] ---")
            # Công thức Slide trang 9
            ak = (m[k+1] - m[k]) / (2 * self.h[k])
            bk = (m[k] * self.x[k+1] - m[k+1] * self.x[k]) / self.h[k]
            
            term_c1 = (-m[k] * self.x[k+1]**2 + m[k+1] * self.x[k]**2)/(2*self.h[k])
            term_c2 = self.y[k] + (m[k]*self.h[k])/2
            ck = term_c1 + term_c2
            
            print(f"   a_{k} = ({m[k+1]:.4f} - {m[k]:.4f}) / (2*{self.h[k]:.4f}) = {ak:.4f}")
            print(f"   b_{k} = ... = {bk:.4f}")
            print(f"   c_{k} = ... = {ck:.4f}")
            print(f"   => PT: y = {ak:.4f}x^2 + {bk:.4f}x + {ck:.4f}")
            coeffs.append((ak, bk, ck))
        return coeffs

    def solve_cubic(self, alpha_start=-1, alpha_end=1):
        """Spline Cấp 3 (Cubic)"""
        print(f"\n{'='*30} LỜI GIẢI SPLINE CẤP 3 (Cubic) {'='*30}")
        print(f"Điều kiện biên đạo hàm cấp 2: alpha_0={alpha_start}, alpha_n={alpha_end}")
        
        n = self.n
        h = self.h
        A = np.zeros((n-2, n-2))
        B = np.zeros(n-2)
        
        print("\n1. Hệ phương trình xác định alpha (đạo hàm cấp 2):")
        
        for i in range(n-2):
            k = i + 1
            # Hệ số ma trận
            c_prev = h[k-1] / 6
            c_curr = (h[k-1] + h[k]) / 3
            c_next = h[k] / 6
            
            # Vế phải
            rhs = (self.y[k+1] - self.y[k])/h[k] - (self.y[k] - self.y[k-1])/h[k-1]
            
            A[i, i] = c_curr
            if i > 0: A[i, i-1] = c_prev
            if i < n-3: A[i, i+1] = c_next
            
            # Xử lý in ấn và biên
            eq_str = f"   Tại x_{k}: "
            if k==1: # Dính biên trái
                rhs -= c_prev * alpha_start
                eq_str += f"{c_curr:.4f}*a_1 + {c_next:.4f}*a_2 = {rhs:.4f} (Đã chuyển biên a_0)"
            elif k==n-2: # Dính biên phải
                rhs -= c_next * alpha_end
                eq_str += f"{c_prev:.4f}*a_{k-1} + {c_curr:.4f}*a_{k} = {rhs:.4f} (Đã chuyển biên a_n)"
            else:
                eq_str += f"{c_prev:.4f}*a_{k-1} + {c_curr:.4f}*a_{k} + {c_next:.4f}*a_{k+1} = {rhs:.4f}"
            
            B[i] = rhs
            print(eq_str)
            
        # Giải hệ
        alpha_inner = np.linalg.solve(A, B)
        alpha = np.concatenate(([alpha_start], alpha_inner, [alpha_end]))
        print(f"\n   -> Nghiệm alpha: {np.round(alpha, 4)}")
        
        print("\n2. Tính hệ số đa thức (theo công thức Slide trang 18):")
        coeffs = []
        for k in range(n - 1):
            print(f"\n--- Đoạn {k+1}: [{self.x[k]}, {self.x[k+1]}] ---")
            
            # Áp dụng y chang công thức slide a, b, c, d
            ak = (alpha[k+1] - alpha[k]) / (6 * h[k])
            bk = (3 * alpha[k] * self.x[k+1] - 3 * alpha[k+1] * self.x[k]) / (6 * h[k])
            
            term_c1 = (-3 * alpha[k] * self.x[k+1]**2 + 3 * alpha[k+1] * self.x[k]**2) / (6 * h[k])
            term_c2 = (self.y[k+1] - self.y[k]) / h[k]
            term_c3 = (alpha[k+1] - alpha[k]) * h[k] / 6
            ck = term_c1 + term_c2 - term_c3
            
            term_d1 = (alpha[k] * self.x[k+1]**3 - alpha[k+1] * self.x[k]**3) / (6 * h[k])
            term_d2 = (self.y[k] * self.x[k+1] - self.y[k+1] * self.x[k]) / h[k]
            term_d3 = (alpha[k+1] * self.x[k] - alpha[k] * self.x[k+1]) * h[k] / 6
            dk = term_d1 + term_d2 + term_d3
            
            print(f"   a = ({alpha[k+1]:.2f} - {alpha[k]:.2f}) / 6h = {ak:.4f}")
            print(f"   b = ... = {bk:.4f}")
            print(f"   c = ... = {ck:.4f}")
            print(f"   d = ... = {dk:.4f}")
            print(f"   => PT: y = {ak:.4f}x^3 + {bk:.4f}x^2 + {ck:.4f}x + {dk:.4f}")
            coeffs.append((ak, bk, ck, dk))
        return coeffs

    def solve_quartic(self):
        """Spline Cấp 4 (Quartic)"""
        print(f"\n{'='*30} LỜI GIẢI SPLINE CẤP 4 (Quartic) {'='*30}")
        print("Phương pháp: Giải hệ phương trình trực tiếp (Ma trận lớn).")
        print("Dạng hàm: S_k(x) = a x^4 + b x^3 + c x^2 + d x + e")
        
        n_seg = self.n - 1
        n_vars = 5 * n_seg
        A = np.zeros((n_vars, n_vars))
        B = np.zeros(n_vars)
        row = 0
        
        print(f"\n1. Thiết lập các nhóm phương trình ({n_vars} ẩn):")
        
        # Nhóm 1: Nội suy
        print(f"   - Nhóm Nội suy: 2 PT/đoạn x {n_seg} đoạn = {2*n_seg} PT")
        for k in range(n_seg):
            # Đầu đoạn
            x_s = self.x[k]
            A[row, 5*k:5*k+5] = [x_s**4, x_s**3, x_s**2, x_s, 1]
            B[row] = self.y[k]
            row += 1
            # Cuối đoạn
            x_e = self.x[k+1]
            A[row, 5*k:5*k+5] = [x_e**4, x_e**3, x_e**2, x_e, 1]
            B[row] = self.y[k+1]
            row += 1
            
        # Nhóm 2: Trơn (Đạo hàm cấp 1, 2, 3)
        print(f"   - Nhóm Trơn (C^1, C^2, C^3): 3 PT/nút x {n_seg-1} nút = {3*(n_seg-1)} PT")
        for k in range(n_seg - 1):
            xn = self.x[k+1]
            # Cấp 1
            d1 = [4*xn**3, 3*xn**2, 2*xn, 1, 0]
            A[row, 5*k:5*k+5] = d1
            A[row, 5*(k+1):5*(k+1)+5] = [-x for x in d1]
            row += 1
            # Cấp 2
            d2 = [12*xn**2, 6*xn, 2, 0, 0]
            A[row, 5*k:5*k+5] = d2
            A[row, 5*(k+1):5*(k+1)+5] = [-x for x in d2]
            row += 1
            # Cấp 3
            d3 = [24*xn, 6, 0, 0, 0]
            A[row, 5*k:5*k+5] = d3
            A[row, 5*(k+1):5*(k+1)+5] = [-x for x in d3]
            row += 1
            
        # Nhóm 3: Biên
        print(f"   - Nhóm Biên bổ sung: 3 PT (Chọn S''(x0)=S'''(x0)=S''(xn)=0)")
        # S''(x0)=0
        A[row, 0:5] = [12*self.x[0]**2, 6*self.x[0], 2, 0, 0]
        row += 1
        # S'''(x0)=0
        A[row, 0:5] = [24*self.x[0], 6, 0, 0, 0]
        row += 1
        # S''(xn)=0
        xn = self.x[-1]
        A[row, 5*(n_seg-1):] = [12*xn**2, 6*xn, 2, 0, 0]
        row += 1
        
        # Giải hệ
        try:
            sol = np.linalg.solve(A, B)
            print("\n2. Kết quả hàm ghép trơn:")
            coeffs = []
            for k in range(n_seg):
                idx = 5*k
                a,b,c,d,e = sol[idx:idx+5]
                print(f"\n--- Đoạn {k+1}: [{self.x[k]}, {self.x[k+1]}] ---")
                print(f"   y = {a:.4f}x^4 + {b:.4f}x^3 + {c:.4f}x^2 + {d:.4f}x + {e:.4f}")
                coeffs.append((a,b,c,d,e))
            return coeffs
        except:
            print("Lỗi giải hệ phương trình cấp 4.")
            return []

# --- MAIN ---
print("************************************************")
print("  CHƯƠNG TRÌNH GIẢI BÀI TẬP LỚN - SPLINE 1->4")
print("************************************************")

# Dữ liệu từ Câu 21
x_raw = [0, 0.5236, 1.0472, 1.5708, 3.1416]
y_raw = [1, 0.866, -0.866, 0, -1]

solver = SplineMasterSolver(x_raw, y_raw)

# 1. Chạy Cấp 1
solver.solve_linear()

# 2. Chạy Cấp 2 (Với biên S'(0) = 0 như đề bài 21a)
solver.solve_quadratic(m0=0)

# 3. Chạy Cấp 3 (Với biên S''(0)=-1, S''(3.14)=1 như đề bài 21b)
solver.solve_cubic(alpha_start=-1, alpha_end=1)

# 4. Chạy Cấp 4
solver.solve_quartic()