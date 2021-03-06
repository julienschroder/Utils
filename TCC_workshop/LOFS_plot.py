import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os 
import rasterstats
import glob


rcParams[ 'xtick.direction' ] = 'out'
rcParams[ 'ytick.direction' ] = 'out'
rcParams[ 'xtick.labelsize' ] = 'XX-large'
rcParams[ 'ytick.labelsize' ] = 'XX-large'
rcParams[ 'figure.titlesize' ] = 'XX-large'
rcParams[ 'axes.titlesize' ] = 'XX-large'
rcParams[ 'axes.spines.top' ] = 'False'
rcParams[ 'axes.spines.right' ] = 'False'
rcParams[ 'savefig.dpi' ] = 1000
rcParams[ 'figure.figsize'] = 12 , 8


pth_YK = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/LOFS_YK-FLATS/'
shp = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/shp/Yukon_flats.shp'
scenarios = ["rcp45","rcp60","rcp85"]

for scen in scenarios :
    if not os.path.exists(os.path.join(pth_YK,"Plots")):
        os.makedirs(os.path.join(pth_YK,'Plots'))
    files = glob.glob(os.path.join(pth_YK,scen,'*.tif'))
    files.sort()
    value = [rasterstats.zonal_stats(shp,f,stats='mean')[0]['mean'] for f in files]

    #for local using rcp85
    # value = [212.07856038424845,
    # 208.03556272000526,
    # 206.4579399282824,
    # 202.2881863341777,
    # 196.8376484521499,
    # 193.11402441030364,
    # 189.8872915090305,
    # 184.48195545613055,
    # 181.71750501694245]

    df = pd.DataFrame(value,index = ['2010s','2020s','2030s','2040s','2050s','2060s','2070s','2080s','2090s'])

    df.columns = ["LOFS"]
    ax = df.plot(kind='bar', legend=False, color='#8055A6')

    #stolen from http://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html                                                       
    totals = []

    # find the values and append to list
    for i in ax.patches:
     totals.append(i.get_height())

    # set individual bar lables using above list
    total = sum(totals)

    # set individual bar lables using above list
    for i in ax.patches:
     # get_x pulls left or right; get_height pushes up or down
     ax.text(i.get_x()+.03, i.get_height()+0.8, \
             str(round(i.get_height())),
                 color='black',fontsize=18)
    plt.xticks(rotation=0)
    ax.yaxis.labelpad = 20

    plt.ylabel('Length of Frozen Season (Days)',fontsize=25)
    # plt.title('Length of Frozen Season in the Yukon Flats Area,\n  CMIP5 - 5 Model Average - {}'.format(scen.upper()))
    # plt.show()

    filename = os.path.join(pth_YK,"Plots", '_'.join(['lofs',scen,'plot','no_title','edit']) + '.png')
    plt.savefig( filename )
    plt.close()
