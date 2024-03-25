sudo apt update
echo "yes" | sudo apt install unzip curl python3-pip
echo "yes" | sudo apt-get install default-jre
echo "yes" | sudo apt-get install pulseaudio libxcursor1 libxdamage1


mkdir Android
export ANDROID_HOME=~/Android/
cd Android/
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip 
rm commandlinetools-linux-9477386_latest.zip
cd cmdline-tools/
# Move everything to new latest directory
mkdir latest && ls | grep -v latest | xargs -I{} mv {} latest/
cd latest/bin
sudo echo "y" | ./sdkmanager "emulator" "platform-tools" "platforms;android-28"
sudo echo "y" | ./sdkmanager "system-images;android-28;google_apis;x86" "build-tools;29.0.3"