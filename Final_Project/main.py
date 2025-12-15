from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QHBoxLayout, QLineEdit, QComboBox, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineCore import QWebEngineSettings
import folium
import pandas as pd
import os
import glob
import random

import sys
from pathlib import Path

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

PPPUserDefined = folium.Map([38.540, -98.328], zoom_start=4, tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
                         attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>')

def bigMapFunction(dataframe, map, state, extra, mapStyle):
    if mapStyle == "Circle":
        if extra == "None":
            for row in dataframe.itertuples():    
                if row.BorrowerState == str(state) :
                    folium.Circle(
                    location=[row.lat + (round(random.uniform(0.0000, 0.01), 5)),
                            row.lng + (round(random.uniform(0.0000, 0.01), 5))],
                    radius = 2,
                    color = "cornflowerblue",
                    stroke=False,
                    fill = True,
                    fill_opacity = 0.6,
                    opacity = 1,
                    ).add_to(map)
        elif extra == "Nonprofit":
            for row in dataframe.itertuples():    
                if (row.BorrowerState == str(state)) and (row.NonProfit == "Y"):
                    folium.Circle(
                    location=[row.lat + (round(random.uniform(0.0000, 0.01), 5)),
                            row.lng + (round(random.uniform(0.0000, 0.01), 5))],
                    radius = 2,
                    color = "cornflowerblue",
                    stroke=False,
                    fill = True,
                    fill_opacity = 0.6,
                    opacity = 1,
                    ).add_to(map)
        else:
            for row in dataframe.itertuples():    
                if (row.BorrowerState == str(state)) and (row.Veteran == "Veteran"):
                    folium.Circle(
                    location=[row.lat + (round(random.uniform(0.0000, 0.01), 5)),
                            row.lng + (round(random.uniform(0.0000, 0.01), 5))],
                    radius = 2,
                    color = "cornflowerblue",
                    stroke=False,
                    fill = True,
                    fill_opacity = 0.6,
                    opacity = 1,
                    ).add_to(map)

# CSVs will take a minute or so to merge
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PPP Visualizer")

        self.browser = QWebEngineView()
        settings = self.browser.settings()
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
            True
        )
        settings.setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            True
        )

        BASE_DIR = Path(__file__).resolve().parent
        html_path = BASE_DIR / "Maps" / "PPPVisualizerMap.html"
        self.browser.load(QUrl.fromLocalFile(str(html_path)))

        layoutLeft = QVBoxLayout()
        layoutRight = QHBoxLayout()
        layoutBoth = QHBoxLayout()

        widgets = [  QComboBox, QLabel, QLineEdit, QPushButton, ]

        self.stateDropdown = QComboBox()
        self.stateDropdown.addItems([
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY" ])
        #styleDropdown = QLabel("Style: Circle") #taking out icons bc they are slow and make large files
        self.extraDropdown = QComboBox()
        self.extraDropdown.addItems(["None", "Veteran", "Nonprofit"])

        generateButton = QPushButton("Generate Map")
        generateButton.clicked.connect(self.generateMap)

        layoutLeft.addWidget(self.stateDropdown)
        #layoutLeft.addWidget(styleDropdown)
        layoutLeft.addWidget(self.extraDropdown)
        layoutLeft.addWidget(generateButton)

        layoutRight.addWidget(self.browser)

        layoutBoth.addLayout(layoutLeft)
        layoutBoth.addLayout(layoutRight)

        widget = QWidget()
        widget.setLayout(layoutBoth)
        self.setCentralWidget(widget)

    def generateMap(self):
            BASE_DIR = Path(__file__).resolve().parent
            html_path = BASE_DIR / "Maps" / "PPPVisualizerMap.html"

            PPPUserDefined = folium.Map([38.540, -98.328], zoom_start=4,
                tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', attr='&copy; OpenStreetMap contributors &copy; CARTO' )

            bigMapFunction(df_PPPcoords, PPPUserDefined, self.stateDropdown.currentText(), self.extraDropdown.currentText(), "Circle")

            PPPUserDefined.save(html_path)

            self.browser.load(QUrl.fromLocalFile(str(html_path)))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()