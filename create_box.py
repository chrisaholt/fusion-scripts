# Simple example for creating a box.

import adsk.core, adsk.fusion, adsk.cam, traceback

def get_input(ui, text_prompt, title, default_value):
    value, cancelled = ui.inputBox(text_prompt, title, default_value)
    if cancelled:
        return None
    if not value:
        raise ValueError("Unknown value entered.")
    return value

def run(context):
    ui = None
    try:
        # Get the active design.
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        root_component = design.rootComponent

        # Set up units.
        units_manager = design.unitsManager
        units_name = units_manager.defaultLengthUnits

        # Create a new value input box for Length, Width, and Height
        inputs = adsk.core.CommandInputs.cast(None)

        length = get_input(ui, f"Enter the length of the box ({units_name}):", "Box Length", "100")
        width = get_input(ui, f"Enter the width of the box ({units_name}):", "Box Width", "50")
        height = get_input(ui, f"Enter the height of the box ({units_name}):", "Box Height", "25")
        if length is None or width is None or height is None:
            return

        length = units_manager.evaluateExpression(length, units_name)
        width = units_manager.evaluateExpression(width, units_name)
        height = units_manager.evaluateExpression(height, units_name)

        # Create a new sketch on the xy plane
        sketches = root_component.sketches
        xy_plane = root_component.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw a rectangle for the base of the box
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(length, width, 0))
        
        # Extrude the rectangle to create the box
        square_profile = sketch.profiles.item(0)
        extrudes = root_component.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            square_profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(height)
        extrude_input.setDistanceExtent(False, distance)
        extrudes.add(extrude_input)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))