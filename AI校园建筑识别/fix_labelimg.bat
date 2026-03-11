@echo off
REM 修复LabelImg在Python 3.13上的兼容性问题

REM 找到canvas.py文件
set CANVAS_FILE=%APPDATA%\Python\Python313\site-packages\libs\canvas.py

REM 使用PowerShell修复canvas.py中的类型错误
powershell -Command "(Get-Content '%CANVAS_FILE%') -replace 'p\.drawLine\(self\.prev_point\.x\(\), 0, self\.prev_point\.x\(\), self\.pixmap\.height\(\)\)', 'p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), self.pixmap.height())' -replace 'p\.drawLine\(0, self\.prev_point\.y\(\), self\.pixmap\.width\(\), self\.prev_point\.y\(\)\)', 'p.drawLine(0, int(self.prev_point.y()), self.pixmap.width(), int(self.prev_point.y()))' | Set-Content '%CANVAS_FILE%'"

echo 修复完成！
pause
