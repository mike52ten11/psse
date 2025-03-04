chcp 65001
@echo off

call  D:\Mike\ProgramData\anaconda3\Scripts\activate.bat PSSE_Python

cd /d D:\Mike\Work_space\業務\電力室合作\改寫\psseweb

python manage.py runserver


pause

