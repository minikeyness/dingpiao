from mysite.models import Myuser
from django.db.models import Q


class Mycustombackend:

    def authenticate(self, name_email=None, password=None):
        try:
            user = Myuser.objects.get(Q(userEmail=name_email) | Q(nickName=name_email))
        except Myuser.DoesNotExist:
            pass
        else:
            user.check_password(password)
            return user
        return None


    def get_user(self, user_id):
        try:
            return Myuser.objects.get(pk=user_id)
        except Myuser.DoesNotExist:
            return None

