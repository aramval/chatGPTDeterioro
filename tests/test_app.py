import ast
import random


def load_deteriorar():
    """Load deteriorar function from app.py without executing other code."""
    with open('app.py', 'r', encoding='utf-8') as f:
        source = f.read()
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'deteriorar':
            func_module = ast.Module(body=[node], type_ignores=[])
            ns = {'random': random}
            exec(compile(func_module, 'app.py', 'exec'), ns)
            return ns['deteriorar']
    raise RuntimeError('deteriorar not found')


deteriorar = load_deteriorar()


def test_nivel_cero_no_cambia():
    random.seed(0)
    assert deteriorar("hola mundo", 0) == "hola mundo"


def test_nivel_uno_cambia_todo():
    random.seed(0)
    resultado = deteriorar("hola mundo", 1)
    palabras = resultado.split()
    assert len(palabras) == 2
    assert palabras[0][:-1][::-1] == "hola"
    assert palabras[1][:-1][::-1] == "mundo"
    assert palabras[0][-1] in "@#*~"
    assert palabras[1][-1] in "@#*~"


def test_probabilidad_intermedia():
    random.seed(1)
    resultado = deteriorar("hola mundo", 0.5)
    assert resultado == "aloh@ odnum~"