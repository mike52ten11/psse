import os
#登入
from django.shortcuts import render, redirect
from django.contrib import auth

#忘記密碼
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

#密碼驗證
from django.contrib.auth.password_validation import validate_password





class MyLogin:

    def __init__(self, request):
        self.request = request
        self.user= request.user
        self.userfolder = f"../Data/User/{self.user}/"

    def login_page(self):
        return render(self.request, 'login.html')

    def mylogin(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if username=='admin':

            return redirect('admin:index')
        else:
            user = auth.authenticate(username=username, password=password)

            '''
                if 使用者活著或不是none
                    --> 建立一個使用者資料夾

            '''
            if user is not None and user.is_active:

                # os.makedirs(f'{self.userfolder}/SavFile', exist_ok=True)
                os.makedirs('temp', exist_ok=True)
                auth.login(self.request, user)
                messages = ['登入成功']

                return render(self.request, 'main.html', {'messages': messages})
            
            else:

                messages = ['登入失敗，未註冊或密碼錯誤']                
                return render(self.request, 'login.html', {'messages': messages})


    def mylogout(self):                
        u = self.request.user
        auth.logout(self.request)



        return render(self.request, 'login.html')


    def forget(self):
        if self.request.method == 'GET':


            return render(self.request, 'forget_user.html')
        else:
            if self.request.POST.get('password') is None:
                if User.objects.filter(username=self.request.POST.get('username')).exists():

                    u = User.objects.get(username=self.request.POST.get('username'))
                    


                    return  render(self.request, 'forget.html')
                else:
                    messages = [f"{self.request.POST.get('username')} 未註冊，請先註冊"]
                    
                    return  render(self.request, 'login.html',{'messages': messages})                
            else:

                try:
                    password = validate_password(self.request.POST.get('password'))
                    u = User.objects.get(username=self.request.POST.get('username'))
                    
                    u.set_password(self.request.POST.get('password'))
                    u.save()
                 
                    return redirect('login_page') 

                except ValidationError as e:
                    u = User.objects.get(username=self.request.POST.get('username'))
                    messages = e.messages
                    messages = [''.join(messages)]

                  
                    # print(messages)
                    return render(self.request, 'forget.html', {'messages': messages})

        return render(self.request, 'forget_user.html')                
