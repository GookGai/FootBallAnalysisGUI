from mplsoccer import Pitch,VerticalPitch
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

def evenOdd(x):
    if (x % 2 == 0):
        print("even")
    else:
        print("odd")

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
    