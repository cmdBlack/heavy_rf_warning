from qgis.core import *
import sys
import re
import os

from qgis.core.additions.edit import edit
from qgis.PyQt.QtXml import QDomDocument
from datetime import date, datetime
from qgis.PyQt.QtGui import (
    QColor,
)
from qgis.utils import iface

from PyQt5.QtGui import QFont


# global variables


# FUNCTION DECLARATIONS

def adjust_fsize_ae(txt):
    hash_cnt = txt.count("#")

    if hash_cnt > 4:
        return 26
    else:
        return 25

def bold_txt(txt):
    if "#IlocosSur(" in txt:
        mun = txt.split("#IlocosSur(")[1].split(")")[0]
        txt = txt.replace("#IlocosSur(" + mun + ")", "<b>#IlocosSur(" + mun + ")</b>")
    elif "#IlocosSur" in txt:
        txt = txt.replace("#IlocosSur", "<b>#IlocosSur</b>")
    else:
        pass

    return txt



now = datetime.now()
curr_time = now.strftime("%I:%M %p")
today = date.today()

# Create a QgsTextFormat object
text_format = QgsTextFormat()
text_format1 = QgsTextFormat()
# text_format1.setSize(20)

# Create a QFont object
font = QFont()
font.setFamily("Arial")  # Or any other font family you prefer
# font.setBold(True)        # Set font to bold (optional)

font1 = QFont()
font1.setFamily("OpenSans")  # Or any other font family you prefer

text_format.setFont(font)
text_format1.setFont(font1)


# Supply path to qgis install location
QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

# Write your code here to load some layers, use processing
# algorithms, etc.

fsize = int(input("Enter text font size: "))


# input tstm string
print("Enter advisory. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish.")
lines = sys.stdin.readlines()
advisory = "".join(lines) # Join the list of lines back into a single string
print("\n--- Your input ---")

# title = lines[0].strip("\n")
# weather_system = lines[1].strip("\n")
# date_time = lines[2].strip("\n")

# expected_string = ""
# affected_string = ""
# expected_string_abra = ""
# affected_string_abra = ""


sur_mun = ["Alilem", "Banayoyo", "Bantay", "Burgos", "Cabugao", "Caoayan", "Cervantes", "CandonCity", "Galimuyod",
           "GregoriodelPilar", "Lidlidda", "Magsingal", "Nagbukel", "Narvacan", "Quirino", "Salcedo",
           "SanEmilio", "SanEsteban", "SanIldefonso", "SanJuan", "SanVicente", "Santa", "SantaCatalina", "SantaCruz",
           "SantaLucia", "SantaMaria", "Santiago", "ViganCity", "SantoDomingo", "Sigay", "Sinait", "Sugpon", "Suyo",
           "Tagudin"]

red_mun = []
orange_mun = []
yellow_mun = []
affected_mun = []
expected_mun = []


red_warning_string = ""
orange_warning_string = ""
yellow_warning_string = ""
affecting_string = ""
expecting_string = ""

all_yellow_flag = False
all_orange_flag = False
all_red_flag = False

rest_of_string = "rest of #IlocosSur"
portion_of_string = "portions of #IlocosSur"

rop = rest_of_string in advisory or portion_of_string in advisory
rest = rest_of_string in advisory
portion = portion_of_string in advisory

print(rop)



for line in lines:
    if "ViganCity" in line:
        pass
    elif "Vigan City" in line:
        line = line.replace("Vigan City", "ViganCity")
        print("replaced")
    elif "CityOfVigan" in line:
        line = line.replace("CityOfVigan", "ViganCity")
        print("replaced")
    elif "Vigan" in line:
        line = line.replace("Vigan", "ViganCity")
        print("replaced")

    if "CandonCity" in line:
        pass
    elif "Candon City" in line:
        line = line.replace("Candon City", "CandonCity")
        print("replaced")
    elif "CityOfCandon" in line:
        line = line.replace("CityOfCandon", "CandonCity")
        print("replaced")
    elif "Candon" in line:
        line = line.replace("Candon", "CandonCity")
        print("replaced")

    if "#NLPRSD" in line:
        title = line.strip("\n")
    elif "Weather" in line:
        weather_system = line.strip("\n")
        print(line)
    elif "Issued" in line:
        date_time = line.strip("\n")

    elif "affecting" in line or "experienced" in line:
        affecting_string = bold_txt(line)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all affecting")
            affected_mun = sur_mun

        elif rest_of_string in line:
            affected_mun = list(set(sur_mun) - set(red_mun + orange_mun + yellow_mun + expected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                affected_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                affected_string_is = affected_string_is.replace(" and ", ", ")
                print(affected_string_is)
                affected_mun = re.split(', ', affected_string_is)
                print(affected_mun)
            except Exception as e:
                affected_mun = sur_mun

    elif "expected" in line:
        expecting_string = bold_txt(line)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all expected")
            expected_mun = sur_mun

        elif rest_of_string in line:
            expected_mun = list(set(sur_mun) - set(red_mun + orange_mun + yellow_mun + affected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                expected_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                expected_string_is = expected_string_is.replace(" and ", ", ")
                print(expected_string_is)
                expected_mun = re.split(', ', expected_string_is)
                print(expected_mun)
            except Exception as e:
                expected_mun = sur_mun

    else:
        pass


# Get the project instance
project = QgsProject.instance()

# Load project
project.read('/Users/kaizerjohnmacni/QGISPROJECTS/hrw_sur.qgz')

layer = project.mapLayersByName('is_mun')[0]

features = layer.getFeatures()
for feature in features:
    # Access feature attributes
    mun_name = feature.attribute('NAME_2')
    hrw = feature.attribute('hrw')

    with edit(layer):
        if mun_name in red_mun:
            feature['hrw'] = 3
        elif mun_name in orange_mun:
            feature['hrw'] = 2
        elif mun_name in yellow_mun:
            feature['hrw'] = 1
        elif mun_name in affected_mun:
            feature['hrw'] = 12
        elif mun_name in expected_mun:
            feature['hrw'] = 11
        else:
            feature['hrw'] = 0


        layer.updateFeature(feature)
        up_hrw = feature.attribute('hrw')

        print(f"Municipality Name: {mun_name}, RAIN_CAT: {up_hrw}")

manager = project.layoutManager()
layouts_list = manager.printLayouts()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
document = QDomDocument()

# read template content
template_file = open("/Users/kaizerjohnmacni/Documents/rainfall_advisory/sur_rf_adv.qpt")
template_content = template_file.read()
template_file.close()
document.setContent(template_content)

# load layout from template and add to Layout Manager
layout.loadFromTemplate(document, QgsReadWriteContext())
project.layoutManager().addLayout(layout)
layout = QgsProject.instance().layoutManager().layoutByName("ra")

# update Text values
header = layout.itemById("advisory_number")
weather = layout.itemById("weather_system")
datetime = layout.itemById("datetime")
affecting_msg = layout.itemById("affecting_msg")
expecting_msg = layout.itemById("expecting_msg")

header.setText(title)
datetime.setText(date_time)
weather.setText(weather_system)

# affecting_msg.setText(affecting_string)
# expecting_msg.setText(expecting_string)


affecting_msg.setText(affecting_string)
# text_format1.setSize(adjust_fsize_ae(affecting_string))
text_format1.setSize(fsize)
affecting_msg.setTextFormat(text_format1)

expecting_msg.setText(expecting_string)
# text_format1.setSize(adjust_fsize_ae(expecting_string))
text_format1.setSize(fsize)
expecting_msg.setTextFormat(text_format1)

# base_path = os.path.join()
png_path = os.path.join("/Users/kaizerjohnmacni/Downloads",
                        str(today) + " " + curr_time[0:2] + "-" + curr_time[-2:] + "IlocosSurRA.png")

exporter = QgsLayoutExporter(layout)
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
print("done")

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()