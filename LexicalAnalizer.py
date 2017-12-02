#!/usr/bin/env python

import re
import operator
import collections

print "Hello!"

shift = 0
words = []
dic = {}
errors = {}
tokens = {}
word = ""

errors["001"] = ["Palabra no reconocida"]
errors["002"] = ["Fin de comentario no encontrado"]

separators = [" ", ";", ">", "<", "=", "(", ")", "[", "]", "{", "}", "+", "-", "*", "/", "%", "\"", "\'"]

tokens["int"] = ["TD_INT"]
tokens["float"] = ["TD_FLOAT"]
tokens["double"] = ["TD_DBL"]
tokens["bool"] = ["TD_BOOL"]
tokens["char"] = ["TD_CHAR"]
tokens["string"] = ["TD_STR"]
tokens["void"] = ["TD_VOID"]
tokens["("] = ["PAR_O"]
tokens[")"] = ["PAR_C"]
tokens["{"] = ["LLA_O"]
tokens["}"] = ["LLA_C"]
tokens["["] = ["COR_O"]
tokens["]"] = ["COR_C"]
tokens["+"] = ["OP_SUM"]
tokens["*"] = ["OP_MULT"]
tokens["-"] = ["OP_SUBS"]
tokens["/"] = ["OP_DIV"]
tokens["="] = ["OP_ASSIG"]
tokens["<"] = ["OP_LESS"]
tokens[">"] = ["OP_MORE"]
tokens["&"] = ["OP_AND"]
tokens["|"] = ["OP_OR"]
tokens["^"] = ["OP_XOR"]
tokens["%"] = ["OP_PCNT"]
tokens["!"] = ["OP_NEG"]
tokens["\'"] = ["COMILLA_S"]
tokens["\""] = ["COMILLA_D"]
tokens[","] = ["COMA"]
tokens[";"] = ["SCOLON"]
tokens["."] = ["POINT"]
tokens[":"] = ["TWO_PNT"]
tokens["if"] = ["PR_IF"]
tokens["else"] = ["PR_ELSE"]
tokens["for"] = ["PR_FOR"]
tokens["while"] = ["PR_WHILE"]
tokens["switch"] = ["PR_SWITC"]
tokens["#define"] = ["PR_DEFIN"]
tokens["#include"] = ["PR_INCLU"]
tokens["return"] = ["PR_RETURN"]
tokens["using"] = ["PR_USING"]
tokens["namespace"] = ["PR_NSPC"]
tokens["std"] = ["PR_STD"]
tokens["main"] = ["PR_MAIN"]

def preprocess1(file):

    dic = {}
    word = ""
    lin = 1
    comment = False
    lines=list(file)
    print lines
    a = 0
    while a < len(lines):
        #print a
        b = 0
        while a < len(lines) and b < len(lines[a]):
            if b+1<len(lines[a]) and lines[a][b]=='/' and lines[a][b+1]=='*':
                print "Inicio de comentario"
                comment = True
                b+=2
                while a < len(lines):
                    
                    if b < len(lines[a]):
                        if b+1<len(lines[a]) and lines[a][b]=='*' and lines[a][b+1]=='/':
                            print "Fin de comentario"
                            comment = False
                            b+=1
                            break
                        else:
                            b+=1
                    else:
                        b=0
                        a+=1
            elif b+1<len(lines[a]) and lines[a][b]=='/' and lines[a][b+1]=='/':
                print "Comentario de una linea"
                b=-1
                a+=1
                lin+=1
            else:
                if lines[a][b]!='\t':
                    word+=lines[a][b]
                    #print word
                if lines[a][b]=='\n' or lines[a][b]=='\r':
                    dic[word[:-1]+" "]=[lin]
                    lin+=1
                    word=""
                    #print dic
            b+=1
        a+=1
    if comment:
        print errors["002"][0]
    dic.pop('', None)
    #print dic
    return dic


def createTokensList (dic):
    aux=""
    tokensList=[]
    print dic
    for line in dic:
        aux=""
        for a in line:
            if a not in separators:
                aux+=a
                #print aux
            else:
                #print "hola" + aux
                if aux!="" and aux in tokens:
                    d=aux,dic[line][0],tokens[aux][0]
                    tokensList.append(d)
                    
                elif aux!="":
                    match = re.match('[a-zA-Z][a-zA-Z0-9]*', aux)
                    if match and len(match.group())==len(aux):
                        d=aux,dic[line][0],'ID'
                        tokensList.append(d)
                    else:
                        match = re.match("[-+]?[0-9]+\.?[0-9]*", aux)
                        if match and len(match.group())==len(aux):
                            print match.group()
                            d=aux,dic[line][0],'NUMBER'
                            tokensList.append(d)
                        else:
                            print errors["001"][0] + " en la linea " + str(dic[line][0]) + " " + aux
                if a != " ":
                    d=a,dic[line][0],tokens[a][0]
                    tokensList.append(d)
                aux=""
    print "\nTokens list:"
    for tkn in tokensList:
        print tkn
    return tokensList

def createSybolTable(tknList):

    SymbolTable = {}

    for token in range(len(tknList)):
        array = False
        if tknList[token][2] == 'ID':
            tam=1
            SymbolTable[tknList[token][0]] = ["NONE", "NONE", "NONE"]
            #if token+1<len(tknList) and token+2<len(tknList) and tknList[token+1][2]=='COR_O' and tknList[token+2][2]=='NUMBER':
            #    array=True
            #    tam=int(tknList[token+2][0])
            #if token-1>0:
            #    if tknList[token-1][2] == 'TD_INT':
            #        SymbolTable[tknList[token][0]] = ["int", 4*tam, array]
            #    elif tknList[token-1][2] == 'TD_FLOAT':
            #        SymbolTable[tknList[token][0]] = ["float", 4*tam, array]
            #    elif tknList[token-1][2] == 'TD_DBL':
            #        SymbolTable[tknList[token][0]] = ["double", 8*tam, array]
            #    elif tknList[token-1][2] == 'TD_BOOL':
            #        SymbolTable[tknList[token][0]] = ["bool", 1*tam, array]
            #    elif tknList[token-1][2] == 'TD_CHAR':
            #        SymbolTable[tknList[token][0]] = ["char", 1*tam, array]
            #    elif tknList[token-1][2] == 'TD_STR':
            #        SymbolTable[tknList[token][0]] = ["string", 100*tam, array]
            #    elif tknList[token-1][2] == 'TD_VOID':
            #        SymbolTable[tknList[token][0]] = ["void", 0, array]

    print "\nSymbol table:"
    for symbol in SymbolTable:
        aux=str(symbol)+"\t"
        for iter in SymbolTable[symbol]:
            aux+=str(iter)+"\t"
        #print symbol + " " + str(SymbolTable[symbol])
        print aux

f = open('prueba1.txt', 'r')
print f

dic = preprocess1(f)
od = collections.OrderedDict(sorted(dic.items(), key=operator.itemgetter(1)))
f.close()

tknList = createTokensList (od)
createSybolTable(tknList)

non_ter = {}
ter = {}
TS = {}

non_ter["S"] = [0]
non_ter["lista_sentencias"] = [1]
non_ter["def_basica"] = [2]
non_ter["tipo_dato"] = [3, {"type": "null"}]
non_ter["lista_def"] = [4, {"type": "null"}]
non_ter["lista_def*"] = [5, {"type": "null"}]
non_ter["def_espec"] = [6, {"type": "null"}]
non_ter["def_espec*"] = [7, {"type": "null", "idlex": "null"}]
non_ter["def_espec**"] = [8, {"type": "null", "value": "null"}]
non_ter["acceso_array"] = [9, {"pos": "null"}]
non_ter["simple_asign"] = [10, {"type": "null", "value": "null"}]
non_ter["sentencia"] = [11]
non_ter["sentencia1"] = [12, {"type": "null", "idlex": "null", "value": "null"}]
non_ter["WHILE"] = [13, {"comienzo": "null", "despues": "null", "codigo": ""}]
non_ter["IF_ELSE"] = [14]
non_ter["IF_ELSE*"] = [15, {"comienzo": "null"}]
non_ter["IF"] = [16, {"despues": "null", "codigo": ""}]
non_ter["W*"] = [17, {"codigo": ""}]
non_ter["condicion"] = [18, {"codigo": "", "lugar": "null"}]
non_ter["condicion*"] = [19]
non_ter["condicion_logica"] = [20]
non_ter["operadores_log"] = [21, {"operator": "null"}]
non_ter["operadores"] = [22, {"operator": "null"}]
non_ter["op_aditivos"] = [23, {"operator": "null"}]
non_ter["op_multiplicativos"] = [24, {"operator": "null"}]
non_ter["E"] = [25, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]
non_ter["E*"] = [26, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]
non_ter["T"] = [27, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]
non_ter["T*"] = [28, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]
non_ter["F"] = [29, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]
non_ter["F*"] = [30, {"type": "null", "value": "null", "codigo": "", "lugar": "null"}]

ter["INCLUDE"] = [0]
ter["TD_INT"] = [1]
ter["TD_FLOAT"] = [2]
ter["TD_DBL"] = [3]
ter["TD_BOOL"] = [4]
ter["TD_CHAR"] = [5]
ter["PR_MAIN"] = [6]
ter["PAR_O"] = [7]
ter["PAR_C"] = [8]
ter["LLA_O"] = [9]
ter["LLA_C"] = [10]
ter["COR_O"] = [11]
ter["COR_C"] = [12]
ter["SCOLON"] = [13]
ter["COMA"] = [14]
ter["OP_ASSIG"] = [15]
ter["PR_RETURN"] = [16]
ter["TKN_NUM_ENTERO"] = [17]
ter["OP_AND"] = [18]
ter["OP_OR"] = [19]
ter["OP_LESS"] = [20]
ter["OP_MORE"] = [21]
ter["OP_MORE_OR_E"] = [22]
ter["OP_LESS_OR_E"] = [23]
ter["OP_EQUAL"] = [24]
ter["OP_DIFFERENT"] = [25]
ter["OP_SUM"] = [26]
ter["OP_SUBS"] = [27]
ter["OP_MULT"] = [28]
ter["OP_DIV"] = [29]
ter["OP_PCNT"] = [30]
ter["ID"] = [31] #{"type": "null", "lexema": "null", "value": 0}
ter["PR_IF"] = [32]
ter["PR_WHILE"] = [33]
ter["PR_ELSE"] = [34]
ter["NUMBER"] = [35]

def rule9_1():
    non_ter["tipo_dato"][1]["type"]="int"
    global shift
    shift+=4
def rule9_2():
    non_ter["tipo_dato"][1]["type"]="float"
    global shift
    shift+=8
def rule9_3():
    non_ter["tipo_dato"][1]["type"]="double"
    global shift
    shift+=16
def rule9_4():
    non_ter["tipo_dato"][1]["type"]="boolean"
    global shift
    shift+=1

TS[0] = ["INCLUDE", "S"]
TS[1] = ["TD_INT", "PR_MAIN", "PAR_O", "PAR_C", "LLA_O", "lista_sentencias", "PR_RETURN", "NUMBER", "SCOLON", "LLA_C"]
TS[37] = ["sentencia", "lista_sentencias"]
TS[38] = ["sentencia", "lista_sentencias"]
TS[39] = ["sentencia", "lista_sentencias"]
TS[40] = ["sentencia", "lista_sentencias"]
TS[41] = ["sentencia", "lista_sentencias"]
TS[43] = ["sentencia", "lista_sentencias"]
TS[45] = ["sentencia", "lista_sentencias"]
TS[46] = ["vacio"]
TS[52] = ["vacio"]
TS[67] = ["sentencia", "lista_sentencias"]
TS[68] = ["sentencia", "lista_sentencias"]
TS[69] = ["sentencia", "lista_sentencias"]
TS[71] = ["sentencia", "lista_sentencias"]
TS[73] = ["tipo_dato", "lista_def", "SCOLON"]
TS[74] = ["tipo_dato", "lista_def", "SCOLON"]
TS[75] = ["tipo_dato", "lista_def", "SCOLON"]
TS[76] = ["tipo_dato", "lista_def", "SCOLON"]
TS[77] = ["tipo_dato", "lista_def", "SCOLON"]
TS[109] = ["TD_INT", rule9_1]
TS[110] = ["TD_FLOAT"]
TS[111] = ["TD_DBL"]
TS[112] = ["TD_BOOL"]
TS[113] = ["TD_CHAR"]
TS[175] = ["def_espec", "lista_def*"]
TS[193] = ["vacio"]
TS[194] = ["COMA", "lista_def"]
TS[247] = ["ID", "def_espec*"]
TS[263] = ["acceso_array", "def_espec**"]
TS[265] = ["vacio"]
TS[266] = ["vacio"]
TS[267] = ["simple_asign"]
TS[301] = ["vacio"]
TS[302] = ["vacio"]
TS[303] = ["simple_asign"]
TS[335] = ["COR_O", "TKN_NUM_ENTERO", "COR_C"]

TS[373] = ["vacio"]
TS[374] = ["vacio"]
TS[375] = ["OP_ASSIG", "E"]
TS[397] = ["def_basica"]
TS[398] = ["def_basica"]
TS[399] = ["def_basica"]
TS[400] = ["def_basica"]
TS[403] = ["PAR_O", "E", "PAR_C", "SCOLON"]
TS[427] = ["ID", "sentencia1", "SCOLON"]
TS[428] = ["IF_ELSE"]
TS[429] = ["WHILE"]
TS[431] = ["NUMBER", "T*", "E*", "SCOLON"]
TS[443] = ["F*", "T*", "E*"]
TS[445] = ["vacio"]
TS[447] = ["def_espec*"]
TS[458] = ["operadores", "OP_ASSIG", "E"]
TS[459] = ["operadores", "OP_ASSIG", "E"]
TS[460] = ["operadores", "OP_ASSIG", "E"]
TS[461] = ["operadores", "OP_ASSIG", "E"]
TS[462] = ["operadores", "OP_ASSIG", "E"]
TS[463] = ["def_spec*"]
TS[501] = ["PR_WHILE", "PAR_O", "condicion", "PAR_C", "W*"]
TS[536] = ["IF", "IF_ELSE*"]
TS[574] = ["PR_ELSE", "W*"]
TS[608] = ["PR_IF", "PAR_O", "condicion", "PAR_C", "W*"]
TS[613] = ["sentencia"]
TS[614] = ["sentencia"]
TS[615] = ["sentencia"]
TS[616] = ["sentencia"]
TS[617] = ["sentencia"]
TS[619] = ["sentencia"]
TS[621] = ["LLA_O", "lista_sentencias", "LLA_C"]
TS[643] = ["sentencia"]
TS[657] = ["condicion_logica", "condicion*"]
TS[679] = ["condicion_logica", "condicion*"]
TS[683] = ["condicion_logica", "condicion*"]
TS[692] = ["vacio"]
TS[702] = ["OP_AND", "OP_AND", "condicion_logica"]
TS[703] = ["OP_AND", "OP_AND", "condicion_logica"]
TS[727] = ["E", "operadores_log", "E"]
TS[751] = ["E", "operadores_log", "E"]
TS[755] = ["E", "operadores_log", "E"]
TS[776] = ["OP_LESS"]
TS[777] = ["OP_MORE"]
TS[778] = ["OP_M_EQ"]
TS[779] = ["OP_L_EQ"]
TS[780] = ["OP_EQ"]
TS[781] = ["OP_DIFF"]
TS[818] = ["op_aditivos"]
TS[819] = ["op_aditivos"]
TS[820] = ["op_multiplicativos"]
TS[821] = ["op_multiplicativos"]
TS[822] = ["op_multiplicativos"]
TS[854] = ["OP_SUM"]
TS[855] = ["OP_SUBS"]
TS[892] = ["OP_MULT"]
TS[893] = ["OP_DIV"]
TS[894] = ["OP_PCNT"]
TS[907] = ["PAR_O", "E", "PAR_C", "SCOLON"]
TS[931] = ["T", "E*"]
TS[935] = ["T", "E*"]
TS[944] = ["vacio"]
TS[949] = ["vacio"]
TS[950] = ["vacio"]
TS[954] = ["vacio"]

TS[955] = ["vacio"]
TS[956] = ["vacio"]
TS[957] = ["vacio"]
TS[958] = ["vacio"]
TS[959] = ["vacio"]
TS[960] = ["vacio"]
TS[961] = ["vacio"]
TS[962] = ["op_aditivos", "E"]
TS[963] = ["op_aditivos", "E"]
TS[1003] = ["F", "T*"]
TS[1007] = ["F", "T*"]
TS[1016] = ["vacio"]
TS[1021] = ["vacio"]
TS[1022] = ["vacio"]
TS[1026] = ["vacio"]

TS[1027] = ["vacio"]
TS[1028] = ["vacio"]
TS[1029] = ["vacio"]
TS[1030] = ["vacio"]
TS[1031] = ["vacio"]
TS[1032] = ["vacio"]
TS[1033] = ["vacio"]
TS[1034] = ["vacio"]
TS[1035] = ["vacio"]
TS[1036] = ["op_multiplicativos", "T"]
TS[1037] = ["op_multiplicativos", "T"]
TS[1038] = ["op_multiplicativos", "T"]
TS[1075] = ["ID", "F*"]
TS[1079] = ["NUMBER"]
TS[1088] = ["vacio"]
TS[1091] = ["acceso_array"]
TS[1093] = ["vacio"]
TS[1094] = ["vacio"]
TS[1098] = ["vacio"]

TS[1099] = ["vacio"]
TS[1100] = ["vacio"]
TS[1101] = ["vacio"]
TS[1102] = ["vacio"]
TS[1103] = ["vacio"]
TS[1104] = ["vacio"]
TS[1105] = ["vacio"]
TS[1106] = ["vacio"]
TS[1107] = ["vacio"]
TS[1108] = ["vacio"]
TS[1109] = ["vacio"]
TS[1110] = ["vacio"]


pila = []

a = non_ter["S"][0]
b = ter[tknList[0][2]][0]
c = TS[36*a+b]
pila.insert(0,c)
pila=pila[0]
print pila
i=0
while i<len(tknList):
    if len(pila)==0:
        print "error1"
        break
    while(i<len(tknList) and len(pila)>=0 and (tknList[i][2]==pila[0] or callable(pila[0]))):
        if callable(pila[0]):
            pila[0]()
        else:
            i+=1
        print "Pop " + str(pila[0])
        pila.pop(0)
        print pila
    if len(pila)==0 and i>=len(tknList):
        #print "ACEPTADA"
        break
    if(pila[0] in non_ter):
        a = non_ter[pila[0]][0]
        b = ter[tknList[i][2]][0]
        print "veo"+" "+str(a)+" "+str(b)+"="+str(36*a+b)
        c = TS[36*a+b]

        if(c[0]=="vacio"):
            pila.pop(0)
        else:
            pila.pop(0)
            for s in reversed(c):
                pila.insert(0,s)
                print pila
                input("control")
        print pila
    else:
        print "error2 se esperaba " + str(pila[0]) + " en linea " + str(tknList[i-1][1])
        pila.pop(0)
        #break

print non_ter["condicion*"]
print non_ter["sentencia1"][1]["type"]