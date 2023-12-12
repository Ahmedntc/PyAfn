import numpy as np

class Automato:
    def __init__(self) -> None:
        self.palavras = []
        self.alfabeto = []
        self.estados = []
        self.estado_inicial = ""
        self.estados_finais = []
        self.transicoes = []
    

    def converter_afnde_para_afn(self):
        print("Convertendo AFNDE para AFN...")
        #fecho lambda dict
        fecho = self.fecho_lambda()
        new_transicoes = []
        
        # a nova transiçao de um estado sera os estados pertencentes ao fecho desse estado 
        # entao exemplo B o fecho é B e C
        # as novas transições de serao o fecho do estado que ele alcança com a letra a e o fecho do estado que C alcança com a letra a 
        # e assim segue para todas letras
        for estado in self.estados:
            fecho_estado = fecho[estado]
            for q in fecho_estado:
                for transicao in self.transicoes:
                    if transicao[0] == q and transicao[1] != 'ê':
                        destino = fecho[transicao[2]]
                        for estado_destino in destino:
                            new_transicoes.append((estado, transicao[1], estado_destino))
                            
        self.transicoes = new_transicoes

    def fecho_lambda(self):
        fec_lamb = {}
        
        for estado in self.estados:
            #fecho lambda de um estado sempre vai ser ele mesmo
            fec_lamb[estado] = estado 
            #fecho lambda de um estado vai ser ele mesmo mais os estados que ele alcança com lambda lambda = ê
            for transicao in self.transicoes:
                #se o estado atual for igual ao estado inicial da transição e a letra for lambda
                if estado == transicao[0] and transicao[1] == 'ê':
                    #adiciona o estado final da transição ao fecho lambda do estado atual
                    fec_lamb[estado] += transicao[2]   
        
        return fec_lamb
    
    def conversor_afnd_afd(self):
        pass



# Função que recebe estado inicial, estado final, palavra e a matriz de transições
def verificar_palavra(palavra, afd):
    atual = afd.estado_inicial
    # Para cada letra na palavra
    for letra in palavra:
        # Lê cada linha da matriz
        for linha in afd.transicoes:
            # Se o estado atual for o mesmo que o estado inicial e a letra for a mesma que a letra na matriz
            if linha[0] == atual and linha[1] == letra:
                # Altera o estado atual para o estado na matriz
                atual = linha[2]
                break

    # Se o estado atual estiver no array de estados finais, retorna true
    if atual in afd.estados_finais:
        return True
    
    else:
        return False
    


if __name__ == '__main__':
    # Criando o objeto automato
    af = Automato()

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
                af.alfabeto = partes[1:]
            elif partes[0] == 'Q':
                af.estados = partes[1:]
            elif partes[0] == 'q':
                af.estado_inicial = partes[1]
            elif partes[0] == 'F':
                af.estados_finais = partes[1:]
            elif partes[0] == 'T':
                af.transicoes.append((partes[1], partes[2], partes[3]))
            elif partes[0] == 'P':
                af.palavras.append(partes[1])

    # Imprimindo as variaveis do automato
    """   
    print('Alfabeto: ', af.alfabeto)
    print('Estados: ', af.estados)
    print('Estado Inicial: ', af.estado_inicial)
    print('Estados Finais: ', af.estados_finais)
    print('Transições: ', af.transicoes)
    print('Palavras: ', af.palavras) 
    """
    
    #escreva em um txt as informações do automato
    with open('out.txt', 'w') as arquivo:
        arquivo.write('Automato a ser testado e suas características: ' + '\n\n')
        arquivo.write('Alfabeto A: ' + ' '.join(af.alfabeto) + '\n')
        arquivo.write('Estados Q: ' + ' '.join(af.estados) + '\n')
        arquivo.write('Estado inicial q: ' + af.estado_inicial + '\n')
        arquivo.write('Estados finais F: ' + ' '.join(af.estados_finais) + '\n')
        arquivo.write('\n' + 'Transicoes originais: ' + '\n')
        for transicao in af.transicoes:
            arquivo.write('T ' + ' '.join(transicao) + '\n')
        arquivo.write('\n' + 'Palavras: ' + '\n')
        for palavra in af.palavras:
            arquivo.write('P ' + palavra + '\n')
            
        #resultado da verificação de cada palavra
        
    print("Transições antes da conversão:")
    print(af.transicoes)

    af.converter_afnde_para_afn()

    print("\nTransições depois da conversão para afnd:")
    print(af.transicoes)
    
    #af.conversor_afnd_afd()
    #print("\nTransições depois da conversão para afd:")
    #print(af.transicoes)
    
    afdTeste = Automato()
    afdTeste = af
    # testando se a palavra é aceita pelo automato quando passo um afd
    afdTeste.transicoes = [
    ('A', 'a', 'B'),
    ('A', 'b', 'C'),
    ('B', 'a', 'D'),
    ('B', 'b', 'C'),
    ('C', 'a', 'B'),
    ('C', 'b', 'D'),
    ('D', 'a', 'D'),
    ('D', 'b', 'D'),
    ]

    print('\nTransições para teste: ', afdTeste.transicoes)
    palavra = 'bb'
    print('Verificando palavras: ')
    print('Palavra: ', palavra)
    print('Resultado: ', verificar_palavra(palavra, afdTeste))
    print()
    
    
    




