import streamlit as st
import ast
import operator as op

# ------------ Safe eval for arithmetic expressions ------------
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_eval(expr: str):
    try:
        node = ast.parse(expr, mode='eval')
        return _eval_node(node.body)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def _eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    if hasattr(ast, "Constant") and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Only numeric constants are allowed.")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type} not allowed")
        operand = _eval_node(node.operand)
        return ALLOWED_OPERATORS[op_type](operand)
    raise ValueError("Unsupported expression")

# ------------ Streamlit App ------------
st.set_page_config(page_title="آلة حاسبة", layout="centered")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("## 🧮 آلة حاسبة متقدمة ")

expr = st.text_input("اكتب التعبير الحسابي:", placeholder="مثال: (12 + 5) * 3 - 4/2")
if st.button("احسب"):
    try:
        result = safe_eval(expr)
        st.session_state.history.insert(0, (expr, result))
        st.success(f"النتيجة: {result}")
    except Exception as e:
        st.error(f"خطأ: {e}")

st.markdown("### التاريخ (أحدث أولاً)")
if st.session_state.history:
    for i, (e, r) in enumerate(st.session_state.history):
        st.write(f"{i+1}. `{e}` = **{r}**")
else:
    st.info("لا توجد عمليات حتى الآن. اكتب تعبيرًا واضغط احسب.")
