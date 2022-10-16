@echo off

pyinstaller --noconfirm --onefile --windowed --icon "./assets/images/icon.ico" --add-data "./assets;assets/"  "./multi_snake.py"
rmdir /q /s build
del "multi_snake.spec"
cd ".\dist"
move "multi_snake.exe" ..
cd ".."
rmdir /q /s dist
