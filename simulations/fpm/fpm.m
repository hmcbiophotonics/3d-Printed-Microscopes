%close gcf; close all; clear all; clc;
close all; clear; clc;

amplitude = double(imread('../figures/monkey_gray.png'));
phase = double(imread('../figures/landscape_gray.png'));
phase = pi * phase ./ max(max(phase));
object = amplitude .* exp(1i .* phase);
        % complex object
figure();
imshow(abs(object),[]);

arraysize = 15;
xlocation = zeros(1,arraysize^2);
ylocation = zeros(1,arraysize^2);
LEDgap = 4;
LEDheight = 90;

for i=1:arraysize
    xlocation(1,1+arraysize*(i-1):15+arraysize*(i-1)) = (-(arraysize-1)/2:1:(arraysize-1)/2)*LEDgap;
    ylocation(1,1+arraysize*(i-1):15+arraysize*(i-1)) = ((arraysize-1)/2-(i-1))*LEDgap;
end

kx_relative = -sin(atan(xlocation/LEDheight));
ky_relative = -sin(atan(ylocation/LEDheight));

wavelength = .63e-6;
k0 = 2*pi/wavelength;
spsize = 2.75e-6;
psize = spsize/4;
NA = .08;
[m,n] = size(object);

m1 = m/(spsize/psize);
n1 = n/(spsize/psize);

imSeqLowRes = zeros(m1,n1,arraysize^2);
kx = k0 * kx_relative;
ky = k0 * ky_relative;
dkx = 2*pi/(psize*n);
dky = 2*pi/(psize*m);
cutoffFrequency = NA * k0;
kmax = pi/spsize;
[kxm, kym] = meshgrid(-kmax:kmax/((n1-1)/2):kmax,-kmax:kmax/((n1-1)/2):kmax);
CTF = ((kxm.^2+kym.^2)<cutoffFrequency^2);
objectFT = fftshift(fft2(object));
for tt =1:arraysize^2
    kxc = round((n+1)/2+kx(1,tt)/dkx);
    kyc = round((m+1)/2+ky(1,tt)/dky);
    kyl=round(kyc-(m1-1)/2);kyh=round(kyc+(m1-1)/2);
    kxl=round(kxc-(n1-1)/2);kxh=round(kxc+(n1-1)/2);
    imSeqLowFT = (m1/m)^2 * objectFT(kyl:kyh,kxl:kxh).*CTF;
    imSeqLowRes(:,:,tt) = abs(ifft2(ifftshift(imSeqLowFT)));
end

figure();
imshow(imSeqLowRes(:,:,1),[]);

seq = gseq(arraysize);

objectRecover = ones(m,n);
objectRecoverFT = fftshift(fft2(objectRecover));
loop = 5;
pupil = 1;
for tt=1:loop
    for i3=1:arraysize^2
        i2=seq(i3);
       
        kxc=round((n+1)/2+kx(1,i2)/dkx);
        kyc=round((m+1)/2+ky(1,i2)/dky);
        kyl=round((kyc-(m1-1)/2));kyh=round(kyc+(m1-1)/2);
        kxl=round((kxc-(n1-1)/2));kxh=round(kxc+(n1-1)/2);

        lowResFT_1 = (m1/m)^2 * objectRecoverFT(kyl:kyh,kxl:kxh).*CTF.*pupil;
        im_lowRes = ifft2(ifftshift(lowResFT_1));
        im_lowRes = (m/m1)^2 * imSeqLowRes(:,:,i3).*exp(1i.*angle(im_lowRes));
        lowResFT_2 = fftshift(fft2(im_lowRes)).*CTF.*(1./pupil);
        
        objectRecoverFT(kyl:kyh,kxl:kxh)=objectRecoverFT(kyl:kyh,kxl:kxh) ...
                + conj(pupil) ./ (max(max(abs(pupil).^2))) ...
                .* (lowResFT_2 - lowResFT_1);

        pupil = pupil + conj(objectRecoverFT(kyl:kyh,kxl:kxh))  ...
                ./ (max(max(abs(objectRecoverFT(kyl:kyh,kxl:kxh)).^2))) ...
                .* (lowResFT_2 - lowResFT_1);
    end
end

objectRecover = ifft2(ifftshift(objectRecoverFT));
figure();
imshow(log(abs(objectRecoverFT)),[])
figure();
imshow(abs(objectRecover),[])
figure();
imshow(abs(pupil),[])

