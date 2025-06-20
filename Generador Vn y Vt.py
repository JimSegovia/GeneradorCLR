import re
def procesar_gramatica(entrada, codigos_terminales):
    if codigos_terminales is None:
        raise ValueError("❌ Debes proporcionar un diccionario con los códigos de los terminales.")

    producciones = []
    no_terminales = set()
    terminales = set()

    # Unir líneas que continúan
    lineas = []
    buffer = ""
    for linea in entrada.strip().split('\n'):
        linea = linea.strip()
        if not linea:
            continue
        if '→' in linea or '->' in linea:
            if buffer:
                lineas.append(buffer)
            buffer = linea
        else:
            buffer += ' ' + linea
    if buffer:
        lineas.append(buffer)

    # Procesar producciones
    for linea in lineas:
        if '→' in linea:
            izquierda, derecha = map(str.strip, linea.split('→'))
        else:
            izquierda, derecha = map(str.strip, linea.split('->'))

        no_terminales.add(izquierda)

        alternativas = [alt.strip() for alt in derecha.split('|')]
        for alt in alternativas:
            alt = alt.strip()
            if alt == 'λ':
                simbolos = []  # Producción vacía
            else:
                simbolos = re.findall(r'<[^<>]+>|[^\s]+', alt)

            producciones.append((izquierda, simbolos))
            for simbolo in simbolos:
                if re.match(r'<[^<>]+>', simbolo):
                    no_terminales.add(simbolo)
                else:
                    terminales.add(simbolo)

    # Asignar códigos faltantes automáticamente
    codigo_actual = max(codigos_terminales.values(), default=599) + 1
    for t in sorted(terminales):
        if t not in codigos_terminales:
            codigos_terminales[t] = codigo_actual
            print(f"⚠️ Terminal '{t}' no estaba codificado. Asignado código {codigo_actual}.")
            codigo_actual += 1

    # Mostrar no terminales
    print("No terminales:")
    print('|'.join(sorted(no_terminales)))

    # Mostrar terminales codificados en formato '|'
    print("\nTerminales (formato codigo para copiar):")
    print('|'.join(str(codigos_terminales[t]) for t in sorted(terminales)))

    # Mostrar terminales en formato '|'
    print("\nTerminales:")
    print('|'.join(sorted(terminales)))

    # Mostrar producciones con códigos
    print("\nProducciones (con terminales codificados):")
    for izquierda, simbolos in producciones:
        reemplazada = []
        for s in simbolos:
            if s in codigos_terminales:
                reemplazada.append(str(codigos_terminales[s]))
            else:
                reemplazada.append(s)
        print(f"{izquierda}→{' '.join(reemplazada)}")


# INGRESAR AQUI SU GRAMATICA, SEPARADA POR ESPACIOS PARA CADA ELEMENTO
entrada = """
<S>→ initHabit { <Declaraciones> mainZoo <BloqueInstr> } finHabit

<Declaraciones> → <DeclVariable> <Declaraciones> | 
<Clase> <Declaraciones> | 
<FuncionesGlobales>  <Declaraciones> | λ

<DeclVariable> → <TipoPrimitivo> <DeclSimple> 
| TORT <TipoPrimitivo> <DeclInicializada> 
| id <DeclObj> 
| <AsignacionObj>
	| <AsignacionArreglo>
| <AsignacionElemArr>
| <AsignacionIdSimple> | <AsignacionIdConArray>
<DeclSimple>→  <ListaIds> ; | 
<DeclInicializada>  | 
<Arreglos> ;

<DeclInicializada> →  <Inicializar> ;
                  		 | <InicializarArreglos>  ;

 <DeclObj> → <ObjSimple> | <ObjArreglo> 

<ObjSimple>  → id <IniObjOpcional> ; 
<IniObjOpcional>   → = NUEVO id ( <Argumentos> )  |  λ

<ObjArreglo> → [ ] id <IniObjArregloOpcional> ;  
<IniObjArregloOpcional> → = NUEVO id [ <ExprAritmeticas> ]  | λ

<AsignacionObj>  → id = NUEVO id ( <Argumentos> ) ;  
<AsignacionArreglo>→ id = NUEVO id [ <ExprAritmeticas> ] ; 
<AsignacionIdSimple>→ id =  <Valor> ;
<AsignacionIdConArray>→ id [ <ExprAritmeticas> ] = <Valor> ; 
<AsignacionElemArr>→ id [ <ExprAritmeticas> ] = NUEVO id ( <Argumentos> ) ;

	<ObjDirectoParametro>→ NUEVO id ( <Argumentos> )

<ListaIds> → id <ListaIdsCont> 
<ListaIdsCont> → , <ListaIds> | λ

<Inicializar> → id = <Valor>  <MasDeclInicializadas>  
<MasDeclInicializadas> → , <Inicializar> | λ

<Arreglos> → id [ <ExprAritmeticas> ] <MasArreglos>
<MasArreglos> → , <Arreglos> | λ

<InicializarArreglos> → id [ ] => { <ListaValores> } <MasIniArreglos> 
<MasIniArreglos> → , <InicializarArreglos> |  λ

<ListaValores> → <ListaIds> | <ListaString> | <ListaNum> | <ListaBool> | <ListaChar>
<ListaString>→ lit_str  <MasString>
	<MasString>→ , <ListaString>  |  λ
<ListaNum>→ <Num> <MasNum>
	<MasNum>→ , <ListaNum>  |  λ
	<ListaBool>→ <ExpreBooleanos> <MasBool>
<ExpreBooleanos> → <Booleanos> | <ExpreLogica>
<MasBool>→ , <ListaBool>  |  λ
	<ListaChar>→ lit_char <MasChar>
	<MasChar>→ , <ListaChar>  |  λ
<ListaExpreArit>→ <ExpreArit> <MasExpreArit>
	<MasExpreArit>→ , <ListaExpreArit>  |  λ

<Argumentos>→ <Valor> <MasArgumentos> |  λ
<MasArgumentos>→ , <Argumentos> |  λ

<Valor> → <ExpreCompletas> | lit_str | lit_char  |  id [ <ExprAritmeticas> ]
<Num>→ lit_ent | lit_decimal
<Booleanos> → verdad | falso                                        
<TipoPrimitivo> → ent | ant | boul | stloro | char 

<Clase> → classHabit  id { <Miembros> }
<Miembros> → <Atributo> <Miembros> 
| <Metodo> <Miembros> 
| <Constructor> <Miembros> 
|  λ
<Constructor> → INICIAR id ( <Parametros> ) <BloqueInstr> 
<Atributo> → <Acceso>  <DeclVariable> 

<Acceso> → libre | encerrado | protect | λ 

<Metodo> → <Acceso> <Met> 
<Met> → <MetodoConRetorno> | <MetodoSinRetorno>
<MetodoConRetorno> → <TipoPrimitivo> <MetPrefijo> id ( <Parametros> )  { <ListaInstr>  devolver  <Valor> ; }
<MetodoSinRetorno> →  corpse <MetPrefijo> id ( <Parametros> ) <BloqueInstr> 
 
<MetPrefijo> → met-> | acced-> | modif-> 

<FuncionesGlobales> → compor <Func>
<Func> → <FuncConRetorno> | <FuncCorpse>
<FuncConRetorno> → <TipoPrimitivo> id ( <Parametros> ) { <ListaInstr> devolver <Valor> ; }
<FuncCorpse> → corpse id ( <Parametros> ) <BloqueInstr> 

<Parametros> → <VeriParametros>  |  λ 
<VeriParametros> → <TiposDeParametros> <ContParametros>
<ContParametros> → , <VeriParametros> | λ 
<TiposDeParametros> →<TipoPrimitivo> id <ConArray> 
| id <ConArray>  id
| <ObjDirectoParametro>
<ConArray> → [ ] |   λ

<BloqueInstr> → { <ListaInstr> }
<ListaInstr> → <Instruccion> <ListaInstr> | λ
<Instruccion> → <DeclVariable> | <Llamadas>| <Paso> | <Asignacion> | <ControlFlujo> | <Rugg> | <Reci> |  huir ;

<Asignacion> → <Variable> = <Valor>  ;
<Variable> → self .. id

<Paso> → id <MasMasMenosMenos> ;
<MasMasMenosMenos> → ++ | --


<Rugg> → rugg ( <ExpreParaRugg> ) ;
<Reci> → reci (  id ) ;
<ExpreParaRugg> → <Valor> <MasExpreParaRugg> 
<MasExpreParaRugg> → <<  <ExpreParaRugg>  | λ

<ExpreCompletas> → <Expre> | <Llamadas>
<Expre> → <ExprLogica> | <ExprAritmeticas> | <Booleanos>

<ExprAritmeticas> → <Termino> <ExprAritmeticas’>
<ExprAritmeticas’> → <OpeSumaResta> <Termino> <ExprAritmeticas’> | λ
<Termino>  → <Factor> <Termino’>
<Termino’> → <OpeMulDiv> <Factor> <Termino’> | λ
<Factor> → ( <ExprAritmeticas> ) | <Num> | id
<OpeSumaResta> → + | -
<OpeMulDiv>    → * | /

<ExprLogica> → <CondicionLogica>
<CondicionLogica> → <Condicion> | <Condicion> <OpeLogico> <CondicionLogica>

<Condicion> → ! <UnidadCondicional> | <UnidadCondicional>  
<UnidadCondicional> → <Comparacion> | ( <ExprLogica> )

<Comparacion>  → <Var1> <OpeRelacionalNum> <Var1>
                     | <Var1> <OpeIgualdad> <Var1>

<Var1> → <ExprAritmeticas>
<Var2> → <Var1> | lit_str | lit_char | <Booleanos>
<OpeRelacionalNum> →  > | < | >= | <= 
<OpeIgualdad> → == | !=
<OpeLogico>  →  Y¡ | O¡

<Llamadas> → id <FuncOMet>;
<FuncOMet> →  ( <Argumentos>) | . id ( <Argumentos>) 

<ControlFlujo> → <IfElse> |<While> | <DoWhile> | <For> | <Switch>  
<IfElse> →cama ( <Expre> ) <BloqueInstr> leon <IfElseAnidadas>
<IfElseAnidadas> → <IfElse> | <BloqueInstr> 
<While> → merodear ( <Expre> ) <BloqueInstr> 
<DoWhile> → me <BloqueInstr> merodear ( <Expre> ) ;
<For>→ rondar ( <DeclOAsignacion> ; <ExprLogica> ; <IncreDecre> ) <BloqueInstr> 
<Switch> → instinto ( id ) { <ListaReacciones> }
<ListaReacciones> → <ReaccionBloque> <ListaReacciones> 
                  | instintoFinal : <BloqueInstr> 
                  | λ
<ReaccionBloque> → reaccion <definicion> : <BloqueInstr>
                 | reaccion <definicion> : <BloqueInstr> huir ;
<BloqueInstrHuir> → <BloqueInstr> huir ;
<ListaReaccion> → <ReaccionBloque> <ListaReaccion> | λ
<definicion> →lit_ent | lit_char
<OpInstintoFinal> →instintoFinal : <BloqueInstr>  | λ

<DeclOAsignacion> → <TipoPrimitivo> <Inicializar> 
<IncreDecre> →  id <ExpreOIncreDecre> <MasIncreDecre> 
<ExpreOIncreDecre> → = <ExprAritmeticas> | <MasMasMenosMenos> 
<MasIncreDecre>  → <IncreDecre>  | λ
"""
# INGRESAR AQUI LOS TOKENS PARA SUS VALORES TERMINALES
codigos_terminales = {
    'initHabit': 400,
    'mainZoo': 401,
    'finHabit': 402,
    'classHabit': 403,
    'acced->': 404,
    'modif->': 405,
    'met->': 406,
    'libre': 407,
    'encerrado': 408,
    'protect': 409,
    'compor': 410,
    'ent': 411,
    'ant': 412,
    'boul': 413,
    'corpse': 414,
    'stloro': 415,
    'char': 416,
    'self': 417,
    'NUEVO': 418,
    'INICIAR': 419,
    'TORT': 420,
    'devolver': 421,
    'rugg': 422,
    'reci': 423,
    'cama': 424,
    'leon': 425,
    'merodear': 426,
    'rondar': 427,
    'me': 428,
    'instinto': 429,
    'instintoFinal': 430,
    'reaccion': 431,
    'huir': 432,
    'verdad': 433,
    'falso': 434,
    '==': 435,
    '!=': 436,
    '<': 437,
    '<=': 438,
    '>': 439,
    '>=': 440,
    'Y¡': 441,
    'O¡': 442,
    '!': 443,
    '+': 444,
    '-': 445,
    '*': 446,
    '/': 447,
    '++': 448,
    '--': 449,
    '(': 450,
    ')': 451,
    '{': 452,
    '}': 453,
    '[': 454,
    ']': 455,
    ';': 456,
    ':': 457,
    ',': 458,
    '.': 459,
    '..': 460,
    '<<': 461,
    'id': 500,
    'lit_str': 501,
    'lit_char': 502,
    'lit_ent': 503,
    'lit_decimal': 504,
    'comentario': 505,
    '=': 506,
    '=>': 507,
    'ERROR': 911,
    'EOF': 999,
}

procesar_gramatica(entrada, codigos_terminales)
