import sys

def organiza_entrada():
	lista = []
	for line in sys.stdin:
		lista.append(int(line.strip()))

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
    if index%4 == 0: # Coloca todos os bits R como falsos a cada 4 referências
        for i in range(len(bitR_SC)): bitR_SC[i] = False
    if len(filaSC) < quadros: # Se a fila não estiver cheia
        if value not in filaSC:
            filaSC.append(value)
            f_paginas_SC += 1
        bitR_SC[value-1] = True
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
del bitR_SC, f_paginas_SC, filaSC, atual

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
del f_paginas_OTM, filaOTM

# ------------------------------------- CONJUNTO DE TRABALHO -------------------------------------------
from random import randint

def fora_conj_trabalho(fila, R, tempos, tempo_atual, limiar):
    menor_tempo = 10000
    ind_menor_tempo = -1
    
    for index, value in enumerate(fila): # Iteração sobre a fila
        ind = value-1
        if R[ind]: # Se R == True
            tempos[ind] = tempo_atual
        else: # Se R == False
            age = tempo_atual - tempos[ind]
            if age > limiar: # Se a idade da página for maior que o limiar
                return index
            else: # age <= limiar
                if tempos[ind] < menor_tempo: # If para guardar a página com bitR == False mais antiga
                    menor_tempo = tempos[ind]
                    ind_menor_tempo = index

    # Chegar nesse ponto significa que nenhuma página com bitR == False e com age > limiar
    # foi encontrada. Logo, deve ser retornado o índice da página com bitR == False mais
    # antiga. Se ind_menor_tempo == -1, significa que não há nenhuma página com bitR == False,
    # então uma página escolhida aleatoriamente será removida do conjunto.
    return ind_menor_tempo if ind_menor_tempo != -1 else randint(0, len(fila)-1)

bitR_CT = [False]*max(refs)
tempos = [0]*max(refs)
limiar = quadros/2 + 1

f_paginas_CT = 0
filaCT = []

for index, value in enumerate(refs):
    if index%4 == 0: # Coloca todos os bits R como falsos a cada 4 referências
        for i in range(len(bitR_CT)): bitR_CT[i] = False
    if len(filaCT) < quadros: # Se a fila não estiver cheia
        if value not in filaCT:
            filaCT.append(value)
            f_paginas_CT += 1
    else: # Se a fila estiver cheia
        if value not in filaCT:
            ind = fora_conj_trabalho(filaCT, bitR_CT, tempos, index, limiar) # Descobre o índice da
            filaCT[ind] = value # Atualiza a página                          # página a ser substituída
            f_paginas_CT += 1
    bitR_CT[value-1] = True # Define o bit R da página como True
    tempos[value-1] = index # Atualiza o tempo em que a página foi referenciada

print(f"CT {f_paginas_CT:.2f}")
del bitR_CT, tempos, limiar, f_paginas_CT, filaCT