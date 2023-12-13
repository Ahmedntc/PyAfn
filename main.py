#############################################################
#
#       Trabalho de Teoria da computação
#              AHMED BAKRI E MATHEUS MIRANDA
#                   12/12/2023
#
############################################################
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
        # as novas transições dele serao o fecho do estado que ele alcança com a letra a e o fecho do estado que C alcança com a letra a 
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
    
    
    #afnd Para afd implementaçao
    #para cada estado veremos as transiçoes dele com uma determinada letra se tiver mais de uma criamos um estado novo 
    # que é a junçao dos estados destinos com tal letra
    #exemplo estado A com b vai para A, B e C então teremos um novo estado ABC

    #criar nova matriz de transições
    #se o estado tiver apenas um estado destino lendo determinada letra a transicao dele permanece a mesma 
    #agora se ele tiver multiplos estados destino lendo determinada letra a transicao dele vai ser o estado novo que é a juncao desses estados
    #o estado resultante dessa junção tera as mesmas transições que os estados que o compoem exemplo ABC tem as mesmas transições que A, B e C
    #exemplo A com b vai para A, B e C então teremos um novo estado ABC que com a letra b vai para ABC e com a letra a vai para A
    def conversor_afnd_afd(self):
        print("Convertendo AFND para AFD...")

        new_trans = []
        aux= []

        #converte as transicoes dos estado A, B, e C que são não deterministico para deterministico 
        # ou seja agora vao para um estado como ABC que é a junção de A, B e C
        for estado in self.estados:
            for letra in self.alfabeto:
                new_state = ""
                for transicao in self.transicoes:
                    if transicao[0] == estado and transicao[1] == letra:
                        #quando um estado lendo uma letra tiver multiplos estados 
                        #cria se um estado novo que é juncao desses estados
                        new_state += transicao[2]
                if new_state != "":
                    new_trans.append((estado, letra, new_state))
                aux.append(new_state)
                
        for q in aux:
        #remover os estados que se repetem e os estados que já fazem parte de self.estados
            if q == "" or q in self.estados:
                aux.remove(q)
            
        aux = list(set(aux))
        aux2 = []   
        #para cada estado uniao exemplo DC as transições dele tem que ser as transições de D e C 
        # exemplo se lendo b D vai para D e C vai para CA então DC vai para DCA 
        # (apenas exemplo didatico no automato nao e exatamente assim)
        for qJunction in aux:
            qlist = list(qJunction)
            #oldDestino = ""
            prevTrans = ()
            for letra in self.alfabeto:
                new_state = ""
                for q in qlist:
                        for transicao in new_trans:
                            if transicao[0] == q and transicao[1] == letra:
                                currTrans = (qJunction, letra, transicao[2])
                                if currTrans != prevTrans:
                                    new_trans.append((qJunction, letra, transicao[2]))
                                    
                                prevTrans = (qJunction, letra, transicao[2])
                                
                                if currTrans[0] == prevTrans[0] and prevTrans[1] == currTrans[1]:
                                    new_state += currTrans[2]
                                
            new_state = list(set(new_state))
            new_state = "".join(sorted(new_state)) 
            
            aux2.append(new_state)
        
        #tratamento de estados que se repetem no novo estado
        for q in aux2:
            if q in aux or q[::-1] in aux:
                aux2.remove(q)
            else:
                aux.append(q)
        
        
        new_trans2 = []
        new_state = ""  
        for qJunction in aux2:
            qlist = list(qJunction)
            #oldDestino = ""
            prevTrans = ()
            for letra in self.alfabeto:
                new_state = list(set(new_state))
                new_state = "".join(sorted(new_state)) 
                if new_state not in aux2 and new_state != "":
                    aux2.append(new_state)
                    
                new_state = ""
                for q in qlist:
                        for transicao in new_trans:
                            if transicao[0] == q and transicao[1] == letra:
                                currTrans = (qJunction, letra, transicao[2])
                                if currTrans != prevTrans:
                                    new_trans2.append((qJunction, letra, transicao[2]))
                                    
                                prevTrans = (qJunction, letra, transicao[2])
                                
                                if currTrans[0] == currTrans[0] and prevTrans[1] == currTrans[1]:
                                    new_state += currTrans[2]
 
            new_state = list(new_state)
            new_state = "".join(sorted(new_state)) 

        for y in aux2:
            for x in aux2[1:]:
                if y != x:
                    if sorted(y) == sorted(x):
                        aux2.remove(x)

        #removendo transicoes que sao repetidos mas com ordem diferente exemplo ABCD e DCBA sao a mesma transicao
        for trans in new_trans2:
            for nextrans in new_trans2[1:]:
                if trans[0] != nextrans[0]:
                    if sorted(trans[0]) == sorted(nextrans[0]):
                        new_trans2.remove(nextrans)   
            
            
            new_trans.append(trans)

        
        # definitivas = []
        # a = range(len(new_trans))
           
        # for i in a:
        #     for j in a:
        #         if i != j:
        #             if new_trans[i][0] == new_trans[j][0] and new_trans[i][1] == new_trans[j][1]:
        #                 destino = new_trans[i][2] + new_trans[j][2]
        #                 #remover estados que se repetem no destino e ordenar
        #                 destino = list(set(destino))
        #                 destino = "".join(sorted(destino))
                        
        #                 new_trans.append((new_trans[i][0], new_trans[i][1], destino))
        #                 new_trans.remove(new_trans[i])
        #                 diff = j - i   
        #                 new_trans.remove(new_trans[j - diff])
        #                 a = range(len(new_trans))
                        
        new_trans_processed = []
        processed_indices = set()

        for i in range(len(new_trans)):
            if i in processed_indices:
                continue

            for j in range(i + 1, len(new_trans)):
                if new_trans[i][0] == new_trans[j][0] and new_trans[i][1] == new_trans[j][1]:
                    destino = new_trans[i][2] + new_trans[j][2]
                    # Remover estados que se repetem no destino e ordenar
                    destino = "".join(sorted(set(destino)))

                    new_trans_processed.append((new_trans[i][0], new_trans[i][1], destino))
                    processed_indices.add(i)
                    processed_indices.add(j)
                    break

            if i not in processed_indices:
                new_trans_processed.append(new_trans[i])

        new_trans = new_trans_processed

  
        for st in aux2:
            if st not in aux:
                aux.append(st)
        
        
        #adicionar os estados novos a self.estados
        for q in aux:
            if q in self.estados:
                aux.remove(q) 
            else:   
                 self.estados.append(q)      


        for estado in self.estados:
            if self.estados_finais[0] in estado and estado != self.estados_finais[0]:
                self.estados_finais.append(estado)
        self.transicoes = new_trans
        
                            
                    
          
# Função que recebe estado inicial, estado final, palavra e a matriz de transições
def verificar_palavra(palavra, afd):
    atual = afd.estado_inicial
    # Para cada letra na palavra
    for letra in palavra:
        # Lê cada linha da matriz
        for linha in afd.transicoes:
            # Se o estado da transicao for o mesmo que o estado atual e a letra for a mesma que a letra na matriz
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
    
        
    print("Transições antes da conversão:")
    print(af.transicoes)

    af.converter_afnde_para_afn()

    print("\nTransições depois da conversão para afnd:")
    print(af.transicoes)
    
    af.conversor_afnd_afd()
    print("\nTransições depois da conversão para afd:")
    print(af.transicoes)
    with open('convertido.txt', 'w') as arquivo:
        arquivo.write('\n' + '# Automato Convertido' + '\n')
        arquivo.write('Alfabeto: ' + ' '.join(af.alfabeto) + '\n')
        arquivo.write('Conjunto de estados Q: ' + ' '.join(af.estados) + '\n')
        arquivo.write('Estado inicial q: ' + af.estado_inicial + '\n')
        arquivo.write('Estado final F: ' + ' '.join(af.estados_finais) + '\n')
        arquivo.write('Transições ' + '\n')
        for transicao in af.transicoes:
            arquivo.write('T ' + ' '.join(transicao) + '\n')
        
        
    with open('out.txt', 'w') as arquivo:
        for palavra in af.palavras:
            if verificar_palavra(palavra, af):
                arquivo.write(f'M aceita a palavra <{palavra}>' + '\n')
            else:
                arquivo.write(f'M rejeita a palavra <{palavra}>' + '\n')
    
        
        
    
        
    # afdTeste = Automato()
    # afdTeste = af
    # # testando se a palavra é aceita pelo automato quando passo um afd
    # afdTeste.transicoes = [
    # ('A', 'a', 'B'),
    # ('A', 'b', 'C'),
    # ('B', 'a', 'D'),
    # ('B', 'b', 'C'),
    # ('C', 'a', 'B'),
    # ('C', 'b', 'D'),
    # ('D', 'a', 'D'),
    # ('D', 'b', 'D'),
    # ]

    # print('\nTransições para teste: ', afdTeste.transicoes)
    # palavra = 'bb'
    # print('Verificando palavras: ')
    # print('Palavra: ', palavra)
    # print('Resultado: ', verificar_palavra(palavra, afdTeste))
    # print()
    
    
    




