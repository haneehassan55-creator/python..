
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewtonRaphsonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Methods Project - Newton-Raphson Solver")
        self.root.geometry("1050x650")
        self.root.configure(bg="#f4f6f9")

        # متغير الرمز الرياضي
        self.x_sym = sp.Symbol('x')

        self.create_widgets()

    def create_widgets(self):
        # === الإطار العلوي للمدخلات ===
        input_frame = tk.LabelFrame(self.root, text=" إدخال بيانات المعادلة (Inputs) ", font=("Arial", 11, "bold"), bg="#f4f6f9", padx=15, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        # الصف الأول: المعادلة ونقطة البداية
        tk.Label(input_frame, text="المعادلة f(x):", font=("Arial", 10, "bold"), bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.eq_entry = tk.Entry(input_frame, width=30, font=("Consolas", 11))
        self.eq_entry.insert(0, "x**3 - 8*x + 5")  # مثال من المحاضرة
        self.eq_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="نقطة البداية (x0):", font=("Arial", 10, "bold"), bg="#f4f6f9").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.x0_entry = tk.Entry(input_frame, width=12, font=("Consolas", 11))
        self.x0_entry.insert(0, "0")
        self.x0_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="نسبة الخطأ (Tolerance):", font=("Arial", 10, "bold"), bg="#f4f6f9").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.tol_entry = tk.Entry(input_frame, width=12, font=("Consolas", 11))
        self.tol_entry.insert(0, "1e-4")
        self.tol_entry.grid(row=0, column=5, padx=5, pady=5)

        # زر الحل
        solve_btn = tk.Button(input_frame, text="احسب وارسم (Solve & Plot)", command=self.solve, bg="#0066cc", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
        solve_btn.grid(row=0, column=6, padx=15, pady=5)

        # أزرار سريعة لأمثلة المحاضرة
        examples_frame = tk.Frame(input_frame, bg="#f4f6f9")
        examples_frame.grid(row=1, column=0, columnspan=7, pady=(8, 0), sticky="w")
        tk.Label(examples_frame, text="أمثلة جاهزة من المحاضرة:", font=("Arial", 9, "bold"), fg="#555", bg="#f4f6f9").pack(side="left", padx=(0, 10))
        
        examples = [
            ("مثال 1: x³ - 8x + 5", "x**3 - 8*x + 5", "0"),
            ("مثال 2: x⁴ - 11x + 8", "x**4 - 11*x + 8", "2"),
            ("مثال 3: e⁻ˣ - x", "exp(-x) - x", "0"),
            ("مثال 4: x³ - 2x² + 0.25x + 0.75", "x*3 - 2*x*2 + 0.25*x + 0.75", "-1")
        ]
        for label, eq, x0_val in examples:
            btn = tk.Button(examples_frame, text=label, font=("Arial", 8), bg="#e1e8ed",
                            command=lambda e=eq, x=x0_val: self.load_example(e, x))
            btn.pack(side="left", padx=4)

        # === إطار عرض معلومات التحليل (المشتقات وشرط التقارب والنتيجة) ===
        self.info_label = tk.Label(self.root, text="أدخل المعادلة واضغط على (احسب وارسم) لبدء الحل.", font=("Arial", 10, "bold"), bg="#e8f4fd", fg="#004085", pady=8, relief="groove")
        self.info_label.pack(fill="x", padx=15, pady=5)

        # === الإطار السفلي (مقسم إلى جدول على اليسار ورسم بياني على اليمين) ===
        bottom_frame = tk.Frame(self.root, bg="#f4f6f9")
        bottom_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # 1. جدول التكرارات (يسار)
        table_frame = tk.LabelFrame(bottom_frame, text=" جدول خطوات الحل (Iterations Table) ", font=("Arial", 10, "bold"), bg="#f4f6f9")
        table_frame.pack(side="left", fill="both", expand=False, padx=(0, 10))

        columns = ("i", "xi", "error")
        self.tree =ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        self.tree.heading("i", text="i")
        self.tree.heading("xi", text="x_i (Approximation)")
        self.tree.heading("error", text="|x_{i+1} - x_i|")

        self.tree.column("i", width=50, anchor="center")
        self.tree.column("xi", width=150, anchor="center")
        self.tree.column("error", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # 2. الرسم البياني (يمين)
        plot_frame = tk.LabelFrame(bottom_frame, text=" الرسم البياني للدالة (Function Plot) ", font=("Arial", 10, "bold"), bg="#f4f6f9")
        plot_frame.pack(side="right", fill="both", expand=True)

        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def load_example(self, eq, x0_val):
        self.eq_entry.delete(0, tk.END)
        self.eq_entry.insert(0, eq)
        self.x0_entry.delete(0, tk.END)
        self.x0_entry.insert(0, x0_val)
        self.solve()

    def solve(self):
        eq_str = self.eq_entry.get().strip()
        try:
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
        except ValueError:
            messagebox.showerror("خطأ في الإدخال", "يرجى إدخال أرقام صحيحة لنقطة البداية ونسبة الخطأ.")
            return

        # تحويل المعادلة النصية إلى دالة رياضية وحساب المشتقات
        try:
            f_expr = sp.sympify(eq_str)
            df_expr = sp.diff(f_expr, self.x_sym)
            d2f_expr = sp.diff(df_expr, self.x_sym)

            f_func = sp.lambdify(self.x_sym, f_expr, 'numpy')
            df_func = sp.lambdify(self.x_sym, df_expr, 'numpy')
            d2f_func = sp.lambdify(self.x_sym, d2f_expr, 'numpy')
        except Exception as e:
            messagebox.showerror("خطأ في صيغة المعادلة", f"تأكد من كتابة المعادلة بشكل صحيح (مثل x**3 - 8*x + 5):\n{e}")
            return

        # التحقق من شرط التقارب (Condition of Convergence) من المحاضرة
        try:
            f_x0 = float(f_func(x0))
            df_x0 = float(df_func(x0))
            d2f_x0 = float(d2f_func(x0))
            if df_x0 == 0:
                messagebox.showerror("خطأ رياضي", "المشتقة الأولى عند نقطة البداية تساوي صفر! اختر نقطة بداية أخرى.")
                return
            conv_val = abs((f_x0 * d2f_x0) / (df_x0 ** 2))
            conv_status = "متحقق (< 1) ✔️" if conv_val < 1 else "غير متحقق (>= 1) ⚠️"
        except Exception:
            conv_val = 0
            conv_status = "غير محدد"

        # مسح الجدول القديم
        for row in self.tree.get_children():
            self.tree.delete(row)

        # تنفيذ خوارزمية نيوتن رافسون
        xi = x0
        max_iter = 100
        self.tree.insert("", "end", values=(0, f"{xi:.6f}", "-"))
        
        root_found = xi
        for i in range(1, max_iter + 1):
            fx = float(f_func(xi))
            dfx = float(df_func(xi))
            
            if abs(dfx) < 1e-12:
                messagebox.showwarning("تنبيه", "المشتقة اقتربت من الصفر، توقف الحساب.")
                break

            x_next = xi - (fx / dfx)
            error = abs(x_next - xi)

            self.tree.insert("", "end", values=(i, f"{x_next:.6f}", f"{error:.6f}"))
            root_found = x_next

            if error < tol:
                break
            xi = x_next

        # تحديث شريط المعلومات العلوي
        info_text = (f"f'(x) = {df_expr}   |   شرط التقارب عند x0 = {conv_val:.4f} ({conv_status})   |   "
                     f"الجذر التقريبي (Root) = {root_found:.6f}")
        self.info_label.config(text=info_text)

        # رسم الدالة وتحديد الجذر
        self.plot_function(f_func, eq_str, x0, root_found)

    def plot_function(self, f_func, eq_str, x0, root_val):
        self.ax.clear()
        
        # تحديد مجال الرسم حول نقطة البداية والجذر
        center = (x0 + root_val) / 2
        span = max(abs(x0 - root_val) * 2.5, 4.0)
        x_vals = np.linspace(center - span, center + span, 500)
        
        try:
            y_vals = f_func(x_vals)
            # معالجة حالة الدوال الثابتة
            if np.ndim(y_vals) == 0:
                y_vals = np.full_like(x_vals, y_vals)
        except Exception:
            y_vals = [f_func(val) for val in x_vals]

        self.ax.plot(x_vals, y_vals, label=f"f(x) = {eq_str}", color="#0066cc", linewidth=2)
        self.ax.axhline(0, color="black", linewidth=1, linestyle="--") # محور X
        self.ax.axvline(0, color="gray", linewidth=0.8, linestyle=":")  # محور Y

        # تمييز نقطة الجذر على الرسم
        self.ax.scatter([root_val], [0], color="red", s=70, zorder=5, label=f"Root ≈ {root_val:.5f}")
        self.ax.axvline(root_val, color="red", linestyle=":", alpha=0.7)

        self.ax.set_title("Newton-Raphson Root Finding", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("x", fontsize=10)
        self.ax.set_ylabel("f(x)", fontsize=10)
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()