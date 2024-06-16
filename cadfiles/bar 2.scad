/*

This is the plastic bar that holds the springs at the bottom of the camera mount (camera_mount.scad)

*/

$fa = 0.2;
$fs = 0.2;

bar_d = 1.8;
rotate([90,0,0]) cylinder(h=23, d=bar_d,center=true);
translate([0,0,-0.5]) cube([bar_d,23,0.9], center=true);