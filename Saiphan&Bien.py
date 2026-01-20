import numpy as np
import matplotlib.pyplot as plt
import math

# Khai báo các hàm toán học để người dùng có thể nhập (ví dụ: sin, cos, exp, log)
from math import sin, cos, exp, log, pi, sqrt

class BVPSolver:
    def __init__(self):
        self.p_func = None
        self.q_func = None
        self.f_func = None
        self.x_vals = None
        self.u_vals = None

    def get_user_input(self):
        print("=== GIẢI BÀI TOÁN BIÊN BẰNG PHƯƠNG PHÁP SAI PHÂN ===")
        print("Dạng phương trình: [p(x)u']' - q(x)u = -f(x)")
        print("Lưu ý: Nhập công thức theo cú pháp Python (ví dụ: 1.25*x*exp(-x**2))")
        
        # Nhập các hàm p, q, f
        p_str = input("Nhập p(x): ")
        q_str = input("Nhập q(x): ")
        f_str = input("Nhập f(x): ") # PDF sử dụng vế phải là -f(x), ta nhập f(x) rồi đổi dấu sau

        self.p_func = lambda x: eval(p_str)
        self.q_func = lambda x: eval(q_str)
        self.f_func = lambda x: eval(f_str)

        # Nhập lưới
        self.a = float(input("Nhập điểm đầu a: "))
        self.b = float(input("Nhập điểm cuối b: "))
        self.h = float(input("Nhập bước lưới h: "))
        
        self.N = int(round((self.b - self.a) / self.h))
        self.x_vals = np.linspace(self.a, self.b, self.N + 1)
        
        # Nhập điều kiện biên
        self.bc_left = self._get_bc_params("trái (tại a)", self.a)
        self.bc_right = self._get_bc_params("phải (tại b)", self.b)

    def _get_bc_params(self, name, x_loc):
        print(f"\n--- Điều kiện biên {name} ---")
        print("1. Loại 1: u({0}) = alpha".format(x_loc))
        print("2. Loại 2: p({0})u'({0}) = -mu".format(x_loc))
        print("3. Loại 3/Hỗn hợp: p({0})u'({0}) - sigma*u({0}) = -mu".format(x_loc))
        
        choice = int(input(f"Chọn loại điều kiện biên cho biên {name} (1-3): "))
        
        params = {'type': choice}
        
        if choice == 1: # Dirichlet [cite: 7]
            val = float(input(f"Nhập giá trị u({x_loc}): "))
            params['val'] = val
        elif choice == 2: # Neumann [cite: 12]
            # p(x)u'(x) = -mu => u'(x) = -mu/p(x)
            # PDF định nghĩa: p(a)u'(a) = -mu1 [cite: 13]
            mu = float(input(f"Nhập giá trị vế phải (-mu) của biểu thức p({x_loc})u'({x_loc}): "))
            # Lưu ý: Người dùng nhập giá trị thực tế của vế phải, ta gán nó là -mu
            params['mu'] = -mu # Code tính toán dùng mu dương theo công thức, nhưng input là vế phải
            params['sigma'] = 0
        elif choice == 3: # Robin [cite: 18]
            # p(x)u'(x) - sigma*u(x) = -mu
            sigma = float(input("Nhập hệ số sigma (hệ số của u): "))
            rhs = float(input("Nhập vế phải (-mu): "))
            params['sigma'] = sigma
            params['mu'] = -rhs 
            
        return params

    def solve(self):
        N = self.N
        h = self.h
        
        # Khởi tạo ma trận hệ số A (kích thước N+1 x N+1) và vế phải b
        M = np.zeros((N + 1, N + 1))
        R = np.zeros(N + 1)
        
        # --- 1. Xây dựng phương trình tại các điểm trong (Interior Points) ---
        # Từ chỉ số 1 đến N-1 [cite: 42]
        for i in range(1, N):
            xi = self.x_vals[i]
            
            # Tính các hệ số p tại bán bước [cite: 36, 38]
            p_minus = self.p_func(xi - h/2) # p_{i-1/2}
            p_plus  = self.p_func(xi + h/2) # p_{i+1/2}
            q_i     = self.q_func(xi)
            f_i     = self.f_func(xi)
            
            # Các hệ số A_i, B_i, C_i theo [cite: 36, 37, 38]
            A_i = p_minus
            C_i = p_plus
            B_i = p_plus + p_minus + h**2 * q_i
            
            # Điền vào ma trận: A_i*u_{i-1} - B_i*u_i + C_i*u_{i+1} = -h^2*f_i [cite: 39]
            M[i, i-1] = A_i
            M[i, i]   = -B_i
            M[i, i+1] = C_i
            R[i]      = - (h**2) * f_i

        # --- 2. Xử lý biên trái (x = a, i = 0) ---
        if self.bc_left['type'] == 1:
            # u(0) = alpha [cite: 45]
            M[0, 0] = 1
            R[0] = self.bc_left['val']
        else:
            # Loại 2 hoặc 3 (Hỗn hợp) tại biên trái [cite: 97]
            # Công thức: p_{1/2}u_1 - [p_{1/2} + h^2*q_0/2 + sigma1]*u_0 = -h^2*f_0/2 - mu1*h
            # Lưu ý: Với loại 2 thì sigma = 0 [cite: 88]
            
            p_half = self.p_func(self.a + h/2)
            q_0 = self.q_func(self.a)
            f_0 = self.f_func(self.a)
            sigma1 = self.bc_left['sigma']
            mu1 = self.bc_left['mu'] # Đây là giá trị mu trong công thức PDF (đã đảo dấu so với vế phải)
            
            # Hệ số của u_0
            coeff_u0 = -(p_half + (h**2 * q_0)/2 + sigma1)
            # Hệ số của u_1
            coeff_u1 = p_half
            # Vế phải
            rhs_val = -(h**2 * f_0)/2 - mu1 * h
            
            M[0, 0] = coeff_u0
            M[0, 1] = coeff_u1
            R[0] = rhs_val

        # --- 3. Xử lý biên phải (x = b, i = N) ---
        if self.bc_right['type'] == 1:
            # u(N) = beta [cite: 46]
            M[N, N] = 1
            R[N] = self.bc_right['val']
        else:
            # Loại 2 hoặc 3 (Hỗn hợp) tại biên phải [cite: 99]
            # Công thức: [p_{N-1/2} + h^2*q_N/2 - sigma2]*u_N - p_{N-1/2}*u_{N-1} = h^2*f_N/2 - mu2*h
            # Lưu ý: Với loại 2 thì sigma = 0 [cite: 95]
            
            p_last_half = self.p_func(self.b - h/2)
            q_N = self.q_func(self.b)
            f_N = self.f_func(self.b)
            sigma2 = self.bc_right['sigma']
            mu2 = self.bc_right['mu']
            
            # Hệ số của u_N
            coeff_uN = p_last_half + (h**2 * q_N)/2 - sigma2
            # Hệ số của u_{N-1}
            coeff_uN_minus = -p_last_half
            # Vế phải
            rhs_val = (h**2 * f_N)/2 - mu2 * h
            
            M[N, N] = coeff_uN
            M[N, N-1] = coeff_uN_minus
            R[N] = rhs_val

        # --- 4. Giải hệ phương trình tuyến tính ---
        try:
            self.u_vals = np.linalg.solve(M, R)
            print("\nĐã giải xong hệ phương trình!")
            
            # In ra giá trị min/max như yêu cầu của ảnh 2
            max_val = np.max(self.u_vals)
            max_idx = np.argmax(self.u_vals)
            min_val = np.min(self.u_vals)
            min_idx = np.argmin(self.u_vals)
            
            print(f"Giá trị lớn nhất: {max_val:.5f} tại x = {self.x_vals[max_idx]:.5f}")
            print(f"Giá trị nhỏ nhất: {min_val:.5f} tại x = {self.x_vals[min_idx]:.5f}")

        except np.linalg.LinAlgError:
            print("Lỗi: Ma trận suy biến, không thể giải hệ phương trình.")

    def plot_solution(self):
        if self.u_vals is not None:
            plt.figure(figsize=(10, 6))
            plt.plot(self.x_vals, self.u_vals, 'b-o', label='Nghiệm xấp xỉ u(x)')
            plt.title(f"Nghiệm phương trình vi phân (h={self.h})")
            plt.xlabel("x")
            plt.ylabel("u(x)")
            plt.grid(True)
            plt.legend()
            plt.show()

if __name__ == "__main__":
    solver = BVPSolver()
    solver.get_user_input()
    solver.solve()
    solver.plot_solution()