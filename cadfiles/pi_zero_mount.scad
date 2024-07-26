/*
 * Filename: pi_zero_mount.scad
 * Author: Fred Kim
 * Email: fred.kim@cooper.edu
 * Date: 07/09/2024
 * Description: A mount for the pi-zero onto the dotstar array mount
 */

$fa = 0.1;
$fs = 1;
$fn = 100;

module PiZeroMount() {
    mount_l = 65;
    mount_w = 56;
    mount_h = 4;

    mount_hole_dia = 3.5;

    pi_l = 65;
    pi_w = 30;
    pi_h = 4;

    pi_hole_dia = 3;

    dotstar_w = 25.4;
    led_pitch = 3.05; // Separation between adjacent LEDs

    difference() {
        union() {
            cube([mount_l,mount_w,mount_h],center = true);
            translate([0,(pi_l-mount_w)/2,0])
                rotate([0,0,90])
                cube([pi_l,pi_w+14,pi_h],center = true);
        }
        translate([led_pitch/2,-led_pitch/2,0])
            cube([dotstar_w,dotstar_w,8],center = true);

        mount_hole_offset = 3.5;
        translate([mount_l/2-mount_hole_offset,mount_w/2-mount_hole_offset,0])
            cylinder(h = 8, d = mount_hole_dia, center = true);
        translate([mount_l/2-mount_hole_offset,-(mount_w/2-mount_hole_offset),0])
            cylinder(h = 8, d = mount_hole_dia, center = true);
        translate([-(mount_l/2-mount_hole_offset),mount_w/2-mount_hole_offset,0])
            cylinder(h = 8, d = mount_hole_dia, center = true);
        translate([-(mount_l/2-mount_hole_offset),-(mount_w/2-mount_hole_offset),0])
            cylinder(h = 8, d = mount_hole_dia, center = true);

        // pi-zero mounting
        translate([0,(pi_l-mount_w)/2,0]) {
            rotate([0,0,90]) {
                cube([pi_l-14,pi_w,8],center=true);

                pi_hole_offset = 3.5;
                translate([pi_l/2-pi_hole_offset,pi_w/2-pi_hole_offset,0])
                    cylinder(h = 8, d = pi_hole_dia, center = true);
                translate([pi_l/2-pi_hole_offset,-(pi_w/2-pi_hole_offset),0])
                    cylinder(h = 8, d = pi_hole_dia, center = true);
                translate([-(pi_l/2-pi_hole_offset),pi_w/2-pi_hole_offset,0])
                    cylinder(h = 8, d = pi_hole_dia, center = true);
                translate([-(pi_l/2-pi_hole_offset),-(pi_w/2-pi_hole_offset),0])
                    cylinder(h = 8, d = pi_hole_dia, center = true);
            }
        }

        // Add a channel for the wires
        translate([0,-30,0])
            cube([pi_w/2,20,8],center=true);

    }
}

PiZeroMount();
