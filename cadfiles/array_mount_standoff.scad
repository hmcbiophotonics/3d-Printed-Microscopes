/*
    Filename: array_mount_standoff.scad
    Author: Fred Kim
    Email: fred.kim@cooper.edu
    Date: 07/02/2024
    Description: A standoff to mount quad_dotstar_array_mount onto microscope housing
*/

$fa = 0.1;
$fs = 1;
$fn = 100;

module Standoff() {
  // Units are assumed to be in millimeters
  length = 7;
  width = 15;
  height = 5;

  hole_dia = 1.5;
  hole_offset = 3; //hole offset from leg
  difference() {
      cube([length,width,height],center=true);
      translate([0,hole_offset,0])
      cylinder(h = height+1, r = hole_dia, center=true);
  }
}

Standoff();
