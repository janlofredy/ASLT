@echo off
Title Installing Requirements
cd..
cd Requirements\
pip install --default-timeout=1000 -r requirements.txt
echo msgbox"Installation Completed!!! :)",0,"ASLT Prototype">message.vbs&message.vbs
del message.vbs
exit