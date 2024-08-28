# Simple example for creating a box.

import adsk.core, adsk.fusion, adsk.cam, traceback

def get_input(ui, text_prompt, title, default_value):
    value, cancelled = ui.inputBox(text_prompt, title, default_value)
    if cancelled:
        return None
    if not value:
        raise ValueError("Unknown value entered.")
    return value

def create_box(root_component, length, width, height):
    """Create a box on the xy-plane."""
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
    box = extrudes.add(extrude_input)
    return box

def extrude_interior_from_box(root_component, box, length, width, height, interior_width):
    """Cut out interior to give a box with specified interior width of walls."""
    top_face = box.endFaces[0]
    sketches = root_component.sketches
    sketch = sketches.add(top_face)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(interior_width, interior_width, 0),
        adsk.core.Point3D.create(length - interior_width, width - interior_width, 0))

    # Extrude the interior rectangle downwards to hollow out the box
    profile = sketch.profiles.item(1)  # Inner profile
    extrudes = root_component.features.extrudeFeatures
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(interior_width - height)
    extrude_input.setDistanceExtent(False, distance)
    container = extrudes.add(extrude_input)

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
        interior_width = get_input(ui, f"Enter the interior width of the box ({units_name}):", "Box Height", "3")
        if length is None or width is None or height is None or interior_width is None:
            return

        length = units_manager.evaluateExpression(length, units_name)
        width = units_manager.evaluateExpression(width, units_name)
        height = units_manager.evaluateExpression(height, units_name)
        interior_width = units_manager.evaluateExpression(interior_width, units_name)

        # Create a box and extruded interior.
        box = create_box(root_component, length, width, height)
        container = extrude_interior_from_box(root_component, box, length, width, height, interior_width)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))