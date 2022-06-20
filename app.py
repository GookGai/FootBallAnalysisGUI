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
    global data, data15, data30, data45, dataShot, dataPass, dataPass15, dataPass30, dataPass45
    data = rawdata.replace("-", float(0))
    dataShot = data[(data['Event'] == 'ShotOnTarget') | (data['Event'] == 'ShotOffTarget')
                    | (data['Event'] == 'ShotGetGoal') | (data['Event'] == 'ShotBlock')]
    a = dataShot['X']
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

    dataShot = dataShot.reset_index()
    dataPass = dataPass.reset_index()
    dataPass15 = dataPass15.reset_index()
    dataPass30 = dataPass30.reset_index()
    dataPass45 = dataPass45.reset_index()
    print("clean data finished")
    return(data, data15, data30, data45, dataShot, dataPass, dataPass15, dataPass30, dataPass45)


def shotmap(data, index, mode):
    cleanData(data)
    shX = dataShot['X']
    shY = dataShot['Y']
    shName = dataShot['Player']
    shsty = dataShot['Event']

    sout = dataShot[dataShot['Event'] == 'ShotOffTarget']
    sot = dataShot[dataShot['Event'] == 'ShotOnTarget']
    sb = dataShot[dataShot['Event'] == 'ShotBlock']
    sgg = dataShot[dataShot['Event'] == 'ShotGetGoal']

    pitch = VerticalPitch(pitch_length=100, pitch_width=100,
                          axis=True, pitch_color='#538053', half=True)
    fig, ax = pitch.draw(nrows=1,  ncols=1, figsize=(20, 10))

    # plt.scatter(dataShot['Y'],dataShot['X'],c='#BE2653',s = 700,marker = "*")
    if mode == 0:
        plt.scatter(sout['Y'], sout['X'], c='#fcf5e1', s=400, marker="o")
        plt.scatter(sot['Y'], sot['X'], c='#1E2453', s=300, marker="o")
        plt.scatter(sb['Y'], sb['X'], c='#1DD473', s=500, marker="P")
        plt.scatter(sgg['Y'], sgg['X'], c='#BF211E', s=700, marker="*")
        title = fig.suptitle('Total Shots', fontsize=40)
        for i in range(len(dataShot['X'])):
            plt.text(shY[i]-1, shX[i]-2.5, shName[i])
    if mode == 1:
        plt.scatter(sout['Y'], sout['X'], c='#fcf5e1', s=400, marker="o")
        title = fig.suptitle('Wide', fontsize=40)
        for i in range(len(dataShot['X'])):
            if shsty[i] == 'ShotOffTarget':
                plt.text(shY[i]-1, shX[i]-2.5, shName[i])
    if mode == 2:
        plt.scatter(sot['Y'], sot['X'], c='#1E2453', s=400, marker="o")
        title = fig.suptitle('On goal', fontsize=40)
        for i in range(len(dataShot['X'])):
            if shsty[i] == 'ShotOnTarget':
                plt.text(shY[i]-1, shX[i]-2.5, shName[i])
    if mode == 3:
        plt.scatter(sb['Y'], sb['X'], c='#1E2453', s=400, marker="o")
        title = fig.suptitle('Blocked', fontsize=40)
        for i in range(len(dataShot['X'])):
            if shsty[i] == 'ShotBlock':
                plt.text(shY[i]-1, shX[i]-2.5, shName[i])
    if mode == 4:
        plt.scatter(sgg['Y'], sgg['X'], c='#1E2453', s=400, marker="*")
        title = fig.suptitle('Goal', fontsize=40)
        for i in range(len(dataShot['X'])):
            if shsty[i] == 'ShotGetGoal':
                plt.text(shY[i]-1, shX[i]-2.5, shName[i])
#     ax[1].plt.scatter(sout['Y'],sout['X'],c='#fcf5e1',s = 400,marker = "o")

    # title = fig.suptitle('Attacking' + str(index), fontsize=50)
    fileName = 'Attacking' + str(index)
    plt.savefig(fileName + '.png')
    return fig


def shotmappercent(data):
    cleanData(data)
    shX = dataShot['X']
    shY = dataShot['Y']
    shName = dataShot['Player']
    shsty = dataShot['Event']

    sout = dataShot[dataShot['Event'] == 'ShotOffTarget']
    sot = dataShot[dataShot['Event'] == 'ShotOnTarget']
    sb = dataShot[dataShot['Event'] == 'ShotBlock']
    sgg = dataShot[dataShot['Event'] == 'ShotGetGoal']

    pitch = VerticalPitch(pitch_length=100, pitch_width=100,
                          axis=True, pitch_color='#538053')
    fig, ax = pitch.draw(nrows=1,  ncols=2, figsize=(20, 10))
    bins = [(6, 5), (12, 5)]
    for i, bin in enumerate(bins):
        binstatistic = pitch.bin_statistic(
            dataShot['X'], dataShot['Y'], statistic='count', bins=bin)
        pitch.heatmap(
            binstatistic, ax=ax[i], cmap="Oranges", edgecolors="#22312b", alpha=0.4)
        pitch.scatter(dataShot['X'], dataShot['Y'], c='gray', ax=ax[i], s=25)
        binstatistic['statistic'] = (pd.DataFrame((binstatistic['statistic']/binstatistic['statistic'].sum()))
                                         .applymap(lambda x: '{:.0%}'.format(x)).values)
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


def genGraph01(file_index, t, v):
    p = shotmap(pd.read_csv(file_index), t, v)
    filenames = os.path.join("Attacking1.png")
    # image = Image.open(filename)
    # image.thumbnail((400,400))
    image = Image.open(filenames)
    image.thumbnail((1200, 800))
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())


def genGraph02(file_index):
    p = shotmappercent(pd.read_csv(file_index))
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
        try:
            genGraph01(file_index, 1, 0)
        except:
            sg.popup("please check your data Input")

    if values["FILE_LIST"][0] == "ได้ประตู":
        try:
            genGraph01(file_index, 1, 4)
        except:
            sg.popup("please check your data Input")
    if values["FILE_LIST"][0] == "ยิงเข้ากรอบ":
        try:
            genGraph01(file_index, 1, 2)
        except:
            sg.popup("please check your data Input")
    if values["FILE_LIST"][0] == "ยิงออก":
        try:
            genGraph01(file_index, 1, 1)
        except:
            sg.popup("please check your data Input")
    if values["FILE_LIST"][0] == "ยิงติดบล็อก":
        try:
            genGraph01(file_index, 1, 3)
        except:
            sg.popup("please check your data Input")


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
sg.theme('Black')
file_layout = [
    [
        sg.Text("Choose file"),
        sg.In(size=(10, 2), enable_events=True, key="-FILE-"),
        sg.FileBrowse(),
    ],
    [
        sg.Listbox(
            values=["ภาพรวม", "ได้ประตู", "ยิงเข้ากรอบ", "ยิงออก", "ยิงติดบล็อก"], enable_events=True, size=(30, 10), key="FILE_LIST"
        ),

    ],
    [
        sg.Text("Choose Mode"),
    ],
    [

        sg.Listbox(
            values=["ตำแหน่ง","เปอร์เซ็นต์"], enable_events=True, size=(30, 2), key="MODE_LIST"
        ),

    ],
    [
        sg.Text("Choose Player Name"),
    ],
    [

        sg.Listbox(
            values=[], enable_events=True, size=(30, 100), key="NAME_LIST"
        ),

    ]
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

window = sg.Window("Gaiyang", layout, size=(1300, 700),resizable=True)
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
        GraphPosition()
            # window["-IMAGE-"].update(filename = filenames )
    # if event == "FILE_LIST":
    #     sg.popup('You entered')
    if event  == "MODE_LIST":
        if values["MODE_LIST"][0] == "ตำแหน่ง":
            GraphPosition()
        if values["MODE_LIST"][0] == "เปอร์เซ็นต์":
            try:
                genGraph02(file_index )
            except:
                sg.popup("please check your data Input")
window.close()
