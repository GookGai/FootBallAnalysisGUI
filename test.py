import io
import os
import PySimpleGUI as sg
from abc import *
from PIL import Image

sg.theme('Material1') 
file_layout = [
    [
        sg.Text("Choose folder"),
        sg.In(size=(10,2), enable_events=True ,key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[],enable_events=True,size=(30,400),key="FILE_LIST"
        ),
        
    ]
]

mode_sel =[
    [   
        sg.Button("ภาพรวม",size=(20,1)),
        sg.Button("ค่าเฉลี่ย",size=(20,1)),
    ]
]

output_column = [
    [sg.Text("Choose mode from the left side")],
    # [sg.Text(size=(40,1),key="-TOUT-")],
    [sg.Image( size=(300,300),key="-IMAGE-")],
    [sg.Button("ภาพรวม",size=(200,2))],
]


layout =[
    [
        sg.Column(file_layout),
        sg.VSeperator(),
        sg.Column(output_column),
    ]
]

window = sg.Window("demo",layout,size=(1200,600))
while True:
    event, values = window.read()
    if event ==sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder =values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list =[]
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder,f))
            and f.lower().endswith((".png",".gif"))
        ]
        window["FILE_LIST"].update(fnames)
    elif event == "FILE_LIST":
        try:
            filenames = os.path.join(values["-FOLDER-"],values["FILE_LIST"][0])
            # image = Image.open(filename)
            # image.thumbnail((400,400))
            image = Image.open(filenames)
            image.thumbnail((900, 800))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
            # window["-IMAGE-"].update(filename = filenames )
        except:
            pass
    if event == "ภาพรวม" :
        sg.popup('You entered')
    # if event == "FILE_LIST":
    #     sg.popup('You entered')

window.close()