from digitalsociety.settings import EMAIL_HOST_PASSWORD
from django.db.models.fields import CharField
import MemberApp
from django.db.models.deletion import PROTECT
from django.shortcuts import render,redirect
from django.urls.conf import path
from .models import *
#from .utils import custom_mail
from django.core.mail import send_mail
from random import randint, choice
from MemberApp.models import *
from Watchman.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#Create your views here.
count = 0
@csrf_exempt
def login(request):
	global count
	if "email" in request.session:
		uid = User.objects.get(email=request.session['email'])
		if uid.role == "Chairman":
			cid = Chairman.objects.get(user_id=uid)
			mcount=Member.objects.all().count()
			ncount=Notice.objects.all().count()
			ecount = Event.objects.all().count()
			com_count = Complain.objects.all().count()
			context = {
						'uid':uid,
						'cid':cid,
						'mcount':mcount,
						'ncount':ncount,
						'ecount':ecount,
						'com_count':com_count,	
			}

			return render(request,'Chairman/index.html',{'context':context})
		elif uid.role == "member":
			mid = Member.objects.get(user_id = uid)
			mcount=Member.objects.all().count()
			ncount=Notice.objects.all().count()
			ecount = Event.objects.all().count()
			context = {
						'uid':uid,
						'mid':mid,
						'mcount':mcount,
						'ncount':ncount,
						'ecount':ecount,	

			}
			return render(request,'MemberApp/m_index.html',{'context':context}) 
		else:
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


	if request.POST:
		try:
			p_email=request.POST['email']
			p_password=request.POST['password']

			uid=User.objects.get(email=p_email)
			print("-->uid",uid)

			

			print("access field of user model using user object-->",uid.password)

			if uid:
				if uid.password	== p_password:
					if uid.role == "Chairman":

						print("-->welcome")	
						cid=Chairman.objects.get(user_id=uid)
						mcount=Member.objects.all().count()
						ncount=Notice.objects.all().count()
						ecount = Event.objects.all().count()
						com_count = Complain.objects.all().count()
						context = {
							'uid':uid,
							'cid':cid,
							'mcount':mcount,
							'ncount':ncount,
							'ecount':ecount,
							'com_count':com_count,
						}	

						request.session['email'] = uid.email
						#send_mail("DIGITAL SOCIETY","WELCOME TO DIGITAL SOCIETY","anjali.20.learn@gmail.com",[uid.email])

						return render(request,'Chairman/index.html',{'context':context})
					elif uid.role == "member":
						mid = Member.objects.get(user_id = uid)
						mcount=Member.objects.all().count()
						ncount=Notice.objects.all().count()
						ecount = Event.objects.all().count()
						if uid.first_time_login == False:
							email = uid.email
							otp = randint(1111,9999)
							uid.otp = otp
							uid.save()
							msg = "your otp is"+str(otp)
							send_mail("forgot_password",msg,"anjali.20.learn@gmail.com",[email])
							return render(request,'MemberApp/m_reset-password.html',{'email':email})
						else:


							context = {
									
									'uid':uid,
									'mcount':mcount,
									'ncount':ncount,
									'ecount':ecount,
							
							}
							request.session['email'] = uid.email
							return render(request,'MemberApp/m_index.html',{'context':context})
					else:	
						wid = tbl_watchman.objects.get(user_id = uid)
						mcount=Member.objects.all().count()
						ncount=Notice.objects.all().count()
						ecount = Event.objects.all().count()
						if uid.is_verified == False:

						    email = uid.email
						    otp = randint(1111,9999)
						    uid.otp = otp
						    uid.save()
						    msg = "Your OTP is"+str(otp)
						    send_mail("Reset-Password",msg,"anjali.20.learn@gmail.com",[email])
						    return render(request,"Watchman/w_reset-password.html",{'email':email})
						else:
							context={
                                'uid':uid,
                                'wid':wid,
                                'mcount':mcount,
                                'ncount':ncount,
                                'ecount':ecount,
                            }
							
							request.session['email'] = uid.email
							return render(request,'Watchman/w_index.html',{'context':context})


				else: 
					count+=1
					e_msg = 'invalid password'
					if count>2:
						e_msg = "You Entered Multiple Time Wrong Password. Crate Your New Password"
						return render(request,"Chairman/forgotpassword.html",{'e_msg':e_msg})
					else:
						print('c',count)
						return render(request,'Chairman/login.html',{'e_msg':e_msg}) 
			else:
				print("-->email",p_email)
				return render(request,'Chairman/login.html')
		except Exception as e:
			e_msg="Invalid email or password"
			print("---->",e)
			return render(request,'Chairman/login.html',{'e_msg':e_msg})
	else:
		return render(request,'Chairman/login.html')


def logout(request):
	if "email" in request.session:
		del request.session['email']
		return redirect('login')
	else:
		return redirect('login')

def c_profile(request):
    if "email" in request.session:
        uid=User.objects.get(email = request.session['email'])
        
        if request.POST:
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']
            if uid.password == currentpassword:
                uid.password=newpassword
                uid.save()
                return redirect('c-profile')
        else:
            if uid.role == "Chairman":
                cid=Chairman.objects.get(user_id=uid)
                context={
                	'uid':uid,
                	'cid':cid,
                }
                return render(request,"Chairman/c_profile.html",{'context':context})
            else:
                 pass
    else:
        return redirect('login')

def c_dashboard(request):
	return redirect('login')


def upload_pic(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        pic = request.FILES['pic']

        cid.profile_pic = pic
        cid.save()

        return redirect('c-dashboard')
    else:
        return redirect('login')


def forgot_password(request):
	if request.POST:
		email=request.POST['email']
		otp=randint(1111,9999)

		uid=User.objects.get(email=email)
		try:
			if uid:
				uid.otp = otp
				uid.save()
				msg="your otp is"+str(otp)
				send_mail("fogot-password",msg,"anjali.20.learn@gmail.com",[email])
				return render(request,'Chairman/reset-password.html',{'email':email})
		except Exception as e :
			e_msg="email does not exist"
			print("--------------------->",e)
			return render(request,'Chairman/forgotpassword.html',{'e_msg':e_msg})
	else:
		return render(request,'Chairman/forgotpassword.html')

def reset_password(request):
	if request.POST:
		email=request.POST['email']
		otp=request.POST['otp']
		newpassword=request.POST['newpassword']
		confirmpassword=request.POST['confirmpassword']

		uid=User.objects.get(email=email)
		if newpassword==confirmpassword:
			if str(uid.otp) == otp and uid.email == email:
				uid.password = newpassword
				uid.is_verified = True
				uid.first_time_login = True
				uid.save()
				return redirect('login')
			else:
				e_msg="Invalid otp"
				return render(request,'Chairman/reset-password.html',{'e_msg':e_msg,'email':email})
		else:
			e_msg="new password and confirm password does not match"
			return render(request,'Chairman/reset-password.html',{'e_msg':e_msg,'email':email})
	else:
		return redirect('forgotpassword')

def add_member(request):
	if "email" in request.session:
		uid=User.objects.get(email = request.session['email'])
		cid = Chairman.objects.get(user_id = uid)
		l1=["aasa345","45asd546","456dsv","9098sd","dsf35f"]

		if request.POST:
			email=request.POST['email']
			password=email[:4]+choice(l1)
			house_no = request.POST['house_no']
			role='member'
			house_no=request.POST['house_no']
			uid = User.objects.create(email=email,password=password,role=role)
			hid = House.objects.get(house_no = house_no)
			hid.status = "Active"
			hid.save()
			mid = Member.objects.create(
						user_id = uid,
						house_id = hid,
						firstname = request.POST['firstname'],
						lastname = request.POST['lastname'],
						mobileno = request.POST['mobileno'],
						job_specification = request.POST['job_specification'],
						job_address = request.POST['job_address'],
						birthdate = request.POST['birthdate'],
						gender = request.POST['gender'],
						no_of_members = request.POST['no_of_members'],
						marrital_status = request.POST['marrital_status'],
						locality = request.POST['locality'],
						nationality = request.POST['nationality'],
						no_of_vehicles = request.POST['no_of_vehicles'],
						vehicle_type = request.POST['vehicle_type'],
						id_proof = request.FILES['id_proof'],
					)
			if mid:
				msg="your password is"+password
				send_mail=("WELCOME TO DIGITAL SOCIETY",msg,"anjali.20.learn@gmail.com",[email])
				m_all = Member.objects.all()
				context ={
							'uid':uid,
							'cid':cid,
							'm_all':m_all
				}	
				return render(request,'Chairman/all_members.html',{'context':context})
		else:
			house_all=House.objects.filter(status = "pending")
			com_count = Complain.objects.all().count()
			context = {
								'uid':uid,
								'cid':cid,
								'house_all': house_all,
								'com_count':com_count,
			}	
			return render(request,'Chairman/add-member.html',{'context':context})
	
	else:
		return redirect('login')

def all_members(request):
	uid=User.objects.get(email = request.session['email'])
	cid = Chairman.objects.get(user_id = uid)
	m_all = Member.objects.all()
	com_count = Complain.objects.all().count()
	context = {
								'uid':uid,
								'cid':cid,
								'm_all':m_all,
								'com_count':com_count,
			}
	return render(request,'Chairman/all_members.html',{'context':context})

def add_notice(request):
	if request.POST:
		if "pic" in request.FILES  and "videofile" not in request.FILES:
			nid = Notice.objects.create(
			title = request.POST['title'],
			description = request.POST['description'],
			pic = request.FILES['pic'],
			)
		elif "videofile" in request.FILES and "pic" not in request.FILES:
			nid = Notice.objects.create(
			title = request.POST['title'],
			description = request.POST['description'],
			videofile = request.FILES['videofile'],
			)
		elif "pic"  in request.FILES and "videofile" in request.FILES:
			nid = Notice.objects.create(
			title = request.POST['title'],
			description = request.POST['description'],
			pic = request.FILES['pic'],
			videofile = request.FILES['videofile'],
			)
		else:
			nid = Notice.objects.create(
			title = request.POST['title'],
			description = request.POST['description'],
			)
		#all_member_emails = User.objects.filter(role=member)
		#print("---------->,all_member_emails")
		#print(type(all_member_emails))
		#custom_mail("New Notice","mail_template","adarsh2828akt@gmail.com",{'fname':'Adarsh','title':nid.title})
		return redirect('all-notice')


		
	else:
		uid=User.objects.get(email = request.session['email'])
		cid = Chairman.objects.get(user_id = uid)
		context = {
								'uid':uid,
								'cid':cid,
		}
		return render(request,'Chairman/add-notice.html',{'context':context})

def all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        n_all = Notice.objects.all().order_by('created_at').reverse()
        com_count = Complain.objects.all().count()
        context={
            'uid':uid,
            'cid':cid,
            'n_all':n_all,
            'com_count':com_count
        }
        return render(request,"Chairman/all-notice.html",{'context':context})
    else:
        return redirect('login')


def add_event(request):
	if request.POST:
		if "pic" in request.FILES  and "videofile" not in request.FILES:
			eid = Event.objects.create(
				title = request.POST['title'],
				description = request.POST['description'],
				pic = request.FILES['pic'],
			
			)
		elif "videofile" in request.FILES and "pic" not in request.FILES:
			eid = Event.objects.create(
				title = request.POST['title'],
				description = request.POST['description'],
				videofile = request.FILES['videofile'],

			)
		elif "pic"  in request.FILES and "videofile" in request.FILES:
			eid = Event.objects.create(
				title = request.POST['title'],
			 	description = request.POST['description'],
				pic = request.FILES['pic'],
				videofile = request.FILES['videofile'],
			
			)
		else:
			eid = Event.objects.create(
				title = request.POST['title'],
				description = request.POST['description'],
			
			)
		return redirect('add-event')


		
	else:
		uid=User.objects.get(email = request.session['email'])
		cid = Chairman.objects.get(user_id = uid)
		com_count = Complain.objects.all().count()
		context = {
								'uid':uid,
								'cid':cid,
								'com_count':com_count,
		}
		return render(request,'Chairman/add-event.html',{'context':context})

def all_event(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id = uid)
    e_all = Event.objects.all().order_by('created_at').reverse()
    com_count = Complain.objects.all().count()
    context={
        'uid':uid,
        'cid':cid,
        'e_all':e_all,
        'com_count':com_count
    }
    return render(request,"chairman/all-event.html",{'context':context})	



def all_complain(request):
    uid = User.objects.get(email = request.session['email'])    
    cid = Chairman.objects.get(user_id = uid)
    com_all = Complain.objects.all()
    context = {
        'cid':cid,
        'com_all':com_all
    }
    return render(request,"Chairman/all-complain.html",{'context':context})


def all_watchman(request):
	if "email" in request.session:
		uid=User.objects.get(email = request.session['email'])
		cid = Chairman.objects.get(user_id = uid)
		wall = tbl_watchman.objects.all()
		context = {
								'uid':uid,
								'cid':cid,
								'wall':wall,
		}
		for i in wall:
			print('=====<>>>>>',i.id)
		return render(request,'Chairman/all-watchman.html',{'context':context})



def approved(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        
        wid = tbl_watchman.objects.get(user_id = pk)
        wemail = wid.user_id.email        
        wid.status = "approved"
        wid.save()

        l1 = ["aasa34","45asd546","456dsv","8098sd","dsf35f"]
        password = wemail[:4]+choice(l1)

        w_uid = User.objects.get(email = wemail)
        w_uid.password = password
        w_uid.save()

        msg = "You are approved by Chairman... Your password is"+password
        send_mail("DIGITAL SOCIETY",msg,"anjali.20.learn@gmail.com",[wemail])
        return redirect('all-watchman')
    else:
        return redirect('login')


def rejected(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        wid = tbl_watchman.objects.get(user_id = pk)
        wid.status = "rejected"
        wid.save()
        return redirect('all-watchman')

def del_notice(request,pk):
	if "email" in request.session:
		uid = User.objects.get(email = request.session['email'])
		cid=Chairman.objects.get(user_id = uid)
		nid = Notice.objects.get(id = pk)
		nid.delete()
		
		return redirect('all-notice')
	else:
		return redirect('login')

def del_event(request,pk):
	if "email" in request.session:
		uid = User.objects.get(email = request.session['email'])
		cid=Chairman.objects.get(user_id = uid)
		eid = Event.objects.get(id = pk)
		eid.delete()
		
		return redirect('add-event')
	else:
		return redirt('login')


def m_noticeview_details(request,pk):
	if "email" in request.session:
		uid = User.objects.get(email = request.session['email'])
		cid = Chairman.objects.get(user_id = uid)
		nid = Notice.objects.get(id=pk)
		nvid = Noticeview.objects.filter(notice_id=nid)
		context	= {
				'uid':uid,
				'cid':cid,
				'nid':nid,
				'nvid':nvid,	
		}
		
		return render(request,'Chairman/m-noticeview-details.html',{'context':context})
	else:
		return redirect('login')

@csrf_exempt
def check_email(request):
	email=request.POST['email']
	print("------>email ajax",email)
	try:
		uid=User.objects.get(email=email)
		print("---->",uid)
		context={
			'msg':"success"
	}
	except:
		context={

			'msg':"Fail"
		}
	return JsonResponse({'context':context}) 

@csrf_exempt
def app(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        myid = request.POST['myid']
        wid = tbl_watchman.objects.get(id = request.POST['id'])
        wemail = wid.user_id.email
        wid.status = "approved"
        x= wid.status
        wid.save()
        l1 = ["aasa34","45asd546","456dsv","8098sd","dsf35f"]
        password = wemail[:4]+choice(l1)

        w_uid = User.objects.get(email = wemail)
        w_uid.password = password
        w_uid.save()

        print('====',x)
        print('------------',myid)
        context = {
            'x' : x,
            'myid' : myid,
        }
        return JsonResponse({'context':context})

    else:
        return redirect('login')

@csrf_exempt
def rejct(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        myid = request.POST['myid']
        wid = Watchman.objects.get(id = request.POST['id'])
        wemail = wid.user_id.email
        wid.status = "rejected"
        x= wid.status
        wid.save()
        context = {
            'x' : x,
            'myid' : myid,
        }
        return JsonResponse({'context':context})


def add_maintenance(request):
	if "email" in request.session:
		if request.POST:
			amount=request.POST['amount']
			penalty=request.POST['penalty']
			total=amount
			status="Pending"
			mall=Member.objects.all()
			for i in mall:
				email=i.user_id.email
				uid=User.objects.get(email=email)
				mtid=Maintenance.objects.create(
					user_id=uid,
					date=request.POST['date'],
					duedate=request.POST['duedate'],
					amount=amount,
					penalty=penalty,
					total=total,
					status=status,


					)
			return redirect('add-maintenance')
		else:
			uid=User.objects.get(email=request.session['email'])
			cid=Chairman.objects.get(user_id=uid)
			context={
						'uid':uid,
						'cid':cid,

			}
			return render(request,'Chairman/add-maintenance.html',{'context':context})
	else:
		return redirect('login')

def view_maintenance(request):
	if "email" in request.session:
		uid=User.objects.get(email=request.session['email'])
		cid=Chairman.objects.get(user_id=uid)
		t_all=Transaction.objects.all()
		context={
			'uid':uid,
			'cid':cid,
			't_all':t_all,
		}
		return render(request,'Chairman/view-maintenance.html',{'context':context})
	else:
		return redirect('login')