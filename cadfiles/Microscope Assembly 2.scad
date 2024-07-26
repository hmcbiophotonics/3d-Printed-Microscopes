use <camera_mount.scad>
use <top.scad>
use <structure.scad>
use <mount_holder.scad>

// 22 mm is the distance from the center line of the mounting holes to the camera center

center_offset = [65.5/2, 70/2];

top_z_offset = 58;
camera_mount_z_offset = 100;

module CameraMountAndHolder () {
  translate([0, 26.6, 0]) rotate([0,0,-90]) CameraMount();
  translate([0, 14, 0]) rotate([0,0,-90]) MountHolder();
}

module MicroscopeAssembly() {
  color("black")
  translate([0, 0, top_z_offset]) Top();
  translate([center_offset[0], 5.9, 70]) CameraMountAndHolder();
  Structure();
  
}

translate(-center_offset) MicroscopeAssembly();

//CameraMountAndHolder();