#!/usr/bin/python
# -*- coding: latin-1 -*-

import xml.etree.ElementTree as ET, os, sys, glob, re
import configparser


# Safe return of config parameter from parser.ini, return 0 if option is not found
def _get_config(_section, _parameter):
    # Get script current directory
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    # Read configuration file options.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(scriptDir, "options.ini"))
    configOptional = []
    try :  return config[_section][_parameter]
    except KeyError:
        if not _parameter in configOptional:
            print( "WARNING : Parameter \"", _parameter, "\" not defined for template : ", _section)
            print( "WARNING : Please review", os.path.join(scriptDir, "options.ini"), " configuration")
        return "none"

# Safe return of config parameter from parser.ini, return 0 if option is not found
def _get_threshold(_section, _parameter):
    # Get script current directory
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    # Read configuration file threshold.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(scriptDir, "threshold.ini"))

    configOptional = ["property", "value"]
    try:
        return config[_section][_parameter]
    except KeyError:
        if not _parameter in configOptional:
            print("WARNING : Parameter \"", _parameter, "\" not defined for template : ", _section)
            print("WARNING : Please review ", os.path.join(scriptDir, "threshold.ini"), "configuration")
        return "none"


mapping_unit = {
    "Kbps":"Bandwidth_bits,kiloBitspersecond",
    "Mbps":"Bandwidth_bits,MegaBitspersecond",
    "Gbps":"Bandwidth_bits,GigaBitspersecond",
    "KB":"Bytes,kiloBytes",
    "MB":"Bytes,MegaBytes",
    "GB":"Bytes,GigaBytes",
    "ms": "Temporal,MilliSecond",
    "s": "Temporal,Second",
    "m": "Temporal,Minute",
    "h": "Temporal,Hour",
    '%': "Percent,Percent"
}

# Header
def gen_xml_tree_root():
    root = ET.Element("Object", x_class="com.infovista.util.nds.NamedDataSet")
    return root


# Default Detail Settings
def gen_xml_tree_header(root, mode):
    sroot = ET.SubElement(root, "DetailDefaultSettings", list="true")
    s2_sroot = ET.SubElement(sroot, "DrillDown", list="true")
    s3_sroot = ET.SubElement(s2_sroot, "DetailDrillDown", list="true")
    s4_sroot = ET.SubElement(s3_sroot, "ShowInColumn")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "true"

    if mode == "temporal":
        s2_sroot = ET.SubElement(sroot, "Layout", list="true")
        s3_sroot = ET.SubElement(s2_sroot, "MasterTemplate")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "table.xml"

        s3_sroot = ET.SubElement(s2_sroot, "HtmlLayoutMode")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "FixedHeader"

        s3_sroot = ET.SubElement(s2_sroot, "ChartAutotPlacement")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "true"

        s3_sroot = ET.SubElement(s2_sroot, "ChartsPerLine")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "2"

    s2_sroot = ET.SubElement(sroot, "TimeSpan", list="true")
    s3_sroot = ET.SubElement(s2_sroot, "TimeSpan_1", list="true")

    s4_sroot = ET.SubElement(s3_sroot, "DisplayRateGeneral", list="true")
    s5_sroot = ET.SubElement(s4_sroot, "Code")
    s6_sroot = ET.SubElement(s5_sroot, "value")
    s6_sroot.text = "11"

    s4_sroot = ET.SubElement(s3_sroot, "UseDefaultTimeSpan")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "true"

    s4_sroot = ET.SubElement(s3_sroot, "DisplayRateGeneral", list="true")
    s5_sroot = ET.SubElement(s4_sroot, "Code")
    s6_sroot = ET.SubElement(s5_sroot, "value")
    s6_sroot.text = "11"

    s4_sroot = ET.SubElement(s3_sroot, "Count")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "1"

    s4_sroot = ET.SubElement(s3_sroot, "Unit")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "20"


    sroot = ET.SubElement(root, "Vista", list="true")
    s2_sroot = ET.SubElement(sroot, "Wid")
    s3_sroot = ET.SubElement(s2_sroot, "value", list="true")
    s3_sroot.text = "0602300080C811E6ABB10050569240C5"

    return root


def gen_column_header(root):
    sroot = ET.SubElement(root, "Columns", list="true")
    return sroot


def gen_column_threshold(root_format, order, threshold_list):

    if order == "UP":
        threshold_list = reversed(threshold_list)
    elif order != "DOWN":
        #print("ERROR: Please specify threshold order UP or DOWN, skipping threshold...")
        return

    sroot = ET.SubElement(root_format, "Table", list="true")
    s1_sroot = ET.SubElement(sroot, "Alignment")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    s2_sroot.text = "0"
    s1_sroot = ET.SubElement(sroot, "Type")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    s2_sroot.text = "3"
    s1_sroot = ET.SubElement(sroot, "DefaultFontStyle")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    s2_sroot.text = "-1"
    s1_sroot = ET.SubElement(sroot, "NullValues", list="true")
    s2_sroot = ET.SubElement(s1_sroot, "FontStyle")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    s3_sroot.text = "-1"
    s2_sroot = ET.SubElement(s1_sroot, "NullValuesIcon")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    s3_sroot.text = "downarrow.gif"
    s2_sroot = ET.SubElement(s1_sroot, "NullValuesText")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    s3_sroot.text = "-"
    s2_sroot = ET.SubElement(sroot, "DecoThresholds", list="true")

    ct = 0

    for item in threshold_list:
        thr_prop = _get_threshold(item, "property")
        val_prop = _get_threshold(item, "value")

        if thr_prop == "none" and val_prop == "none":
            print("ERROR: Please define at least on of the 2 parameters (property or value) in threshold.ini for threshold:", str(item))
        ct += 1
        s3_sroot = ET.SubElement(s2_sroot, "DecoThreshold_"+str(ct), list="true")
        s4_sroot = ET.SubElement(s3_sroot, "Image")
        s5_sroot = ET.SubElement(s4_sroot, "value")
        # Image failback - Default:circlelight_red_a_4x.gif
        if not _get_threshold(item, "icon") == "none":
            s5_sroot.text = str(_get_threshold(item, "icon"))
        else:
            #failback default
            s5_sroot.text = "circlelight_red_a_4x.gif"
        s4_sroot = ET.SubElement(s3_sroot, "PropertyWID")
        s5_sroot = ET.SubElement(s4_sroot, "value")
        # Property failback - Common - Threshold High - 4827FE70EE4C11DF9966001422438980
        if not thr_prop == "none":
            s5_sroot.text = str(thr_prop)
        else:
            # failback default
            s5_sroot.text = "4827FE70EE4C11DF9966001422438980"
        s4_sroot = ET.SubElement(s3_sroot, "Threshold")
        s5_sroot = ET.SubElement(s4_sroot, "value")
        # Value failback - 99
        if not val_prop == "none":
            s5_sroot.text = str(val_prop)
        else:
            # failback default
            s5_sroot.text = "99"
        s4_sroot = ET.SubElement(s3_sroot, "CompareTo")
        s5_sroot = ET.SubElement(s4_sroot, "value")

        if not thr_prop == "none":
            s5_sroot.text = "Property"
        else:
            s5_sroot.text = "Value"

    s1_sroot = ET.SubElement(sroot, "DefaultImage")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    if order == "DOWN":
        default_icon = _get_config('DEFAULT-DOWN', 'icon')
    elif order == "UP":
        default_icon = _get_config('DEFAULT-UP', 'icon')
    else:
        #Failback
        default_icon = "circlelight_red_a_4x.gif"
    s2_sroot.text = str(default_icon)

    s1_sroot = ET.SubElement(sroot, "Position")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    s2_sroot.text = "0"
    s1_sroot = ET.SubElement(sroot, "Icon", list="true")
    s2_sroot = ET.SubElement(s1_sroot, "MaxWidth")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    s3_sroot.text = "5"
    s1_sroot = ET.SubElement(sroot, "ShowText")
    s2_sroot = ET.SubElement(s1_sroot, "value")
    s2_sroot.text = "true"


#Default Detail Settings
def gen_xml_column_data(root_col, col, name, wid, drilldown, unit="None", order="none", threshold_list=[]):

    sroot = ET.SubElement(root_col, "Column_"+str(col), list="true")
    s2_sroot = ET.SubElement(sroot, "Data", list="true")
    s3_sroot = ET.SubElement(s2_sroot, "Metric", list="true")
    # WID VALUE INPUT
    s4_sroot = ET.SubElement(s3_sroot, "Indicator_"+wid, list="true")
    s5_sroot = ET.SubElement(s4_sroot, "Name")
    s6_sroot = ET.SubElement(s5_sroot, "value")
    # NAME VALUE INPUT
    s6_sroot.text = name

    s1_root = ET.SubElement(sroot, "DrillDowns", list="true")
    s2_sroot = ET.SubElement(s1_root, "DrillDown_0", list="true")

    s3_sroot = ET.SubElement(s2_sroot, "AccessFrom")
    s4_sroot = ET.SubElement(s3_sroot, "value")
    s4_sroot.text = "1"

    s3_sroot = ET.SubElement(s2_sroot, "Type")
    s4_sroot = ET.SubElement(s3_sroot, "value")
    s4_sroot.text = "2"

    s3_sroot = ET.SubElement(s2_sroot, "VistaPortalTemplate", list="true")

    s4_sroot = ET.SubElement(s3_sroot, "ReportTemplate")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    #DRILLDOWN VALUE INPUT
    s5_sroot.text = drilldown

    s4_sroot = ET.SubElement(s3_sroot, "TemporalEvolution")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "false"

    s4_sroot = ET.SubElement(s3_sroot, "ExploreGroupsMode")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "-1"

    s4_sroot = ET.SubElement(s3_sroot, "Vista")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "none"

    s4_sroot = ET.SubElement(s3_sroot, "Property")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "none"

    s4_sroot = ET.SubElement(s3_sroot, "DisplayRate", list="true")
    s5_sroot = ET.SubElement(s4_sroot, "Code")
    s6_sroot = ET.SubElement(s5_sroot, "value")
    s6_sroot.text = "-1"

    s3_sroot = ET.SubElement(s2_sroot, "IconLink", list="true")

    s4_sroot = ET.SubElement(s3_sroot, "Image")
    s5_sroot = ET.SubElement(s4_sroot, "value")

    s5_sroot.text = "downarrow.gif"

    s4_sroot = ET.SubElement(s3_sroot, "ToolTip")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "Raw Counters"

    s1_root = ET.SubElement(sroot, "Format", list="true")
    s2_sroot = ET.SubElement(s1_root, "SubLabel")

    if unit != "None":
        try:
            split = mapping_unit[unit].split(',')
            #print("Mapped unit:", split[0], split[1])
        except:
            #print("INFO - no match for unit:", unit)
            return

        s2_sroot = ET.SubElement(s1_root, "Unit", list="true")
        s3_sroot = ET.SubElement(s2_sroot, "UnitType")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = split[0]
        s3_sroot = ET.SubElement(s2_sroot, "UnitNbFractionDigits")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "3"
        s3_sroot = ET.SubElement(s2_sroot, "UnitNbElt")
        if (unit == "%"):
            s4_sroot = ET.SubElement(s3_sroot, "value")

            s3_sroot = ET.SubElement(s2_sroot, "UnitBase")
            s4_sroot = ET.SubElement(s3_sroot, "value")
            s4_sroot.text = split[1]

            s3_sroot = ET.SubElement(s2_sroot, "UnitToFitTo")
            s4_sroot = ET.SubElement(s3_sroot, "value")

        else:
            s4_sroot = ET.SubElement(s3_sroot, "value")
            s4_sroot.text = "0"

            s3_sroot = ET.SubElement(s2_sroot, "UnitBase")
            s4_sroot = ET.SubElement(s3_sroot, "value")
            s4_sroot.text = split[1]

        s3_sroot = ET.SubElement(s2_sroot, "UnitHeader")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "true"

        s3_sroot = ET.SubElement(s2_sroot, "UnitCell")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "true"

        s3_sroot = ET.SubElement(s2_sroot, "UnitYAxis")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "true"

        s3_sroot = ET.SubElement(s2_sroot, "UnitLegend")
        s4_sroot = ET.SubElement(s3_sroot, "value")
        s4_sroot.text = "true"

        gen_column_threshold(s1_root, order, threshold_list)


def gen_xml_footer(root):

    sroot = ET.SubElement(root, "PortalVersion", list="true")

    s2_sroot = ET.SubElement(sroot, "Version")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    if _get_config('DEFAULT', 'VP_VERSION') != "none":
        s3_sroot.text = str(_get_config('DEFAULT', 'VP_VERSION'))
    else:
        #Failback
        s3_sroot.text = "5.1"


    s2_sroot = ET.SubElement(sroot, "BuildNumber")
    s3_sroot = ET.SubElement(s2_sroot, "value")
    if _get_config('DEFAULT', 'BUILD_NUMBER') != "none":
        s3_sroot.text = str(_get_config('DEFAULT', 'BUILD_NUMBER'))
    else:
        #Failback
        s3_sroot.text = "51029"

    sroot = ET.SubElement(root, "GroupingsLabel", list="true")

    s2_sroot = ET.SubElement(sroot, "DrillDowns", list="true")
    s3_sroot = ET.SubElement(s2_sroot, "DrillDown_1", list="true")
    s4_sroot = ET.SubElement(s3_sroot, "AccessFrom")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "0"

    s4_sroot = ET.SubElement(s3_sroot, "Type")
    s5_sroot = ET.SubElement(s4_sroot, "value")
    s5_sroot.text = "0"

    return sroot
