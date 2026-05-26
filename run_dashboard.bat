@echo off
cd /d "%~dp0"
echo ====================================
echo  Atlas Global Capital ESG Dashboard
echo ====================================
echo.
echo Abriendo dashboard en http://localhost:8501
echo.
echo Cierra esta ventana o presiona Ctrl+C para detenerlo.
echo.
"C:\Users\uriel\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run app.py
pause
