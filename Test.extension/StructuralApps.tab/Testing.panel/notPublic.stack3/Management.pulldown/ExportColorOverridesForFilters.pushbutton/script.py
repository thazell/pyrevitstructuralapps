"""
Copyright (c) 2014-2016 Gui Talarico
Written for pyRevit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2016

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

# Original Code by dp-stuff.org
# http://dp-stuff.org/revit-view-underlay-property-python-problem/
import os
import csv
from subprocess import Popen

from Autodesk.Revit.UI import TaskDialog

from scriptutils.userinput import SelectFromList
from scriptutils import logger, this_script

import clr

from System.Collections.Generic import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def getNames(z_element):
	z_elementname = []
	for e in z_element:
		z_elementname.append(e.Name)
	return z_elementname
	


views = []
baseid = "802532"
baseview = doc.GetElement(ElementId(int(baseid)))

#TaskDialog.Show("Original View",baseview.Name)

collector = FilteredElementCollector(doc)
allviews = collector.OfClass(View).ToElements()
templatelist = []
viewlist = []
for view in allviews:
    #if view.ViewType == ViewType.ThreeD:
        if (view.IsTemplate) and view.ViewType != ViewType.Schedule:
            templatelist.append(view)
        elif view.ViewType == ViewType.Elevation:
            viewlist.append(view)
        elif view.ViewType == ViewType.FloorPlan:
            viewlist.append(view)
        elif view.ViewType == ViewType.ThreeD:
            viewlist.append(view)
        elif view.ViewType == ViewType.EngineeringPlan:
            viewlist.append(view)
        elif view.ViewType == ViewType.Section:
            viewlist.append(view)
        elif view.ViewType == ViewType.Detail:
            viewlist.append(view)
        elif view.ViewType == ViewType.DraftingView:
            viewlist.append(view)
ids = []
options = sorted(getNames(viewlist)) + sorted(getNames(templatelist))

if options:
    selected_fromlist = SelectFromList.show(options)
    logger.debug('Selected symbols are: {}'.format(selected_fromlist))
    if selected_fromlist:
        for item in selected_fromlist:
            for v in viewlist:
                if item == v.Name:
                    views.append(v)
            for t in templatelist:
                if item == t.Name:
                    views.append(t)
                    #TaskDialog.Show('pyRevit', 'Appended T to views.')
    else:
             TaskDialog.Show('pyRevit', 'Unable to execute application.')
else:
     TaskDialog.Show('pyRevit', 'You must select one item')

file_path = "c:\Temp\export.csv"
directory = os.path.dirname(file_path)

try:
    os.stat(directory)
except:
    os.mkdir(directory)  
    

     
with open(file_path, 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    fieldnames = ['ViewName', 'FilterName', 'ProjectionLineColor', 'ProjectionLinePatternId', 'ProjectionLineWeight', 'ProjectionFillColor', '	ProjectionFillPattern', 'Transparency', 	'CutLineColor', 'CutLineWeight', '	CutLinePatternId',  '	CutFillColor', 	'CutFillPatternId']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for v in views:
        filters = v.GetFilters() # Get all the filter ids
        for f in filters:
            ogs = v.GetFilterOverrides(f)
            plred = ''
            plblue = ''
            plgreen = ''
            filtername = ''
            pfred = ''
            pfgreen = ''
            pfblue = ''
            clred = ''
            clgreen = ''
            clblue = ''
            cfred = ''
            cfgreen = ''
            cfblue = ''
            plpname = ''
            pfpname = ''
            clpname = ''
            cfpname = ''
            plw = ''
            clw = ''
            
            if ogs.IsValidObject:
                filtername = (doc.GetElement(f).Name)
                if ogs.ProjectionLineColor.IsValid:
                    plred = "R-" + str(ogs.ProjectionLineColor.Red)
                    plgreen = " G-" + str(ogs.ProjectionLineColor.Green)
                    plblue = " B-" + str(ogs.ProjectionLineColor.Blue)
                if ogs.ProjectionFillColor.IsValid:
                    pfred = "R-" + str(ogs.ProjectionFillColor.Red)
                    pfgreen = " G-" + str(ogs.ProjectionFillColor.Green)
                    pfblue = " B-" + str(ogs.ProjectionFillColor.Blue)
                if ogs.CutLineColor.IsValid:
                    clred = "R-" + str(ogs.CutLineColor.Red)
                    clpgreen = " G-" + str(ogs.CutLineColor.Green)
                    clblue = " B-" + str(ogs.CutLineColor.Blue)
                if ogs.CutFillColor.IsValid:
                    cfred = "R-" + str(ogs.CutFillColor.Red)
                    cfpgreen = " G-" + str(ogs.CutFillColor.Green)
                    cfblue = " B-" + str(ogs.CutFillColor.Blue)
                if ogs.ProjectionLineWeight != -1:
                    plw = ogs.ProjectionLineWeight
                if ogs.ProjectionLinePatternId.ToString() != "-1":
                    plpname = doc.GetElement(ogs.ProjectionLinePatternId).Name
                if ogs.ProjectionFillPatternId.ToString() != "-1":
                    pfpname = doc.GetElement(ogs.ProjectionFillPatternId).Name
                if ogs.CutLineWeight != -1:
                    clw = ogs.CutLineWeight
                if ogs.CutLinePatternId.ToString() != "-1":
                    clpname = doc.GetElement(ogs.CutLinePatternId).Name
                if ogs.CutFillPatternId.ToString() != "-1":
                    cfpname = doc.GetElement(ogs.CutFillPatternId).Name
                if ogs.CutFillPatternId.ToString() != "-1":
                    cfpname = doc.GetElement(ogs.CutFillPatternId).Name
            writer.writerow({'ViewName': v.Name, 'FilterName': filtername, 'ProjectionLineColor': (plred + plgreen + plblue), 'ProjectionLinePatternId': plpname , 'ProjectionLineWeight': plw, 'ProjectionFillColor': (pfred + pfgreen + pfblue), '	ProjectionFillPattern': pfpname, 'Transparency':ogs.Transparency, 	'CutLineColor': (clred + clgreen + clblue), 'CutLineWeight': clw, '	CutLinePatternId': clpname,  '	CutFillColor': (cfred + cfgreen + cfblue), 	'CutFillPatternId': cfpname })
            
p = Popen(file_path, shell=True)
