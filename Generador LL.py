from collections import defaultdict
import primerosysiguientes
from primerosysiguientes import production_list, nt_list as ntl, t_list as tl
import csv
import sys

LAMBDA = 'λ'

codigos_equivalentes = {
    'k': 300, 'f': 301, 'id': 100, 'C': 400, 'V': 401,
    'E': 402, 'R': 403, 'L': 404, 'P': 405, ',': 200,
    ';': 201, '=': 202, '*': 203, '+': 204, '(': 205,
    ')': 206, ':': 207
}

def codificar(simbolo):
    return str(codigos_equivalentes.get(simbolo, simbolo))

def decodificar(codigo):
    for k, v in codigos_equivalentes.items():
        if str(v) == str(codigo):
            return k
    return str(codigo)


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
            cod_term = "36" if term == "$" else codificar(term)
            simbolo_legible = codificar(term)
            print(f'    c(M["{nt}"]["{cod_term}"], "{prod_rhs}"); // Producción {prod_idx} por {simbolo_legible}')
    print("}")

def exportar_tabla_ll1_csv(tabla, filename):
    terminales = sorted(tl.keys()) + ["$"]
    terminales_legibles = [decodificar(t) if t != "$" else "$" for t in terminales]

    with open(filename, mode="w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["NT \\ T"] + terminales_legibles
        writer.writerow(header)

        for nt in ntl:
            fila = [nt]
            for t in terminales:
                prod_idx = tabla.get(nt, {}).get(t, "")
                if prod_idx != "":
                    prod_rhs = production_list[prod_idx].split("→")[1].strip()
                    cuerpo_legible = " ".join([decodificar(tok) for tok in prod_rhs.split()])
                    fila.append(cuerpo_legible)
                else:
                    fila.append("")
            writer.writerow(fila)

def exportar_first_follow_csv(filename):
    with open(filename, mode="w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["No Terminal", "First", "Follow"])

        for nt in ntl:
            primerosysiguientes.compute_first(nt)
            primerosysiguientes.compute_follow(nt)
            first_nombres = [decodificar(s) for s in primerosysiguientes.get_first(nt)]
            follow_nombres = [decodificar(s) for s in primerosysiguientes.get_follow(nt)]
            writer.writerow([nt, ", ".join(first_nombres), ", ".join(follow_nombres)])

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
        pass

    if not user_productions:
        print("No se ingresaron producciones. Finalizando.")
        return

    production_list[:] = user_productions
    primerosysiguientes.main(production_list)

    # Guardar todo en salida.txt
    with open("salida_clr1.txt", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        sys.stdout = f

        print("\tFIRST AND FOLLOW OF NON-TERMINALS")
        for nt in ntl:
            primerosysiguientes.compute_first(nt)
            primerosysiguientes.compute_follow(nt)
            print(nt)
            print("\tFirst:\t", [codificar(s) for s in primerosysiguientes.get_first(nt)])
            print("\tFollow:\t", [codificar(s) for s in primerosysiguientes.get_follow(nt)], "\n")

        tabla_ll1 = generar_tabla_ll1()
        exportar_tabla_ll1_cpp(tabla_ll1)

        sys.stdout = original_stdout

    # Exportar CSVs
    tabla_ll1 = generar_tabla_ll1()
    exportar_tabla_ll1_csv(tabla_ll1, "tabla_ll1.csv")
    exportar_first_follow_csv("primeros_siguientes.csv")

if __name__ == "__main__":
    main()
