from collections import deque
from collections import OrderedDict
from pprint import pprint
import primerosysiguientes
from primerosysiguientes import production_list, nt_list as ntl, t_list as tl

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

from collections import defaultdict

def generar_tabla_ll1():
    tabla = defaultdict(dict)

    for i, prod in enumerate(production_list):
        cabeza, cuerpo = prod.split("→")
        cabeza = cabeza.strip()
        cuerpo_syms = cuerpo.strip().split()

        first = primerosysiguientes.compute_first_sequence(cuerpo_syms)

        for t in first - {LAMBDA}:
            tabla[cabeza][t] = i

        if LAMBDA in first:
            for f in primerosysiguientes.get_follow(cabeza):
                tabla[cabeza][f] = i

    return tabla


def exportar_tabla_ll1_cpp(tabla):
    print("\n// --- TABLA LL(1) en formato estilo C++ ---")
    print("TABLA::TABLA() {")

    for nt, fila in tabla.items():
        for term, prod_idx in fila.items():
            prod_rhs = production_list[prod_idx].split("→")[1].strip()
            cod_term = "36" if term == "$" else term
            simbolo_legible = codigos_equivalentes.get(term, term)
            print(f'    c(M["{nt}"]["{cod_term}"], "{prod_rhs}"); // Producción {prod_idx} por {simbolo_legible}')

    print("}")

import sys
def main():
    global production_list, ntl, nt_list, tl, t_list

    print("Ingresa los símbolos NO TERMINALES separados por |:")
    non_terminal_input = input().strip()
    non_terminal_symbols = non_terminal_input.split('|')

    primerosysiguientes.nt_list.clear()
    for nt in non_terminal_symbols:
        primerosysiguientes.nt_list[nt] = primerosysiguientes.NonTerminal(nt)

    print("\nIngresa los símbolos TERMINALES separados por |:")
    terminal_input = input().strip()
    terminal_symbols = terminal_input.split('|')

    primerosysiguientes.t_list.clear()
    for term in terminal_symbols:
        primerosysiguientes.t_list[term] = primerosysiguientes.Terminal(term)

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

    # Toda la salida en .txt
    with open("salida_clr1.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        sys.stdout = f  # Redirige toda la salida print al archivo
    # Aqui acaba
    production_list[:] = user_productions

    primerosysiguientes.main(production_list)

    production_list[:] = user_productions
    primerosysiguientes.main(production_list)

    print("\tFIRST AND FOLLOW OF NON-TERMINALS")
    for nt in ntl:
        primerosysiguientes.compute_first(nt)
        primerosysiguientes.compute_follow(nt)
        print(nt)
        print("\tFirst:\t", primerosysiguientes.get_first(nt))
        print("\tFollow:\t", primerosysiguientes.get_follow(nt), "\n")


    # LL(1) desde aquí
    tabla_ll1 = generar_tabla_ll1()
    exportar_tabla_ll1_cpp(tabla_ll1)
    return

if __name__ == "__main__":
    main()
