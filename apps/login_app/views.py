from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages
#from .. book_app.models import Author,Book,Review


def index(request):
	print "--------inside INDEX route----------"
	
	return render(request, 'login_app/index.html')


def register(request, methods='POST'):
	print '------------------------      IN REGISTER ROUTE  (POST)                                ---------------'
	print '*'*50
	print request.POST['birthday']," <---heres the birthday input"
	print type(request.POST['birthday'])
	if request.method == 'GET':
		return redirect('login_app:index')
		
	else:
		response = User.objects.check_create(request,request.POST)
		# response will return a list [] that will contain either a False and the errors, or a True statement with the new user that is created
		# response = [False, errors] or [True, new_user]

		print response, '<----------here is the response'
		if response[0]== False:
			for message in response[1]: #saying  for message in errors:
				print "joe mamma"
				messages.error(request, message[1])
			return redirect('login_app:index')
		else:
			request.session['message'] = "Successfully Registered!"
			request.session['user']= {
			"id": response[1].id,
			'name': response[1].name,
			'alias': response[1].alias,
			}
			print request.session['user']
			print request.method
			return redirect('trip_app:index')

	




def login(request, methods='POST'):
	print '------------------------      IN LOGIN ROUTE    (POST)                              ---------------'
	print '*'*50

	if request.method == 'POST':
		print request.POST, "<-------------------------- here is what is being posted"
		response = User.objects.check_password(request,request.POST)

		print response, '<----------here is the response'
		
		if response[0]== False:
			for message in response[1]:
				print "joe mamma"
				messages.error(request, message[1])
				return redirect('login_app:index')
		else:
			print response[0]
			print response[1]
			
			request.session['message'] = "Successfully Logged In!"
			print request.session['message'] 

			
			request.session['user']= {
	
				'name': response[1].name,
				'alias': response[1].alias,
				'id': response[1].id,
				'email': response[1].email
				}
			
			print request.session['user'], "<<<<------------request.session['user']----------->>>"
			return redirect('trip_app:index')
	else:

		return redirect('login_app:index')
