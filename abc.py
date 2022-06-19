from mplsoccer import Pitch,VerticalPitch
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

def displayText():
    print( "Geeks 4 Geeks !")


def cleanData(rawdata):
    global data,data15,data30,data45,dataShot,dataPass,dataPass15,dataPass30,dataPass45
    data = rawdata.replace("-",float(0))
    dataShot = data[(data['Event'] == 'ShotOnTarget') |  (data['Event'] == 'ShotOffTarget') 
                    |(data['Event'] == 'ShotGetGoal') | (data['Event'] == 'ShotBlock')]
    a = dataShot['X'] 
    a= a.reset_index() 
    if(a['X'][0] > 60):
        data['X'] = data['X']*1.2
        data['Y'] = data['Y']*.8
        data['X2'] =data['X2']*1.2
        data['Y2'] = data['Y2']*.8
        data15 = data[(data['Mins'] <= 15 ) ]
        data30 = data[(data['Mins'] <= 30) &(data['Mins'] > 15 ) ]
        data45 = data[(data['Mins'] <= 45 ) &(data['Mins'] > 30 )]
    else:
        data['X'] = 120-data['X']*1.2
        data['Y'] = 80-data['Y']*.8
        data['X2'] = 120-data['X2']*1.2
        data['Y2'] = 80-data['Y2']*.8
        data15 = data[(data['Mins'] <= 60) &(data['Mins'] > 45 ) ]
        data30 = data[(data['Mins'] <= 75) &(data['Mins'] > 60 ) ]
        data45 = data[(data['Mins'] <= 90 ) &(data['Mins'] > 75 )]
        
        
    dataShot = data[(data['Event'] == 'ShotOnTarget') |  (data['Event'] == 'ShotOffTarget') |
                    (data['Event'] == 'ShotGetGoal') | (data['Event'] == 'ShotBlock')]
    dataPass = data[(data['Event'] == 'Pass') |  (data['Event'] == 'go') |
                    (data['Event'] == 'Passfail') | (data['Event'] == 'Cross')|  (data['Event'] == 'Assist')]
    dataPass15 = data15[(data15['Event'] == 'Pass') |  (data15['Event'] == 'go') |
                        (data15['Event'] == 'Passfail') | (data15['Event'] == 'Cross')|  (data15['Event'] == 'Assist')]
    dataPass30 = data30[(data30['Event'] == 'Pass') |  (data30['Event'] == 'go') |
                        (data30['Event'] == 'Passfail') | (data30['Event'] == 'Cross')|  (data30['Event'] == 'Assist')]
    dataPass45 = data45[(data45['Event'] == 'Pass') |  (data45['Event'] == 'go') |
                        (data45['Event'] == 'Passfail') | (data45['Event'] == 'Cross')|  (data45['Event'] == 'Assist')]
    
    dataShot= dataShot.reset_index()   
    dataPass = dataPass.reset_index()
    dataPass15 = dataPass15.reset_index()
    dataPass30 = dataPass30.reset_index()
    dataPass45 = dataPass45.reset_index()
    print("clean data finished")
    return(data,data15,data30,data45,dataShot,dataPass,dataPass15,dataPass30,dataPass45)
    
def shotmap(data,index):
    cleanData(data)
    shX = dataShot['X']
    shY = dataShot['Y']
    shName = dataShot['Player']
    shsty = dataShot['Event']

    sout = dataShot[dataShot['Event'] == 'ShotOffTarget' ]
    sot =  dataShot[dataShot['Event'] == 'ShotOnTarget' ]
    sb =  dataShot[dataShot['Event'] == 'ShotBlock']
    sgg =  dataShot[dataShot['Event'] == 'ShotGetGoal']

    pitch = VerticalPitch(pitch_length=100, pitch_width=100,axis=True,pitch_color = '#538053',half=True)
    fig,ax =pitch.draw(nrows=1,  ncols=1,figsize =(20,10))
    
    #plt.scatter(dataShot['Y'],dataShot['X'],c='#BE2653',s = 700,marker = "*")
    plt.scatter(sout['Y'],sout['X'],c='#fcf5e1',s = 400,marker = "o")
    plt.scatter(sot['Y'],sot['X'],c='#1E2453',s = 300,marker = "o")
    plt.scatter(sb['Y'],sb['X'],c='#1DD473',s = 500,marker = "P")
    plt.scatter(sgg['Y'],sgg['X'],c='#BF211E',s = 700,marker = "*")
    
#     ax[1].plt.scatter(sout['Y'],sout['X'],c='#fcf5e1',s = 400,marker = "o")

    for i in range(len(dataShot['X'])):
        plt.text(shY[i]-1,shX[i]-2.5,shName[i])
        
        
    title = fig.suptitle('Attacking'+ str(index),fontsize = 50)
    fileName = 'Attacking'+ str(index)
    plt.savefig(fileName + '.png')
    return fig

p = shotmap(pd.read_csv('firsthalf.csv'),1)
p1 = shotmap(pd.read_csv('secoundhalf.csv'),2)
pp = PdfPages('test.pdf')
pp.savefig(p)
pp.savefig(p1)