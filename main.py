import numpy as np

# Função que recebe estado inicial, estado final, palavra e a matriz de transições
def verificar_palavra(estado_inicial, estados_finais, palavra, matriz_transicoes):
    atual = estado_inicial
    # Para cada letra na palavra
    for letra in palavra:
        # Lê cada linha da matriz
        for linha in matriz_transicoes:
            # Se o estado atual for o mesmo que o estado inicial e a letra for a mesma que a letra na matriz
            if linha[0] == atual and linha[1] == letra:
                # Altera o estado atual para o estado na matriz
                atual = linha[2]
                break

    # Se o estado atual estiver no array de estados finais, retorna 1
    if atual in estados_finais:
        return True


if __name__ == '__main__':
    # Inicializando variáveis
    alfabeto = []
    estados = []
    estado_inicial = ""
    estados_finais = []
    transicoes = []
    palavras = []

    # Lendo o arquivo
    with open('automata.txt', 'r') as arquivo:
        for linha in arquivo:
            # Ignorando linhas que começam com #
            if linha.startswith('#'):
                continue
            
            # Removendo quebras de linha e dividindo a linha em palavras
            partes = linha.strip().split()

            # Verificando o tipo de informação na linha
            if partes[0] == 'A':
                alfabeto = partes[1:]
            elif partes[0] == 'Q':
                estados = partes[1:]
            elif partes[0] == 'q':
                estado_inicial = partes[1]
            elif partes[0] == 'F':
                estados_finais = partes[1:]
            elif partes[0] == 'T':
                transicoes.append((partes[1], partes[2], partes[3]))
            elif partes[0] == 'P':
                palavras.append(partes[1])

    # Exibindo as variáveis
    print("Alfabeto:", alfabeto)
    print("Estados:", estados)
    print("Estado Inicial:", estado_inicial)
    print("Estados Finais:", estados_finais)
    print("Transições:", transicoes)
    print("Palavras:", palavras)
    
    
    for palavra in palavras:
        verificar_palavra(estado_inicial, estados_finais, palavra, transicoes)



