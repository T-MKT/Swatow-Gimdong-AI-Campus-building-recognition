@echo off
REM 修复LabelImg读取UTF-8编码文件的兼容性问题

set YOLO_IO=%APPDATA%\Python\Python313\site-packages\libs\yolo_io.py

REM 使用PowerShell修复yolo_io.py中的编码问题
powershell -Command "(Get-Content '%YOLO_IO%') -replace \"open\(self\.class_list_path, 'r'\)\", 'open(self.class_list_path, \"r\", encoding=\"utf-8\")' | Set-Content -Path '%YOLO_IO%' -Encoding utf8"

echo 修复完成！
pause
