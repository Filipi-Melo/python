def main():
    registro, resposta = [], ''
    textos = ["\nDigite o seu nome: ","Digite o seu sobrenome: ","Digite sua senha: "]
    
    while resposta != 'não':
        resposta = input("Deseja se registrar?\nDigite 'sim' ou 'não':")
        if resposta =='sim':
            registro.append([input(t) for t in textos])
            print()
    
    print('\n\nUsuários registrados:')
    
    for usuario in registro:
        print("--------------------------")
        print('\n'.join(t + v for t,v in zip(["Nome: ","Sobrenome: ","Senha: "],usuario)))

if __name__ == '__main__': main()