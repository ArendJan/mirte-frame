
import FreeCADGui as Gui
import time
import os
import sys
import subprocess

def runStartupMacros(name):
    # Do not run when NoneWorkbench is activated because UI isn't yet completely there
    print(name)
    if name != "NoneWorkbench":
        # Run macro only once by disconnecting the signal at first call
        FreeCADGui.getMainWindow().workbenchActivated.disconnect(runStartupMacros)
        import subprocess
        exec(open("/tmp/mirte-frame/scripts/build_instructions/mirte_pioneer/generate_instructions_test.py").read())

        # call the script
        # subprocess.run(["python3", "/tmp/mirte-frame/scripts/RenderSteps/build_instructions/mirte_pioneer/generate_instructions.py"])
        # FreeCAD.openDocument('/tmp/mirte-frame/freecadFiles/layer.FCStd')
        # FreeCAD.setActiveDocument("layer")
        # print("done")
        # App.setActiveDocument("layer")
        # App.ActiveDocument=App.getDocument("layer")
        # Gui.ActiveDocument=Gui.getDocument("layer")
        # doc = FreeCAD.ActiveDocument
        # doc.recompute()
        # Gui.runCommand('Std_OrthographicCamera',1)
        # Gui.Selection.addSelection('layer','Body001')
        print("klaar!!!")

        # Following 2 lines shall be duplicated for each macro to run
        # import MySuperMacro
        # MySuperMacro.run()

        # Eg. if a second macro shall be launched at startup
        # import MyWonderfulMacro
        # MyWonderfulMacro.run()

# The following 2 lines are important because InitGui.py files are passed to the exec() function...
# ...and the runMacro wouldn't be visible outside. So explicitly add it to __main__
import __main__
__main__.runStartupMacros = runStartupMacros
print("start asdflkjdfsaljkdfsa")
# Connect the function that runs the macro to the appropriate signal
FreeCADGui.getMainWindow().workbenchActivated.connect(runStartupMacros)
