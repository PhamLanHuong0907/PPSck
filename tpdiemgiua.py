import math

def midpoint_rule_detailed(f, a, b, n):
    """
    Tính tích phân điểm giữa và in bảng số liệu chi tiết để làm bài tập.
    """
    h = (b - a) / n
    total_area = 0.0
    
    # 1. In thông số đầu vào
    print("\n" + "="*50)
    print(f"PHƯƠNG PHÁP ĐIỂM GIỮA (Midpoint Rule)")
    print(f"Cận: [{a}, {b}], Số đoạn n = {n}")
    print(f"Bước nhảy h = (b - a)/n = {h}")
    print("-" * 50)
    
    # 2. In tiêu đề bảng
    # Căn lề: i (5 ký tự), x_mid (15 ký tự), f(x_mid) (20 ký tự)
    print(f"{'i':<5} | {'x_mid (Điểm giữa)':<15} | {'f(x_mid)':<20}")
    print("-" * 50)
    
    for i in range(n):
        # Tính điểm giữa
        x_mid = a + (i + 0.5) * h
        
        # Tính giá trị hàm
        fx = f(x_mid)
        total_area += fx
        
        # 3. In từng dòng dữ liệu (Làm tròn 6 chữ số thập phân)
        print(f"{i:<5} | {x_mid:<15.6f} | {fx:<20.6f}")
        
    print("-" * 50)
    
    # 4. In kết quả tổng và tích
    result = total_area * h
    print(f"Tổng S = sum(f(x_mid)) = {total_area:.6f}")
    print(f"Kết quả I ≈ h * S      = {h} * {total_area:.6f}")
    print(f"KẾT QUẢ CUỐI CÙNG      = {result:.8f}")
    print("="*50 + "\n")
    
    return result

# --- VÍ DỤ SỬ DỤNG ---

# Hàm cần tính: f(x) = x^2
def my_function(x):
    return x**2  
    # Hoặc ví dụ khác: return math.exp(x)

# Tham số
a = 0
b = 1
n = 10 

# Gọi hàm
result = midpoint_rule_detailed(my_function, a, b, n)

# Kiểm tra sai số (nếu biết kết quả đúng)
exact_value = 1/3
print(f"Giá trị thực (lý thuyết): {exact_value:.8f}")
print(f"Sai số tuyệt đối:         {abs(result - exact_value):.8f}")