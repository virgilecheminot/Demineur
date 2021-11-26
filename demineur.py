import random as rd
from colorama import Fore, Style

def creerGrille(N,M,v=0): return [[v for j in range(M)] for i in range(N)]

def placerMines(grille,N,M,X,l,c):
    cpt = 0
    while cpt != X:
        ligne = rd.randint(0,N-1)
        case = rd.randint(0,M-1)
        while (ligne == l and case == c) or grille[ligne][case] == 1:
            ligne = rd.randint(0,N-1)
            case = rd.randint(0,M-1)
        grille[ligne][case] = 1
        cpt += 1

def afficheSolution(grille):
    for i in grille:
        for j in i:
            if j:
                print('*',end=' ')
            else:
                print('-',end=' ')
        print('')

def testMine(grille,l,c):
    if grille[l][c] == 1:
        return True
    else:
        return False

def compteMinesVoisines(grille,l,c):
    nbVoisines = 0
    haut, bas, gauche, droite = False,False,False,False
    if l==0:
        haut = True
    if l==len(grille)-1:
        bas = True
    if c==0:
        gauche = True
    if c==len(grille[l])-1:
        droite = True
    if not haut:
        nbVoisines += grille[l-1][c]
    if not haut and not droite:
        nbVoisines += grille[l-1][c+1]
    if not droite:
        nbVoisines += grille[l][c+1]
    if not droite and not bas:
        nbVoisines += grille[l+1][c+1]
    if not bas:
        nbVoisines += grille[l+1][c]
    if not bas and not gauche:
        nbVoisines += grille[l+1][c-1]
    if not gauche:
        nbVoisines += grille[l][c-1]
    if not gauche and not haut:
        nbVoisines += grille[l-1][c-1]
    return nbVoisines

def afficheJeu(grille,casesD):
    print(Style.RESET_ALL,end='')
    print(' '*3,end='')
    for i in range(len(grille[0])):
        print(i+1,end=' ')
    print('\n')
    for l in range(len(grille)):
        sepa = ' '*(3-len(str(l+1)))
        print(l+1,end=sepa)
        for c in range(len(grille[l])):
            if casesD[l][c]:
                if grille[l][c]:
                    print('*',end=' ')
                else:
                    val = compteMinesVoisines(grille,l,c)
                    if val == 0:
                        print(Fore.BLUE + str(val), end=' ')
                    elif val == 1:
                        print(Fore.CYAN + str(val), end=' ')
                    elif val == 2:
                        print(Fore.GREEN + str(val), end=' ')
                    elif val == 3:
                        print(Fore.YELLOW + str(val), end=' ')
                    elif val == 4:
                        print(Fore.RED + str(val), end=' ')
                    elif val >= 5:
                        print(Fore.MAGENTA + str(val), end=' ')
                    print(Style.RESET_ALL, end='')

            else:
                print('?',end=' ')
        print(Style.RESET_ALL)

def getCoords(casesD,N,M):
    print('À toi de jouer !')
    casePrise = True
    while casePrise:
        l = int(input("Ligne ? "))-1
        c = int(input('Colonne ? '))-1
        while not 0<=l<=N-1:
            l = int(input('0 ≤ ligne <',N,'svp ? '))
        while not 0<=c<=M-1:
            c = int(input('0 ≤ colonne <',M,'svp ? '))
        if casesD[l][c]:
            print('Case déjà dévoilée, recommencez')
        else:
            casePrise = False
    return l,c

def victoire(grille,casesD,N,M):
    for l in range(N):
        for c in range(M):
            if not grille[l][c] and not casesD[l][c]:
                return False
    return True

def decimateCase(grille,casesD,l,c,add,listeToDecimate):
    haut, bas, gauche, droite = False,False,False,False
    if l==0:
        haut = True
    if l==len(grille)-1:
        bas = True
    if c==0:
        gauche = True
    if c==len(grille[l])-1:
        droite = True
    
    if not haut:
        add.append([l-1,c])
        if compteMinesVoisines(grille,l-1,c) == 0 and not grille[l-1][c]:
            if not casesD[l-1][c]:
                listeToDecimate.append([l-1,c])
            casesD[l-1][c] = True

    if not haut and not droite:
        add.append([l-1,c+1])
        if compteMinesVoisines(grille,l-1,c+1) == 0 and not grille[l-1][c+1]:
            if not casesD[l-1][c+1]:
                listeToDecimate.append([l-1,c+1])
            casesD[l-1][c+1] = True

    if not droite:
        add.append([l,c+1])
        if compteMinesVoisines(grille,l,c+1) == 0 and not grille[l][c+1]:
            if not casesD[l][c+1]:
                listeToDecimate.append([l,c+1])
            casesD[l][c+1] = True

    if not droite and not bas:
        add.append([l+1,c+1])
        if compteMinesVoisines(grille,l+1,c+1) == 0 and not grille[l+1][c+1]:
            if not casesD[l+1][c+1]:
                listeToDecimate.append([l+1,c+1])
            casesD[l+1][c+1] = True

    if not bas:
        add.append([l+1,c])
        if compteMinesVoisines(grille,l+1,c) == 0 and not grille[l+1][c]:
            if not casesD[l+1][c]:
                listeToDecimate.append([l+1,c])
            casesD[l+1][c] = True

    if not bas and not gauche:
        add.append([l+1,c-1])
        if compteMinesVoisines(grille,l+1,c-1) == 0 and not grille[l+1][c-1]:
            if not casesD[l+1][c-1]:
                listeToDecimate.append([l+1,c-1])
            casesD[l+1][c-1] = True

    if not gauche:
        add.append([l,c-1])
        if compteMinesVoisines(grille,l,c-1) == 0 and not grille[l][c-1]:
            if not casesD[l][c-1]:
                listeToDecimate.append([l,c-1])
            casesD[l][c-1] = True

    if not gauche and not haut:
        add.append([l-1,c-1])
        if compteMinesVoisines(grille,l-1,c-1) == 0 and not grille[l-1][c-1]:
            if not casesD[l-1][c-1]:
                listeToDecimate.append([l-1,c-1])
            casesD[l-1][c-1] = True

def decimator3000(grille,casesD,l,c):
    add = []
    ligne = l
    case = c
    listeToDecimate = [[ligne,case]]
    while len(listeToDecimate)!=0:
        for i in listeToDecimate:
            ligne = i[0]
            case = i[1]
            if ligne == l and case == c:
                decimateCase(grille,casesD,ligne,case,add,listeToDecimate)
                listeToDecimate.remove([ligne,case])
            elif casesD[ligne][case] and grille[ligne][case] == 0 and compteMinesVoisines(grille,ligne,case) == 0:
                decimateCase(grille,casesD,ligne,case,add,listeToDecimate)
                listeToDecimate.remove([ligne,case])
    for i in add:
        casesD[i[0]][i[1]] = True


## PROGRAMME PRINCIPAL

N = int(input('Nombre de lignes : '))
M = int(input('Nombre de colonnes : '))
grille = creerGrille(N,M)

X = int(input('Nombre de mines : '))
while X >= N*M:
    X = int(input('Nombre de mines : '))

## Premier coup
nbCoups = 1
print('\nCou numéro',nbCoups)
casesD = [[False for j in range(M)] for i in range(N)]
afficheJeu(grille,casesD)
l,c=getCoords(casesD,N,M)
casesD[l][c] = True
placerMines(grille,N,M,X,l,c)
if compteMinesVoisines(grille,l,c) == 0:
    decimator3000(grille,casesD,l,c)

perdu = False
gagne = victoire(grille,casesD,N,M)


## Tour de jeu
while not gagne and not perdu:
    nbCoups += 1
    print('\nCoup numéro', nbCoups)
    afficheJeu(grille,casesD)
    l,c=getCoords(casesD,N,M)
    casesD[l][c] = True
    if testMine(grille,l,c):
        perdu = True
    if compteMinesVoisines(grille,l,c) == 0 and not perdu:
        decimator3000(grille,casesD,l,c)
    gagne = victoire(grille,casesD,N,M)

if gagne:
    print('\nBravo, tu gagnes en',nbCoups,'coups !\n')
    casesD = [[True for j in range(M)] for i in range(N)]
    afficheJeu(grille,casesD)

else:
    print('\nPerdu, touché une mine !')
    print('\nTon jeu :')
    afficheJeu(grille,casesD)
    print('\nLa solution était :')
    afficheSolution(grille)