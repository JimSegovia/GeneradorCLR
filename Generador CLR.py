from collections import deque
from collections import OrderedDict
from pprint import pprint
import Primeros_y_Siguientes
from Primeros_y_Siguientes import production_list, nt_list as ntl, t_list as tl

LAMBDA = 'λ'

codigos_equivalentes = {
'400': 'initHabit',
'401': 'mainZoo',
'402': 'finHabit',
'403': 'classHabit',
'404': 'acced->',
'405': 'modif->',
'406': 'met->',
'407': 'libre',
'408': 'encerrado',
'409': 'protect',
'410': 'compor',
'411': 'ent',
'412': 'ant',
'413': 'boul',
'414': 'corpse',
'415': 'stloro',
'416': 'char',
'417': 'self',
'418': 'NUEVO',
'419': 'INICIAR',
'420': 'TORT',
'421': 'devolver',
'422': 'rugg',
'423': 'reci',
'424': 'cama',
'425': 'leon',
'426': 'merodear',
'427': 'rondar',
'428': 'me',
'429': 'instinto',
'430': 'instintoFinal',
'431': 'reaccion',
'432': 'huir',
'433': 'verdad',
'434': 'falso',
'435': '==',
'436': '!=',
'437': '<',
'438': '<=',
'439': '>',
'440': '>=',
'441': 'Y¡',
'442': 'O¡',
'443': '!',
'444': '+',
'445': '-',
'446': '*',
'447': '/',
'448': '++',
'449': '--',
'450': '(',
'451': ')',
'452': '{',
'453': '}',
'454': '[',
'455': ']',
'456': ';',
'457': ':',
'458': ',',
'459': '.',
'460': '..',
'461': '<<',
'500': 'id',
'501': 'lit_str',
'502': 'lit_char',
'503': 'lit_ent',
'504': 'lit_decimal',
'505': 'comentario',
'506': '=',
'507': '=>',
'911': 'ERROR',
'999': 'EOF'
#eliminar si es necesario
}


class State:
    _id = 0

    def __init__(self, closure):
        self.closure = closure
        self.no = State._id
        State._id += 1


class Item(str):
    def __new__(cls, item, lookahead=list()):
        if '.' not in item:
            raise ValueError(f"Item mal formado, sin '.': {item}")
        self = str.__new__(cls, item)
        self.lookahead = lookahead
        return self

    def __str__(self):
        return super(Item, self).__str__() + ", " + '|'.join(self.lookahead)



def closure(items):
    def exists(newitem, items):
        for i in items:
            if i == newitem and sorted(set(i.lookahead)) == sorted(set(newitem.lookahead)):
                return True
        return False

    global production_list

    while True:
        flag = 0
        for i in items:
            head, body = i.split('→')
            symbols = split_body_with_dot(body.strip())

            if '.' not in symbols or symbols.index('.') == len(symbols) - 1:
                continue

            dot_pos = symbols.index('.')
            B = symbols[dot_pos + 1]  # símbolo después del punto

            if B not in nt_list:
                continue

            beta = symbols[dot_pos + 2:]  # lo que sigue después de B
            lookaheads = set()

            for la in i.lookahead:
                sequence = beta + [la]
                result = firstfollow.compute_first_sequence(sequence)
                lookaheads.update(result)

            for prod in production_list:
                lhs, rhs = prod.split('→')
                if lhs.strip() != B:
                    continue

                rhs_symbols = rhs.strip().split()
                new_body = '. ' + ' '.join(rhs_symbols)
                new_item = Item(f"{B}→{new_body}", lookaheads)

                if not exists(new_item, items):
                    items.append(new_item)
                    flag = 1

        if not flag:
            break

    return items

def split_body_with_dot(body):
    result = []
    i = 0
    while i < len(body):
        if body[i] == '.':
            result.append('.')
            i += 1
        elif body[i] == ' ':
            i += 1  # ignora espacios extra
        else:
            sym = ''
            while i < len(body) and body[i] not in ['.', ' ']:
                sym += body[i]
                i += 1
            result.append(sym)
    return result


def pretty_print_items(items, codigos_equivalentes={}):
    for item in items:
        # Remplaza '.' por '●' solo para mostrar
        item_str = item.replace('.', '●').replace('→', '->')

        # Reemplazar símbolos codificados por su forma legible
        if codigos_equivalentes:
            for codigo, texto in codigos_equivalentes.items():
                item_str = item_str.replace(codigo, texto)

        for lookahead in item.lookahead:
            lookahead_str = codigos_equivalentes.get(lookahead, lookahead) if codigos_equivalentes else lookahead
            print(f"[ {item_str}, {lookahead_str} ]")


def goto(items, symbol):
    initial = []

    for i in items:
        head, body = i.split('→')
        symbols = split_body_with_dot(body.strip())

        if '.' not in symbols:
            continue

        dot_pos = symbols.index('.')

        # Verificamos si hay símbolo después del punto
        if dot_pos + 1 < len(symbols) and symbols[dot_pos + 1] == symbol:
            # Mover el punto a la derecha del símbolo actual
            new_symbols = symbols[:dot_pos] + [symbol, '.'] + symbols[dot_pos + 2:]
            new_body = ' '.join(new_symbols)
            initial.append(Item(f"{head}→{new_body}", i.lookahead))

    return closure(initial)



def calc_states():
    def contains(states, t):

        for s in states:
            if len(s) != len(t): continue

            if sorted(s) == sorted(t):
                for i in range(len(s)):
                    if s[i].lookahead != t[i].lookahead: break
                else:
                    return True

        return False

    global production_list, nt_list, t_list

    head, body = production_list[0].split('→')

    states = [closure([Item(head + '→.' + body, ['$'])])]

    while True:
        flag = 0
        for s in states:

            for e in nt_list + t_list:

                t = goto(s, e)
                if t == [] or contains(states, t): continue

                states.append(t)
                flag = 1

        if not flag: break

    return states


def make_table(states):
    global nt_list, t_list

    def getstateno(t):
        for s in states:
            if len(s.closure) != len(t):
                continue
            if sorted(s.closure) == sorted(t):
                for i in range(len(s.closure)):
                    if s.closure[i].lookahead != t[i].lookahead:
                        break
                else:
                    return s.no
        return -1

    def getprodno(item):
        head, body = item.split('→')
        body_without_dot = body.replace('.', '').strip()
        clean = head.strip() + '→' + body_without_dot
        for i, prod in enumerate(production_list):
            if prod.strip() == clean:
                return i
        return -1

    SLR_Table = OrderedDict()

    for i in range(len(states)):
        states[i] = State(states[i])  # Asigna números de estado

    for s in states:
        SLR_Table[s.no] = OrderedDict()

        for item in s.closure:
            head, body = item.split('→')
            body_symbols = split_body_with_dot(body.strip())


            if body_symbols == ['.']:  # Producción completamente reducida
                for term in item.lookahead:
                    if term not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][term] = {'r' + str(getprodno(item))}
                    else:
                        SLR_Table[s.no][term] |= {'r' + str(getprodno(item))}
                continue

            try:
                dot_pos = body_symbols.index('.')
            except ValueError:
                raise ValueError(f"Producción inválida sin punto: {item}")

            if dot_pos == len(body_symbols) - 1:
                # Punto al final (producción lista para reducir)
                if getprodno(item) == 0:
                    SLR_Table[s.no]['$'] = 'Aceptar'
                else:
                    for term in item.lookahead:
                        if term not in SLR_Table[s.no].keys():
                            SLR_Table[s.no][term] = {'r' + str(getprodno(item))}
                        else:
                            SLR_Table[s.no][term] |= {'r' + str(getprodno(item))}
                continue

            # Punto no al final: shift o goto
            nextsym = body_symbols[dot_pos + 1]
            t = goto(s.closure, nextsym)
            if t != []:
                if nextsym in t_list:
                    if nextsym not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][nextsym] = {'d' + str(getstateno(t))}
                    else:
                        SLR_Table[s.no][nextsym] |= {'d' + str(getstateno(t))}
                else:
                    SLR_Table[s.no][nextsym] = str(getstateno(t))

    return SLR_Table

def augment_grammar():
    for i in range(ord('Z'), ord('A') - 1, -1):
        new_start = chr(i)
        if new_start not in ntl:
            start_prod = production_list[0]
            production_list.insert(0, new_start + '→' + start_prod.split('→')[0])
            ntl[new_start] = firstfollow.NonTerminal(new_start)  # <- Añadido
            return


def main():
    global production_list, ntl, nt_list, tl, t_list

    print("Ingresa los símbolos NO TERMINALES separados por |:")
    non_terminal_input = input().strip()
    non_terminal_symbols = non_terminal_input.split('|')

    firstfollow.nt_list.clear()
    for nt in non_terminal_symbols:
        firstfollow.nt_list[nt] = firstfollow.NonTerminal(nt)

    print("\nIngresa los símbolos TERMINALES separados por |:")
    terminal_input = input().strip()
    terminal_symbols = terminal_input.split('|')

    firstfollow.t_list.clear()
    for term in terminal_symbols:
        firstfollow.t_list[term] = firstfollow.Terminal(term)

    print("\nPega tus producciones (una por línea).")
    print("Cuando termines, presiona Enter en una línea vacía:")

    user_productions = []
    try:
        while True:
            line = input()
            if line.strip() == "":
                break
            user_productions.append(line.strip())
    except EOFError:
        pass  # Por si usas redirección o termina entrada con Ctrl+D (Linux/Mac)

    if not user_productions:
        print("No se ingresaron producciones. Finalizando.")
        return

    production_list[:] = user_productions

    firstfollow.main(production_list)

    print("\tFIRST AND FOLLOW OF NON-TERMINALS")
    for nt in ntl:
        firstfollow.compute_first(nt)
        firstfollow.compute_follow(nt)
        first = sorted(firstfollow.get_first(nt))
        follow = sorted(firstfollow.get_follow(nt))
        print(nt)
        print("\tFirst:\t", firstfollow.get_first(nt))
        print("\tFollow:\t", firstfollow.get_follow(nt), "\n")

    augment_grammar()

    nt_list = list(ntl.keys())
    t_list = list(tl.keys()) + ['$']

    print(nt_list)
    print(t_list, "\n")

    j = calc_states()

    ctr = 0
    for idx, state in enumerate(j):
        print(f"Item{idx}{{")  # ACA SER CAMBIA EL ITEM POR I SI QUIERES
        pretty_print_items(state, codigos_equivalentes)
        print("}\n")

    table = make_table(j)

    print("\n\tCLR(1) TABLE\n")

    sr, rr = 0, 0

    for i, fila in table.items():
        print(i, "\t", fila)
        shift_count, reduce_count = 0, 0

        for simbolo, acciones in fila.items():
            if acciones == 'Aceptar':
                continue
            if isinstance(acciones, set) and len(acciones) > 1:
                acciones_list = list(acciones)

                tipos = {'shift': 0, 'reduce': 0}
                for accion in acciones_list:
                    if accion.startswith('d'):
                        tipos['shift'] += 1
                    elif accion.startswith('r'):
                        tipos['reduce'] += 1

                # Mostrar nombre del símbolo si existe en el diccionario
                simbolo_legible = codigos_equivalentes.get(simbolo, simbolo)

                if tipos['shift'] > 0 and tipos['reduce'] > 0:
                    sr += 1
                    print(f"⚠️ SR conflict en estado {i}, símbolo '{simbolo_legible}' => acciones: {acciones_list}")
                elif tipos['reduce'] > 1:
                    rr += 1
                    print(f"⚠️ RR conflict en estado {i}, símbolo '{simbolo_legible}' => acciones: {acciones_list}")

    print("\n", sr, "s/r conflicts |", rr, "r/r conflicts")
    #export_table_as_java_format(table)
    export_table_as_csv_format(table)
    return

def export_table_as_java_format(table):
    print("\n// --- TABLA CLR(1) en formato estilo Java ---\n")
    print("Map<Integer, Map<String, String>> tabla = new HashMap<>();\n")

    for state_no, transitions in table.items():
        print(f"Map<String, String> fila{state_no} = new HashMap<>();")

        for symbol, action in transitions.items():
            if isinstance(action, set):
                action_str = list(action)[0]  # Tomamos uno (en caso de conflicto)
            else:
                action_str = action

            symbol_key = "36" if symbol == "$" else symbol
            lexema = codigos_equivalentes.get(symbol, symbol)

            # Determinar tipo de acción y construir comentario
            if action_str == "Aceptar":
                comentario = "// Aceptar entrada"
            elif action_str.startswith("d"):
                comentario = f"// Desplazar a estado {action_str[1:]} por símbolo {lexema}"
            elif action_str.startswith("r"):
                prod_num = int(action_str[1:])
                if 0 <= prod_num < len(production_list):
                    comentario = f"// Reducir con producción {prod_num} por símbolo {lexema}  "
                # : {production_list[prod_num]}
                else:
                    comentario = f"// Reducir con producción {prod_num} por símbolo {lexema}"
            else:
                comentario = f"// Ir a estado {action_str} por símbolo {lexema}"

            print(f'fila{state_no}.put("{symbol_key}", "{action_str}"); {comentario}')

        print(f"tabla.put({state_no}, fila{state_no});\n")

def export_table_as_csv_format(table):
    print("estado,símbolo,acción")  # Encabezado CSV
    for estado, fila in table.items():
        for simbolo, accion in fila.items():
            # Buscar si el símbolo tiene código equivalente
            simbolo_codificado = simbolo
            for cod, nombre in codigos_equivalentes.items():
                if nombre == simbolo:
                    simbolo_codificado = cod
                    break

            # Imprimir cada acción, incluso si hay múltiples (conflictos)
            if isinstance(accion, set):
                for a in accion:
                    print(f"{estado},{simbolo_codificado},{a}")
            else:
                print(f"{estado},{simbolo_codificado},{accion}")

if __name__ == "__main__":
    main()
