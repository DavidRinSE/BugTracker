from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password
        )
        user.is_admin = True
        user.save(using=self.db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'username'
    # Found solution here in line 54 of the source for createsuperuser
    # https://github.com/django/django/blob/master/django/contrib/auth/management/commands/createsuperuser.py
    
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
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Ticket(models.Model):
    title = models.CharField(max_length=50)
    dateFiled = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    userFiled = models.ForeignKey(MyUser, related_name="filed_user", on_delete=models.CASCADE)
    userAssigned = models.ForeignKey(MyUser, related_name="assigned_user", on_delete=models.CASCADE, blank=True, null=True)
    userCompleted = models.ForeignKey(MyUser, related_name="completed_user", on_delete=models.CASCADE, blank=True, null=True)
    STATUS_CHOICES = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
        ("Invalid", "Invalid"),
    ]
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default="New"
    )

    def assignTo(self, user):
        self.status = "In Progress"
        self.userAssigned = user
        self.userCompleted = None
        self.save()
    # When a ticket is assigned, these change as follows:

    #     Status: In Progress
    #     User Assigned: person the ticket now belongs to
    #     User who Completed: None

    def finishedBy(self, user):
        self.status = "Done"
        self.userAssigned = None
        self.userCompleted = user
        self.save()
    # When a ticket is Done, these change as follows:

    #     Status: Done_
    #     User Assigned: None
    #     User who Completed: person who the ticket used to belong to

    def markInvalid(self):
        self.status = "Invalid"
        self.userAssigned = None
        self.userCompleted = None
        self.save()
    # When a ticket is marked as Invalid, these change as follows:

    #     Status: Invalid
    #     User Assigned: None
    #     User who Completed: None
