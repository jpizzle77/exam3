from django.shortcuts import render, HttpResponse, redirect
from models import Trip, Trip_planner
from django.contrib import messages
from .. login_app.models import User
from itertools import chain



def index(request):
	print "------##############  inside TRIP APP INDEX route ##################----------"
	print request.session['user']['id'],"<------------------here's the user_id"


	current_user_trips= User.objects.get(id =request.session['user']['id']).trips.all()
	current_user_trips =current_user_trips.values('id','users','destination','start_date','end_date', 'plan').distinct()

	#print current_user_trips, "current_user_trips data"


	other_trips = Trip.objects.exclude(users=None)
	other_trips =other_trips.values('id','users','destination','start_date','end_date', 'plan')
	#print other_trips, "other_trips data"
	other_trips=list(other_trips)
	
	travelers= User.objects.exclude(id =request.session['user']['id'])
	travelers= travelers.values('id','name','trips')
	travelers=list(travelers)
	
	joined_trip= Trip_planner.objects.filter(user=request.session['user']['id'])
	joined_trip =joined_trip.values('id', 'joined_trip', 'user__id', 'trips_id', 'trip_maker')
	#print joined_trip, "filtering the dipshits that JOINED the trip"

	context = {
		
		'current_user_trips': current_user_trips,
		'travelers':travelers,
		'other_trips':other_trips,
		'joined_trip':joined_trip
	}

	return render(request, 'trip_app/index.html', context)



def add_trip(request, methods='POST'):

	print "--------inside ADD TRIP route----------"
	print request.session['user']['id'],"<------------------here's the user_id"

		
	return render(request, 'trip_app/add_trip.html')


def create_trip(request, methods='POST'):
	print "--------inside CREATE TRIP route----------"
	print request.session['user']['id'],"<------------------here's the user_id"
	print request.POST


	response = Trip.objects.validate_info(request,request.POST)

	print response, "<-----------here is the response. Either [False, errors] or [True]"

	if response[0]== False:
		for message in response[1]: #saying  for message in errors:
			print "errors on the add trip form"
			messages.error(request, message[1])
		return redirect('trip_app:add_trip')

	else:
		print "<----Validations passed. About to update the trip-----------"
		trip = Trip_planner.objects.create_trip(request,request.POST)
		print trip[0]
		print trip[1]

	return redirect('trip_app:index')



def show_trip(request, number):

	print "--------inside SHOW TRIP route----------"

	selected_trip= Trip.objects.get(id=number)
	'''print selected_trip
	print selected_trip.destination
	print selected_trip.plan'''

	
	trip_maker= Trip_planner.objects.filter(trips_id=number) #this grabs all the users that have joined the selected trip(including person who created the trip)
	#print trip_maker, "yo yo ma"

	context = {
		
		'selected_trip':selected_trip,
		'trip_maker':trip_maker,
		'travelers':User.objects.all()
		
	}
		
	return render(request, 'trip_app/show_trip.html',context)



def join_trip(request, number,  methods='POST'):

	print "--------VIEWS JOIN TRIP route----------"
	request.session['number']= number


	join_trip = Trip.objects.join(request,request.POST)
	print join_trip, "this will return a T/F"

	if join_trip[0]== False:
		for message in join_trip[1]: #saying  for message in errors:
			print "errors on the add trip form"
			messages.error(request, message[1])
		return redirect('trip_app:index')

	else:
		print join_trip[0]
		print join_trip[1]
		return redirect('trip_app:index')


def clear(request):
	print '----------------            CLEARING THE SESSION         ---------------------'

	request.session.clear()

	return redirect('login_app:index')

