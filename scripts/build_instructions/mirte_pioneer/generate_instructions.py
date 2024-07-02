from freecad_build_instruction_generator import instruction_generator as gen
from pathlib import Path
import time
import importlib
importlib.reload(gen)

#TODO: 
# - alle onderdelen goede plaats (eerste Dante step export goed)
# - L.add time sleep om zwtart et vorkomen
# - L.do we need the orth fix?
# - L.closeDocument in assembly (met vraag of export)
# - L.frame houten kleur

# - met breadboard
# - mirte light & basic

# - warnings weg
# - step inport/export kleiner zodat snelle laadt (en overzichterlijker wordt)
# - new PCB
# - top goed als step export
# - step names when exporting
# - 3/4 mm???
# - combine with: https://osh-autodoc.org/#_installation

mirte = "basic"
type = "pcb"

# set the path where we are running the sources
dir_path = os.path.dirname(os.path.realpath(__file__))
gen.setCwdPath(dir_path)
gen.addSourcesPath('mirte', str(     (Path(dir_path) / '../../../build/step').resolve()     ))
gen.addSourcesPath('external', str(     (Path(dir_path) / '../../../external_parts').resolve()     ))
gen.setWarningPath( str(     (Path(dir_path) / '../warnings').resolve()     ))


if mirte == "pioneer":
  ### STEP 1 ####
  ## Insert SD card into Orange Pi
  opi_assembly = gen.AssemblyProject("OPI", False) # folfer files
  opi = opi_assembly.import_object("external", "OrangePi_Zero2.step", App.Vector(-27,7,0), App.Rotation(0,90,0))
  sd = opi_assembly.import_object("external", "Micro SD Card.STEP", App.Vector(-14.3,6.7,39.6), App.Rotation(0,180,90))
  #mirte_assembly.addWarning("sd")
  opi_assembly.addStep(gen.Step(sd, App.Vector(0,0,10)))
  opi_assembly.save_image_new_parts()
  opi_assembly.export()
  App.closeDocument("OPI") # todo: in module export

### CREATE Mirte assembly
mirte_assembly = gen.AssemblyProject("MIRTE", False) # folfer files

##### STEP 2 ####
### Add Orange Pi to base
base_lower = mirte_assembly.import_object("mirte", "layer_bottom.step") # + name
if mirte == "pioneer":
  pcb_step = mirte_assembly.import_object("build", "OPI.step", App.Vector(0, -5,0), App.Rotation(0,0,0))
  mirte_assembly.addWarning("orangepi")
  mirte_assembly.addStep(gen.Step(pcb_step, App.Vector(0,50,0)))
  mirte_assembly.save_image_new_parts()

  ###### STEP 3 ####
  ### Add Bolts and Nuts
  opi_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-54.5,6,24), App.Rotation(0,90,180))
  opi_bolt2 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(.5,6,24), App.Rotation(0,90,180))
  opi_bolt3 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-54.5,6,-24), App.Rotation(0,90,180))
  opi_bolt4 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(.5,6,-24), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(opi_bolt1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(opi_bolt2, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(opi_bolt3, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(opi_bolt4, App.Vector(0,50,0)) ])]))
  opi_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-54.5,-3,24), App.Rotation(0,90,180))
  opi_nut2 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(.5,-3,24), App.Rotation(0,90,180))
  opi_nut3 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-54.5,-3,-24), App.Rotation(0,90,180))
  opi_nut4 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(.5,-3,-24), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(opi_nut1, App.Vector(0,-60,0))]), gen.Sequence([gen.Step(opi_nut2, App.Vector(0,-60,0)) ]), gen.Sequence([gen.Step(opi_nut3, App.Vector(0,-60,0)) ]), gen.Sequence([gen.Step(opi_nut4, App.Vector(0,-60,0)) ])]))
  mirte_assembly.save_image_new_parts()

####### STEP 4 ####
##### Add Line Follow (incl nuts and bolts)
linefollow = mirte_assembly.import_object("external", "TCRT5000mod.step", App.Vector(59.5,3,-7), App.Rotation(-58,0,0))
mirte_assembly.addStep(gen.Step(linefollow, App.Vector(0,50,0)))
lf_bolt = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(58,6,0), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.Step(lf_bolt, App.Vector(0,50,0)))
lf_nut = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(58,-3,0), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.Step(lf_nut, App.Vector(0,-60,0)))
mirte_assembly.save_image_new_parts()

####### STEP 5 ####
##### Add Motor Frames
motor_frame_front = mirte_assembly.import_object("mirte", "motor_clamp_plate.step", App.Vector(-2.7,-9.1,47), App.Rotation(0,90,-90))
motor_frame_back = mirte_assembly.import_object("mirte", "motor_clamp_plate.step", App.Vector(-2.7 + 25,-9.1,47), App.Rotation(0,90,-90))
###TODO: this should be: ParallelSequence([Step(motor_frame_front, App.Vector(0,100,0)), Step(motor_frame_back, App.Vector(0,100,0))]).execute()
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_frame_front, App.Vector(0,100,0))]), gen.Sequence([gen.Step(motor_frame_back, App.Vector(0,100,0))])]))
mirte_assembly.save_image_new_parts()

###### STEP 6 ####
#### Add Holders
mirte_assembly.toggleView()
motor_frame_holder_left = mirte_assembly.import_object("mirte", "motor_clamp_wedge.step", App.Vector(-3 ,-3,-44.4), App.Rotation(0,0,0))
motor_frame_holder_right = mirte_assembly.import_object("mirte", "motor_clamp_wedge.step", App.Vector(-3 ,-3,36.2), App.Rotation(0,0,0))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_frame_holder_left, App.Vector(-100,0,0))]), gen.Sequence([gen.Step(motor_frame_holder_right, App.Vector(-100,0,0))])]))
mirte_assembly.save_image_new_parts()

###### STEP 7 ####
### Add caster wheel
caster_wheel = mirte_assembly.import_object("external", "Low ball caster plastic.step", App.Vector(-87,-3,0), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.Step(caster_wheel,  App.Vector(0,-50,0)))
mirte_assembly.save_image_new_parts()

##### STEP 8 ####
### Add Bolts and Nuts
caster_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-87,3,20), App.Rotation(0,90,180))
caster_bolt2 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-87,3,-20), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(caster_bolt1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(caster_bolt2, App.Vector(0,50,0)) ])]))
caster_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-87,-6,20), App.Rotation(0,90,180))
caster_nut2 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-87,-6,-20), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(caster_nut1, App.Vector(0,-50,0))]), gen.Sequence([gen.Step(caster_nut2, App.Vector(0,-50,0)) ])]))
mirte_assembly.save_image_new_parts()

##### STEP 9 ####
### Assemble PCB with pico
pcb_assembly = gen.AssemblyProject("PCB", False) # folfer files 
pcb = pcb_assembly.import_object("external", "mirte_pcb.step", App.Vector(91, 46, 91.5), App.Rotation(0,180,-90)) # + name
pipico = pcb_assembly.import_object("external", "PICO_PinsDown.STEP", App.Vector(-16.5, 58, -31.5), App.Rotation(0,180,0))
mirte_assembly.addWarning("pipico")
pcb_assembly.addStep(gen.Step(pipico, App.Vector(0,40,0)))
pcb_assembly.save_image_new_parts()

##### STEP 10 ####
### Assemble PCB with motor controller
motordriver = pcb_assembly.import_object("external", "I9110 motor driver.STEP", App.Vector(-38.5, 55, 41), App.Rotation(0,90,0))
mirte_assembly.addWarning("pins")
pcb_assembly.addStep(gen.Step(motordriver, App.Vector(0,40,0)))
pcb_assembly.save_image_new_parts()
pcb_assembly.export()
App.closeDocument("PCB")

##### STEP 11 ####
### Add PCB to OPi
mirte_assembly.toggleView()
if mirte == "pioneer":
  pcb_step = mirte_assembly.import_object("build", "PCB.step", App.Vector(-104, 2,0), App.Rotation(-90,0,0))
else:
  pcb_step = mirte_assembly.import_object("build", "PCB.step", App.Vector(4.2, -42.8,0), App.Rotation(0,0,0))
mirte_assembly.addWarning("pins")
mirte_assembly.addStep(gen.Step(pcb_step, App.Vector(0,50,0)))
mirte_assembly.save_image_new_parts()

if mirte == "pioneer":
  ###### STEP 12 ####
  #### Add Upper Base
  base_upper = mirte_assembly.import_object("mirte", "layer_top.step", App.Vector(-.5, 40.15, 0), App.Rotation(0,0,0))
  mirte_assembly.addStep(gen.Step(base_upper, App.Vector(0,100,0)))
  mirte_assembly.save_image_new_parts()

  ###### STEP 13 ####
  #### Pen hole lock
  pen_hole_lock = mirte_assembly.import_object("mirte", "motor_clamp_lock.step", App.Vector(-3.5, 43.9, -12.4), App.Rotation(0,0,0))
  mirte_assembly.addStep(gen.Step(pen_hole_lock, App.Vector(100,0,0)))
  wig = mirte_assembly.import_object("mirte", "wedge.step", App.Vector(25, 27, 1.5), App.Rotation(0,180,-90))
  mirte_assembly.addStep(gen.Step(wig, App.Vector(0,100,0)))
  mirte_assembly.save_image_new_parts()

  ####### STEP 14 ####
  ##### Spacers
  spacer1 = mirte_assembly.import_object("mirte", "spacer.step", App.Vector(57.8, 45.3, 64), App.Rotation(0,180,90))
  spacer2 = mirte_assembly.import_object("mirte", "spacer.step", App.Vector(57.8, 45.3, -64), App.Rotation(0,180,90))
  spacer3 = mirte_assembly.import_object("mirte", "spacer.step", App.Vector(-67, 44, 67), App.Rotation(0,45,90))
  spacer4 = mirte_assembly.import_object("mirte", "spacer.step", App.Vector(-70, 43, -64.5), App.Rotation(0,-45,90))
  #mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(spacer1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(spacer2, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(spacer3, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(spacer4, App.Vector(0,50,0)) ])]))
  #mirte_assembly.save_image_new_parts()

###### STEP 15 ####
motor_left = mirte_assembly.import_object("external", "GearedMotor 3-6V.step", App.Vector(11.5, 4.5, 37.5), App.Rotation(90,0,0))
motor_right = mirte_assembly.import_object("external", "GearedMotor 3-6V.step", App.Vector(11.5, 4.5, -37.5), App.Rotation(90,0,0))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_left, App.Vector(0,0,0), App.Vector(0,1,0), -30), gen.Step(motor_left, App.Vector(0,0,50))]), gen.Sequence([gen.Step(motor_right, App.Vector(0,0,0), App.Vector(0,1,0), 30), gen.Step(motor_right, App.Vector(0,0,-50))])]))
mirte_assembly.save_image_new_parts()

###### STEP 16 ####
#wheel_left = mirte_assembly.import_object("external", "Wheel D65x25.STEP", App.Vector(11.5, 15.5, 77), App.Rotation(0,0,0))
#wheel_right = mirte_assembly.import_object("external", "Wheel D65x25.STEP", App.Vector(11.5, 15.5, -77), App.Rotation(0,0,180))
#mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(wheel_left, App.Vector(0,0,50))]), gen.Sequence([gen.Step(wheel_right, App.Vector(0,0,-50))])]))
#mirte_assembly.save_image_new_parts()
#
######## STEP 17 ####
###### Powerbank
#powerbank = mirte_assembly.import_object("external", "dummy_powerbank.step", App.Vector(-76, 36, 0), App.Rotation(0,90,0))
#mirte_assembly.addStep(gen.Step(powerbank, App.Vector(0,100,0)))
#mirte_assembly.save_image_new_parts()
#
#
###### Export full STEP ####
#save_image()
#mirte_assembly.export()
#App.closeDocument("Mirte")

