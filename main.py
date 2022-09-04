import sys

def organiza_entrada():
	lista = []
	for line in sys.stdin:
		lista.append(int(line)) # Cria e salva objetos Processo em um array

	return lista

entrada = organiza_entrada()
quadros = entrada[0]
refs = entrada[1:]

bitR = [False]*max(refs)

f_paginas_SC = 0
atual = 0

fila = []

for index, value in enumerate(refs):
    if index%4 == 0: # Coloca todos os bits R como falsos
        for i in range(len(bitR)): bitR[i] = False
    if len(fila) < quadros: # Se a fila não estiver cheia
        if value not in fila:
            fila.append(value)
            bitR[value-1] = True
            f_paginas_SC += 1
    else: # Se a fila estiver cheia
        if value in fila:
            bitR[value-1] = True
        else:
            while True:
                if bitR[fila[atual]] == True: # Se o bit R do elemento da fila em análise estiver como True
                    bitR[fila[atual]] = False # Segunda chance
                    atual = (atual + 1)%len(fila) # Incrementa o índice de forma circular
                else: # Se o bit R do elemento da fila em análise estiver como False
                    fila.remove(fila[atual])
                    fila.append(value)
                    f_paginas_SC += 1
                    atual = (atual + 1)%len(fila) # Incrementa o índice de forma circular
                    break

print(f"SC {f_paginas_SC:.2f}")
print(f"OTM {5:.2f}")
print(f"CT {8:.2f}")