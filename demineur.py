import random as rd
from colorama import Fore, Back, Style


def creerGrille(N, M, v=0): return [[v for j in range(M)] for i in range(N)]


def placerMines(grille, N, M, X, l, c):
    cpt = 0
    while cpt != X:
        ligne = rd.randint(0, N-1)
        case = rd.randint(0, M-1)
        while (ligne == l and case == c) or grille[ligne][case] == 1 or (
                ligne == l and case == c+1) or (ligne == l and case == c-1) or (ligne == l-1 and case == c-1) or (
                ligne == l-1 and case == c) or (ligne == l-1 and case == c+1) or (ligne == l+1 and case == c-1) or (
                ligne == l+1 and case == c) or (ligne == l+1 and case == c+1):
            ligne = rd.randint(0, N-1)
            case = rd.randint(0, M-1)
        grille[ligne][case] = 1
        cpt += 1


def afficheSolution(grille):
    print(Style.RESET_ALL, end='')
    print(' '*3, end='')
    for i in range(len(grille[0])):
        sepa = ' '*(3-len(str(i+1)))
        print(i+1, end=sepa)
    print('\n')
    for l in range(len(grille)):
        sepa = ' '*(3-len(str(l+1)))
        print(l+1, end=sepa)
        for c in range(len(grille[l])):
            sepa2 = ' '*2
            if grille[l][c]:
                print(Back.RED+'*', end='')
                print(Style.RESET_ALL, end=sepa2)
            else:
                print('-', end=sepa2)
        print('')


def testMine(grille, l, c):
    if grille[l][c] == 1:
        return True
    else:
        return False


def compteMinesVoisines(grille, l, c):
    nbVoisines = 0
    for i in range(l-1, l+2):
        for j in range(c-1, c+2):
            if i >= 0 and i < len(grille) and j >= 0 and j < len(grille[l]):
                nbVoisines += grille[i][j]
    return nbVoisines


def afficheJeu(grille, casesD, drapeau):
    print(Style.RESET_ALL, end='')
    print(' '*3, end='')
    for i in range(len(grille[0])):
        sepa = ' '*(3-len(str(i+1)))
        print(i+1, end=sepa)
    print('\n')
    for l in range(len(grille)):
        sepa = ' '*(3-len(str(l+1)))
        print(l+1, end=sepa)
        for c in range(len(grille[l])):
            sepa2 = ' '*2
            if casesD[l][c]:
                if grille[l][c]:
                    print(Back.RED+'*', end='')
                    print(Style.RESET_ALL, end=sepa2)
                else:
                    val = compteMinesVoisines(grille, l, c)
                    if val == 0:
                        print(Fore.BLUE + str(val), end=sepa2)
                    elif val == 1:
                        print(Fore.CYAN + str(val), end=sepa2)
                    elif val == 2:
                        print(Fore.GREEN + str(val), end=sepa2)
                    elif val == 3:
                        print(Fore.YELLOW + str(val), end=sepa2)
                    elif val == 4:
                        print(Fore.RED + str(val), end=sepa2)
                    elif val >= 5:
                        print(Fore.MAGENTA + str(val), end=sepa2)
                print(Style.RESET_ALL, end='')

            elif drapeau[l][c]:
                print(Back.WHITE + Fore.BLACK + '!', end='')
                print(Style.RESET_ALL, end=sepa2)

            else:
                print('?', end=sepa2)
        print(Style.RESET_ALL)


def getCoords(casesD, N, M):
    print('À toi de jouer !')
    casePrise = True
    while casePrise:
        l = input("Ligne ? ")
        while not l:
            l = input("Ligne ?")
        l = int(l)-1
        c = input('Colonne ? ')
        while not c:
            c = input("Colonne ?")
        c = int(c)-1
        while (not 0 <= l <= N-1):
            l = int(input('0 ≤ ligne <', N, 'svp ? '))
        while (not 0 <= c <= M-1):
            c = int(input('0 ≤ colonne <', M, 'svp ? '))
        if casesD[l][c]:
            print('Case déjà dévoilée, recommencez')
        else:
            casePrise = False
    return l, c


def victoire(grille, casesD, N, M):
    for l in range(N):
        for c in range(M):
            if not grille[l][c] and not casesD[l][c]:
                return False
    return True


def decimateCase(grille, casesD, l, c, add, listeToDecimate):
    for i in range(l-1, l+2):
        for j in range(c-1, c+2):
            if i >= 0 and i < len(grille) and j >= 0 and j < len(grille[l]):
                add.append([i, j])
                if compteMinesVoisines(grille, i, j) == 0 and not grille[i][j]:
                    if not casesD[i][j]:
                        listeToDecimate.append([i, j])
                casesD[i][j] = True


def decimator3000(grille, casesD, l, c):
    add = []
    ligne = l
    case = c
    listeToDecimate = [[ligne, case]]
    while len(listeToDecimate) != 0:
        for i in listeToDecimate:
            ligne = i[0]
            case = i[1]
            if ligne == l and case == c:
                decimateCase(grille, casesD, ligne, case, add, listeToDecimate)
                listeToDecimate.remove([ligne, case])
            elif casesD[ligne][case] and grille[ligne][case] == 0 and compteMinesVoisines(grille, ligne, case) == 0:
                decimateCase(grille, casesD, ligne, case, add, listeToDecimate)
                listeToDecimate.remove([ligne, case])
    for i in add:
        casesD[i[0]][i[1]] = True


# PROGRAMME PRINCIPAL

N = int(input('Nombre de lignes : '))
M = int(input('Nombre de colonnes : '))
grille = creerGrille(N, M)
drapeau = creerGrille(N, M)

X = int(input('Nombre de mines : '))
while X >= N*M-8:
    X = int(input('Nombre de mines : '))

# Premier coup
nbCoups = 1
print('\nCoup numéro', nbCoups)
casesD = [[False for j in range(M)] for i in range(N)]
afficheJeu(grille, casesD, drapeau)
l, c = getCoords(casesD, N, M)
casesD[l][c] = True
placerMines(grille, N, M, X, l, c)
if compteMinesVoisines(grille, l, c) == 0:
    decimator3000(grille, casesD, l, c)

perdu = False
gagne = victoire(grille, casesD, N, M)


# Tour de jeu
while not gagne and not perdu:
    print('\nCoup numéro', nbCoups)
    afficheJeu(grille, casesD, drapeau)
    l, c = getCoords(casesD, N, M)
    drap = input(
        'Placer un drapeau ?\n⏎ pour ignorer, 1 pour placer, 0 pour suprr. : ')
    if drap == '':
        nbCoups += 1
        casesD[l][c] = True
        if testMine(grille, l, c):
            perdu = True
        if compteMinesVoisines(grille, l, c) == 0 and not perdu:
            decimator3000(grille, casesD, l, c)
        gagne = victoire(grille, casesD, N, M)
    elif drap == '1':
        drapeau[l][c] = 1
    elif drap == '0':
        drapeau[l][c] = 0


if gagne:
    print('\nBravo, tu gagnes en', nbCoups, 'coups !\n')
    casesD = [[True for j in range(M)] for i in range(N)]
    afficheJeu(grille, casesD, drapeau)

else:
    print('\nPerdu, touché une mine !')
    print('\nTon jeu :')
    afficheJeu(grille, casesD, drapeau)
    print('\nLa solution était :')
    afficheSolution(grille)
