from django.shortcuts import render
from Chairman.models import User
from django.core.mail import send_mail
from MemberApp.models import *
from Watchman.models import * 

# Create your views here.

def sign_up(request):
    
    if request.POST:
        email = request.POST['email']
        password = ""
        role = "watchman"

        uid = User.objects.create(email = email, password = password, role =role)
        wid = tbl_watchman.objects.create(
                user_id = uid,
                firstname = request.POST['firstname'],
                lastname = request.POST['lastname'],
                id_pic = request.FILES['id_pic'],
                profile_pic=request.FILES['profile_pic'],
            )
        
        if wid:
                msg = "You have been Successfully registered, Your password will ge generated and sent to you when your Status will be Approved"
                send_mail("Welcome to Digital Society",msg,"anjali.20.learn@gmail.com",[email])
                context = {
                            'uid':uid,
                            'wid':wid,
                        }
                return render(request,"Watchman/w_reset-password.html",{'context':context})
    else:
        return render(request,"Watchman/sign-up.html")

def w_dashboard(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = tbl_watchman.objects.get(user_id = uid)
        mcount = Member.objects.all().count()
        ncount = Notice.objects.all().count()
        ecount = Event.objects.all().count()
        context = {
            'uid':uid,
            'wid':wid,
            'mcount':mcount,
            'ncount':ncount,
            'ecount':ecount,
        }

        return render(request,"Watchman/w_index.html",{'context':context})


def w_profile(request):
    if "email" in request.session:
        uid=User.objects.get(email = request.session['email'])
        
        if request.POST:
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password=newpassword
                uid.save()
                return redirect('w-profile')
        else:
            if uid.role == "watchman":
                wid=tbl_watchman.objects.get(user_id=uid)
                context={
                    'uid':uid,
                    'wid':wid,
                }
                return render(request,"Watchman/w_profile.html",{'context':context})
            else:
                 pass
    else:
        return redirect('login')

def upload_pic(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = tbl_watchman.objects.get(user_id = uid)
        pic = request.FILES['pic']

        cid.profile_pic = pic
        cid.save()

        return redirect('c-dashboard')
    else:
        return redirect('login')


def w_all_member(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=tbl_watchman.objects.get(user_id=uid)
        m_all=Member.objects.all()
        context={

                'uid':uid,
                'wid':wid,
                'm_all':m_all,
        }
        return render(request,"Watchman/w-all-members.html",{'context':context})

def w_all_notice(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=tbl_watchman.objects.get(user_id=uid)
        nall=Notice.objects.all()
        context={

                'uid':uid,
                'wid':wid,
                'nall':nall
        }
        return render(request,"Watchman/w-all-notice.html",{'context':context})
    else:
        return redirect('login')

def w_all_event(request):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=tbl_watchman.objects.get(user_id=uid)
        eall=Event.objects.all()
        context={

                'uid':uid,
                'wid':wid,
                'eall':eall,
        }
        return render(request,"Watchman/w-all-event.html",{'context':context})
    else:
        return redirect('login')


def w_add_visitor(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = tbl_watchman.objects.get(user_id = uid)
        house_all = House.objects.all()

        if request.POST:
            vid = Visitor.objects.create(
                house_no = request.POST['house_no'],
                firstname = request.POST['fname'],
                lastname = request.POST['lname'],
                phone = request.POST['phone'],
                v_detail = request.POST['v_detail']
            )
            context={
            'uid':uid,
            'wid':wid,
            'house_all':house_all,
            }

           
            return render(request,"Watchman/w-add-visitor.html",{'context':context})
            

        

        return render(request,"Watchman/w-add-visitor.html") 

    else:
        return redirect('login')

def w_all_visitor(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        wid = tbl_watchman.objects.get(user_id=uid)

        v_all = Visitor.objects.all()
        context={   
            'uid':uid,
            'wid':wid,
            'v_all':v_all,
        }

        return render(request,"Watchman/w-all-visitor.html",{'context':context})
    else:
        return redirect('login')