import streamlit as st
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter
plt.style.use('ggplot')
import seaborn as sns



def main():
    
    df = load_data()
    countries = load_countries(df)
    data = grouped_data(df)
    
    page = st.sidebar.selectbox("Choose a page", ['Homepage', 'Top 10', 'Prediction'])
    
    if page == 'Homepage':
        # Front Image
        url = 'https://www.charlescountymd.gov/Home/ShowPublishedImage/4496/637195158875230000'
        st.image(url,use_column_width=True)
        st.title("COVID-19")
        ####################################################################################################
        st.subheader('1. DATA BY COUNTRY')
        ##########################################
        filtro = st.selectbox('Select a Country',countries)
        st.subheader('1.1 '+filtro+' Dataframe')
        st.write(df.loc[df['Country'] == filtro,['Country','Date','Confirmed','Recovered','Deaths']])
        ###########################################
        st.subheader('1.2 '+filtro+' Plot')
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
        st.subheader('1.3 '+filtro+': New Cases by day')
        filtro3 = st.selectbox('Select Feature',['Confirmed','Recovered','Deaths'],key='filtro3')
        ax = data.loc[filtro][[filtro3]].diff().plot(kind='bar',figsize=(12,6),color='blue',alpha=0.6)
        ax.set_xticklabels(data.loc[filtro].index.strftime("%d/%m"),rotation=90)
        plt.title(filtro)
        st.pyplot()
        ####################################################################################################
        st.subheader('2. CUMULATIVE PLOT')
        ##########################################
        st.subheader('2.1 Cumulative Plot since 10th Death')
        multiselect = st.multiselect('Select Countries',options=df['Country'].unique().tolist(),default=['Spain','Italy','France','Germany','United States','United Kingdom'],key='number8')
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
            ax.set_yticks([20, 50, 100, 200, 500, 1000,2000,3000,10000])
            ax.get_yaxis().set_major_formatter(ScalarFormatter())
            plt.plot(x,y,'--',color='black',alpha=0.5)
            plt.text(len(x),y[-1],'33% Daily Increase',color='grey',weight="bold",family="monospace")
            plt.title('Cumulative Number of Deaths, by number of days since 10th death')
        st.pyplot()
        for i in less_10:
            st.text('Attention: '+i+' has less than 10 Deaths. Please, Remove this country.')
        ##########################################    
        st.subheader('2.2 Cumulative Plot since 500th Confirmed Case')
        multiselect_2 = st.multiselect('Select Countries',options=df['Country'].unique().tolist(),default=['Spain','Italy','France','Germany','United States','United Kingdom'],key='number9')
        x = list(range(24))
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
            ax.set_yticks([500,1000,5000,10000,20000,50000,100000])
            ax.get_yaxis().set_major_formatter(ScalarFormatter())
            plt.plot(x,y,'--',color='black',alpha=0.5)
            plt.text(len(x),y[-1],'33% Daily Increase',color='grey',weight="bold",family="monospace")
            plt.title('Cumulative Number of Confirmed cases, by number of days since 500th Confirmed')
        st.pyplot()
        for i in less_500:
            st.text('Attention: '+i+' has less than 500 Confirmed Cases. Please, Remove this country.')
        ####################################################################################################
    elif page == 'Top 10':
        # Front Image
        url = 'https://www.charlescountymd.gov/Home/ShowPublishedImage/4496/637195158875230000'
        st.image(url,use_column_width=True)
        st.title("COVID-19")
    


########### FUNCTIONS ###########
@st.cache
def load_data():
    # Paths
    path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    files = []
    # Dates
    start_date =  datetime.date(2020,1,22) # First Report
    end_date = datetime.date.today() - datetime.timedelta(days=1)# Today
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
    data = dataframe.groupby(['Country','Date'])['Confirmed','Recovered','Deaths'].sum()
    return data

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

if __name__ == '__main__':
    main()