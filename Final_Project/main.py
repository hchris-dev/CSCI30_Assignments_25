import folium
import pandas as pd
import os
import glob
import random
import requests

path = os.getcwd()
csv_files = glob.glob(os.path.join("Data", "*.csv"))

df_PPPall = pd.DataFrame()

for f in csv_files:

    df_current = pd.read_csv(f, encoding="windows-1252")
    df_current.drop(["SBAOfficeCode", "BorrowerAddress", "BorrowerZip", "Term", "SBAGuarantyPercentage", "CurrentApprovalAmount",
                    "UndisbursedAmount", "FranchiseName", "ServicingLenderLocationID", "ServicingLenderName", "ServicingLenderAddress",
                    "ServicingLenderCity","ServicingLenderState","ServicingLenderZip","RuralUrbanIndicator","HubzoneIndicator","LMIIndicator",
                    "ProjectCity", "ProjectCountyName", "ProjectState", "ProjectZip", "CD", "NAICSCode", "UTILITIES_PROCEED","PAYROLL_PROCEED",
                    "MORTGAGE_INTEREST_PROCEED", "RENT_PROCEED","REFINANCE_EIDL_PROCEED","HEALTH_CARE_PROCEED","DEBT_INTEREST_PROCEED",
                    "OriginatingLenderLocationID", "OriginatingLender", "OriginatingLenderCity", "OriginatingLenderState"], axis=1, inplace=True)
    df_temp = df_PPPall

    print("File Path:", f)

    df_PPPall = pd.concat([df_temp, df_current], ignore_index=True)

df_PPPall["BorrowerCity"] = df_PPPall["BorrowerCity"].str.upper()
df_PPPall["BorrowerState"] = df_PPPall["BorrowerState"].str.upper()

df_latLong = pd.read_excel("Data/uscities.xlsx")
df_latLong.drop(["city_ascii","state_name", "county_fips", "county_name", "population", "density", 
                 "source", "military", "incorporated", "timezone", "ranking", "zips","id"], axis=1, inplace=True)
df_latLong.rename(columns={"city":"BorrowerCity", "state_id" : "BorrowerState"}, inplace=True)
df_latLong["BorrowerCity"] = df_latLong["BorrowerCity"].str.upper()
df_latLong["BorrowerState"] = df_latLong["BorrowerState"].str.upper()

df_PPPcoords = pd.merge(df_PPPall, df_latLong, on=["BorrowerCity", "BorrowerState"])
df_PPPcoords.dropna(subset=["lat", "lng", "LoanStatus", "BusinessType", "BorrowerName", "InitialApprovalAmount"], inplace=True)

PPPMarkers = folium.Map([38.540, -98.328], zoom_start=4, tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
                         attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

PPPHeatMap = folium.Map([38.540, -98.328], zoom_start=4, tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
                         attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

'''for row in df_PPPcoords.itertuples():
    folium.Marker(
    location=[row.lat + (round(random.uniform(0.0000, 0.0010), 5)),
               row.lng + (round(random.uniform(0.0000, 0.0010), 5))],
    tooltip="Click me!",
    popup=str(row.BorrowerName),
    icon=folium.Icon(color="green"),
    ).add_to(PPPMarkers)''' #This loop ran for 2 hours before I ended it
#10 million rows was too much

for row in df_PPPcoords.itertuples():
    if row.LoanStatus == "Charged Off":
        folium.Marker(
        location=[row.lat + (round(random.uniform(0.0000, 0.0010), 5)),
                row.lng + (round(random.uniform(0.0000, 0.0010), 5))],
        tooltip=str(row.BorrowerName),
        popup=str(row.BorrowerName) + "\n" + str(row.InitialApprovalAmount) + "\n" + str(row.BusinessType),
        icon=folium.Icon(color="red"),
        ).add_to(PPPMarkers)
    
PPPMarkers.save("LoansInCollections.html") #Creates LoansInCollections.html, copy in Maps Folder

stateLoans = df_PPPall.groupby("BorrowerState")["InitialApprovalAmount"].sum().reset_index()

state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json() #from Folium getting started

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=stateLoans,
    columns=["BorrowerState", "InitialApprovalAmount"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Sum of Loans By State",
).add_to(PPPHeatMap)

folium.LayerControl().add_to(PPPHeatMap)

PPPHeatMap.save("LoanHeatMap.html") #Creates LoansInCollections.html, copy in Maps Folder