import ast
import operator
import customtkinter as ctk

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def evaluate(expr):
    """Безопасно вычисляет арифметическое выражение."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.operand))
        raise ValueError("bad expression")

    result = ev(ast.parse(expr.replace("×", "*").replace("÷", "/"), mode="eval"))
    return int(result) if float(result).is_integer() else round(result, 10)


def main():
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Калькулятор")
    root.resizable(False, False)
    var = ctk.StringVar()
    ctk.CTkLabel(root, textvariable=var, anchor="e", height=70, corner_radius=10,
                 fg_color="#1e1e1e", font=("Segoe UI", 32)).grid(
        row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=(10, 5))

    def press(ch):
        if var.get() == "Ошибка":
            var.set("")
        if ch == "C":
            var.set("")
        elif ch == "<":
            var.set(var.get()[:-1])
        elif ch == "=":
            if var.get():
                try:
                    var.set(str(evaluate(var.get())))
                except Exception:
                    var.set("Ошибка")
        else:
            var.set(var.get() + ch)

    def on_key(e):
        kp = {"KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "×",
              "KP_Divide": "÷", "KP_Decimal": "."}
        if e.keysym.startswith("KP_") and e.keysym[3:].isdigit():
            ch = e.keysym[3:]
        else:
            ch = kp.get(e.keysym) or {"*": "×", "/": "÷", ",": "."}.get(e.char, e.char)
        if ch and ch in "0123456789.+-×÷":
            press(ch)
        elif e.keysym in ("Return", "KP_Enter"):
            press("=")
        elif e.keysym == "BackSpace":
            press("<")
        elif e.keysym == "Escape":
            press("C")

    root.bind("<Key>", on_key)

    keys = ["C", "<", "÷", "×", "7", "8", "9", "-", "4", "5", "6", "+",
            "1", "2", "3", "=", "0", "."]
    for i, k in enumerate(keys):
        r, c = divmod(i, 4)
        span = 2 if k == "0" else 1
        if k == ".":
            c = 2
        if k == "=":
            c, r, span = 3, 3, 1
        color = ("#ff9f0a" if k in "÷×-+=" else "#5a5a5a" if k in "C<" else "#333333")
        ctk.CTkButton(root, text=k, width=70 * span + 10 * (span - 1), height=60, corner_radius=12,
                      font=("Segoe UI", 22), fg_color=color, hover_color="#777777",
                      command=lambda k=k: press(k)).grid(
            row=r + 1, column=c, columnspan=span, padx=5, pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()
