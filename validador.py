# augusto TSS
import re

TOKENS = {
    '(': 'ABREPAREN',
    ')': 'FECHAPAREN',
    r'\neg': 'OP_UNARIO',
    r'\wedge': 'OP_BINARIO',
    r'\vee': 'OP_BINARIO',
    r'\rightarrow': 'OP_BINARIO',
    r'\leftrightarrow': 'OP_BINARIO',
    'true': 'CONSTANTE',
    'false': 'CONSTANTE'
}

PROP_REGEX = re.compile(r'[0-9][0-9a-z]*$')

def lexer(expr):
    tokens = []
    expr = expr.strip()
    i = 0
    while i < len(expr):
        match = None
        for k in sorted(TOKENS, key=len, reverse=True):
            if expr.startswith(k, i):
                tokens.append((TOKENS[k], k))
                i += len(k)
                match = True
                break
        if not match:
            if expr[i] == ' ':
                i += 1
                continue
            m = re.match(r'[0-9][0-9a-z]*', expr[i:])
            if m:
                prop = m.group(0)
                tokens.append(('PROPOSICAO', prop))
                i += len(prop)
            else:
                return None  # erro léxico
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def consumir(self, tipo_esperado):
        if self.atual()[0] == tipo_esperado:
            self.pos += 1
            return True
        return False

    def parse(self):
        if not self.FORMULA():
            return False
        return self.pos == len(self.tokens)

    def FORMULA(self):
        t = self.atual()[0]
        if t == 'CONSTANTE':
            return self.consumir('CONSTANTE')
        elif t == 'PROPOSICAO':
            return self.consumir('PROPOSICAO')
        elif t == 'ABREPAREN':
            self.consumir('ABREPAREN')
            t2 = self.atual()[0]
            if t2 == 'OP_UNARIO':
                self.consumir('OP_UNARIO')
                if not self.FORMULA():
                    return False
                return self.consumir('FECHAPAREN')
            elif t2 == 'OP_BINARIO':
                self.consumir('OP_BINARIO')
                if not self.FORMULA():
                    return False
                if not self.FORMULA():
                    return False
                return self.consumir('FECHAPAREN')
        return False
