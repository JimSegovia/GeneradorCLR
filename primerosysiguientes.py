from re import *  # Expresiones regulares



# ------------------------------------------------------------------

class Terminal:  # Representa a un simbolo terminal

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


# ------------------------------------------------------------------

class NonTerminal:  # Representa a un simbolo no terminal

    def __init__(self, symbol):
        self.symbol = symbol
        self.first = set()
        self.follow = set()

    def __str__(self):
        return self.symbol

    def add_first(self, symbols): self.first |= set(symbols)  # conjunto first del no terminal

    def add_follow(self, symbols): self.follow |= set(symbols)  # conjunto follow del no terminal

from collections import OrderedDict  # Diccionario ordenado para mantener el orden de inserción

LAMBDA = 'λ'

t_list = OrderedDict()

nt_list = OrderedDict()

production_list = []  # Lista de producciones

# ------------------------------------------------------------------

def compute_first(symbol=None):
    global production_list, nt_list, t_list

    changed = True
    while changed:
        changed = False
        for prod in production_list:
            head, body = prod.split('→')
            head = head.strip()
            body_syms = body.strip().split()

            if body == '':
                body_syms = [LAMBDA]

            all_nullable = True
            for sym in body_syms:
                # Terminal o símbolo especial
                if sym in t_list or sym == '$':
                    if sym not in nt_list[head].first:
                        nt_list[head].first.add(sym)
                        changed = True
                    all_nullable = False
                    break
                elif sym == LAMBDA:
                    if LAMBDA not in nt_list[head].first:
                        nt_list[head].first.add(LAMBDA)
                        changed = True
                    all_nullable = False
                    break
                else:
                    before = len(nt_list[head].first)
                    nt_list[head].first |= (nt_list[sym].first - {LAMBDA})
                    if len(nt_list[head].first) > before:
                        changed = True

                    if LAMBDA in nt_list[sym].first:
                        continue
                    else:
                        all_nullable = False
                        break

            if all_nullable:
                if LAMBDA not in nt_list[head].first:
                    nt_list[head].first.add(LAMBDA)
                    changed = True

    # Si se llamó con un símbolo específico (modo wrapper)
    if symbol:
        if symbol in t_list or symbol == '$':
            return {symbol}
        elif symbol in nt_list:
            return nt_list[symbol].first
        else:
            return set()


def compute_follow(symbol):
	global production_list, nt_list, t_list

	# Si es el símbolo inicial, se le agrega $
	if symbol == list(nt_list.keys())[0]:
		nt_list[symbol].add_follow({'$'})

	for prod in production_list:
		head, body = prod.split('→')
		head = head.strip()
		body_tokens = body.strip().split()

		for i, B in enumerate(body_tokens):
			if B != symbol:
				continue

			# Caso A → α B β
			if i < len(body_tokens) - 1:
				beta = body_tokens[i + 1:]
				first_beta = compute_first_sequence(beta)
				nt_list[B].add_follow(first_beta - {LAMBDA})

				if LAMBDA in first_beta:
					nt_list[B].add_follow(nt_list[head].follow)

			# Caso A → α B  (B al final)
			elif i == len(body_tokens) - 1 and B != head:
				nt_list[B].add_follow(nt_list[head].follow)

# ------------------------------------------------------------------

def get_first(symbol):  # wrapper method for compute_first

    return compute_first(symbol)


# ------------------------------------------------------------------

def main(pl=None):
    global production_list

    if pl:
        production_list[:] = pl

        for prod in production_list:
            head, body = prod.split('→')
            head = head.strip()
            body_tokens = body.strip().split()

            if head not in nt_list:
                nt_list[head] = NonTerminal(head)

            for sym in body_tokens:
                if sym != LAMBDA and sym not in nt_list and sym not in t_list:
                    print(f"[Advertencia] símbolo '{sym}' no fue declarado como terminal ni no terminal.")

        return pl
    else:
        print("Debe pasarse una lista de producciones como argumento.")



# ------------------------------------------------------------------

def get_follow(symbol):
    global nt_list, t_list

    if symbol in t_list.keys():
        return None

    return nt_list[symbol].follow


# ------------------------------------------------------------------
def compute_first_sequence(symbols):
    result = set()
    for sym in symbols:
        first = get_first(sym)
        result.update(first - {'λ'})
        if 'λ' not in first:
            break
    else:
        result.add('λ')
    return result


# ------------------------------------------------------------------
def main(pl=None):
    global production_list

    if pl:
        production_list[:] = pl

        for prod in production_list:
            head, body = prod.split('→')
            head = head.strip()
            body_tokens = body.strip().split()

            # Asegura que el símbolo de la cabeza es un no terminal
            if head not in nt_list:
                nt_list[head] = NonTerminal(head)

            for sym in body_tokens:
                if sym == LAMBDA:
                    continue

                if sym not in nt_list and sym not in t_list:
                    # Si el símbolo aparece por primera vez
                    # Lo consideramos terminal si no ha sido cabeza de producción
                    is_non_terminal = any(sym == p.split('→')[0].strip() for p in production_list)
                    if is_non_terminal:
                        nt_list[sym] = NonTerminal(sym)
                    else:
                        t_list[sym] = Terminal(sym)
                # Si el símbolo ya existe como terminal pero aún es None
                elif sym in t_list and t_list[sym] is None:
                    t_list[sym] = Terminal(sym)
                # Si el símbolo ya existe como no terminal pero aún es None
                elif sym in nt_list and nt_list[sym] is None:
                    nt_list[sym] = NonTerminal(sym)

        return pl
    else:
        print("Debe pasarse una lista de producciones como argumento.")

# ------------------------------------------------------------------

if __name__ == '__main__':
    from pprint import pprint
    main()

