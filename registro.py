def registrar():
    registro, resposta = [], ''
    while resposta != 'não':
        resposta = input("Deseja se registar?\nDigite 'sim' ou 'não': ")
        if resposta =='sim':
            text = ["\nDigite o seu nome: ","Digite o seu sobrenome: ","Digite sua senha:"]
            for i in range(3): registro.append(input(text[i]))
    
    print('\nUsuários registrados:')
    for i in range(0,len(registro),3):
        print("--------------------------")
        for x in range(3): print(["Nome: ","Sobrenome: ","Senha: "][x] + registro[i+x])

if __name__ == '__main__': registrar()