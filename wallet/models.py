from django.db import models
from accounts.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email

class WalletHistory(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)