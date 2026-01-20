import math

def tim_moc_noi_suy_toi_uu_v2(n, a, b):
    """
    Hàm tính n mốc nội suy tối ưu (mốc Chebyshev) trên khoảng [a, b]
    dựa trên THUẬT TOÁN 2.

    Tham số:
    n (int): Số lượng mốc nội suy cần tìm (n > 0).
    a (float): Mút trái của khoảng nội suy.
    b (float): Mút phải của khoảng nội suy (phải thỏa mãn a < b).

    Trả về:
    list: Danh sách chứa n mốc nội suy, đã được sắp xếp tăng dần,
          hoặc None nếu input không hợp lệ.
    """
    
    # --- Kiểm tra điều kiện (Tương tự thuật toán 1) ---
    if not isinstance(n, int) or n <= 0: # Thuật toán 2 ghi n > 0
        print(f"Lỗi: n (số mốc) phải là số nguyên > 0. Nhận được: {n}")
        return None
    
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        print(f"Lỗi: a và b phải là số thực. Nhận được: a={a}, b={b}")
        return None

    if a >= b:
        print(f"Lỗi: Khoảng nội suy không hợp lệ. Phải là a < b. Nhận được: a={a}, b={b}")
        return None

    # --- 1. Khởi tạo danh sách rỗng X ---
    X = []

    # --- 2. Vòng lặp for k = 0 to n-1 ---
    for k in range(n):
        
        # --- 3. Tính nghiệm Chebyshev gốc t_k trên [-1, 1] ---
        # Công thức: t_k = cos( (2k + 1) * pi / (2n) )
        t_k = math.cos((2 * k + 1) * math.pi / (2 * n))
        
        # --- 4. Ánh xạ nghiệm t_k sang đoạn [a, b] ---
        x_k = (a + b) / 2 + (b - a) / 2 * t_k
        
        # --- 5. Thêm x_k vào danh sách X ---
        X.append(x_k)
        
    # --- 6. (end for) ---

    # --- 7. Sắp xếp lại danh sách X theo thứ tự tăng dần ---
    # Ghi chú: Vòng lặp trên tạo ra dãy GIẢM DẦN (vì k=0 cho cos() lớn nhất)
    # nên chúng ta cần sắp xếp lại.
    X.sort()
    
    # --- 8. return Danh sách X ---
    return X