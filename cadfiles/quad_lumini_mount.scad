/*
    Filename: quad_lumini_array_mount.scad
    Author: Fred Kim
    Email: fred.kim@cooper.edu
    Date: 07/10/2024
    Description: A mount to attach four 8x8 LuMini array to hmscope
*/

$fa = 0.1;
$fs = 1;
$fn = 100;


module LuMiniMount() {
    mount_l = 65;
    mount_w = 56;
    mount_h = 4;
    mount_hole_offset = 3.5;
    mount_hole_dia = 3.5;

    LuMini_w = 25.4;
    LuMini_h = 2;
    tab_w = 7.62;
    tab_h = 2;
    tab_hole_dia = 3.5;
    k = 0.01;
        // Tolerance Constant
    difference() {
        union() {
            rotate([0,0,90])
                cube([mount_l,mount_w,mount_h],center=true);
            cube([mount_l,LuMini_w*2,mount_h],center=true);
        }
        for(i=[-1,1]) {
            for(j=[-1,1])
                union() {
                    translate([i*(mount_w/2-mount_hole_offset),j*(mount_l/2-mount_hole_offset),0])
                        // w & l swapped here because mount is rotated 90 deg
                        cylinder(h = mount_h+k, d = mount_hole_dia, center = true);
                    translate([i*LuMini_w/2,j*LuMini_w/2,0])
                        LuMini();
                }
        }
    }

    module LuMini() {
        cube([LuMini_w+k,LuMini_w+k,mount_h+k],center=true);
        for(i=[-1,1]) {
            for(j=[-1,1]) {
                translate([i*(LuMini_w+tab_w+2*k)/2,j*(LuMini_w-tab_w)/2,1+k/2]) {
                    union() {
                        cube([tab_w+k+0.01,tab_w+k,tab_h+k],center=true);
                        cylinder(h = 8, d = tab_hole_dia, center = true);
                    }
                }
            }
        }
    }
}
LuMiniMount();
