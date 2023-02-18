from getpass import getpass

if __name__=='__main__':
    name = input("Digte o nome: ")
    password = getpass("Digte a senha: ")

    print('nome: ',name,'\n','senha: ',password)
    print('fim')