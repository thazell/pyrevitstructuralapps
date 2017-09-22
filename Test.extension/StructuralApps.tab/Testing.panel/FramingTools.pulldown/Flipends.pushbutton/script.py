"""
Copyright (c) 2017 Timon Hazell
BaseCode Copyright (c) 2014-2016 Gui Talarico
"""

import sys
import os
import clr
sys.path.append(os.path.dirname(__file__))

import Autodesk
from Autodesk.Revit.DB import *

from System.Collections.Generic import *

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
t = Transaction(doc, 'Flip Ends')
t.Start()
    
for b in beams:
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.FlipEnds(b)    
t.Commit()