#!/bin/bash
set -e
clear

echo "
██████╗ ███████╗     █████╗ ███████╗ █████╗ ███████╗███╗   ██╗████████╗
██╔══██╗██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║╚══██╔══╝
██████╔╝█████╗      ███████║███████╗███████║█████╗  ██╔██╗ ██║   ██║   
██╔══██╗██╔══╝      ██╔══██║╚════██║██╔══██║██╔══╝  ██║╚██╗██║   ██║   
██║  ██║███████╗    ██║  ██║███████║██║  ██║███████╗██║ ╚████║   ██║   
╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   
"

echo "🔧 Checking Python..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python 3 is not installed. Please install it first from https://www.python.org/downloads/"
  exit 1
fi

echo "🔧 Installing dependencies..."
python3 -m pip install --upgrade pip >/dev/null 2>&1
python3 -m pip install requests >/dev/null 2>&1

echo "📦 Setting up REAgent..."
mkdir -p ~/REAgent
cd ~/REAgent

# Download latest version number from GitHub
LATEST_VERSION=$(curl -s https://raw.githubusercontent.com/saudmisk21/REAgent/main/version)
if [ -f version ]; then
  CURRENT_VERSION=$(cat version)
else
  CURRENT_VERSION="none"
fi

if [ "$LATEST_VERSION" != "$CURRENT_VERSION" ]; then
  echo "⬇️  Updating REAgent to version $LATEST_VERSION..."
  rm -f reagent.py
  curl -s -o reagent.py https://raw.githubusercontent.com/saudmisk21/REAgent/main/reagent.py
  echo "$LATEST_VERSION" > version
else
  echo "✅ REAgent is already up to date (v$CURRENT_VERSION)"
fi

echo "🚀 Launching REAgent..."
python3 reagent.py
