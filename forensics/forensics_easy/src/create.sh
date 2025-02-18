echo "magpieCTF{WH4T_D1D_T3RRY_S1GN}" > flag.txt
zip -e -9 flag.zip flag.txt Form.pdf
F0rS4l3!2025
steghide embed -cf wallpaper.jpg -ef flag.zip
exiftool -Comment="Password for zip : RjByUzRsMyEyMDI1" wallpaper.jpg
