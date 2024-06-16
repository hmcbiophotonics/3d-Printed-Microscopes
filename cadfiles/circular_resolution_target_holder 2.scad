/*
  https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4338
*/


$fa = 0.5;
$fs = 0.5;

function resolutionTargetDiameter() = 25.4; // Diameter of target [mm]
function resolutionTargetDiameterMargin() = 0.2; // Margin for fit of target [mm]
function holderThickness() = 2; // Thickness of mount [mm]
function ringThickness() = 1.6 + resolutionTargetLipThickness(); // Thickness of mount [mm]
function tabDimensions() = [15, 5, holderThickness()]; // Dimensions for tabs [mm]
function resolutionTargetLipThickness() = 0.4; // Height of the lip to hold the target [mm]

echo(str("Overall length is: ",2*tabDimensions()[0]+resolutionTargetDiameter()+1));


module CircularResolutionTargetHolder() {
  translate([resolutionTargetDiameter()/2+resolutionTargetDiameterMargin(), -tabDimensions()[1]/2, 0]) cube(tabDimensions());
  translate([-(resolutionTargetDiameter()/2+resolutionTargetDiameterMargin()), tabDimensions()[1]/2, 0]) rotate([0, 0, 180]) cube(tabDimensions());
  difference() {
    translate([0, 0, 0]) cylinder(d = resolutionTargetDiameter()+5, h = ringThickness());;
    translate([0, 0, resolutionTargetLipThickness()]) cylinder(d = resolutionTargetDiameter()+resolutionTargetDiameterMargin(), h = ringThickness()+0.1);
    translate([0,0,-holderThickness()]) cylinder(d = resolutionTargetDiameter()-2, h = ringThickness()+2);
  }
   
};

CircularResolutionTargetHolder();


