/*

surface to place sample and attach the translation stage (mount_holder.scad)
fits on top of structure.scad

*/

use <mount_holder.scad>
use <camera_mount.scad>


$fa = 0.5;
$fs = 0.5;

module Top() {
    //separation of the raspberry pi bolt holes
    bolt_separation = 49;

    foot_width = 7;
    foot_length = 6 + 0.5 + 0.5 + 1;

    //the amount by which the structure is larger than the raspberry pi over the sides
    extra = 7;


    //the - 1 is since the holes in the feet arent at foot_length/2 but at foot_length/2 - 0.5.
    top_width = bolt_separation + 2*extra + foot_length - 1;

    // the final +0.5 is just to allow extra space for the LED
    top_length = (58 + 3 + 3 + 0.5 + 0.5) + 0.5;
    top_thickness = 2;
    aperture_d = 6;

    //6 instead of 5 for a better fit
    fitting_height = 5;
    //The 0.x at the end is to account for the tolerance of the 3D printer, very annoying to get right!
    // Default if 0.15
    fitting_width = extra/3 - 0.05;

    //radius of the attachment screws
    attachment_screw_d = 6-0.25;
    //perpendicular distance from the aperture to the line connecting the attachment holes (depends on camera_mount.scad)
    aperture_to_attachment = 22.1;
    //separation of the attachment holes (depends on mount_holder.scad)
    attachment_separation = mounting_holes_separation();


    //location of the aperture: centered in the top. This is different than the original design where the centering was taken care of in this module.
        aperture_x = top_length/2;
        aperture_y = top_width/2;

    //creates the "fitting" which is the part that fits on to the corresponding "fitting" on structure.scad
        //the top surface
    rotate([0,0,0]) {
        difference(){
            //surface and fitting, from which you subtract the holes
            union(){
                cube([top_length, top_width, top_thickness]);
                translate([0,0,-fitting_height]) fitting(length=top_length,width=top_width,thickness = fitting_width,f_height = fitting_height);
            };
            
            //aperture, located above center of the LED array
            translate([aperture_x,aperture_y,-1]) cylinder(d=aperture_d, h = top_thickness+2);
                
            //attachment holes  
            translate([aperture_x+attachment_separation/2,aperture_y-aperture_to_attachment,-fitting_height-1]) cylinder(d=attachment_screw_d,h=top_thickness+fitting_height+8);
            translate([aperture_x-attachment_separation/2,aperture_y-aperture_to_attachment,-fitting_height-1]) cylinder(d=attachment_screw_d,h=top_thickness+fitting_height+8);
        
        /*    
            translate([aperture_x-aperture_to_attachment,aperture_y-attachment_separation/2,-fitting_height-1]){
                cylinder(r=attachment_r,h=top_thickness+fitting_height+2);
                cylinder(r=attachment_r*2,h=fitting_height+1);
            }
            translate([aperture_x-aperture_to_attachment,aperture_y+attachment_separation/2,-fitting_height-1]){
                cylinder(r=attachment_r,h=top_thickness+fitting_height+2);
                cylinder(r=attachment_r*2,h=fitting_height+1);
            */
            }
                   
            
    }
};

module fitting(width,length,thickness,f_height){
        cube([length,thickness,f_height]);
        cube([thickness,width,f_height]);
        translate([length-thickness,0,0]) cube([thickness,width,f_height]);
        translate([0,width-thickness,0]) cube([length,thickness,f_height]);
    }


Top();


