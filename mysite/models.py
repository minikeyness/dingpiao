from django.db import models
import hashlib
from django.utils.crypto import salted_hmac
from django.contrib.auth.models import AbstractBaseUser

class CustomUserManager:

    @staticmethod
    def create_user(self, nickName, userEmail, passPwd):
        newuser = Myuser(nickName=nickName, userEmail=userEmail, passPwd=passPwd)
        newuser.save()
        return newuser

    @staticmethod
    def create_superuser(self, nickName, userEmail, passPwd):
        newuser = Myuser(nickName=nickName, userEmail=userEmail, passPwd=passPwd, isSuper=True)
        newuser.save()
        return newuser


class Myuser(models.Model):

    nickName = models.CharField(max_length=50, unique=True)
    passPwd = models.CharField(max_length=50)
    userEmail = models.EmailField(unique=True)
    realName = models.CharField(max_length=20, blank=True)
    idCard = models.CharField(max_length=20, blank=True)
    phoneNum = models.CharField(max_length=20, blank=True)
    isSuper = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'userEmail'
    REQUIRED_FIELDS = ['nickName', 'passPwd']
    object = CustomUserManager

    def is_authenticated(self):
        return True

    def set_hashedpwd(self):
        self.passPwd = hashlib.md5(self.passPwd.encode('utf-8')).hexdigest()

    def hashed_password(self, password=None):
        if not password:
            return self.passPwd
        else:
            return hashlib.md5(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        if self.hashed_password(password) == self.passPwd:
            return True
        return False

    def get_full_name(self):
        return self.nickName

    def get_short_name(self):
        return self.nickName

    def get_username(self):
        return self.userEmail

    def is_anonymous(self):
        return False

    def get_session_auth_hash(self):
        return salted_hmac("mysite", self.passPwd).hexdigest()

    def changepwd(self, newpwd):
        Myuser.objects.filter(id=self.id).update(passPwd=newpwd)

    class Meta:
        db_table = "users"

