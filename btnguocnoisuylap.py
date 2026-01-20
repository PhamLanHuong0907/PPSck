import numpy as np
import math

def giai_noi_suy_nguoc_lap_chi_tiet(x_nodes, y_nodes, y_target, epsilon=1e-5, max_iter=20):
    """
    Giải và in chi tiết bài toán nội suy ngược (PP Lặp).
    Input:
        x_nodes, y_nodes: Bảng dữ liệu (mốc cách đều).
        y_target: Giá trị y cần tìm x.
        epsilon: Sai số cho phép.
    """
    n = len(x_nodes)
    h = x_nodes[1] - x_nodes[0]
    
    print("\n" + "="*70)
    print(f"{'GIẢI BÀI TOÁN NỘI SUY NGƯỢC (PHƯƠNG PHÁP LẶP)':^70}")
    print("="*70 + "\n")
    
    print(f"Yêu cầu: Tìm x sao cho f(x) = {y_target}")
    print(f"Dữ liệu: {n} điểm. Bước nhảy h = {h:.4f}")

    # --- BƯỚC 1: TÌM KHOẢNG CÁCH LY NGHIỆM ---
    print(f"\n" + "-"*30 + " BƯỚC 1: TÌM KHOẢNG CÁCH LY " + "-"*30)
    
    k_idx = -1
    for i in range(n - 1):
        # Kiểm tra y_target có nằm giữa y[i] và y[i+1] không
        if (y_nodes[i] - y_target) * (y_nodes[i+1] - y_target) <= 0:
            k_idx = i
            break
            
    if k_idx == -1:
        print("Lỗi: Giá trị y cần tìm nằm ngoài miền giá trị của bảng số liệu.")
        return None
        
    print(f"Khoảng chứa nghiệm: [(x{k_idx}, y{k_idx}), (x{k_idx+1}, y{k_idx+1})]")
    print(f"   x: {x_nodes[k_idx]} -> {x_nodes[k_idx+1]}")
    print(f"   y: {y_nodes[k_idx]} -> {y_nodes[k_idx+1]}")
    
    # Kiểm tra đơn điệu
    is_increasing = y_nodes[k_idx+1] > y_nodes[k_idx]
    direction = "Tăng" if is_increasing else "Giảm"
    print(f"   Hàm số đơn điệu {direction} trong khoảng này.")

    # --- BƯỚC 2: TÍNH BẢNG SAI PHÂN ---
    print(f"\n" + "-"*30 + " BƯỚC 2: BẢNG SAI PHÂN " + "-"*30)
    
    # Tính bảng sai phân đầy đủ
    delta = np.zeros((n, n))
    delta[:, 0] = y_nodes
    for j in range(1, n):
        for i in range(n - j):
            delta[i][j] = delta[i+1][j-1] - delta[i][j-1]

    # In bảng (chỉ in vùng lân cận k để tiết kiệm không gian nếu bảng lớn)
    start_print = max(0, k_idx - 2)
    end_print = min(n, k_idx + 4)
    
    headers = ["x", "y"] + [f"Delta^{k}" for k in range(1, 6)] # In đến cấp 5
    header_str = "".join([f"{h:<10}" for h in headers])
    print(header_str)
    print("-" * 70)
    
    for i in range(start_print, end_print):
        row_str = f"{x_nodes[i]:<10.2f}"
        for j in range(min(n - i, 7)): # Giới hạn cột in
            row_str += f"{delta[i][j]:<10.4f}"
        print(row_str)

    # --- BƯỚC 3: THIẾT LẬP CÔNG THỨC LẶP ---
    print(f"\n" + "-"*30 + " BƯỚC 3: QUÁ TRÌNH LẶP " + "-"*30)
    
    # Quyết định dùng Newton Tiến (từ x_k) hay Lùi (từ x_k+1)
    # Nếu y_target gần y_k hơn -> Tiến. Gần y_k+1 hơn -> Lùi.
    dist_to_k = abs(y_target - y_nodes[k_idx])
    dist_to_k1 = abs(y_target - y_nodes[k_idx+1])
    
    # Mặc định dùng Newton TIẾN từ x_k (theo tài liệu thường dùng TH1)
    # Tuy nhiên, nếu muốn tối ưu có thể switch. Ở đây mình code TH1 (Tiến) cho phổ biến.
    print(f"Chọn mốc xuất phát: x_k = {x_nodes[k_idx]} (Newton Tiến)")
    
    # Lấy các hệ số sai phân tiến từ hàng k_idx: Delta^j y_k
    # Trong bảng delta của mình, delta[i][j] chính là sai phân cấp j tại dòng i
    coeffs = delta[k_idx, :]
    
    y0 = coeffs[0]   # y_k
    dy0 = coeffs[1]  # Delta y_k
    
    print(f"Công thức lặp: t = ({y_target} - {y0} - R(t)) / {dy0}")
    print(f"với R(t) = (Delta^2/2!)t(t-1) + (Delta^3/3!)t(t-1)(t-2) + ...")

    # Hàm tính R(t)
    def calculate_R_t(t):
        val = 0
        t_term = 1 # t(t-1)...
        # Bắt đầu từ cấp 2
        for j in range(2, min(n - k_idx, 6)): # Dùng tối đa bậc 5 hoặc hết bảng
            t_term *= (t - (j - 2)) 
            term = (coeffs[j] / math.factorial(j)) * t_term * (t - (j - 1))
            val += term
        return val

    # Khởi tạo t0
    t_curr = (y_target - y0) / dy0
    print(f"\nGiá trị khởi đầu t0 = ({y_target} - {y0}) / {dy0} = {t_curr:.6f}")
    
    print(f"\n{'Lần lặp':<10} | {'t_cu':<12} | {'R(t)':<12} | {'t_moi':<12} | {'Sai số':<12}")
    print("-" * 65)

    final_t = t_curr
    for j in range(max_iter):
        # 1. Tính R(t)
        r_val = calculate_R_t(t_curr)
        
        # 2. Tính t mới
        t_next = (y_target - y0 - r_val) / dy0
        
        # 3. Tính sai số
        error = abs(t_next - t_curr)
        
        print(f"{j+1:<10} | {t_curr:<12.6f} | {r_val:<12.6f} | {t_next:<12.6f} | {error:<12.6e}")
        
        t_curr = t_next
        final_t = t_next
        
        if error < epsilon:
            print(f"\n-> Hội tụ sau {j+1} bước lặp.")
            break
            
    # --- BƯỚC 4: TÍNH KẾT QUẢ CUỐI CÙNG ---
    print(f"\n" + "-"*30 + " BƯỚC 4: KẾT QUẢ " + "-"*30)
    x_res = x_nodes[k_idx] + final_t * h
    
    print(f"Nghiệm t tìm được: t ≈ {final_t:.6f}")
    print(f"Công thức nghiệm: x = x_k + t*h")
    print(f"                  x = {x_nodes[k_idx]} + {final_t:.6f} * {h}")
    print(f"Kết quả x ≈ {x_res:.6f}")
    
    return x_res

# ==============================================================================
# PHẦN NHẬP DỮ LIỆU CỦA BẠN
# ==============================================================================

# Dữ liệu mẫu (x cách đều)
x_in = np.array([1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8])
y_in = np.array([4.02, 3.98, 4.23, 3.67, 2.99, 1.24, 0.87, 2.08, 4.54])

# Giá trị cần tìm nghiệm (Ví dụ tìm x để y = 1.0)
# Lưu ý: 1.0 nằm giữa 1.24 (x=2.2) và 0.87 (x=2.4) -> Khoảng [2.2, 2.4]
y_can_tim = 1.0 

# Chạy hàm
giai_noi_suy_nguoc_lap_chi_tiet(x_in, y_in, y_can_tim)