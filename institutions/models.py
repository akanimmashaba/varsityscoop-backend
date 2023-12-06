from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
from django.utils import timezone
import uuid



class Institution(models.Model):
    class InstitutionTypes(models.TextChoices):
        UNIVERSITY = "uni", ("University")
        UNIVERSITY_TECHNOLOGY = "uot", ("University Of Tech")
        COLLAGE = "col", ("Collage")
        PRIVATE_COLLAGE = "pco", ("Private Collage")

    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.SlugField(max_length=20, unique=True)
    established_date = models.DateField()
    website = models.URLField()
    description = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    raw_file = models.FileField(upload_to='raw/', null=True,blank=True, storage=RawMediaCloudinaryStorage())
    Institution_type = models.CharField(max_length=3,choices=InstitutionTypes.choices, default=InstitutionTypes.UNIVERSITY)
    
    
    def __str__(self):
        return self.abbreviation.upper()
    
class Application(models.Model):
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    content = models.TextField(blank=True,null=True)
    opening_date = models.DateField(blank=True, null=True)
    closing_date = models.DateField(blank=True, null=True)
    late_opening_date = models.DateField(blank=True, null=True)
    late_closing_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.institution.abbreviation} - application'
    
    def get_application_fee(self):
        if self.fee < 1:
            return f'free'.capitalize()
        return str(self.fee)
    
    def is_application_period_open(self):
        current_date = timezone.now().date()
        if self.opening_date and self.closing_date:
            if self.opening_date <= current_date <= self.closing_date:
                return True
        return False
    def is_late_application_period_open(self):
        if self.late_opening_date and self.late_closing_date:
            current_date = timezone.now().date()
            if self.late_opening_date <= current_date <= self.late_closing_date:
                return True
        return False


    def get_application_period(self):
        if self.opening_date and self.closing_date:
            context = {
                'is_open': self.is_application_period_open,
                'opening_date': self.opening_date.strftime("%d-%m-%Y"),
                'closing_date': self.closing_date.strftime("%d-%m-%Y"),}
            return context
        else:
            context = {
                'message': 'Application period not set'
                }
            return context

    def get_late_application_period(self):
        if self.late_opening_date and self.late_closing_date:
            context = {
                'is_open': self.is_late_application_period_open,
                'opening_date': self.late_opening_date.strftime("%d-%m-%Y"),
                'closing_date': self.late_closing_date.strftime("%d-%m-%Y"),}
            return context
            
        else:
            context = {
                'is_open': self.is_late_application_period_open,
                'opening_date': self.late_opening_date.strftime("%d-%m-%Y"),
                'closing_date': self.late_closing_date.strftime("%d-%m-%Y"),
                'message': 'Late application period not set',
                }
            return context
