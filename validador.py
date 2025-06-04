# augusto TSS
import sys
import re

# -----------------------------
# TOKEN TYPES
# -----------------------------
TOKENS = {
    'ABREPAREN': r'\(|\(',
    'FECHAPAREN': r'\)|\)',
    'OPUNARIO': r'\\neg',
    'OPBIN': r'\\wedge|\\vee|\\rightarrow|\\leftrightarrow',
    'CONST': r'true|false',
    'PROP': r'[0-9][0-9a-z]*'
}

# -----------------------------
# TOKENIZER (FSM SIMULATION)
# -----------------------------
def tokenize(expr):
    tokens = []
    while expr:
        expr = expr.lstrip()
        match = None
        for token_type, regex in TOKENS.items():
            pattern = re.compile(regex)
            match = pattern.match(expr)
            if match:
                tokens.append((token_type, match.group()))
                expr = expr[match.end():]
                break
        if not match:
            return None  # Token inválido
    return tokens

# -----------------------------
# PARSER LL(1)
# -----------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def accept(self, token_type):
        if self.current()[0] == token_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        if not self.formula():
            return False
        return self.pos == len(self.tokens)

    def formula(self):
        tok, val = self.current()
        if tok == 'CONST':
            self.accept('CONST')
            return True
        elif tok == 'PROP':
            self.accept('PROP')
            return True
        elif tok == 'ABREPAREN':
            self.accept('ABREPAREN')
            if self.accept('OPUNARIO'):
                if self.formula() and self.accept('FECHAPAREN'):
                    return True
            elif self.accept('OPBIN'):
                if self.formula() and self.formula() and self.accept('FECHAPAREN'):
                    return True
        return False

# -----------------------------
# MAIN
# -----------------------------
def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.txt>")
        return

    with open(sys.argv[1], 'r') as f:
        lines = f.read().strip().split('\n')

    try:
        n = int(lines[0])
        exprs = lines[1:n+1]
    except:
        print("Erro de leitura do arquivo.")
        return

    for expr in exprs:
        tokens = tokenize(expr)
        if not tokens:
            print("invalida")
            continue
        parser = Parser(tokens)
        print("valida" if parser.parse() else "invalida")

if __name__ == "__main__":
    main()

