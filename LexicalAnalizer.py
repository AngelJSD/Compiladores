#!/usr/bin/env python

import re
import operator
import collections

print "Hello!"

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
tokens["for"] = ["PR_FOR"]
tokens["while"] = ["PR_WHILE"]
tokens["switch"] = ["PR_SWITC"]
tokens["#define"] = ["PR_DEFIN"]
tokens["#include"] = ["PR_INCLU"]
tokens["return"] = ["PR_RETURN"]
tokens["using"] = ["PR_USING"]
tokens["namespace"] = ["PR_NSPC"]
tokens["std"] = ["PR_STD"]

def preprocess1(file):

    dic = {}
    word = ""
    lin = 1
    comment = False
    lines=list(file)
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
                if lines[a][b]=='\n' or lines[a][b]=='\r':
                    dic[word[:-1]+" "]=[lin]
                    lin+=1
                    word=""
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



