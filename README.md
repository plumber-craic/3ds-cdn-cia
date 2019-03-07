Batch converter for encrypted 3DS CDN files downloaded by the WiiU USB loader. 

Requires encTitleKeys.bin, not included. Tested with one that has an MD5 of E820A44B43770B79892E91DBDA5F2D64. 
Requires python 3. 

Usage:
    python make_cias_from_eShop.py "C:\Wiiu USB eShop Games\3DS" c:\converted_cias

Get extra info with:
    python make_cias_from_eShop.py -h
    
make_cdn_cia.exe was created from this source: https://github.com/llakssz/make_cdn_cia. All I did was add support for the USB loader filenames.

maketicket_from_enctitlekeys_v3.py is updated for py3 and wrapped in a function so I can import it. Not entirely sure who wrote this, but let me know if you do so I can credit them. 