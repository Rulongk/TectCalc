import ast
import operator
import tkinter as tk

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
    root = tk.Tk()
    root.title("Калькулятор")
    root.resizable(False, False)
    var = tk.StringVar()
    tk.Entry(root, textvariable=var, font=("Arial", 20), justify="right",
             state="readonly").grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

    def press(ch):
        if var.get() == "Ошибка":
            var.set("")
        if ch == "C":
            var.set("")
        elif ch == "=":
            try:
                var.set(str(evaluate(var.get())))
            except Exception:
                var.set("Ошибка")
        else:
            var.set(var.get() + ch)

    keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "-",
            "0", ".", "=", "+", "C"]
    for i, k in enumerate(keys):
        r, c = divmod(i, 4)
        span = 4 if k == "C" else 1
        tk.Button(root, text=k, font=("Arial", 16), width=4 if span == 1 else 18,
                  command=lambda k=k: press(k)).grid(row=r + 1, column=c, columnspan=span, padx=2, pady=2)
    root.mainloop()


if __name__ == "__main__":
    main()
