import streamlit as st
import pandas as pd
import streamlit_extras
from typing import List
from streamlit_searchbox import st_searchbox
from millify import millify
import wikipedia
import os
from streamlit_card import card
from streamlit_extras.colored_header import colored_header
import pixabay
import plotly.express as px
import matplotlib.pyplot as plt


st.set_page_config(
    page_title=("GeoPolitical Data Science App"),
    page_icon=(":tada:"),
    layout=("wide")
)

pd.options.plotting.backend = "matplotlib"

# Read the Geodataset using the pandas read_csv function and store it in the 'geoData' variable
@st.cache
def read_geodata():
    df = pd.read_csv(r"./dataset/geodata.csv")
    return df

geoData = read_geodata()

# Read the GDPdataset using the pandas read_csv function and store it in the 'geoData' variable
@st.cache
def read_gdpdata():
    gdpDF = pd.read_csv(r"./dataset/gdp_dataset.csv")
    return gdpDF

gdpData = read_gdpdata()

# Extract the 'Country Name' column from the dataset and convert it to a list of strings
countryList = geoData["Country Name"].tolist()

# Define the search function to return suggestions based on the input search term
def search_function(search_term: str) -> List[str]:
    suggestions = []
    # Loop through the list of countries
    for country in countryList:
        # Check if the search term appears in the country name (case-insensitive)
        if search_term.lower() in country.lower():
            suggestions.append(country)
    return suggestions

# Sidebar Code

with st.sidebar:
    st.image(
        r"./media/logo.png"
    )
    
    st.header(
        " **Global Analysis App :tada:**"
        )

    with st.expander("Datasets & Last Updated :"):
        st.write("""
                *   Population Analysis : 2022
                *   Religion Analysis   : 2022
                *   National Leader     : 2018
                *   Happiness Rank      : 2020
                *   Freedom Rank        : 2022
                *   Press Freedom Index : 2018               
                *   Democracy Ratings   : 2022
                *   COVID-19 Data       : 2022
                *   GDP Stats           : 2021            
                *   Economy Analysis    : 2022
                *   Development Analysis: 2022
                *   Energy Production   : 2019            
                """)

    with st.expander("Omitted Countries :"):
        st.write("""
                 #### Due to unserialized/unreliable data, 33 Countries Below are ommitted
                *   Andorra
                *   Anguilla
                *   Bonaire
                *   British Virgin Islands
                *   Cayman Islands
                *   Dominica
                *   Falkland Islands (Malvinas)
                *   Gibraltar
                *   Holy See
                *   Isle of Man
                *   Liechtenstein                
                *   Monaco
                *   Montserrat
                *   Saint Helena
                *   Saint Kitts and Nevis
                *   Saint Pierre and Miquelon
                *   Tokelau
                *   Tuvalu
                *   American Samoa
                *   Channel Islands
                *   Faroe Islands
                *   French Guiana
                *   Guadeloupe
                *   Guam
                *   Martinique
                *   Mayotte
                *   Niue
                *   Northern Mariana Islands
                *   United States Virgin Islands
                *   Wallis and Futuna Islands
                *   Western Sahara
                *   San Marino
                *   Sint Maarten (Dutch part)
                """)

### Begin Main Body :
        
# Use the st_searchbox function to create a search box
country_name = st_searchbox(
    search_function,
    key="searchbox_1"
)

if not country_name:
  st.warning('Please select a country.')
  st.stop()
  
# Use the country name selected by the user to create the final message
st.success("Currently analyzing country: %s" % country_name)

#Generate a query to create a df as per our search input.
statDf = geoData.query("`Country Name` == @country_name")
gdpDf  = gdpData.query("`Country Name` == @country_name")
pivoted_gdpDf = gdpDf.set_index('Country Name').T

#Variable generation

## ## GeoDataset - From the First Dataframe :

totalPop   = int(geoData["Population (2022)"].sum())
totalMass  = int(geoData["Surface area (km2)"].sum())

## GeoDataset - From the Second (Query Based) Dataframe :

CountryCode= str(statDf["Code"].values[0])
Continent  = str(statDf["Continent"].values[0])  #Returns First Value of new DF
Region     = str(statDf["Region"].values[0])
Language   = str(statDf["Language"].values[0])
Population = int(statDf["Population (2022)"].values[0])
landMass   = int(statDf["Surface area (km2)"].values[0])
capital    = str(statDf["Capital"].values[0])
nationType = str(statDf["Nation Type"].values[0])
UniversalCurrency = str(statDf["Universal Currency"].values[0])
nationGDP  = str(statDf["GDP million US$"].values[0])
gdpGrowth  = str(statDf["GDP growth %"].values[0])
gdpCapita  = str(statDf["GDP/capita US$"].values[0])
tradeBalance=str(statDf["Trade: Balance (million US$)"].values[0])
mainExport = str(statDf["Country Main Export"].values[0])
globalRank = str(statDf["Rank"].values[0])
ISO_Code   = str(statDf['ISO_Code'].values[0])

### Methods and Functions :

@st.experimental_memo
def imgpath_gen(CountryCode):
    imgpath = "media\\flags\\" + CountryCode.lower() + ".png"
    # Check if the flag image exists
    if os.path.exists(imgpath):
        return imgpath
    else:
        return "Flag image not found for the given country code."

@st.experimental_memo
def get_country_page(country_name):
  # Check if the country name exists in Wikipedia
    page_summary = wikipedia.summary(country_name, sentences=4)
    return page_summary

@st.experimental_memo
def population_percentage(x: int,y: int) -> str:
    percent = (x/y*100)
    return str(percent)

percentage_func = millify(
    population_percentage(Population,totalPop),
    precision=2,
    drop_nulls=False,
    prefixes=["Home to"]
    ).__add__("% of global Population")

landMassPercent_func = millify(
    population_percentage(landMass, totalMass),
    precision=2,
    drop_nulls=False,
    prefixes=["Contains"],
).__add__("% of World Surface Area")

initial_dir = os.getcwd()

@st.experimental_memo
def imgLoderfunc(country_name: str) -> str:
    try:
        px = pixabay.core(st.secrets["pxkey"])   # Enter your pixabay API Key Here (by replacing the #) !
        # Use the 'query' method to search for images with the given query
        results = px.query(country_name)
        # Check if there are any search results
        # print(results[0].getPageURL())
        if not results:
            return "https://cdn.pixabay.com/photo/2022/11/07/18/33/hibiscus-7577002_960_720.jpg"
        # Get the first result from the search
        first_result = results[0].getLargeImageURL()
        # Return the URL of the image
        return first_result
    except Exception as e:
        return "An error occurred: {}".format(str(e))

#The Big Map Thing

def get_country_coordinates(ISO_Code):
    lat = statDf['Latitude'].values[0]
    lon = statDf['Longitude'].values[0]
    return lat, lon

lat, lon = get_country_coordinates(ISO_Code)

country_map = px.scatter_geo(
    geoData,
    locations='ISO_Code',
    #projection='orthographic',
    color='Continent',
    opacity= 0.8,
    hover_name='Country Name',
    hover_data=['Population (2022)','Surface area (km2)'],
    center=dict(lat=lat,lon=lon),
    )
country_map.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="RebeccaPurple",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="LightBlue",
    lataxis_showgrid=True, 
    lonaxis_showgrid=True,
     #showlakes=True, lakecolor="Blue",
     #showrivers=True, rivercolor="Blue"
    )
country_map.update_layout(
    height=450,
    geo = dict(
        projection_scale=5, #this is kind of like zoom
        center=dict(lat=lat, lon=lon)),
        #margin={"r":0,"t":0,"l":0,"b":0}
    )

country_globe = px.scatter_geo(
    geoData,
    locations='ISO_Code',
    projection='orthographic',
    color='Continent',
    opacity= 0.8,
    hover_name='Country Name',
    hover_data=['Population (2022)','Surface area (km2)'],
    center=dict(lat=lat,lon=lon),
    )
country_globe.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="crimson",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Cyan",
    showocean=True, oceancolor="LightBlue",
    lataxis_showgrid=False, 
    lonaxis_showgrid=False,
    showlakes=True, lakecolor="Blue",
    showrivers=True, rivercolor="Blue"
    )
country_globe.update_layout(
    height=450,
    geo = dict(
        projection_scale=2, #this is kind of like zoom
        center=dict(lat=lat, lon=lon)),
    margin={"r":0,"t":0,"l":0,"b":0}
    )

religions = ['Hindus', 'Islam', 'Jews', 'Atheist', 'Other Groups', 'Christians', 'Buddists', 'Pagen Religions']
religion_plot = statDf[religions]
reliplot_transposed = religion_plot.T

barchart = px.bar(
    reliplot_transposed,
    )
barchart.update_layout(
    showlegend=False
)
pichart = px.pie(reliplot_transposed,
                 values=reliplot_transposed.columns[0], 
                 names=reliplot_transposed.index,
                 color_discrete_sequence=px.colors.sequential.RdBu
                 )


#Basic KPI 4 Coloums

gridA1, gridA2, gridA3, gridA4 = st.columns(4)

with gridA1:

    st.metric(
        label="Continent & Region",
        value=Continent,
        delta=Region,
        help=(country_name+" is a Part of "+Continent +" continent. It is located in the "+Region)
    )
        
with gridA2:
    
    st.metric(
        label="Language",
        value=Language,
        help=("In "+country_name+"'s, The Primary language is "+Language +".")        
    )

with gridA3:
    
    st.metric(
        label="Population",
        value=millify(Population, precision=2, drop_nulls=False),
        #delta=(Population/totalPop * 100), this works, removed due to better percent func  
        delta=(percentage_func)
    )

with gridA4:
    
    st.metric(
        label="Land Mass",
        value=millify(landMass, precision=2, drop_nulls=False, prefixes=[" KM2"]),
        delta=(landMassPercent_func)
    )
    
gridB1, gridB2 = st.columns([8, 2])

with gridB1:
    st.write(get_country_page(country_name))

with gridB2:
    st.image(imgpath_gen(CountryCode))
    st.write("\n" +country_name+" Global Rank is: "+globalRank)

colored_header(
    label=country_name+ " Nation Key Demographic",
    description=Region + " Region",
    color_name="violet-70",
)

gridC1, gridC2, gridC3 = st.columns(3)

with gridC1: 
    acapitalstat = card(
        title=capital,
        text=(country_name+" Capital."),
        image=imgLoderfunc(country_name),
    )

with gridC2:
    acapitalstat = card(
        title=UniversalCurrency,
        text=(country_name+" Currency."),
        image=imgLoderfunc(country_name),
    )
    
with gridC3:
    acapitalstat = card(
        title=nationType,
        text=(country_name+" is a "+nationType+" Nation Type."),
        image=imgLoderfunc(country_name),
    )

colored_header(
    label=country_name+ " Nation Economic Stats",
    description=Region + " Region",
    color_name="orange-70",
)

gridD1, gridD2 = st.columns([1, 4])

# Cleaning the $ Mark :
def cleanNationGDP(nationGDP: str) -> int:
    # Remove the $ symbol and any commas
    cleaned = nationGDP.replace("$", "").replace(",", "")
    # Convert the cleaned string to a float
    gdp = float(cleaned)
    # Round the float to the nearest integer
    gdp_rounded = round(gdp)
    # Convert the rounded float to an integer and return it
    return int(gdp_rounded*1000000)
cleanedgdp = millify(
    cleanNationGDP(nationGDP),
    precision=2,
    drop_nulls=True,
)

with gridD1:
        st.metric(
        label="Gross Domestic Produce",
        value=cleanedgdp,
        delta=(f"{gdpGrowth}% GDP Growth"),
        help=("Nation GDP as of Year: 2022")
    )
        st.metric(
        label="GDP/capita US$",
        value=gdpCapita,
        delta=(tradeBalance+"(Mill $) Trade Bal."),
        help=("International Trade Balance as of Year: 2022")
    )
        st.metric(
        label="Main Export",
        value=mainExport
    )

with gridD2:
        st.area_chart(pivoted_gdpDf)

colored_header(
    label=country_name+ " Nation Population Stats",
    description=Region + " Region",
    color_name="violet-70",
)

gridE1, gridE2 = st.columns([2, 3])

with gridE1:
    happinesscard = card(
        title=(f"{statDf['Happiness Rank'].values[0]}"),
        text=(f"Is the Happiness Rank of {country_name} with {statDf['Urban population %'].values[0]}% Urban Population"),
        image=imgLoderfunc(capital),
    )
    st.subheader(f"{country_name} Details")
    st.write(f" Independence Status: {statDf['Independent'].values[0]} || Obtained Freedom in: {str(statDf['Independence Year'].values[0])}")
    st.write(f" It is a {statDf['Governence'].values[0]} with {statDf['Leader'].values[0]} as last known Leader. It is placed under WHO Region of {statDf['WHO Regions'].values[0]}")
       
with gridE2:
    
    tab1, tab2, tab3, tab4 = st.tabs(["Country Location [Map View]", "World Location [Global View]",
                                      "Religion Plotting [Bar Chart]","Religion Plotting [Pi Chart]"])
    
    with tab1:
        st.plotly_chart(
            country_map,
            use_container_width=True,
            sharing="streamlit",
            #theme="streamlit",
            theme=None
        )

    with tab2:
        st.plotly_chart(
            country_globe,
            use_container_width=True,
            sharing="streamlit",
            theme=None,
        )

    with tab3:
        st.plotly_chart(barchart,use_container_width=True,theme=None)    

    with tab4:    
        st.plotly_chart(pichart,use_container_width=True)
