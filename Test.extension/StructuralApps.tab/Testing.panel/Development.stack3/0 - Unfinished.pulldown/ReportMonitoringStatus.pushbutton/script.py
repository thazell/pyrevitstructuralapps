"""
Copyright Silman 2017

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
from scriptutils import this_script

import clr

clr.AddReference("System")
from System.Collections.Generic import List

collector = FilteredElementCollector(doc)
allelements = collector.WhereElementIsNotElementType().ToElements()

allmonitoredelements = filter(lambda x: (Element.IsMonitoringLinkElement(x)),allelements)
allmonitoredelementsids = []
for element in allmonitoredelements:
    allmonitoredelementsids.append(element.Id)
apilist = List[ElementId](allmonitoredelementsids)
#exclude monitorred elements from allgrids
gridsNotMonitorredfilter = ExclusionFilter(apilist)

allgrids = collector.OfCategory(BuiltInCategory.OST_Grids).ToElements()

print "allgrid count" + str(len(allgrids))
#exclude monitorred elements from alllevels
#levelsNotMonitorredfilter = 
allgrids = collector.OfCategory(BuiltInCategory.OST_Levels).ToElements()

#Assign your output to the OUT variable.
#output:
print "All Monitored Elements:" 
for element in allmonitoredelements:
    try:
        elementname = element.Name
        elementid = element.Id
        elementtype = element.GetType().Name
    except:
        elementname = "<no view name available>"
        elementid = "<no view name available>"
    this_script.output.print_md("\n"    \
                                "{2}:{1}\n "                     \
                                "   {0}\n ".format(this_script.output.linkify(elementid),elementname,elementtype))
                                
print "Grids not Monitored:" 
for element in allgrids:
    if element not in allmonitoredelements:
        try:
            elementname = element.Name
            elementid = element.Id
            elementtype = element.GetType().Name
        except:
            elementname = "<no view name available>"
            elementid = "<no view name available>"
        this_script.output.print_md("\n"    \
                                "{2}:{1}\n "                     \
                                "   {0}\n ".format(this_script.output.linkify(elementid),elementname,elementtype))
