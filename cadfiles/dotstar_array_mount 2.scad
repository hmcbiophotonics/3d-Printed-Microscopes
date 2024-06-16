/*
    Filename: Dotstar_8x8_Array_Pi_Mount.scad
    Author: Josh Brake
    Email: jbrake@hmc.edu
    Date: 12/19/21
    Description: A mount to attach an 8x8 Dotstar array to the mounting holes for a Raspberry Pi
*/

$fa = 0.1;
$fs = 1;
$fn = 100;

module DotstarArrayMount() {
  // Units are assumed to be in millimeters
  hat_thickness=4;
  hat_length = 65;
  hat_width = 56;
  mounting_hole_offset = 3.5;
  mounting_hole_diameter = 3.5;

  led_pitch = 3.05; // Separation between adjacent LEDs

  difference() {
      cube([hat_length, hat_width, hat_thickness], center=true);
      
      // Mounting holes for hat
      translate([hat_length/2-mounting_hole_offset, hat_width/2 - mounting_hole_offset, 0]) cylinder(hat_thickness+0.01, d = mounting_hole_diameter, center = true);
      translate([hat_length/2-mounting_hole_offset, -(hat_width/2-mounting_hole_offset), 0]) cylinder(hat_thickness+0.01, d = mounting_hole_diameter, center = true);
      translate([-(hat_length/2-mounting_hole_offset), hat_width/2-mounting_hole_offset, 0]) cylinder(hat_thickness+0.01, d = mounting_hole_diameter, center = true);
      translate([-(hat_length/2-mounting_hole_offset), -(hat_width/2-mounting_hole_offset), 0]) cylinder(hat_thickness+0.01, d = mounting_hole_diameter, center = true);
    
      translate([led_pitch/2, led_pitch/2 ,0]) DotstarArray();
    }
  module DotstarArray() {
      // Mounts for 8x8 dotstar array
      dotstar_thickness = 2;
      dotstar_w = 25.4;
      dotstar_tab_w = 5.25;
      cube([dotstar_w, dotstar_w, hat_thickness+0.01], center=true);
      
      tab_centers_x = [(dotstar_w + dotstar_tab_w)/2, (dotstar_w + dotstar_tab_w)/2, -(dotstar_w + dotstar_tab_w)/2, -(dotstar_w + dotstar_tab_w)/2];
          
      tab_centers_y = [(dotstar_w - dotstar_tab_w)/2, -(dotstar_w - dotstar_tab_w)/2, (dotstar_w - dotstar_tab_w)/2, -(dotstar_w - dotstar_tab_w)/2];
      
      for(i = [0:3]) {
              translate([tab_centers_x[i],tab_centers_y[i],hat_thickness - dotstar_thickness]) cube([dotstar_tab_w + 0.01, dotstar_tab_w + 0.01, 4], center=true); 
          
          translate([tab_centers_x[i],tab_centers_y[i],0]) cylinder(hat_thickness+0.01, d=3, center=true);
      }
  }
}

DotstarArrayMount();