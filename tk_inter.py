from tkinter import *

def cotacao():
    texto=f"""
    Dolar:{entrada.get()}
    Euro:5,23
    Ouro:300
    """
    mostrar["text"]=texto
    return texto

janela=Tk()
janela.geometry("100x150")
janela.title("Cotação")

texto=Label(janela,text="escreva")
texto.grid(column=0,row=0,padx=40)

entrada=Entry(janela,width=10)
entrada.grid(column=0,row=1)

but=Button(janela,text="clique",bg="green",command=cotacao)
but.grid(column=0,row=2)

mostrar=Label(janela,text="")
mostrar.grid(column=0,row=3)

janela.mainloop()