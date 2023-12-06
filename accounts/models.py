from django.db import models
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser,PermissionsMixin)
import uuid 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import Group




class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    class UserTypeOptions(models.TextChoices):
        REGULAR = "R", ("Regular")
        WRITTER = "W", ("Writer")
        EDITOR = "E", ("Editor")
        MANAGER = "M", ("Manager")


    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False) 
    username = models.SlugField(max_length=150,unique=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=1,choices=UserTypeOptions.choices, default=UserTypeOptions.REGULAR)



    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_creator(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        if self.user_type != self.UserTypeOptions.REGULAR:
            return True
        return False
    
    @property
    def is_regular(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        if self.user_type == self.UserTypeOptions.REGULAR:
            return True
        return False
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avator = models.ImageField(upload_to='avator/', blank=True)


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()