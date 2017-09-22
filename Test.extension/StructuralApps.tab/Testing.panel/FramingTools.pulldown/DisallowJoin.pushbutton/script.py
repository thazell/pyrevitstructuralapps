"""
Copyright (c) 2017 Timon Hazell
BaseCode Copyright (c) 2014-2016 Gui Talarico
"""

import sys
import os
import clr
sys.path.append(os.path.dirname(__file__))

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *
from Autodesk.Revit.DB import Transaction

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def get_selected_elements():
    """ Add Doc """
    selection = uidoc.Selection
    selection_ids = selection.GetElementIds()
    selection_size = selection_ids.Count
    #logger.debug('selection_size: {}'.format(selection_size))
    # selection = uidoc.Selection.Elements  # Revit 2015
    if not selection_ids:
        #logger.error('No Elements Selected')
        sys.exit(0)
    elements = []
    for element_id in selection_ids:
        elements.append(doc.GetElement(element_id))
    return elements
beams = []   
beams = get_selected_elements()
t = Transaction(doc, 'Disallow Join on Selected Beams')
t.Start()
    
for b in beams:
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(b,0)
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.DisallowJoinAtEnd(b,1)    
t.Commit()