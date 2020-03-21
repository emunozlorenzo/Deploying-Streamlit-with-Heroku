import streamlit as st
import numpy as np
import pandas as pd
#from datetime import date, timedelta, datetime
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    
    df = load_data()
    countries = load_countries(df)
    
    page = st.sidebar.selectbox("Choose a page", ['Homepage', 'Exploration', 'Prediction'])
    
    if page == 'Homepage':
        # Front Image
        url = 'https://www.charlescountymd.gov/Home/ShowPublishedImage/4496/637195158875230000'
        st.image(url,use_column_width=True)
        st.title("COVID-19")
        # Table
        filtro = st.selectbox('Select a Country',countries)
        st.subheader(filtro+' Dataframe')
        st.write(df.loc[df['Country'] == filtro,['Country','Date','Confirmed','Recovered','Deaths']])
    
    
    
    
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