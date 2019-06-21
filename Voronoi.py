#Author-
#Description-
import adsk.core, adsk.fusion, adsk.cam, traceback
import random
import numpy as np
import scipy
from scipy.spatial import Voronoi, voronoi_plot_2d


# global set of event handlers to keep them referenced for the duration of the command
handlers = []
commandId = 'ApplyVoronoiFace'
commandName = 'ApplyFaceToSelection'
commandDescription = 'Apply Voronoi to selected bodies or occurrences'
#import matplotlib.pyplot as plt

#import sys, os

#module = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Module')
#sys.path.insert(0, module)
#popped = sys.path.pop(0)
#assert(popped == module)




app = None
ui  = None
# Event handler that reacts when the command definitio is executed which
# results in the command being created and this event being fired.
def getSelectedObjects(selectionInput):
    objects = []
    for i in range(0, selectionInput.selectionCount):
        selection = selectionInput.selection(i)
        selectedObj = selection.entity
        if type(selectedObj) is adsk.fusion.BRepBody or \
           type(selectedObj) is adsk.fusion.BRepFace or \
           type(selectedObj) is adsk.fusion.Occurrence:
           objects.append(selectedObj)
    return objects

def putRandomPoints(SelecFace):
    radius = 200
    rangeX = (0, 2500)
    rangeY = (0, 2500)
    qty = 100  # or however many points you want
    
    points = sketch.sketchPoints
    # Generate a set of all points within 200 of the origin, to be used as offsets later
    # There's probably a more efficient way to do this.
    deltas = set()
    for x in range(-radius, radius+1):
        for y in range(-radius, radius+1):
            if x*x + y*y <= radius*radius:
                deltas.add((x,y))

    randPoints = []
    excluded = set()
    i = 0
    while i<qty:
        x = random.randrange(*rangeX)
        y = random.randrange(*rangeY)
        if (x,y) in excluded: continue
        randPoints.append((x,y))
        point = adsk.core.Point3D.create(x, y, 0)
        sketchPoint = points.add(point)
        i += 1
        #excluded.update((x+dx, y+dy) for (dx,dy) in deltas)

class ApplyAppearanceExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmd = args.firingEvent.sender
            inputs = cmd.commandInputs
            selectionInput = None
            appearanceListInput = None
            for inputI in inputs:
                global commandId
                if inputI.id == commandId + '_selection':
                    selectionInput = inputI
           
            objects = getSelectedObjects(selectionInput)

            if not objects or len(objects) == 0:
                return
            
            if not appearanceListInput.selectedItem:
                if ui:
                    ui.messageBox('Appearance is not selected.')
                return
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                
class ApplyAppearanceDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # when the command is done, terminate the script
            # this will release all globals which will remove all event handlers
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class ApplyAppearanceCreatedHandler(adsk.core.CommandCreatedEventHandler):    
    def __init__(self):
        super().__init__()        
    def notify(self, args):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            onExecute = ApplyAppearanceExecuteHandler()
            cmd.execute.add(onExecute)
            
            # keep the handler referenced beyond this function
            handlers.append(onExecute)
            inputs = cmd.commandInputs
            global commandId
            selectionInput = inputs.addSelectionInput(commandId + '_selection', 'Select', 'Select bodies or occurrences')
            selectionInput.setSelectionLimits(1)
            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Tab 1')
            tab1ChildInputs = tabCmdInput1.children
            Number_Points = tab1ChildInputs.addIntegerSliderCommandInput('Points', 'Number Points', 0, 100);
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
      #  doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) 
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        lines = sketch.sketchCurves.sketchLines
         
        #createConstrain
        constraints = sketch.geometricConstraints
         #handle the input selection
 #       global commandId
 #       global commandName
 #       global commandDescription
        
#        cmdDef = ui.commandDefinitions.itemById(commandId)
#        if not cmdDef:
#            cmdDef = ui.commandDefinitions.addButtonDefinition(commandId, commandName, commandDescription) # no resource folder is specified, the default one will be used
#        onCommandCreated = ApplyAppearanceCreatedHandler()
#        cmdDef.commandCreated.add(onCommandCreated)
        # keep the handler referenced beyond this function
#        handlers.append(onCommandCreated)

 #       inputs = adsk.core.NamedValues.create()
 #       cmdDef.execute(inputs)

        # prevent this module from being terminate when the script returns, because we are waiting for event handlers to fire
 #       adsk.autoTerminate(False)
 #      *******************************************************************************************************************
        High = 15
        Width = 10
        a = 0
        b = 0
        square = lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(10, 15, 0))
        help(square)        
        #constraints.addCoincident(o, square)
        
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
