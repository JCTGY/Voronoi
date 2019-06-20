#Author-
#Description-
import adsk.core, adsk.fusion, adsk.cam, traceback
import random

_app = None
_ui  = None
_rowNumber = 0
# Event handler that reacts when the command definitio is executed which
# results in the command being created and this event being fired.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Get the command that was created.
            cmd = adsk.core.Command.cast(args.command)
        
            # Get the CommandInputs collection associated with the command.
            inputs = cmd.commandInputs
            # Create a tab input.
            tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Tab 1')
            tab1ChildInputs = tabCmdInput1.children
            selectionInput = tab1ChildInputs.addSelectionInput('selection', 'Select', 'Basic select command input')
            selectionInput.setSelectionLimits(0)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
      #  doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) 
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        o = sketch.originPoint
        
        #sketch.geometricConstraints_var.addCoincident(origin, Cir_In.centerSketchPoint)
        dims = sketch.sketchDimensions
        points = sketch.sketchPoints
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs
        
        #createParam(design, "test", "10", "mm", "comment test")
        constraints = sketch.geometricConstraints
        
        radius = 200
        rangeX = (0, 2500)
        rangeY = (0, 2500)
        qty = 100  # or however many points you want

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
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
