# 🖼️ Simple image editor in Python

An **educational image editor** project built to explore image filters and GUI programming in Python.  
Some methods (like handling images as 3D arrays or skipping certain libraries) are intentionally simple for learning purposes.  
Features include basic filters, color editing, and cropping — no image deformations implemented (yet).

---

<img src="static/README.png" heigh=500>

---

## ✨ Features
- ✅ Simple filters  
- ✅ Color channel editor  
- ✅ Cropping  
- ✅ Brightness and Saturation adjustment  
- ✅ Painting  

---

## ⚙️ Technologies
- **PyQt** — GUI framework  
- **NumPy** — Used for working with images (educational, not performance-focused)  
- **OpenCV** — Accelerated kernel operations  

---

## 🚀 How to Use

1. install PyInstaller 
```pip3 install PyInstaller```
2. create the executable
```pyinstaller --noconsole --onedir --icon=static\icon.png src/main.py```
3. the executable will be located in dist/main/
