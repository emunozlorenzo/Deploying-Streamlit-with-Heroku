import streamlit as st
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec
plt.style.use('ggplot')
import seaborn as sns
# Bokeh
from bokeh.plotting import figure, output_file, show, gmap
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
import pandas_bokeh
pandas_bokeh.output_notebook()


def main():
    
    df = load_data()
    countries = load_countries(df)
    data = grouped_data(df)
    coords = load_coords()
    maps = load_maps(data,coords)
    
    st.sidebar.image("https://s27389.pcdn.co/wp-content/uploads/2019/12/top-5-data-science-strategy-predictions-2020-1024x440.jpeg",use_column_width=True)
    st.sidebar.markdown('# COVID-19 Dashboard')
    page = st.sidebar.selectbox("Choose a page", ['Homepage', 'Top 10'])
    st.sidebar.markdown('Author: [Eduardo Muñoz](https://www.linkedin.com/in/eduardo-mu%C3%B1oz-lorenzo-14144a144/)')
    st.sidebar.markdown('GitHub Repo: [Link](https://github.com/emunozlorenzo/Deploying-Streamlit-with-Heroku)')
    
    if page == 'Homepage':
        # Front Image
        url = 'https://www.charlescountymd.gov/Home/ShowPublishedImage/4496/637195158875230000'
        st.image(url,use_column_width=True)
        st.title("COVID-19")
        st.markdown('Data Source: [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)')
        ####################################################################################################
        st.markdown('## MAP')
        radio = st.radio(
        "Select an option",
        ('Confirmed', 'Recovered', 'Deaths'))
        radio_dict = {'Confirmed':['size_Confirmed_2','size_Confirmed'],'Recovered':['size_Recovered_2','size_Recovered'],'Deaths':['size_Deaths_2','size_Deaths']}
        if st.checkbox('Change Scale',value=False):
            sizes=radio_dict[radio][1]
        else:
            sizes=radio_dict[radio][0]
        m = maps.plot_bokeh.map(
            x="lon",
            y="lat",
            size=sizes,
            hovertool_string="""<h2> @{Country} </h2> 

                                <h3> Confirmed: @{Confirmed} </h3>
                                <h3> Recovered: @{Recovered} </h3>
                                <h3> Deaths: @{Deaths} </h3>""",
            tile_provider="CARTODBPOSITRON_RETINA",
            colormap="Plasma",
            colormap_uselog=False,
            marker="circle",
            category=radio,
            alpha=0.6,
            #figsize=(900, 600),
            title="")
        st.bokeh_chart(m)
        ##########################################
        def function_color(val,c='red'):

            color = c
            return 'color: %s' % color
        st.markdown('## 1. REPORT')
        slider = st.slider('Top Countries', min_value=1, max_value=50, value=10, step=1,key='Slider')
        table = top_table(data,slider)
        st.text('Date: '+str(datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=1)),'%Y-%m-%d'))[0:10])
        st.table(table.style.applymap(lambda x: function_color(val=x,c='orange'),subset=['Confirmed']).applymap(lambda x: function_color(val=x,c='green'),subset=['Recovered']).applymap(lambda x: function_color(val=x,c='red'),subset=['Deaths']))
        ##########################################
        st.markdown('## 2. DATA BY COUNTRY')
        ##########################################
        filtro = st.selectbox('Select a Country',countries)
        st.markdown('### 2.1 '+filtro+' Dataframe')
        st.write(df.loc[df['Country'] == filtro,['Country','Date','Confirmed','Recovered','Deaths']])
        ###########################################
        st.markdown('### 2.2 '+filtro+' Plot')
        features = {'Confirmed':'blue','Recovered':'green','Deaths':'red','All':None}
        filtro2 = st.selectbox('Select Feature',list(features.keys()),key='filtro2')
        fig, ax = plt.subplots(figsize=(12,6))
        if filtro2 =='All':
            ax.plot(data.loc[filtro,['Confirmed','Recovered','Deaths']],alpha=0.6)
            plt.legend(['Confirmed','Recovered','Deaths'])
        else:
            ax.plot(data.loc[filtro,[filtro2]],label=filtro2,color=features[filtro2],alpha=0.6)
            plt.legend()
        plt.title(filtro)
        
        if st.checkbox('Log Scale',value=False):
            ax.set_yscale('log')
        st.pyplot()
        ##########################################
        st.markdown('### 2.3 '+filtro+': New Cases by day')
        filtro3 = st.selectbox('Select Feature',['Confirmed','Recovered','Deaths'],key='filtro3')
        ax = data.loc[filtro][[filtro3]].diff().plot(kind='bar',figsize=(12,6),color='blue',alpha=0.6)
        ax.set_xticklabels(data.loc[filtro].index.strftime("%d/%m"),rotation=90)
        plt.title(filtro)
        st.pyplot()
        ####################################################################################################
        st.markdown('## 3. CUMULATIVE PLOT')
        ##########################################
        st.markdown('### 3.1 Cumulative Plot since 10th Death')
        multiselect = st.multiselect('Select Countries',options=df['Country'].unique().tolist(),default=['Spain','Italy','France','Germany','United States','United Kingdom'],key='number80')
        x = list(range(24))
        y = [10*(1+0.33)**num for num in x]
        jet= plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0,1,len(multiselect))))
        less_10 = []
        fig, ax = plt.subplots(figsize=(12,6))
        for c in multiselect:
            if data.loc[c,['Deaths']]['Deaths'].values[-1] >=10:
                my_color = next(colors)
                ax.plot(data.loc[c].query('Deaths>=10')['Deaths'].values,label=c,marker=".",color=my_color)
                ax.text(len(data.loc[c].query('Deaths>=10')['Deaths'].values.tolist()),data.loc[c].query('Deaths>=10')['Deaths'].values.tolist()[-1],c,color=my_color,weight="bold",family="monospace")
            else:
                less_10.append(c)
            ax.set_yscale('log')
            ax.set_yticks([20, 50, 100, 200, 500, 1000,2000,3000,6000,10000])
            ax.get_yaxis().set_major_formatter(ScalarFormatter())
            plt.plot(x,y,'--',color='black',alpha=0.5)
            plt.text(len(x),y[-1],'33% Daily Increase',color='grey',weight="bold",family="monospace")
            plt.title('Cumulative Number of Deaths, by number of days since 10th death')
        st.pyplot()
        for i in less_10:
            st.text('Attention: '+i+' has less than 10 Deaths. Please, Remove this country.')
        ##########################################    
        st.subheader('3.2 Cumulative Plot since 500th Confirmed Case')
        multiselect_2 = st.multiselect('Select Countries',options=df['Country'].unique().tolist(),default=['Spain','Italy','France','Germany','United States','United Kingdom'],key='number81')
        x = list(range(18))
        y = [500*(1+0.33)**num for num in x]
        jet= plt.get_cmap('jet')
        colors = iter(jet(np.linspace(0,1,len(multiselect_2))))
        less_500 = []
        fig, ax = plt.subplots(figsize=(12,6))
        for c in multiselect_2:
            if data.loc[c,['Confirmed']]['Confirmed'].values[-1] >=500:
                my_color = next(colors)
                ax.plot(data.loc[c].query('Confirmed>=500')['Confirmed'].values,label=c,marker=".",color=my_color)
                ax.text(len(data.loc[c].query('Confirmed>=500')['Confirmed'].values.tolist()),data.loc[c].query('Confirmed>=500')['Confirmed'].values.tolist()[-1],c,color=my_color,weight="bold",family="monospace")
            else:
                less_500.append(c)
            ax.set_yscale('log')
            ax.set_yticks([500,1000,5000,10000,20000,50000,80000,100000])
            ax.get_yaxis().set_major_formatter(ScalarFormatter())
            plt.plot(x,y,'--',color='black',alpha=0.5)
            plt.text(len(x),y[-1],'33% Daily Increase',color='grey',weight="bold",family="monospace")
            plt.title('Cumulative Number of Confirmed cases, by number of days since 500th Confirmed')
        st.pyplot()
        for i in less_500:
            st.text('Attention: '+i+' has less than 500 Confirmed Cases. Please, Remove this country.')

    if page == 'Top 10':
        # Front Image
        url = 'https://www.charlescountymd.gov/Home/ShowPublishedImage/4496/637195158875230000'
        st.image(url,use_column_width=True)
        st.title("COVID-19")
        st.markdown('Data Source: [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)')
        plot_top_10(data)
        st.pyplot()
        
        st.write(datetime.datetime.now().hour)
        

########### FUNCTIONS ###########
@st.cache
def load_data():
    # Paths
    path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    files = []
    # Dates
    start_date =  datetime.date(2020,1,22) # First Report
    if 0 == datetime.datetime.now().hour:
        end_date = datetime.date.today() - datetime.timedelta(days=2)# Today
    else:
        end_date = datetime.date.today() - datetime.timedelta(days=1)
    delta = end_date - start_date # Days from the first report
    # Files
    for i in range(delta.days+1):
        date_ = start_date + datetime.timedelta(days=i)
        files.append(date_.strftime('%m-%d-%Y'))
    # Bug 13/03/2020
    df = pd.DataFrame()
    for f in files:
        if f != '03-13-2020': # there is a bug in this report
            df_aux = pd.read_csv(path+f+'.csv')
            df_aux['Date'] = pd.to_datetime(f)
            df = pd.concat([df,df_aux])
        else:
            df_aux = pd.read_csv(path+f+'.csv')
            df_aux.loc[df_aux['Country/Region']!='China',['Last Update']] = df_aux[df_aux['Country/Region'] != 'China']['Last Update'].str.replace('-11T','-13T')    
            df_aux['Date'] = pd.to_datetime(f)
            df = pd.concat([df,df_aux])
    
    # Renaming
    df.rename(columns={'Country/Region':'Country'},inplace=True)
    df.rename(columns={'Province/State':'Province'},inplace=True)
    dict_countries = load_dict_countries()
    dict_provinces = load_dict_provinces()
    
    rename_countries(df,dict_countries)
    fix_provinces(df,dict_provinces)
    
    return df

@st.cache
def grouped_data(dataframe):
    return dataframe.groupby(['Country','Date'])['Confirmed','Recovered','Deaths'].sum()

@st.cache
def load_coords():
    return pd.read_csv('https://raw.githubusercontent.com/albertyw/avenews/master/old/data/average-latitude-longitude-countries.csv')

@st.cache
def load_maps(dataframe,coordinates):
    dataset = pd.merge(dataframe.loc[dataframe.index.get_level_values(1) == datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=1)),'%Y-%m-%d')],coordinates,on=['Country'])
    dataset.rename(columns={'Latitude':'lat','Longitude':'lon'},inplace=True)
    dataset["size_Confirmed"] = np.log(dataset["Confirmed"]*100)
    dataset["size_Recovered"] = np.log(dataset["Recovered"]*100)
    dataset["size_Deaths"] = np.log(dataset["Deaths"]*100)
    dataset["size_Confirmed_2"] = (dataset["Confirmed"]/dataset["Confirmed"].max())*100
    dataset["size_Recovered_2"] = (dataset["Recovered"]/dataset["Recovered"].max())*100
    dataset["size_Deaths_2"] = (dataset["Deaths"]/dataset["Deaths"].max())*100
    return dataset

@st.cache
def load_dict_countries():
    dict_countries = {'United States':['US'],
                      'United Kingdom':['UK','Jersey','Guernsey'],
                      'China':['Mainland China'],
                      'Macao':['Macau'],
                      'Korea, Republic of':['South Korea','Korea, South'],
                      'Korea, North':['North Korea'],
                      'Russian Federation':['Russia'],
                      'Iran, Islamic Republic of':['Iran'],
                      'Macedonia':['North Macedonia'],
                      'Moldova, Republic of':['Moldova'],
                      'Cote d\'Ivoire':['Ivory Coast'],
                      'Holy See (Vatican City State)':['Holy See'],
                      'Congo, The Democratic Republic of the':['Congo (Kinshasa)','Republic of the Congo'],
                      'Congo':['Congo (Brazzaville)'],
                      'Brunei Darussalam':['Brunei'],
                      'Czech Republic':['Czechia'],
                      'Palestinian Territory':['occupied Palestinian territory'],
                      'Swaziland':['Eswatini'],
                      'Netherlands':['Curacao'],
                      'Serbia':['Kosovo'],
                      'Tanzania, United Republic of':['Tanzania'],
                      'Bahamas':['The Bahamas','Bahamas, The'],
                      'Gambia':['Gambia, The','The Gambia'],
                      'Cape Verde':['Cabo Verde'],
                      'Taiwan':['Taipei and environs','Taiwan*'],
                     }
    return dict_countries

@st.cache
def load_dict_provinces():
    dict_provinces = {'Hong Kong':['Hong Kong'],
                      'Macao':['Macao','Macau'],
                      'Taiwan':['Taiwan','Taipei and environs','Taiwan*'],
                     }
    return dict_provinces

@st.cache
def rename_countries(dataframe,dictionary):
    for key, value in dictionary.items():
        for val in value:
            dataframe['Country'] = dataframe['Country'].str.replace(val,key)
@st.cache
def fix_provinces(dataframe,dictionary):
    for key, value in dictionary.items():
        for val in value:
            dataframe.loc[dataframe['Province']== val,['Country']] = key

@st.cache
def load_countries(dataframe):
    list_ = sorted(list(set(dataframe['Country'].values.tolist())))
    list_.insert(0, "Spain")
    return list_

@st.cache
def top_table(dataframe,slider):
    data_last_report = dataframe.loc[dataframe.index.get_level_values(1) == datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=1)),'%Y-%m-%d')]
    data_last_report_2 = dataframe.loc[dataframe.index.get_level_values(1) == datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=2)),'%Y-%m-%d')]
    top_list = data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][:slider].index.get_level_values(0).tolist()
    data_report = pd.concat([data_last_report_2,data_last_report])
    data_report = data_report.loc[top_list]
    data_report['New Confirmed'] = 0
    data_report['New Recovered'] = 0
    data_report['New Deaths'] = 0
    for c in top_list:
        for i in ['Confirmed','Recovered','Deaths']:
            data_report.loc[c,['New '+i]] = data_report.loc[c,[i]].diff()
    data_last_day = data_report.loc[data_report.index.get_level_values(1) == datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=1)),'%Y-%m-%d')]
    data_last_day = data_last_day.astype(int)
    data_last_day = data_last_day.sort_values(by='Confirmed',ascending=False)
    data_last_day['Confirmed'] = data_last_day[['Confirmed','New Confirmed']].astype(str).apply(lambda x: ' (+'.join(x)+')',axis=1)
    data_last_day['Recovered'] = data_last_day[['Recovered','New Recovered']].astype(str).apply(lambda x: ' (+'.join(x)+')',axis=1)
    data_last_day['Deaths'] = data_last_day[['Deaths','New Deaths']].astype(str).apply(lambda x: ' (+'.join(x)+')',axis=1)
    data_last_day = data_last_day[['Confirmed','Recovered','Deaths']]
    data_last_day.index = data_last_day.index.droplevel(1)
    return data_last_day

@st.cache
def plot_top_10(dataframe):
    data_last_report = dataframe.loc[dataframe.index.get_level_values(1) == datetime.datetime.strptime(str(datetime.date.today()- datetime.timedelta(days=1)),'%Y-%m-%d')]
    top_list = data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][:10].index.get_level_values(0).tolist()
    fig = plt.figure(figsize=(16,10),constrained_layout=True)
    gs = GridSpec(4, 3, figure=fig)
    ax1 = fig.add_subplot(gs[:2, :])
    ax2 = fig.add_subplot(gs[2, :1])
    ax3 = fig.add_subplot(gs[2, 1:2])
    ax4 = fig.add_subplot(gs[2, -1])
    ax5 = fig.add_subplot(gs[3, :1])
    ax6 = fig.add_subplot(gs[3, 1:2])
    ax7 = fig.add_subplot(gs[3, -1])
    # Colors
    jet= plt.get_cmap('jet')
    colors = iter(jet(np.linspace(0,1,10)))
    clist = [(0, "red"), (0.125, "red"), (0.25, "orange"), (0.5, "green"), 
             (0.7, "green"), (0.75, "blue"), (1, "blue")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)
    N1 = 10
    N2 = 9
    x1 = np.arange(N1).astype(float)
    x2 = np.arange(N2).astype(float)
    y1 = np.random.uniform(0, 5, size=(N1,))
    y2 = np.random.uniform(0, 5, size=(N2,))
    # Axis 1
    for country in top_list:
        ax1.plot(dataframe.loc[country,['Confirmed']],label=country[:15],color=next(colors),alpha=0.5)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_minor_locator(mdates.DayLocator())
    ax1.legend(loc='upper left', bbox_to_anchor=(0.0, 1, 0.20, 0),mode="expand",ncol=2)
    ax1.set_title('COVID-19')
    # Axis 2, 5
    ax2.bar(data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][:10].index.get_level_values(0),data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][:10].values,color=rvb(x1/N1))
    ax2.tick_params(labelrotation=45,labelsize=8)
    ax2.title.set_text('TOP Confirmed')
    ax5.bar(data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][1:10].index.get_level_values(0),data_last_report.sort_values(by='Confirmed',ascending=False)['Confirmed'][1:10].values,color=rvb(x2/N2))
    ax5.tick_params(labelrotation=45,labelsize=8)
    ax5.title.set_text('TOP Confirmed w/o China')
    # Axis 3, 6
    ax3.bar(data_last_report.sort_values(by='Recovered',ascending=False)['Recovered'][:10].index.get_level_values(0),data_last_report.sort_values(by='Recovered',ascending=False)['Recovered'][:10].values,color=rvb(x1/N1))
    ax3.tick_params(labelrotation=45,labelsize=8)
    ax3.title.set_text('TOP Recovered')
    ax6.bar(data_last_report.sort_values(by='Recovered',ascending=False)['Recovered'][1:10].index.get_level_values(0),data_last_report.sort_values(by='Recovered',ascending=False)['Recovered'][1:10].values,color=rvb(x2/N2))
    ax6.tick_params(labelrotation=45,labelsize=8)
    ax6.title.set_text('TOP Recovered w/o China')
    # Axis 4, 7
    ax4.bar(data_last_report.sort_values(by='Deaths',ascending=False)['Deaths'][:10].index.get_level_values(0),data_last_report.sort_values(by='Deaths',ascending=False)['Deaths'][:10].values,color=rvb(x1/N1))
    ax4.tick_params(labelrotation=45,labelsize=8)
    ax4.title.set_text('TOP Deaths')
    ax7.bar(data_last_report.sort_values(by='Deaths',ascending=False)['Deaths'][1:10].index.get_level_values(0),data_last_report.sort_values(by='Deaths',ascending=False)['Deaths'][1:10].values,color=rvb(x2/N2))
    ax7.tick_params(labelrotation=45,labelsize=8)
    ax7.title.set_text('TOP Deaths w/o China')

if __name__ == '__main__':
    main()