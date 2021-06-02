# django dependancy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from  django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

from .forms import UserRegisterForm
from .forms import Share_Text_Form
from .forms import Share_Text_Decryption_key_Form

from .models import Message
from .util.comman_utility import CommonUtility
from .util.comman_utility import CommonUtility
from Share_Text import settings
import uuid
import jwt



def register(request):
    '''This view will accept for register a user into our system
       it will accept Post request if post request is valid then and then 
       user entry aadded in database 
    '''
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for {} !'.format(username))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# @login_required is View decorators can be used to restrict access of user 
# it is accessible only when user is login  
@login_required
def home(request):
    '''
    Basicaly this view is call if user is login in not view will not be display to user
    this view will accept post request 
    '''
    # chacking request is POST request or not
    if request.method == 'POST':
        form = Share_Text_Form(request.POST)
        sms = request.POST['message']

        if sms != '':
            if form.is_valid():
                sms_id = str(uuid.uuid4())
                sms = request.POST['message']
                
                # checking user want to encrypted text pr not if yes 
                # application generate secret key alog with sharable url 
                if 'encrypt' in request.POST:
                    # encypt massage and store into db
                    ecrypted_message_and_key = CommonUtility.encrypt(sms)
                    ecrypted_message = ecrypted_message_and_key[0]
                    
                    secret_key = ''
                    secret_key = ecrypted_message_and_key[1]                       
                    Message(message = ecrypted_message, message_id=sms_id).save()
                    
                    token = CommonUtility.generate_token(sms_id, settings.SECRET_KEY,encrypt_flag=True)
                    
                    # generating sharebale link to share with other user
                    link = 'http://127.0.0.1:8000'+reverse('show_text')+'?'+'token='+token['token']
                    
                    #str_link = '<form>Shareable link:<textarea name="message" rows="10" cols="100" readonly >{}</textarea></form>'.format(link)
                    return render(request,'users/sharable_link.html',{'link':link,'secret_key':secret_key})
                
                # storing text in db without encryption
                else:
                    Message(message = sms, message_id=sms_id).save()
                    token = CommonUtility.generate_token(sms_id,settings.SECRET_KEY)

                    # generating sharebale link to share with other user
                    link = 'http://127.0.0.1:8000'+reverse('show_text')+'?'+'token='+token['token']
                    #str_link = '<form>Shareable link:<textarea name="message" rows="10" cols="100" readonly >{}</textarea></form>'.format(link)
                    return render(request,'users/sharable_link.html',{'link':link,'secret_key':''})
                
            else:
                form = Share_Text_Form()
                return render(request, 'users/home.html', {'form': form,})
        else:
            messages.success(request, 'Required field')
            form = Share_Text_Form()
            return render(request, 'users/home.html', {'form': form,})    
    else:
        form = Share_Text_Form()
    return render(request, 'users/home.html', {'form': form,})

# @login_required is View decorators can be used to restrict access of user 
# it is accessible only when user is login  
@login_required
def show_text(request):
    '''this view will accept GET request and get the token from GET request 
    then decode that token and retrieve message after it will decode that massage and
    display on screen '''
    try:
        # gettting token from url 
        token = request.GET.get('token')
        token_dict = CommonUtility.decode_token(token,settings.SECRET_KEY)
        
        #chacking if message_id is None or not if message id is None return invalid token
        if token_dict['message_id']:

            # chacking message is  encrypted or not if message is encrypted the app will ask decryption key 
            # else without encryption key it will show text message
            if token_dict['encrypt_flag']:
                txt = Message.objects.filter(message_id = token_dict['message_id'])
                message = txt[0].message
                form = Share_Text_Decryption_key_Form()

                if 'decryption_key' in request.POST:
                    decryption_key = request.POST['decryption_key']
                    decrypted_message = CommonUtility.decrypt(decryption_key,message)

                    # chacking decryption key is valid or not  
                    if decrypted_message is None:
                        return HttpResponse('Invalid Decryption Key')
                    return render(request,'users/show_txt.html', {'message': decrypted_message})
                else:
                    return render(request,'users/enter_key.html',{'form':form})
            else:
                txt = Message.objects.filter(message_id = token_dict['message_id'])
                message = txt[0].message
                return render(request,'users/show_txt.html', {'message': message})
        return HttpResponse('Invalid token')
    
    except jwt.DecodeError:       
        return HttpResponse('Invalid token')
    
    except jwt.ExpiredSignatureError:
        return HttpResponse('Token has expired')
    
    except Exception:
        return HttpResponse('Something went wrong')






