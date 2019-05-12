#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# UFMG - ICEx - DCC - Pesquisa Operacional - 2019/1
# 
# TP1: Programação Linear - Simplex
# 
# Aluna: Scarlet Gianasi Viana
# Matrícula: 2016006891
# 
# Versão utilizada: Python 3.6.7
# =============================================================================

import sys

def lePL(arquivoE):
    entrada = open(arquivoE, "r")
    A = []
    b = []
    n, m = entrada.readline().split()
    m = int(m)
    n = int(n)
    c = entrada.readline().split()
    c = list(map(float, c))
    for i in range(0,n):
        s = entrada.readline().split()
        s = list(map(float, s))
        A.append(s[0:m])
        b.append(s[m])
    return c, A, b, n, m

def checaNegativos(vetor):
    count = 0
    for item in vetor:
        if item < 0:
            count+=1
    if count == 0:
        return False, count
    else:
        return True, count

def montaTableau(c, A, b, n, m, duasFases):   
    aux = m
    Atableau = A
    cTableau = [-i+0 for i in c] 
    # Inserindo variaveis de folga:
    for i in range(0,n):
        for j in range(0,n):
            Atableau[i].append(0.0)
    # Identidade    
    for i in range(0,n):
       Atableau[i][aux] = 1.0
       aux+=1  
    if duasFases:
        # Inserindo variaveis artificiais
        cAux = []
        count = 0
        col = 0
        for item in b:
            if item < 0:
                count += 1    
        for i in range(0,n):
            for x in range(count):
                Atableau[i].append(0.0)
        for i in range(0,n):
            if b[i] < 0:
                Atableau[i][col-count] = -1.0
                col += 1
        for i in range(0,n):
            Atableau[i].append(b[i])
            if b[i] < 0:
                for j in range(0,len(Atableau[0])):
                    if Atableau[i][j] != 0:
                        Atableau[i][j] *= -1.0   
        for i in range(0,len(Atableau[0])-count-1):
            cAux.append(0.0)
        for x in range(0,count):
            cAux.append(1.0)
        cAux.append(0.0)
        Atableau.insert(0,cAux)
        for i in range(1,n+1):
            if b[i-1] < 0:
                for x in range(0,len(Atableau[0])):
                    Atableau[0][x] = Atableau[0][x] - Atableau[i][x]             
    else: 
        for i in range(0,n):
            Atableau[i].append(b[i])    
        for i in range(0,n+1):
            cTableau.append(0.0)    
        Atableau.insert(0,cTableau)    
    return Atableau

def iniciaSimplex(Atableau, b, n, m):
    while True:
        pivot, haPivot, cNegativo = buscaPivot(Atableau, n)
        if haPivot:
            pivoteia(pivot, Atableau, n, m)
        else:              
            if cNegativo:
                sol = 'ilimitada'
            else:
                sol = 'viavel'
            VO = Atableau[0][len(Atableau[0])-1]
            return round(VO,2), sol
            
def pivoteia(pivot, At, n, m):
    linhaP = pivot[0]
    colunaP = pivot[1]    
    elem = At[linhaP][colunaP]    
    for x in range(0,len(At[0])):
        At[linhaP][x] /= elem
        At[linhaP][x] = At[linhaP][x]    
    for linha in range(0,n+1):
        if linha != linhaP:
            mult = At[linha][colunaP]
            if mult != 0:
                for x in range(0,len(At[0])):
                    At[linha][x] = At[linha][x] - At[linhaP][x]*mult        

def buscaPivot(Atableau, n):    
    c = Atableau[0]
    tam = len(c)-1
    razao = 10000.0
    pivot = [-1,-1]
    haPivot = False
    cNeg = False    
    for coluna in range(0,tam):
        if c[coluna] < 0:
            cNeg = True
            razao = 10000.0
            for linha in range(1,n+1):
                p = Atableau[linha][coluna]
                bi = Atableau[linha][tam]
                if (p > 0) & (bi >= 0):
                    if bi/p < razao:
                        pivot = [linha, coluna]
                        razao = bi/p
            if pivot[1] > -1:
                haPivot = True
                break                        
    return pivot, haPivot, cNeg

def certificado(At, m, n):
    cert = At[0][m:n+m]
    cert = [round(i,2) for i in cert]
    return cert

def certificadoIlimitada(At, m, n):
    cert = []    
    for coluna in range(0,m):
        if At[0][coluna] < 0:
            for colunaM in range(0,m):
                if At[0][colunaM] == 0:
                    for linha in range(1,n+1):
                        if At[linha][colunaM] == 1:
                            cert.append(At[linha][coluna]*(-1.0) + 0)
                elif colunaM != coluna:
                    cert.append(0.0)
            cert.insert(coluna,1.0)
            break        
    cert = [round(i,2) for i in cert]
    return cert

def solucaoViavel(At,m,n):
    sol = [0.0 for i in range(0,m)]    
    for coluna in range(0,m):
        if At[0][coluna] == 0:
            for linha in range(0,n):
                if At[linha+1][coluna] == 1:
                    sol[coluna] = At[linha+1][len(At[0])-1]
    sol = [round(i,2) for i in sol]
    return sol
    
def simplex():
    arqE = sys.argv[1]
    c, A, b, n, m = lePL(arqE)   
    negativos, count = checaNegativos(b)    
    if negativos:
        duasFases = True
        Aaux = montaTableau(c,A,b,n,m,duasFases)
        VO, sol = iniciaSimplex(Aaux, b, n, m)
        if VO == 0:
            Atab = Aaux
            Atab[0] = c
            Atab[0] = [i*-1.0 for i in Atab[0]]
            for i in range(0,len(Aaux[1])-len(c)):
                Atab[0].append(0.0)            
            VO, sol = iniciaSimplex(Atab,b,n,m)
            cert = certificado(Atab,m,n)
            s = solucaoViavel(Atab, m, n)
            if sol == 'viavel':
                print("otima")
                print(round(VO,2))
            else:
                print("ilimitada")
            print(str(s))
            print(str(cert))
        else:
            if VO < 0:
                print("inviavel")
                cert = certificado(Aaux,m,n)
                print(str(cert))
            else:
                print("ilimitada")
                cert = certificadoIlimitada(Aaux,m,n)
                s = solucaoViavel(Aaux, m, n)
                print(str(s))
                print(str(cert))
    else:
        duasFases = False
        Atab = montaTableau(c,A,b,n,m,duasFases)
        VO, sol = iniciaSimplex(Atab, b, n, m)
        if sol == 'ilimitada':
            print("ilimitada")
            cert = certificadoIlimitada(Atab,m,n)
        else:
            print("otima")
            print(round(VO,2))
            cert = certificado(Atab,m,n)            
        s = solucaoViavel(Atab, m, n)
        print(str(cert))
        print(str(s))

if __name__ == "__main__":
    simplex()
