import subprocess
import os

excel_exe = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
xlsx_file = r"c:\Users\pankh\OneDrive\Desktop\Govt\NESFIC_D36_Government_AI_Dataset_Master.xlsx"
html_file = r"c:\Users\pankh\OneDrive\Desktop\Govt\view_dataset.html"

# Launch Excel
if os.path.exists(excel_exe) and os.path.exists(xlsx_file):
    print("Launching Microsoft Excel...")
    subprocess.Popen([excel_exe, xlsx_file])

# Launch Chrome
print("Launching Chrome Browser Viewer...")
try:
    subprocess.Popen(["chrome.exe", html_file])
except Exception:
    import webbrowser
    webbrowser.open("file://" + html_file)

# Also open using Windows default file association
os.startfile(xlsx_file)

print("Opened both successfully!")
