#!/bin/bash
# ============================================================
# StudyApp — Android APK Builder for Windows (via WSL2)
# Run this script inside WSL2 Ubuntu terminal
# ============================================================

echo "============================================"
echo "  StudyApp APK Builder — Windows via WSL2"
echo "============================================"

# Step 1: Update system
echo ""
echo "[1/6] Updating system packages..."
sudo apt update -y && sudo apt upgrade -y

# Step 2: Install all required system dependencies
echo ""
echo "[2/6] Installing system dependencies..."
sudo apt install -y \
    python3 python3-pip python3-dev \
    build-essential git wget curl zip unzip \
    libffi-dev libssl-dev \
    zlib1g-dev \
    openjdk-17-jdk \
    autoconf automake libtool \
    pkg-config \
    libltdl-dev \
    cmake \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    ccache

# Step 3: Install Python tools
echo ""
echo "[3/6] Installing Python tools..."
pip3 install --upgrade pip setuptools wheel
pip3 install buildozer cython virtualenv

# Step 4: Set JAVA_HOME
echo ""
echo "[4/6] Setting JAVA_HOME..."
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Step 5: Navigate to project and build
echo ""
echo "[5/6] Building APK (this takes 20-40 minutes first time)..."
echo "      Android SDK and NDK will be downloaded automatically."
echo ""

# Navigate to the StudyApp folder
# Edit this path to where you extracted StudyApp.zip
cd ~/StudyApp || { echo "ERROR: StudyApp folder not found. Check the path."; exit 1; }

buildozer android debug

# Step 6: Done
echo ""
echo "[6/6] Build complete!"
echo ""
if ls bin/*.apk 1>/dev/null 2>&1; then
    APK=$(ls bin/*.apk | head -1)
    echo "SUCCESS! APK is at: $APK"
    echo ""
    echo "To copy APK to Windows desktop:"
    echo "  cp '$APK' /mnt/c/Users/\$USER/Desktop/"
    cp "$APK" /mnt/c/Users/$USER/Desktop/ 2>/dev/null && echo "  Done! Check your Windows Desktop."
else
    echo "Build may have failed. Check the logs above for errors."
    echo "Common fix: run 'buildozer android debug 2>&1 | tee build.log'"
fi
