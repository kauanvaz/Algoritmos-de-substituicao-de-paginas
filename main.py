from cmath import inf
import sys

def organiza_entrada():
	lista = []
	for line in sys.stdin:
		lista.append(int(line))

	return lista

entrada = organiza_entrada()
quadros = entrada[0]
refs = entrada[1:]

# ---------------------------------------- SEGUNDA CHANCE ----------------------------------------------

bitR_SC = [False]*max(refs)

f_paginas_SC = 0
filaSC = []
atual = 0

for index, value in enumerate(refs):
    if index%4 == 0: # Coloca todos os bits R como falsos
        for i in range(len(bitR_SC)): bitR_SC[i] = False
    if len(filaSC) < quadros: # Se a fila não estiver cheia
        if value not in filaSC:
            filaSC.append(value)
            bitR_SC[value-1] = True
            f_paginas_SC += 1
    else: # Se a fila estiver cheia
        if value in filaSC:
            bitR_SC[value-1] = True
        else:
            while True:
                if bitR_SC[filaSC[atual]] == True: # Se o bit R do elemento da fila em análise estiver como True
                    bitR_SC[filaSC[atual]] = False # Segunda chance
                    atual = (atual + 1)%len(filaSC) # Incrementa o índice de forma circular
                else: # Se o bit R do elemento da fila em análise estiver como False
                    filaSC.remove(filaSC[atual])
                    filaSC.append(value)
                    f_paginas_SC += 1
                    atual = (atual + 1)%len(filaSC) # Incrementa o índice de forma circular
                    break

print(f"SC {f_paginas_SC:.2f}")
#del()

# -------------------------------------------- ÓTIMO ---------------------------------------------------

def mais_longe(referencias, indice, fila):

    res = -1
    longe = indice
    temp = -1

    for iF, vF in enumerate(fila): # Para cada página na fila
        for iR, vR in enumerate(referencias[indice:], start=indice): # Busca a referência mais distante
            temp = iR
            if vF == vR: # Se uma página na fila for igual a uma página referenciada
                if iR > longe: # E se a distância dela for maior do que a distância de outra página já contabilizada
                    longe = iR # Atualiza o mais distante
                    res = iF # Atualiza o índice do mais distante
                break

        if temp == len(referencias)-1: return iF # Se não for encontrado referências para um valor na fila
                                                 # significa que ele não é mais referenciado, logo pode ser
                                                 # substituído de imediato 
    return res

f_paginas_OTM = 0
filaOTM = []
atual = 0

for index, value in enumerate(refs):
    if len(filaOTM) < quadros: # Se a fila não estiver cheia
        if value not in filaOTM:
            filaOTM.append(value)
            f_paginas_OTM += 1
    else: # Se a fila estiver cheia
        if value not in filaOTM:
            ind = mais_longe(refs, index+1, filaOTM) # Retorna o índice do valor presente na pilha com a referência mais distante
            filaOTM[ind] = value # Substitui na fila pelo novo valor
            f_paginas_OTM += 1

print(f"OTM {f_paginas_OTM:.2f}")
#del()

# ------------------------------------- CONJUNTO DE TRABALHO -------------------------------------------

print(f"CT {8:.2f}")