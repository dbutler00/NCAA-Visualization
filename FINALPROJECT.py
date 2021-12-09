"""
Name:       Daniel Butler
CS230:      Section 5
Data:       NCAA Stadiums Dataset
URL:        .

Description:

This program is a web application to visualize data about NCAA Stadiums.
On the map page, you'll find an interactive Map which can be used to visualize
the locations of the stadiums as well as give you the name of the stadium and team,
along with capacity information. The graphs page show two visualizations
of the data, mainly through a pie chart of the proportions of each college division and a
histogram showing how spread out the capacities of the stadiums are.
The raw data page allows users to create their own dataframe using pandas and
then sort using a category of their liking.
"""

import folium
import streamlit as st
from streamlit_folium import folium_static #not used in class
import csv
import pandas as pd
import matplotlib.pyplot as plt

def main(): #main function which does not return a value

    hed1, hed2 = st.columns([1,4]) #Aligns the header and image next to each other with proper spacing
    with hed1:
        st.image("ncaafootball.png",width = 100)
    with hed2:
        st.header("NCAA Stadiums Visualizations")
        st.write("by Daniel Butler")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Which Page?",("Home","Map","Graphs","Raw Data")) #This variable lets user select which page to view

    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    } #These two dictionaries are thanks to Roger Allen on github https://gist.github.com/rogerallen/1583593
    abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items())) #This saved me time by not having to write out this dictionary myself

    stadiumfile = pd.read_csv("stadiums.csv") #Pandas reads the stadium csv
    stadiumdict = [row for row in csv.DictReader(open("stadiums.csv", "r"))] #csv dict reader reads the same file but makes it into a dictionary
    for row in stadiumdict:
        if len(row["state"]) == 2:                      #This loop replaces the dictionary state with the full name if it is an abbreviation
            row["state"]=abbrev_to_us_state[row["state"]]

    if page == "Home": #This if statement provides the content for the home screen
        st.subheader("Welcome to my final Project application!")
        st.subheader("On the sidebar, you can find navigation for the site!")
        st.write("Map will bring you to an interactive map of the stadiums that can be filtered by state and/or capacity")
        st.write("Graphs will bring you to two charts; a pie chart showing division distribution and a histogram showing capacity distribution")
        st.write("Raw Data will allow you to create a table of your choosing")
    elif page == "Map": #This if statement provides content for the Map screen
        #This page is my proudest code, it took much trial and error to pass special cases
        st.subheader("Red indicates FBS teams while Green represents FCS teams")
        st.sidebar.header("Filter the map here")
        number = float(st.sidebar.slider('Capacity', 0.00, 110000.00))
        state = st.sidebar.text_input("Focus in on a certain state?").lower().title()
        if len(state) == 2: #This if statement handles state abbreviations
            state = state.upper()
            state = (abbrev_to_us_state[state])

        if (state not in us_state_to_abbrev.keys()) and (state != ""): #This if statement handles incorrect state inputs
            st.sidebar.write("State not found. Try Again")
            state = ""

        center = [31.51073, -96.4247] #geographic center of continental US
        stadiummap = folium.Map(location=center, zoom_start=3)
        for place in stadiumdict: #This loop places map markers for each stadium based on if they meet selected criteria
            if (state=="" and float(place.get("capacity")) >= number) or (place.get("state") == state and float(place.get("capacity")) >= number):
                lat = place.get("latitude")
                lon = place.get("longitude")
                if place.get("div") == "fbs": #if the stadium is used by a FBS division team it will have a trophy marker icon and a red marker color
                    icon = folium.Icon(icon= 'trophy', prefix="fa", color='red')
                else:                         #if the stadium is used by a FCS division team it will have a bank marker and a green marker color
                    icon = folium.Icon(icon= 'bank', prefix="fa", color='green')
                folium.Marker(location=[lat, lon],
                                popup = "Team: " + place.get("team") + "\n" + "Capacity: " + place.get("capacity"), #shows team and capacity items on popup after click
                                tooltip= place.get("stadium").replace("â€“"," "), #removes special characters found in the data
                                icon = icon).add_to(stadiummap)
        folium_static(stadiummap) #displays the folium map directly to the streamlit app
    elif page == "Graphs":
        col1, col2 = st.columns([2.1,2.5]) #these columns allow for the graphs to be well formatted next to each other
        with col1: #col1 handles the division pie chart
            capacity_list = []
            fbs_count = 0
            fcs_count = 0
            div_labels = ["FBS teams", "FCS teams"]
            for i in stadiumdict:
                capacity_list.append(float(i["capacity"]))
                if i["div"].lower() == "fcs":
                    fcs_count += 1
                else:
                    fbs_count +=1
            conference_count = [fbs_count,fcs_count]
            fig, ax = plt.subplots()
            plt.title("Division Distribution")
            ax.pie(conference_count, labels=div_labels, autopct='%.1f%%')
            st.pyplot(fig)
        with col2: #col2 handles the capacity histogram
            fig2, ax2 = plt.subplots()
            ax2.hist(capacity_list, bins=[0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000], color="y", edgecolor="black")
            plt.title("Histogram of Capacities")
            plt.xticks([0,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000])
            plt.xticks(rotation=75)
            plt.xlabel('Capacity')
            plt.ylabel('No. of Schools')
            st.pyplot(fig2)
    elif page == "Raw Data": #Allows user to interact with the data and make their own dataframes
        st.header("Create Your Own Filtered Table")
        headers = ["stadium","city","state","team","conference","capacity","built","expanded","div","latitude","longitude"] #this list gives multiselect its options
        st.sidebar.header("Select:")
        selectedheaders = st.sidebar.multiselect("Which categories would you like?", headers) #selectedheaders determines which columns are pulled from data
        sorter = st.sidebar.multiselect("Sort by:", selectedheaders) #allows user to select one or more columns to sort by
        order = st.sidebar.radio("How should we sort the selected column?", ("Ascending","Descending")) #determines which way to sort the selected column(s)
        torf = True #handles ascending or descending
        if order=="Descending":
            torf=False
        dataframe1 = stadiumfile.loc[:,selectedheaders]
        try:
            dataframe1.sort_values(by=sorter, inplace=True, ascending=torf) #sorts the data frame
        except:
            st.write(" ") #this handles errors during selection
        st.write(dataframe1)


main()


