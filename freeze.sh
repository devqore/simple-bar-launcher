rm build dist -rf
pyinstaller main.py --onefile -n "simple-bar-launcher"
chmod a+x dist/simple-bar-launcher