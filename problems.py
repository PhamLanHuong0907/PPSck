import numpy as np
import re

def preprocess_expression(expr):
    """
    Chuyển đổi input người dùng (math dạng text) sang Python syntax hợp lệ.
    Ví dụ: "e^x + ln(y) + 2t^2" -> "np.exp(x) + np.log(y) + 2*t**2"
    """
    # 1. Chuyển mũ ^ thành **
    expr = expr.replace('^', '**')
    
    # 2. Xử lý hàm log, ln, e^, sin, cos...
    # Thay 'ln' thành 'np.log', 'e^' hoặc 'exp' thành 'np.exp'
    # Dùng regex để tránh thay thế nhầm tên biến (ví dụ biến 'aln' không bị đổi)
    
    replacements = {
        r'\bln\b': 'np.log',
        r'\blog\b': 'np.log10', # Mặc định log là log10, ln là log tự nhiên
        r'\be\*\*': 'np.exp(',  # e**x -> np.exp(x
        r'\bexp\b': 'np.exp',
        r'\bsin\b': 'np.sin',
        r'\bcos\b': 'np.cos',
        r'\btan\b': 'np.tan',
        r'\bsqrt\b': 'np.sqrt',
        r'\bpi\b': 'np.pi',
    }
    
    for pattern, repl in replacements.items():
        expr = re.sub(pattern, repl, expr)
        
    return expr

def get_problem(problem_id):
    """
    Trả về: (f_numeric, t_span, y0, h, raw_expressions, param_name)
    """
    # Nếu là input custom
    if problem_id in ['custom', 'nhap', '0']:
        print("\n" + "="*50)
        print(" NHẬP ĐỀ BÀI (Hỗ trợ: ^, ln, e^, sin, cos...)")
        print("="*50)
        
        try:
            num_eq = int(input(">> Số lượng phương trình: "))
            
            expressions = []
            print(f"\n>> Nhập biểu thức vế phải f(t, x, y...):")
            
            vars_hint = ['x', 'y', 'z', 'w']
            for i in range(num_eq):
                var_name = vars_hint[i] if i < len(vars_hint) else f"y[{i}]"
                raw_expr = input(f"   PT {i+1} ({var_name}' = ...): ")
                # Xử lý chuỗi input
                expr_ready = preprocess_expression(raw_expr)
                expressions.append(expr_ready)

            # Tự động tìm biến tham số (k, m, a...)
            param_name = None
            potential_params = set()
            
            # Whitelist các từ khóa không phải là tham số
            whitelist = ['x','y','z','t','np','math','sin','cos','tan','exp','sqrt','log','abs','pi']
            
            for expr in expressions:
                words = re.findall(r'[a-zA-Z_]+', expr)
                for w in words:
                    if w not in whitelist and 'y[' not in w:
                        potential_params.add(w)
            
            if potential_params:
                param_name = list(potential_params)[0]
                print(f"-> Phát hiện tham số: '{param_name}'")

            t0 = float(input("   t bắt đầu: "))
            tf = float(input("   t kết thúc: "))
            
            y0_list = []
            print(f"\n>> Điều kiện đầu tại t = {t0}:")
            for i in range(num_eq):
                val = float(input(f"   y{i}({t0}) = "))
                y0_list.append(val)
                
            h = float(input(">> Bước nhảy h: "))

            def f_numeric_wrapper(t, y_vec, param_val=0):
                # Môi trường tính toán
                env = {
                    't': t, 'np': np, 'math': np,
                    'y_arr': y_vec
                }
                if param_name: env[param_name] = param_val
                
                # Mapping biến
                if len(y_vec) == 1: env['y'] = y_vec[0]; env['x'] = y_vec[0] # x cũng là y nếu 1 biến
                elif len(y_vec) >= 2:
                    env['x'] = y_vec[0]; env['y'] = y_vec[1]
                    if len(y_vec) >= 3: env['z'] = y_vec[2]

                res = []
                for expr in expressions:
                    expr_eval = expr.replace('y[', 'y_arr[')
                    res.append(eval(expr_eval, env))
                return np.array(res)

            return f_numeric_wrapper, [t0, tf], y0_list, h, expressions, param_name

        except Exception as e:
            print(f"[LỖI NHẬP LIỆU]: {e}")
            return None

    # Mẫu test nhanh
    if problem_id == 'test': 
        # y' = y, y(0)=1
        return lambda t, y, p=0: np.array([y[0]]), [0, 1], [1.0], 0.1, ["y"], None
    
    return None