# Author-korintje.
# Description-Get Appearance ID
import adsk.core, adsk.fusion, traceback

# Global set of event handlers
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface
newComp = None


# Define execute command
class AppearanceCommandExecuteHandler(adsk.core.CommandEventHandler):

    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            unitsMgr = app.activeProduct.unitsManager
            command = args.firingEvent.sender
            inputs = command.commandInputs
            selection_type = "no type"
            appearance_id = "no id"
            appearance_name = "no name"
            material_id = "no id"
            material_name = "no name"
            for ipt in inputs:
                if ipt.id == "selectedObject":
                    selection = ipt.selection(0)
                    entity = selection.entity
                    try:
                        appearance = entity.appearance
                        appearance_id = appearance.id
                        appearance_name = appearance.name
                        material = entity.material
                        material_id = material.id
                        material_name = material.name
                    except:
                        pass
                elif ipt.id == "appearanceId":
                    ipt.text = appearance_id
                elif ipt.id == "appearanceName":
                    ipt.text = appearance_name
                elif ipt.id == "materialId":
                    ipt.text = material_id
                elif ipt.id == "materialName":
                    ipt.text = material_name
            args.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Define destroy command
class AppearanceCommandDestroyHandler(adsk.core.CommandEventHandler):

    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        try:
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Define Command handler
class AppearanceCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):

    def __init__(self):
        super().__init__()

    def notify(self, args):

        try:
            cmd = args.command
            cmd.isRepeatable = False

            # Register Execute
            onExecute = AppearanceCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)

            # Register ExecutePreview
            onExecutePreview = AppearanceCommandExecuteHandler()
            cmd.executePreview.add(onExecutePreview)
            handlers.append(onExecutePreview)

            # Register Destroying event
            onDestroy = AppearanceCommandDestroyHandler()
            cmd.destroy.add(onDestroy)
            handlers.append(onDestroy)

            # Define the inputs
            inputs: adsk.core.CommandInputs = cmd.commandInputs
            selIpt = inputs.addSelectionInput('selectedObject', 'Selected object', 'select target object')
            selIpt.setSelectionLimits(1, 1)
            textAppearanceID = inputs.addTextBoxCommandInput('appearanceId', 'Appearance ID', 'Appearance ID', 2, True)
            textAppearanceName = inputs.addTextBoxCommandInput('appearanceName', 'Appearance Name', 'Appearance Name', 2, True)
            textMaterialID = inputs.addTextBoxCommandInput("materialId", "Material ID", "Material ID", 2, True)
            textMaterialName = inputs.addTextBoxCommandInput("materialName", "Material Name", "Material Name", 2, True)

        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Entry point of the script
def run(context):

    try:
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace.')
            return

        # Check the command exists or not
        commandDefinitions = ui.commandDefinitions
        cmdDef = commandDefinitions.itemById('GetAppearanceId')
        if not cmdDef:
            cmdDef = commandDefinitions.addButtonDefinition(
                'GetAppearanceId',
                'Get Appearance ID',
                'Get the appearance ID of the selected object.',
            )

        onCommandCreated = AppearanceCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
        inputs = adsk.core.NamedValues.create()
        cmdDef.execute(inputs)
        adsk.autoTerminate(False)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

