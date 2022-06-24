from ast import Pass
import io
import os
import PySimpleGUI as sg
from abc import *
from PIL import Image
from mplsoccer import Pitch, VerticalPitch
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
playerLists = {"ALL PLayer", ""}
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################


def cleanData(rawdata):
    global data, data15, data30, data45, dataShot, dataPass, dataPass15, dataPass30, dataPass45,cl,cr
    data = rawdata.replace("-", float(0))
    dataShot = data[(data['Event'] == 'ShotOnTarget') | (data['Event'] == 'ShotOffTarget')
                    | (data['Event'] == 'ShotGetGoal') | (data['Event'] == 'ShotBlock')]
    Cornerpass = data[(data['Event'] == 'CornerLeft') | (data['Event'] == 'CornerRight')]
    if(len(dataShot) > 0 ):
        a = dataShot['X']
    else:
        a = Cornerpass['X']
    a = a.reset_index()
    if(a['X'][0] > 60):
        data['X'] = data['X']*1.2
        data['Y'] = data['Y']*.8
        data['X2'] = data['X2']*1.2
        data['Y2'] = data['Y2']*.8
        data15 = data[(data['Mins'] <= 15)]
        data30 = data[(data['Mins'] <= 30) & (data['Mins'] > 15)]
        data45 = data[(data['Mins'] <= 45) & (data['Mins'] > 30)]
    else:
        data['X'] = 120-data['X']*1.2
        data['Y'] = 80-data['Y']*.8
        data['X2'] = 120-data['X2']*1.2
        data['Y2'] = 80-data['Y2']*.8
        data15 = data[(data['Mins'] <= 60) & (data['Mins'] > 45)]
        data30 = data[(data['Mins'] <= 75) & (data['Mins'] > 60)]
        data45 = data[(data['Mins'] <= 90) & (data['Mins'] > 75)]

    dataShot = data[(data['Event'] == 'ShotOnTarget') | (data['Event'] == 'ShotOffTarget') |
                    (data['Event'] == 'ShotGetGoal') | (data['Event'] == 'ShotBlock')]
    dataPass = data[(data['Event'] == 'Pass') | (data['Event'] == 'go') |
                    (data['Event'] == 'Passfail') | (data['Event'] == 'Cross') | (data['Event'] == 'Assist')]
    dataPass15 = data15[(data15['Event'] == 'Pass') | (data15['Event'] == 'go') |
                        (data15['Event'] == 'Passfail') | (data15['Event'] == 'Cross') | (data15['Event'] == 'Assist')]
    dataPass30 = data30[(data30['Event'] == 'Pass') | (data30['Event'] == 'go') |
                        (data30['Event'] == 'Passfail') | (data30['Event'] == 'Cross') | (data30['Event'] == 'Assist')]
    dataPass45 = data45[(data45['Event'] == 'Pass') | (data45['Event'] == 'go') |
                        (data45['Event'] == 'Passfail') | (data45['Event'] == 'Cross') | (data45['Event'] == 'Assist')]
    cl = data[data['Event'] == 'CornerLeft']
    cr = data[data['Event'] == 'CornerRight']

    dataShot = dataShot.reset_index()
    dataPass = dataPass.reset_index()
    dataPass15 = dataPass15.reset_index()
    dataPass30 = dataPass30.reset_index()
    dataPass45 = dataPass45.reset_index()
    print("clean data finished")
    return(data, data15, data30, data45, dataShot, dataPass, dataPass15, dataPass30, dataPass45,cl,cr)


def shotmap(data1, mode):
    cleanData(data1)
    shX = dataShot['X']
    shY = dataShot['Y']
    shName = dataShot['Player']
    shsty = dataShot['Event']

    sout = dataShot[dataShot['Event'] == 'ShotOffTarget']
    sot = dataShot[dataShot['Event'] == 'ShotOnTarget']
    sb = dataShot[dataShot['Event'] == 'ShotBlock']
    sgg = dataShot[dataShot['Event'] == 'ShotGetGoal']

    img = plt.imread("vll.jpg")
    ext = [0.0, 120.0, 0.00, 80.0]
    plt.scatter(dataShot['X'],dataShot['Y'],s = 150, alpha=0.8,cmap='viridis')
    plt.scatter(dataShot['X'],dataShot['Y'],s = 150, alpha=0.8,cmap='viridis')
    plt.imshow(img, extent=ext ,aspect='auto')
    fileName = 'Vle Attacking'
    c = plt.savefig(fileName + '.png')
    return c


def shotmappercent(data,k):
    cleanData(data)
    sout = dataShot[dataShot['Event'] == 'ShotOffTarget']
    sot = dataShot[dataShot['Event'] == 'ShotOnTarget']
    sb = dataShot[dataShot['Event'] == 'ShotBlock']
    sgg = dataShot[dataShot['Event'] == 'ShotGetGoal']
    sout = sout.reset_index()
    sot = sot.reset_index()
    sb = sb.reset_index()
    sgg = sgg.reset_index()

    pitch = VerticalPitch(pitch_length=100, pitch_width=100,axis=True, pitch_color='#538053')
    fig, ax = pitch.draw(nrows=1,  ncols=2, figsize=(20, 10))
    bins = [(6, 5), (12, 5)]
    if k == 0:
        for i, bin in enumerate(bins):
            binstatistic = pitch.bin_statistic(dataShot['X'], dataShot['Y'], statistic='count', bins=bin)
            pitch.heatmap(binstatistic, ax=ax[i], cmap="Oranges", edgecolors="#22312b", alpha=0.4)
            pitch.scatter(dataShot['X'], dataShot['Y'],c='gray', ax=ax[i], s=25)
            binstatistic['statistic'] = (pd.DataFrame((binstatistic['statistic']/binstatistic['statistic'].sum())).applymap(lambda x: '{:.0%}'.format(x)).values)
            pitch.label_heatmap(binstatistic, color='black',
                                fontsize=20, ax=ax[i], ha='center', va='bottom')
    title = fig.suptitle('Attacking Area', fontsize=50)
    fileName = 'AttackingArea'
    plt.savefig(fileName + '.png')
    return fig


def genname(data):
    playerList = pd.read_csv(file_index).Player.unique()


####################################################################################################################################
####################################################################################################################################


def genGraph01(file_index, v):
    p = shotmap(pd.read_csv(file_index), v)
    filenames = os.path.join("Vle Attacking.png")
    # image = Image.open(filename)
    # image.thumbnail((400,400))
    image = Image.open(filenames)
    image.thumbnail((1200, 800))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())


def genGraph02(file_index,k):
    p = shotmappercent(pd.read_csv(file_index),k)
    filenames = os.path.join("AttackingArea.png")
    # image = Image.open(filename)
    # image.thumbnail((400,400))
    image = Image.open(filenames)
    image.thumbnail((1200, 800))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())


def GraphPosition():
    if values["FILE_LIST"][0] == "ภาพรวม":
        if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
            try:
                genGraph02(file_index,0)
            except:
                sg.popup("please check your data Input2")
        else:
            try:
                genGraph01(file_index,0)
            except:
                sg.popup("please check your data Input")

    # if values["FILE_LIST"][0] == "ได้ประตู":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,4)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 4)
    #         except:
    #             sg.popup("please check your data Input")

    # if values["FILE_LIST"][0] == "ยิงเข้ากรอบ":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,2)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 2)
    #         except:
    #             sg.popup("please check your data Input")

    # if values["FILE_LIST"][0] == "ยิงออก":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,1)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 1)
    #         except:
    #             sg.popup("please check your data Input")

    # if values["FILE_LIST"][0] == "ยิงติดบล็อก":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,3)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 3)
    #         except:
    #             sg.popup("please check your data Input")

    # if values["FILE_LIST"][0] == "เตะมุมซ้าย":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,5)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 5)
    #         except:
    #             sg.popup("please check your data Input")
    
    # if values["FILE_LIST"][0] == "เตะมุมขวา":
    #     if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
    #         try:
    #             genGraph02(file_index,6)
    #         except:
    #             sg.popup("please check your data Input2")
    #     else:
    #         try:
    #             genGraph01(file_index, 1, 6)
    #         except:
    #             sg.popup("please check your data Input")
    
    # if values["FILE_LIST"][0] == "เตะมุมขวา":
    #     sg.popup("ยังไม่ได้ทำ")



####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
sg.theme('Dark2')
file_layout = [
    [
        sg.Text("Choose file"),
        sg.In(size=(15, 2), enable_events=True, key="-FILE-"),
        sg.FileBrowse(),
    ],
    [
        sg.Listbox(
            values=["ภาพรวม", "ได้ประตู", "ยิงเข้ากรอบ", "ยิงออก", "ยิงติดบล็อก","เตะมุมซ้าย",'เตะมุมขวา',"Mark"], enable_events=True, size=(30, 12), key="FILE_LIST"
        ),

    ],
    [
        sg.Text("Choose Mode"),
    ],
    [

        sg.Listbox(
            values=["ตำแหน่ง", "เปอร์เซ็นต์"], enable_events=True, size=(30, 2), key="MODE_LIST"
        ),

    ],
    [
        sg.Text("Choose Player Name"),
    ],
    [

        sg.Listbox(
            values=[], enable_events=True, size=(30, 15), key="NAME_LIST"
        ),

    ],
    [sg.Button("ทั้งหมด", size=(25, 1))],
]

# mode_sel =[
#     [
#         sg.Button("ภาพรวม",size=(20,1)),
#         sg.Button("ค่าเฉลี่ย",size=(20,1)),
#     ]
# ]

output_column = [
    [sg.Text("Choose mode from the left side")],
    # [sg.Text(size=(40,1),key="-TOUT-")],
    [sg.Image(size=(1000, 700), key="-IMAGE-")],
    [sg.Button("ภาพรวม", size=(150, 2))],
]


layout = [
    [
        sg.Column(file_layout),
        sg.VSeperator(),
        sg.Column(output_column),
    ]
]

window = sg.Window("Gaiyang", layout, size=(1400, 720), resizable=True)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-FILE-":
        file_index = values["-FILE-"]
        try:
            playerList = pd.read_csv(file_index).Player.unique()
            print(playerList[2])
            print(len(playerList))
        except:
            playerLists = []
        # for i in range(len(playerList)):
        #     playerLists[i+1] = playerList[i]
        #     print("123")
        window["NAME_LIST"].update(playerList)

    if event == "FILE_LIST":
        try:
            GraphPosition()
        except:
            pass
            # window["-IMAGE-"].update(filename = filenames )
    # if event == "FILE_LIST":
    #     sg.popup('You entered')
    if event == "MODE_LIST":
        try:
            GraphPosition()
        except:
            sg.popup("please check your data Input3")
window.close()
