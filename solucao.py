from typing import Iterable, Set, Tuple, Optional

class Nodo:
    def __init__(self, estado:str, pai:Optional['Nodo'], acao:str, custo:int):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
               

def swapString (string:str, ind1:int, ind2:int):
    if ind1 != 0 and ind2 != (len(string) - 1):
        nova_string = f"{string[:ind1]}{string[ind2]}{string[ind1 + 1:ind2]}{string[ind1]}{string[ind2+1:]}"
    elif ind1 == 0:
        nova_string = f"{string[ind2]}{string[ind1 + 1:ind2]}{string[ind1]}{string[ind2+1:]}"
    else:
        nova_string = f"{string[:ind1]}{string[ind2]}{string[ind1 + 1:ind2]}{string[ind1]}"
    
    return nova_string
    

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    
    tuplas = []

    index = estado.find('_')

    if (index + 3) in range(9): #Movimento para baixo
        novo_estado = swapString(estado, index, index + 3)
        tuplas.append(("abaixo", novo_estado))
    if (index - 3) in range(9): #Movimento para cima
        novo_estado = swapString(estado, index - 3, index)
        tuplas.append(("acima", novo_estado))
    if (index - 1) not in [-1, 2, 5]: #Movimento para a esquerda
        novo_estado = swapString(estado, index - 1, index)
        tuplas.append(("esquerda", novo_estado))
    if (index + 1) not in [3, 6, 9]: #Movimento para a direita
        novo_estado = swapString(estado, index, index + 1)
        tuplas.append(("direita", novo_estado))

    return tuplas


def expande(nodo:Nodo)->Set[Nodo]:

    novos_nodos = []

    for no in sucessor(nodo.estado):
        novo_nodo = Nodo(estado = no[1], pai = nodo, acao = no[0], custo = nodo.custo + 1)
        novos_nodos.append(novo_nodo)
    
    return novos_nodos
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """

def custoHamming (estado):
    custo = 0
    for index, char in enumerate('12345678_'):
        if char != estado[index]:
            custo += 1
    
    return custo

def astar_hamming (estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """

    X = set()
    F = {custoHamming(estado):[Nodo(estado, None, None, 0)]}
    caminho = []

    while True:
        
        if len(F) != 0:
            for nodo_atual in F.pop(min(F)):
                if nodo_atual.estado == '12345678_':
                    while(nodo_atual.pai != None):
                        caminho.append(nodo_atual.acao)
                        nodo_atual = nodo_atual.pai
                    return caminho[::-1]
                if nodo_atual.estado not in X:
                    X.add(nodo_atual.estado)
                    for novo_nodo in expande(nodo_atual):
                        if novo_nodo.estado not in X:
                            if (custoHamming(novo_nodo.estado) + novo_nodo.custo) in F:
                                F[custoHamming(novo_nodo.estado) + novo_nodo.custo].append(novo_nodo)
                            else:
                                F[custoHamming(novo_nodo.estado) + novo_nodo.custo] = [novo_nodo]
        else:
                return None
                    

def custoManhattan (estado):
    custo = 0
    for index_modelo, char_modelo in enumerate('12345678_'):
        index_nodo = estado.find(char_modelo)
        if char_modelo == '_':
            char_modelo = 9
        else:
            char_modelo = int(char_modelo)
        if abs(((char_modelo - 1) - index_nodo)) == 1 or abs(((char_modelo -1) - index_nodo)) == 3: 
            custo += 1
        elif abs(((char_modelo - 1) - index_nodo)) == 8:
            custo += 4
        elif abs(((char_modelo - 1) - index_nodo))%2 == 0 and abs(((char_modelo - 1) - index_nodo)) != 0:
            custo += 2
        elif abs(((char_modelo - 1) - index_nodo)) == 5 or abs(((char_modelo -1) - index_nodo)) == 7:
            custo += 3    

    return custo


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    X = set()
    F = {custoManhattan(estado):[Nodo(estado, None, None, 0)]}
    caminho = []

    while True:
        
        if len(F) != 0:
            for nodo_atual in F.pop(min(F)):
                if nodo_atual.estado == '12345678_':
                    while(nodo_atual.pai != None):
                        caminho.append(nodo_atual.acao)
                        nodo_atual = nodo_atual.pai
                    return caminho[::-1]
                if nodo_atual.estado not in X:
                    X.add(nodo_atual.estado)
                    for novo_nodo in expande(nodo_atual):
                        if novo_nodo.estado not in X:
                            if (custoManhattan(novo_nodo.estado) + novo_nodo.custo) in F:
                                F[custoManhattan(novo_nodo.estado) + novo_nodo.custo].append(novo_nodo)
                            else:
                                F[custoManhattan(novo_nodo.estado) + novo_nodo.custo] = [novo_nodo]
        else:
                return None

#opcional,extra
#def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
#    raise NotImplementedError

#opcional,extra
#def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
#    raise NotImplementedError

#opcional,extra
#def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
#    raise NotImplementedError