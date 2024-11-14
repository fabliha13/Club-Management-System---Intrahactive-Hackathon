
from django.db import models
from django.contrib.auth.models import User



class club_panel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=True)
    club_name= models.CharField(max_length=50)
    status=models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.club_name)



#club_logo = models.ImageField(upload_to='profile_pic/ClubPic/',null=True,blank=True)

class Event(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    club = models.ForeignKey(club_panel, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    submission_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.location})"

class RoomBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="room_bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.room.name} for {self.event.title}"

class BudgetRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="budget_requests")
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    budget_description = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Budget for {self.event.title}"

class Communication(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.from_user} to {self.to_user}"

class EventReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reports")
    is_live = models.BooleanField(default=False)
    summary = models.TextField()
    participation_count = models.IntegerField()
    total_budget_used = models.DecimalField(max_digits=10, decimal_places=2)
    room_booking_details = models.ManyToManyField(RoomBooking, related_name="reports")

    def __str__(self):
        return f"Report for {self.event.title}"