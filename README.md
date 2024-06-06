# fc_sensors

# Cross compiling
Needs to run on Ubuntu 20 wsl

guide:
https://medium.com/swlh/compiling-rust-for-raspberry-pi-arm-922b55dbb050

partially useful comment:
https://users.rust-lang.org/t/building-for-raspberry-from-windows-10/21648/20

sudo apt-get update
sudo apt install build-essential


change source to:
source $HOME/.cargo/env

You also need to add target:
rustup target add armv7-unknown-linux-gnueabihf
rustup toolchain install stable-armv7-unknown-linux-gnueabihf
????rustup target add armv7-unknown-linux-gnueabihf

sudo apt-get install gcc-arm*
 

sudo apt-get install libudev-dev

# To configure gstreamer on raspi:
https://docs.rs/gstreamer/latest/gstreamer/
needs qt5:
https://qengineering.eu/install-gstreamer-1.18-on-raspberry-pi-4.html
so we install qt5:
https://www.tal.org/tutorials/building-qt-515-lts-raspberry-pi-raspberry-pi-os

# To allow cross compile with working camera

when in wsl, allow docker to work in ubuntu 20 from docker desktop

then 
cross run --target armv7-unknown-linux-gnueabihf

login into container and:

apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

this is from 
https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c


the above didnt help
## now from https://www.collabora.com/news-and-blog/blog/2020/06/23/cross-building-rust-gstreamer-plugins-for-the-raspberry-pi/

[target.armv7-unknown-linux-gnueabihf]
linker = "arm-linux-gnueabihf-gcc"

stopped on this one

## now trying to use docker for that
create dockerfile

build docker image
gstreamer = "0.18.3"
gstreamer-app = "0.18.3"
gstreamer-video = "0.18.3"
mmal-sys = "0.1.0-3"

# to cross compile with vl53l1x

add to variables
export VL53L1X_CC=arm-linux-gnueabihf-gcc
export VL53L1X_AR=arm-linux-gnueabihf-ar


# to setup rpi for camera capture
https://forum.arducam.com/t/how-to-use-arducam-64mp-arducam-64mp-faq/2848/2

sudo apt install dphys-swapfile
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
 - set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon


### possible problems:
1. CMA memory
source: https://github.com/raspberrypi/rpicam-apps/issues/555

2. Swap space
3. https://forums.raspberrypi.com/viewtopic.php?t=339182
echo 2 > /sys/module/videobuf2_common/parameters/debug

# To config rpi for VL53L1X

cd
sudo apt-get install wiringpi
#For Raspberry Pi systems after May 2019 (earlier than that can be executed without), an upgrade may be required:
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v

# Bullseye branch system using the following command:
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
gpio -v

# when faced with error:
error: linking with `arm-linux-gnueabihf-gcc` failed: exit status: 1
just cargo clean

# for uart
enable serial port in raspi-config
chmod 766 /dev/ttyS0
remove ```console=serial0, 115200``` from ```sudo nano /boot/cmdline.txt```


export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_DEBUG=true 
export RUST_BACKTRACE=1