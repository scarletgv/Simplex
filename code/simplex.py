#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 18:47:08 2019

@author: scarletgv
"""

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

def imprimeMatriz(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

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
        # Inserir variaveis artificiais
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
        
        cAux.append(0.0) # V.O.
        Atableau.insert(0,cAux)
        
        imprimeMatriz(Atableau)
        
        for i in range(1,n+1):
            if b[i-1] < 0:
                for x in range(0,len(Atableau[0])):
                    Atableau[0][x] = Atableau[0][x] - Atableau[i][x] 
        
        # Zerando as artificiais 
#        maior = max(c)
#        print("Maior: "+str(maior))
#        for j in range(0,len(c)):
#            if c[j] == maior:
#                razao = 10000.0
#                for i in range(1,n+1):
#                    if Atableau[i][j] > 0:
#                        if Atableau[i][len(Atableau[0])-1]/Atableau[i][j] < razao:
#                            razao = Atableau[i][len(Atableau[0])-1]/Atableau[i][j]
#                            p = [i, j]
#                if razao < 10000.0:
#                    pivoteia(p, Atableau, n,m)
            
#        razao = 10000.0
#        for i in range(1,n+1):
#            if b[i-1] < 0:
#                razao = 10000.0
#                for j in range(0,len(Atableau[0])-1):
#                    if Atableau[i][j] > 0:
#                        if Atableau[i][len(Atableau[0])-1]/Atableau[i][j] < razao:
#                            razao = Atableau[i][len(Atableau[0])-1]/Atableau[i][j]
#                            p = [i, j]
#                if razao < 10000.0:
#                    pivoteia(p, Atableau, n,m)
          
            
    else: 
        for i in range(0,n):
            Atableau[i].append(b[i])
    
        for i in range(0,n+1):
            cTableau.append(0.0)
    
        Atableau.insert(0,cTableau)
    
    print("Tableau da PL:")    
    imprimeMatriz(Atableau)
    
    return Atableau

def iniciaSimplex(Atableau, b, n, m):
    print("Iniciando simplex.")
    while True:
        pivot, haPivot, cNegativo = buscaPivot(Atableau, n)
    
        if haPivot:
            print("Pivoteando.")
            pivoteia(pivot, Atableau, n, m)
        else:              
            if cNegativo:
                print("PL ilimitada, não há elemento para pivotear.")
                sol = 'ilimitada'
            else:
                print("Fim do simplex.")
                sol = 'viavel'
            VO = Atableau[0][len(Atableau[0])-1]
            print("VO:"+str(VO))
            return VO, sol
            #break
            

def pivoteia(pivot, At, n, m):
    linhaP = pivot[0]
    colunaP = pivot[1]
    
    elem = At[linhaP][colunaP]
    
    for x in range(0,len(At[0])):
        At[linhaP][x] /= elem
    
    for linha in range(0,n+1):
        if linha != linhaP:
            mult = At[linha][colunaP]
            if mult != 0:
                for x in range(0,len(At[0])):
                    At[linha][x] = At[linha][x] - At[linhaP][x]*mult
    print("Matriz pivoteada:")
    imprimeMatriz(At)
        

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
            print("c negativo: "+str(c[coluna]))
            razao = 10000.0
            for linha in range(1,n+1):
                p = Atableau[linha][coluna]
                bi = Atableau[linha][tam]
                if (p > 0) & (bi >= 0):
                    print("Pivot possível: "+str(p))
                    if bi/p < razao:
                        pivot = [linha, coluna]
                        razao = bi/p
            if pivot[1] > -1:
                print("Pivot encontrado!")
                print("P:"+str(pivot))
                haPivot = True
                break                        
    return pivot, haPivot, cNeg

def criaVERO(n):
    #VERO = []
    init = [0.0 for x in range(n)]
    
        # Inserindo variaveis de folga:
    VERO=[[0.0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        VERO[i][i] = 1.0
    
    VERO.insert(0,init)
    
    return VERO

def certificado(At, m, n):
    cert = At[0][m:n+m]
    
    print(cert)
    return cert

def certificadoIlimitada(At, m, n):
    cert = [1.0]
    
    for coluna in range(0,m):
        if At[0][coluna] < 0:
            for linha in range(1,n+1):
                cert.append(At[linha][coluna])
            break
    print(cert)
    return cert

def solucaoViavel(At,m,n):
    sol = [0.0 for i in range(0,m)]
    
    for coluna in range(0,m):
        if At[0][coluna] == 0:
            for linha in range(0,n):
                if At[linha+1][coluna] == 1:
                    sol[coluna] = At[linha+1][len(At[0])-1]
    print(sol)
    
def main():
    arqE = "tp1_tests/03"
    c, A, b, n, m = lePL(arqE)   
    print("n: "+str(n)+" m: "+str(m))
    print("c: "+str(c))
    print("A:")    
    imprimeMatriz(A)
    print("b: "+str(b))
    
    VERO = criaVERO(n)
    print("VERO:")
    imprimeMatriz(VERO)
    
    negativos, count = checaNegativos(b)
    #negativos = False
    
    if negativos:
        print("Vetor b com valores negativos. Simplex de Duas fases necessário.")
        print("Montando PL auxiliar.")
        duasFases = True
        Aaux = montaTableau(c,A,b,n,m,duasFases)
        VO, sol = iniciaSimplex(Aaux, b, n, m)
        if VO == 0:
            print("Há solução viável!")
            Atab = Aaux
            Atab[0] = c
            Atab[0] = [i*-1.0 for i in Atab[0]]
            for i in range(0,len(Aaux[1])-len(c)):
                Atab[0].append(0.0)
            imprimeMatriz(Atab)
            
            #At = montaTableau(c,A,b,n,m,False)
            
            VO, sol = iniciaSimplex(Atab,b,n,m)
            cert = certificado(Atab,m,n)
            solucaoViavel(Atab, m, n)
        else:
            if VO < 0:
                print("PL inviável.") 
                cert = certificado(Aaux,m,n)
            else:
                print("PL ilimitada.")
                cert = certificadoIlimitada(Aaux,m,n)
    else:
        print("Simplex normal.")
        duasFases = False
        Atab = montaTableau(c,A,b,n,m,duasFases)
        VO, sol = iniciaSimplex(Atab, b, n, m)
        if sol == 'ilimitada':
            cert = certificadoIlimitada(Atab,m,n)
        else:
            cert = certificado(Atab,m,n)
        solucaoViavel(Atab, m, n)
        

if __name__ == "__main__":
    main()
