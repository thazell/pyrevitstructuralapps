"""
Copyright (c) 2014-2016 Gui Talarico
Written for pyRevit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

Copyright (c) 2014-2017 Timon Hazell
Python scripts for Autodesk Revit
TESTED API: 2015 | 2016

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
	
TaskDialog.Show('Not working', "programming isn't done yet, need a way to save to new file")

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
        if not (view.IsTemplate) and view.ViewType == ViewType.DraftingView:
            viewlist.append(view)
ids = []

#select the views you want to export
options = sorted(getNames(viewlist))
if options:
    selected_fromlist = SelectFromList.show(options)
    logger.debug('Selected symbols are: {}'.format(selected_fromlist))
    if selected_fromlist:
        for item in selected_fromlist:
            for v in viewlist:
                if item == v.Name:
                    baseview = v
                    TaskDialog.Show('BaseView', v.Name)
    else:
        TaskDialog.Show('pyRevit', 'You must select at least one item')
        sys.exit
else:
    TaskDialog.Show('pyRevit', 'You must select one item')
    sys.exit
#this does not work in 2-16
newdoc = Autodesk.Revit.ApplicationServices.Application.NewProjectDocument("L:\Drafting Resources\Revit\Templates\2016 - Silman.rte")
 
newdoc.SaveAs( "C:/tmp/new_project.rvt" );