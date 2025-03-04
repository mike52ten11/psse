chcp 65001
@echo off
call D:\Mike\ProgramData\anaconda3\Scripts\activate.bat PSSE_Python

cd /d D:\Mike\Work_space\業務\電力室合作\改寫\pssefunction

python manage.py runserver 127.0.0.1:800

pause


