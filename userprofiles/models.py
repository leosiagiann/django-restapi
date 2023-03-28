from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=255, unique=True, null=False, db_index=True)
    age = models.IntegerField()
    status = models.CharField(max_length=32)

class DompetDigital(models.Model):
    # userprofile = models.OneToOneField(
    #     UserProfile,
    #     on_delete=models.CASCADE,
    #     primary_key=True,
    # )
    # saldo = models.IntegerField()
    TYPE = (
        ('O', 'Ovo'),
        ('D', 'Dana'),
        ('G', 'Gopay')
    )
    user_profiles = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=1, choices=TYPE, db_index=True)
    saldo = models.IntegerField()