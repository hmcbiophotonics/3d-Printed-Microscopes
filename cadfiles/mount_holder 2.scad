/*

Part of the translation stage for the Raspberry Pi camera, together with camera_mount.scad

Design by Tomas Aidukas, modified by Victor Lovic

*/

// angle is tan(delta_h/slider_hole_w_h)

function mounting_holes_separation() = 40;

module MountHolder() {
  //I have changed these values to give a bigger margin
  slider_hole_w_h = 30.4; 
  slider_x_shift_h = 10.5;
  slider_z_shift_h = -8;
  delta_h = -20.7;
  $fn = 100;
  height = 33;

  // Main Block with mount holes
  difference(){
      
      translate([0,0,5]){
          cube([40.6,53,height],center=true);   
      }
      
      translate([7,mounting_holes_separation()/2,0]){
          //Hole diameter for the mount is 6.4mm
          cylinder(d=6.4,h=200,center=true);
      }
      
      translate([7,-mounting_holes_separation()/2,0]){
          //Hole diameter for the mount is 6.4mm, 30mm apart
          cylinder(d=6.4,h=200,center=true);
      }
      
      // Large block chop
      translate([-18,0,-10]){
          cube([40,70,80], center=true);
      }
      
      //second chop
      translate([34,0,-10]) cube([40,70,80],center=true);

  // Slider Hole
  hull(){
      translate([slider_x_shift_h,slider_hole_w_h/2,slider_z_shift_h]){
          cube([0.1,0.1,50], center=true);
      }
      
      translate([slider_x_shift_h,-slider_hole_w_h/2,slider_z_shift_h]){
          cube([0.1,0.1,50], center=true);
      }
      
      translate([slider_x_shift_h+delta_h,0,slider_z_shift_h]){
          cube([0.1,0.1,50], center=true);
      }
  }// Slider hole ENDS

  /*
      // Stabilizer
      #translate([5,16.5,-10]){
          cube([10,1,50],center=true);
      }
      #translate([5,13,14.5]){
          cube([10,8,1],center=true);
      }// stabilizer END
  */
      
      //Bushing
      translate([6,0,14.5]){
          cylinder(d=5+0.3,h=200,center=true);}
            // 0.3 added here for bushing tolerance
      translate([6,0,14.5]){
          cylinder(d=6,h=6,center=true);}

      //Bushing END
      
      // Spring Holes
      translate([6,6.5,14.5]){
          cylinder(d=5.6,h=200,center=true);}
      translate([6,-6.5,14.5]){
          cylinder(d=5.6,h=200,center=true);}// Spring Holes END
          
      //Groove for spring holder
      translate([6,0,21.5]){
          //cube([2.5,30,2],center=true);  
          cube([8.1,8.1,2], center=true);
      }
  }

  /*
  // Spring holder
      translate([5.5,3,+height/2+3]){
          cube([1,7,2]);}
          
      translate([5.5,-10,+height/2+3]){
          cube([1,7,2]);}// Spring holder END
  */
}

translate([-2,0,0]) MountHolder();
