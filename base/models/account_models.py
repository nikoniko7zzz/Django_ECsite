from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id
# item_models.py のcreate_ideのこと(22文字のランダムな文字列を作る)

# Djangoのユーザーモデルをカスタマイズ


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# ユーザーのコア情報
class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, max_length=22)
    username = models.CharField(
        max_length=50, unique=True, blank=True, default='匿名')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.email

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

#ユーザーのプロフィール ユーザーコア情報と紐づいている
# blank=True 任意で入力でOK (注文時には空白NGとする)
class Profile(models.Model):
    # OneToOneField 1対1で紐づく.
    # on_delete=models.CASCADE ユーザーコア情報が削除されたらプロフィールも削除するよ
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(default='', blank=True, max_length=50) # 名前(宛名)
    zipcode = models.CharField(default='', blank=True, max_length=8) # 郵便番号
    prefecture = models.CharField(default='', blank=True, max_length=50) # 都道府県
    city = models.CharField(default='', blank=True, max_length=50) # 市町村
    address1 = models.CharField(default='', blank=True, max_length=50) # 番地など
    address2 = models.CharField(default='', blank=True, max_length=50)
    tel = models.CharField(default='', blank=True, max_length=15) # tel
    created_at = models.DateTimeField(auto_now_add=True) # 作成日
    updated_at = models.DateTimeField(auto_now=True) # 更新日

    def __str__(self):
        return self.name


# ユーザーコア情報作成時にプロフィールも同時に作れる
# OneToOneFieldを同時に作成
@receiver(post_save, sender=User) # Userモデルが入力保存されたときに実行する
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])