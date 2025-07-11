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


# Define the path to the PROJ data directory
# proj_lib_path = "/Applications/QGIS-LTR.app/Contents/Resources/proj"  # Replace with the actual path

# Set the environment variable
os.environ["PROJ_LIB"] = "/Applications/QGIS-LTR.app/Contents/Resources/proj"


# FUNCTION DECLARATIONS
def adjust_fsize(txt):
    hash_cnt = txt.count("#")

    if hash_cnt == 1:
        return 35
    elif hash_cnt > 4:
        return 15
    else:
        return 23

    # return 110 - len(txt) * 0.1


def adjust_fsize_ae(txt):
    hash_cnt = txt.count("#")

    if hash_cnt > 4:
        return 20
    else:
        return 25

    # return 16 - len(txt) * 0.2

def filter_warning_txt(txt):

    # line.split("#IlocosSur(")[1].split(")")[0]
    # txt = txt.replace("#IlocosSur", "<b>#IlocosSur</b>")
    return txt.split(": ")[1]

def bold_txt(txt):
    if "#IlocosSur(" in txt:
        mun = txt.split("#IlocosSur(")[1].split(")")[0]
        print(mun)
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

fsize = int(input("Enter text font size for HRW: "))
fsize2 = int(input("Enter text font size for AE: "))


# input tstm string
print("Enter advisory. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish.")
lines = sys.stdin.readlines()
advisory = "".join(lines) # Join the list of lines back into a single string
print("\n--- Your input ---")

# title = lines[0].strip("\n")
# weather_system = lines[1].strip("\n")
# date_time = lines[2].strip("\n")


# expected_string_abra = lines[6].split("#Abra(")[1].split("), ")[0]
# affected_string_abra = lines[4].split("#Abra(")[1].split("), ")[0]
# affected_string = filter_txt(lines[4].strip("\n"))
# expected_string = filter_txt(lines[6].strip("\n"))

# expected_string = ""
# affected_string = ""
# expected_string_abra = ""
# affected_string_abra = ""
#


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

    elif "Red Warning" in line:
        red_warning_string = filter_warning_txt(line)
        red_warning_string = bold_txt(red_warning_string)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all red")
            red_mun = sur_mun

        elif rest_of_string in line:
            red_mun = list(set(sur_mun) - set(orange_mun + yellow_mun + affected_mun + expected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                red_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                red_string_is = red_string_is.replace(" and ", ", ")
                print(red_string_is)
                red_mun = re.split(', ', red_string_is)
                print(red_mun)
            except Exception as e:
                red_mun = sur_mun

    elif "Orange Warning" in line:
        orange_warning_string = filter_warning_txt(line)
        orange_warning_string = bold_txt(orange_warning_string)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all orange")
            orange_mun = sur_mun

        elif rest_of_string in line:
            orange_mun = list(set(sur_mun) - set(red_mun + yellow_mun + affected_mun + expected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                orange_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                orange_string_is = orange_string_is.replace(" and ", ", ")
                print(orange_string_is)
                orange_mun = re.split(', ', orange_string_is)
                print(orange_mun)
            except Exception as e:
                orange_mun = sur_mun

    elif "Yellow Warning" in line:
        yellow_warning_string = filter_warning_txt(line)
        yellow_warning_string = bold_txt(yellow_warning_string)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all yellow")
            yellow_mun = sur_mun

        elif rest_of_string in line:
            yellow_mun = list(set(sur_mun) - set(red_mun + orange_mun + affected_mun + expected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                yellow_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                yellow_string_is = yellow_string_is.replace(" and ", ", ")
                print(yellow_string_is)
                yellow_mun = re.split(', ', yellow_string_is)
                print(yellow_mun)
            except Exception as e:
                yellow_mun = sur_mun

    elif "affecting" in line:
        affecting_string = bold_txt(line)
        if "#IlocosSur" in line and not "#IlocosSur(" in line and not rop:
            print("all affecting")
            affected_mun = sur_mun

        elif rest_of_string in line:
            affected_mun = list(set(sur_mun) - set(red_mun + orange_mun + yellow_mun + expected_mun))

        elif "#IlocosSur(" in line or portion_of_string in line:
            try:
                affected_string_is = line.split("#IlocosSur(")[1].split(")")[0]
                # affecting_string = affecting_string.replace("#IlocosSur(" + affected_string_is + ")", "<b>#IlocosSur(" + affected_string_is + ")</b>")
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
                # expecting_string = expecting_string.replace("#IlocosSur(" + expected_string_is + ")", "<b>#IlocosSur(" + expected_string_is + ")</b>")
                expected_string_is = expected_string_is.replace(" and ", ", ")
                print(expected_string_is)
                expected_mun = re.split(', ', expected_string_is)
                print(expected_mun)
            except Exception as e:
                expected_mun = sur_mun

    else:
        pass

    # if "#Abra" in line and "expected" in line:
    #     if "#Abra(" not in line and rest_of_abra_string not in line:
    #         all_expected_flag = True
    #         expected_string = filter_txt(line.strip("\n"))
    #         # expected_string = line.strip("\n")
    #
    #     elif rest_of_abra_string in line or portion_of_abra_string in line:
    #         for mun in all_mun_abra:
    #             if mun not in affected_mun:
    #                 expected_mun.append(mun)
    #                 print(f"Municipality Name: {expected_mun}")
    #
    #                 expected_string_abra = '(' +  ", ".join(expected_mun) + ')'
    #                 expected_string = filter_txt(line.strip("\n"))
    #                 # expected_string = line.strip("\n")
    #
    #     else:
    #         expected_string_abra = line.split("#Abra(")[1].split("), ")[0]
    #         expected_string = filter_txt(line.strip("\n"))
    #         # expected_string = line.strip("\n")
    #
    # elif "#Abra" in line and ("affecting" in line or "experienced" in line):
    #     if ("#Abra(" not in line and rest_of_abra_string not in line) or ("#Abra(" not in line and portion_of_abra_string not in line):
    #         all_affected_flag = True
    #         affected_string = filter_txt(line.strip("\n"))
    #         # affected_string = line.strip("\n")
    #     else:
    #         affected_string_abra = line.split("#Abra(")[1].split(")")[0]
    #         affected_string = filter_txt(line.strip("\n"))
    #         # affected_string = line.strip("\n")
    #
    #         affected_string_abra_1 = affected_string_abra.replace("and", ", ")
    #         affected_mun = re.split(r", ", affected_string_abra_1)
    #
    #         affected_mun = [mun.strip(" ") for mun in affected_mun]
    #
    #         print("dsdsdsd")
    #         print(affected_mun)
    #
    # else:
    #     pass




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
    # print(f"Municipality Name: {mun_name}, TSTM: {ex_af}")

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





        # if all_expected_flag:
        #     feature['rain_cat'] = 1
        # elif all_affected_flag:
        #     feature['rain_cat'] = 2
        # elif mun_name not in expected_string_abra and mun_name not in affected_string_abra:
        #     feature['rain_cat'] = 0
        # elif mun_name in expected_string_abra:
        #     feature['rain_cat'] = 1
        # elif mun_name in affected_string_abra:
        #     feature['rain_cat'] = 2
        # else:
        #     feature['rain_cat'] = 0

        layer.updateFeature(feature)
        up_hrw = feature.attribute('hrw')

        print(f"Municipality Name: {mun_name}, RAIN_CAT: {up_hrw}")

manager = project.layoutManager()
layouts_list = manager.printLayouts()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
document = QDomDocument()

# read template content
template_file = open("/Users/kaizerjohnmacni/Documents/rainfall_advisory/hrw_sur.qpt")
template_content = template_file.read()
template_file.close()
document.setContent(template_content)

# load layout from template and add to Layout Manager
layout.loadFromTemplate(document, QgsReadWriteContext())
project.layoutManager().addLayout(layout)
layout = QgsProject.instance().layoutManager().layoutByName("hrw_is")

# update Text values
header = layout.itemById("advisory_number")
weather = layout.itemById("weather_system")
datetime = layout.itemById("datetime")
red_hrw = layout.itemById("red_hrw")
orange_hrw = layout.itemById("orange_hrw")
yellow_hrw = layout.itemById("yellow_hrw")
affecting_msg = layout.itemById("affecting_msg")
expecting_msg = layout.itemById("expecting_msg")

header.setText(title)
datetime.setText(date_time)
weather.setText(weather_system)
# red_hrw.setText(red_warning_string)
# orange_hrw.setText(orange_warning_string)
# yellow_hrw.setText(yellow_warning_string)
#
# affecting_msg.setText(affecting_string)
# expecting_msg.setText(expecting_string)

red_hrw.setText(red_warning_string)
# text_format.setSize(adjust_fsize(red_warning_string))
text_format.setSize(fsize)
red_hrw.setTextFormat(text_format)

orange_hrw.setText(orange_warning_string)
# text_format.setSize(adjust_fsize(orange_warning_string))
text_format.setSize(fsize)
orange_hrw.setTextFormat(text_format)

yellow_hrw.setText(yellow_warning_string)
# text_format.setSize(adjust_fsize(yellow_warning_string))
text_format.setSize(fsize)
yellow_hrw.setTextFormat(text_format)

affecting_msg.setText(affecting_string)
# text_format1.setSize(adjust_fsize_ae(affecting_string))
text_format1.setSize(fsize2)
affecting_msg.setTextFormat(text_format1)

expecting_msg.setText(expecting_string)
# text_format1.setSize(adjust_fsize_ae(expecting_string))
text_format1.setSize(fsize2)
expecting_msg.setTextFormat(text_format1)

# base_path = os.path.join()
png_path = os.path.join("/Users/kaizerjohnmacni/Downloads",
                        str(today) + " " + curr_time[0:2] + "-" + curr_time[-2:] + "IlocosSurHRW.png")

exporter = QgsLayoutExporter(layout)
exporter.exportToImage(png_path, QgsLayoutExporter.ImageExportSettings())
print("done")

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()