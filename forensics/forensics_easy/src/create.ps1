echo "magpieCTF{this_is_the_flag}" > flag.txt
zip -e -9 flag.zip flag.txt Form.pdf
steghide embed -cf wallpaper.jpg -ef flag.zip
exiftool -Comment="Password for zip : bXlfc2VjcmV0X3Bhc3N3b3Jk" wallpaper.jpg
rm wallpaper.jpg_original
