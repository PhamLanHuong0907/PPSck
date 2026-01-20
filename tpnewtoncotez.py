import numpy as np
from scipy.integrate import quad
from fractions import Fraction

def he_so_newton_cotes(n):
    """
    Tính bộ hệ số Cotes C_i cho bậc n.
    """
    C = []
    # Hàm tạo đa thức Lagrange cơ sở L_i(t)
    def lagrange_basis(t, i, n):
        result = 1.0
        for j in range(n + 1):
            if j != i:
                result *= (t - j) / (i - j)
        return result

    print(f"\n-> Đang tính bộ hệ số Cotes chuẩn hóa cho n={n}...")
    for i in range(n + 1):
        val, error = quad(lagrange_basis, 0, n, args=(i, n))
        C.append(val)
    
    return np.array(C)

def tich_phan_newton_cotes_trinh_bay(f, a, b, n):
    """
    Tính tích phân và in bảng chi tiết dạng phân số
    """
    print("="*65)
    print(f"PHƯƠNG PHÁP NEWTON-COTES (Bậc n={n})")
    print(f"Cận [{a}, {b}]")
    
    # 1. Tính bước h
    h = (b - a) / n
    print(f"1. Bước nhảy h = ({b} - {a}) / {n} = {h}")
    
    # 2. Tạo các nút x
    X = np.linspace(a, b, n + 1)
    Y = f(X)
    
    # 3. Lấy hệ số Cotes (dạng float)
    C_floats = he_so_newton_cotes(n)
    
    # 4. Chuyển đổi sang Phân số (để trình bày đẹp)
    # Lưu ý: limit_denominator giúp làm tròn số thực về phân số gần nhất
    C_fractions = [Fraction(x).limit_denominator(100000) for x in C_floats]
    
    # In kiểm tra hệ số dạng phân số (Rất quan trọng khi làm bài tập)
    print(f"2. Bộ hệ số Cotes (Ci): {', '.join(str(c) for c in C_fractions)}")
    
    # 5. In bảng tính chi tiết
    print("\n3. Bảng tính chi tiết:")
    print("-" * 65)
    print(f"{'i':<4} | {'xi':<10} | {'yi = f(xi)':<12} | {'Ci (Hệ số)':<10} | {'Thành phần (Ci*yi)':<15}")
    print("-" * 65)
    
    sum_weighted_y = 0.0
    
    for i in range(n + 1):
        weighted_val = C_floats[i] * Y[i]
        sum_weighted_y += weighted_val
        
        # In dòng dữ liệu
        print(f"{i:<4} | {X[i]:<10.5f} | {Y[i]:<12.5f} | {str(C_fractions[i]):<10} | {weighted_val:<15.5f}")
        
    print("-" * 65)
    
    # 6. Tính kết quả cuối
    I = h * sum_weighted_y
    
    print(f"Tổng trọng số S = {sum_weighted_y:.6f}")
    print(f"Công thức: I ≈ h * S")
    print(f"Kết quả:   I ≈ {h} * {sum_weighted_y:.6f} = {I:.8f}")
    
    return I

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    def f_test(x):
        return np.exp(-x**2) # Ví dụ: e^-x^2
    
    a, b = 0, 2
    
    # Thử với n=1 (Hình thang), n=2 (Simpson 1/3), n=3 (Simpson 3/8), n=4 (Boole)
    # Code sẽ tự động tìm ra các phân số quen thuộc như 1/2, 4/3, 3/8...
    
    # Test Simpson 1/3 (n=2)
    tich_phan_newton_cotes_trinh_bay(f_test, a, b, n=2)
    
    # Test Simpson 3/8 (n=3)
    tich_phan_newton_cotes_trinh_bay(f_test, a, b, n=3)
    
    # Test Boole's Rule (n=4) - Ít gặp nhưng code vẫn cân được
    tich_phan_newton_cotes_trinh_bay(f_test, a, b, n=4)