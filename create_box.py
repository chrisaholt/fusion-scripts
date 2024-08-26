# Simple example for creating a box.

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        # Get the active design.
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        root_component = design.rootComponent

        # Create a new sketch on the xy plane
        sketches = root_component.sketches
        xy_plane = root_component.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw a rectangle for the base of the box
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(100, 100, 0))
        
        # Extrude the rectangle to create the box
        square_profile = sketch.profiles.item(0)
        extrudes = root_component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            square_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(50)
        extrude_input.setDistanceExtent(False, distance)
        extrudes.add(extrude_input)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))