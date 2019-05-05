# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:07:38 2019

@author: Scarlet
"""

def tableau(c, A, b, n, m):   
    aux = m
    Atableau = A
    cTableau = [-i+0 for i in c]
    # Inserindo variaveis de folga:
    for i in range(n):
        for j in range(n):
            Atableau[i].append(0.0)
            
    for i in range(0,n):
       Atableau[i][aux] = 1.0
       aux+=1
       Atableau[i].append(b[i])
    
    for i in range(n+1):
        cTableau.append(0.0)
    
    Atableau.insert(0,cTableau)
    
    print("Tableau da PL:")
    
    for line in Atableau:
        print(line)
    
    return Atableau

def tableauAuxiliar(c, A, b, n, m):   
    aux = m
    Atableau = A
    cTableau = [-i+0 for i in c]
    # Inserindo variaveis de folga:
    for i in range(n):
        for j in range(n):
            Atableau[i].append(0.0)
    
    # Conta variaveis artificiais
    artificial = 0
    lArt = [0 for i in range(0,n)]
    
    for i in range(0,len(b)):
        if b[i] < 0:
            artificial += 1
            lArt[i] = 1.0
            
    print("Mascara")
    print(lArt)
    
    for x in range(n):
        for y in range(artificial):
            Atableau[x].append(0.0) 
    
    shift = m*2
    
    for i in range(n):
        if b[i] < 0:
            Atableau[i][shift] = 1.0
            shift += 1
    
    for i in range(0,n):
        Atableau[i][aux] = 1.0
        aux+=1        
        Atableau[i].append(b[i])
     
    for i in range(n+1+artificial):
        cTableau.append(0.0)
    
    cArtificial = []
    for i in range(m+n):
        cArtificial.append(0.0)
    for i in range(artificial):
        cArtificial.append(-1.0)
    cArtificial.append(0.0)
    
    #Atableau.insert(0,cTableau)
    Atableau.insert(0,cArtificial)
    
    print("Tableau auxiliar:")
    
    for line in Atableau:
        print(line)
    
    return Atableau

def lePL(arquivoE):
    entrada = open(arquivoE, "r")
    
    A = []
    b = []
    
    n, m = entrada.readline().split()
    m = int(m)
    n = int(n)
    c = entrada.readline().split()
    c = list(map(float, c))
    
    for i in range(n):
        s = entrada.readline().split()
        s = list(map(float, s))
        A.append(s[0:m])
        b.append(s[m])
    
    return c, A, b, n, m

def encontraPivot(tab, n, m):
    # Busca elemento negativo em c:
    coluna = -1 # Default
    linha = -1
    razao = 100
    
    # Buscando coluna negativa para pivotear
    for j in range(0,m+n-1):
        if tab[0][j] < 0:
            coluna = j
            break
    if(coluna == -1):
        print("Não há mais items para pivotear.")
        return False, False
    else:
        print("Coluna "+str(coluna)+", elem "+str(tab[0][coluna]))
    
    # Buscando linha com nao negativo diferente de zero para pivotear
    for i in range(n+1):
        if(tab[i][coluna] > 0) & (tab[i][m+n] > 0):
            if(tab[i][coluna]/tab[i][m+n]) < razao:
                linha = i
                razao = tab[i][coluna]/tab[i][m+n]
    if(linha == -1):
         print("PL inviável, não possui positivos para pivotear.")
         return False, False
    else:
        print("Linha "+str(linha)+", elem "+ str(tab[linha][coluna]))
        return linha, coluna

def pivoteia(ilinha, icoluna, tab, n, m):
    #ilinha, icoluna = encontraPivot(tab, n, m)
#    linhaPivot = tab[ilinha]
    #print(linhaPivot)
    #print(pivot)
    pivot = tab[ilinha][icoluna]
    
    print("Continua.")
    # Dividindo a linha do pivot para que seja = 1
    if pivot != 1:    
        for i in range(0,m-1):
            tab[ilinha][i] /= pivot
        for i in tab:
            print(i)
        # Zera cada elemento na coluna do pivot
#    print("Pivoteando")
    for i in range(0,n+1):
        if i != ilinha:
            linhaPivot = tab[ilinha]
            elem = tab[i][icoluna]
            linhaPivot = [elem*j for j in linhaPivot]
            if elem < 0:
                tab[i] = [x1 - x2 for (x1, x2) in zip(tab[i], linhaPivot)]
            else:
                tab[i] = [x1 + x2 for (x1, x2) in zip(tab[i], linhaPivot)]
    print("Após pivotear")
    for line in tab:
        print(line)
    #return tab

def iniciaSimplex(tab, n, m):
    while True:
        ilinha, icoluna = encontraPivot(tab, n, m)
        if ilinha:
            pivoteia(ilinha, icoluna, tab, n, m)
        else:
            print("Fim do simplex.")
            break
    
def main():
    arquivo = "testes/04"
    
    c, A, b, n, m = lePL(arquivo)
    print("n: "+str(n)+" m: "+str(m))
    print("c: "+str(c))
    print("A:")    
    for line in A:
        print(line)
    print("b: "+str(b))
    
    #duasFases = False
    
    # Chega se há b negativo
   
    
    #matrizTab = tableau(c,A,b,n,m)
    #iniciaSimplex(matrizTab, n, m)
    
    taux = tableauAuxiliar(c, A, b, n, m)
    iniciaSimplex(taux, n, len(taux[0]))


if __name__ == "__main__":
    main()
