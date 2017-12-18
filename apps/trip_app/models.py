from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login_app.models import User
import datetime
from time import time, gmtime, strftime, strptime
import pytz
import time

class TravelManager(models.Manager):

	def validate_info(self,request,data):
		print "<----------------------------inside the validate_info()"


		errors=[]

		if len(data['destination']) < 1:
			errors.append([request,"Destination cannot be empty!"])
		if len(data['plan']) <1:
			errors.append([request,"Description cannot be empty!"])
		
		if len(data['start_date']) <1:
			errors.append([request,"Travel date from cannot be empty!"])
			print "errors"

		if len(data['end_date']) <1:
			errors.append([request,"Travel date to cannot be empty!"])
			print "errors"
			return [False, errors]

		
		

		else:
			today = datetime.date.today()
			today = str(today)
			print today, "<------------what is today------>"
			print type(today)
		
			start_date = data['start_date']
			print start_date, "<----------------- THE START DATE THAT WAS SELECTED FOR TRIP "
			start_date= str(start_date)
			print type(start_date)
			
			end_date = (data['end_date'])
			print end_date, "<----------------- THE END DATE THAT WAS SELECTED FOR TRIP "
			end_date= str(end_date)
			print type(end_date)
			
			if  (today > start_date) | (today > end_date):
				errors.append([request,"The dates you selected has already passed. Please select a later start date and/or end date"])
				return [False, errors]
			if  (end_date < start_date) :
				errors.append([request,"The end date you selected must be later than the start date. "])
				return [False, errors]

			else:
				return [True,errors]



	

	def join(self,request,data):
		print "INSIDE THE MODELS JOIN_TRIP()^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
		print data, "Data inside the def join() model"

		errors=[]

		user= User.objects.get(id=request.session['user']['id'])
		print user.id, "The user that will be joining the trip"

		trips_joined =user.trips.filter(id=request.session['number'])
		print trips_joined, "Here's the trips the user has or has not joined"

		if trips_joined:
			print "This user joined already"
			errors.append([request,"You already joined this trip!!"])
			return [False, errors]

		else:
			print " No join"
			trip=Trip.objects.get(id=request.session['number'])
			trip_has_been_joined= Trip_planner.objects.create(user=user, trips=trip, trip_maker=False, joined_trip=True)
			return [True, trip_has_been_joined]

		

class Trip_plannerManager(models.Manager):
	def create_trip(self,request,data):
		print "inside the create_trip() method"
		print data, "heres some data to look at"
		trip = Trip(destination=data['destination'], start_date=data['start_date'],end_date=data['end_date'],plan=data['plan'])#,trip_maker=data['trip_maker'])
		print data['trip_maker']
		trip.save()
		print trip.destination
	 	person_creating_trip=User.objects.get(id=request.session['user']['id'])
	 	print person_creating_trip.name
	 	x= Trip_planner(user=person_creating_trip, trips= trip, trip_maker=data['trip_maker'])
		x.save()
		print x
		return [trip,x]
		





class Trip(models.Model):
	destination = models.CharField(max_length=255)
	users = models.ManyToManyField(User,  related_name="trips", through="Trip_planner")
	start_date = models.DateField(['%Y-%m-%d'], null=True)
	end_date = models.DateField(['%Y-%m-%d'], null=True)
	plan =   models.CharField(max_length=255)
	
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = TravelManager()

	

	def __repr__(self):
		return "<ID: {}-Destination: {}- Start Date:{}- End Date: {}- Plan:{} - >".format(self.id, self.destination, self.start_date, self.end_date, self.plan)


class Trip_planner(models.Model):
    user = models.ForeignKey(User)
    trips = models.ForeignKey(Trip)
    trip_maker = models.BooleanField(default=False)
    joined_trip = models.BooleanField(default=False)
    objects = Trip_plannerManager()

    def __repr__(self):
		return "<User Id: {}- Trip Id:{}- Trip Maker:{} Joined Trip {}: - >".format(self.user, self.trips, self.trip_maker,self.joined_trip)


    

