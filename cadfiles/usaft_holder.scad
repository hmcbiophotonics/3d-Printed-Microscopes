/*
    Filename: usaft_holder.scad
    Author: Fred Kim
    Email: fred.Kim@cooper.edu
    Date: 06/17/2024
    Description: A holder for the Ready Optics USAFT
*/

$fa = 0.1;
$fs = 1;
$fn = 100;

// constant params
USAFT_length = 75;
USAFT_width = 25;
USAFT_height = 3;
target_offset = 25; // Target center is offset 25mm from short edge

holder_length = 65.5;
holder_width = 70;
holder_height = 2;

mount_length = 53;
mount_width = 12;
mount_offset = 17.1; // Edge of mount is 17.1mm from center of system

tolerance = 0.01;

module CameraMountHolder()
{
    cube([mount_length+tolerance,mount_width+tolerance,3],center=true);
    translate([0,-6,0]) cube([mount_length+tolerance,mount_width+tolerance,3],center=true);
        // Cutoff the rest of the mount for ease of mounting here ^
}

module USAFT()
{
    cube([USAFT_length+tolerance+1,USAFT_width+tolerance,USAFT_height],center=true);
}

module USAFTHolder()
{
    difference()
    {
        cube([holder_length,holder_width,holder_height],center=true);
        translate([USAFT_length/2 - target_offset,0,0]) USAFT();
        translate([0,-(mount_width/2 + mount_offset),0]) CameraMountHolder();
    }
}
USAFTHolder();
