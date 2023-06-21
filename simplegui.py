import PySimpleGUI as sg

# sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
# 'BACKGROUND': '#00baaf', 
# 'TEXT': '#000000', 
# 'INPUT': '#339966', 
# 'TEXT_INPUT': '#000000', 
# 'SCROLL': '#99CC99', 
# 'BUTTON': ('#003333', '#FFCC66'), 
# 'PROGRESS': ('#D1826B', '#CC8019'), 
# 'BORDER': 1, 'SLIDER_DEPTH': 0,  
# 'PROGRESS_DEPTH': 0
# } 
# sg.theme('MyCreatedTheme')                       

layout=[
    [sg.Text("texto")],
    [sg.InputText(key="inp1")],
    [sg.Button("guardar"),sg.Text("  ",key="t1"),sg.Button("limpar"),sg.Text("  ",key="t2"),sg.Button("Cancelar")],
    [sg.Text("",key="text")]
]

window=sg.Window("titulo",layout)

def loop():
    event = True
    while event and event!="Cancelar":
        event,value = window.read()
        if event == "guardar":
            window["text"].update("Valor Digitado: "+value["inp1"])
            window["t1"].update("█")
            window["t2"].update("  ")
        if event == "limpar":
            window["t1"].update("  ")
            window["t2"].update("█")
            window["text"].update("")
    window.close()
loop()