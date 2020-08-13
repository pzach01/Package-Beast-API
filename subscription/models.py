from django.db import models

# Create your models here.

class Subscription():
    owner = models.ForeignKey(
        'users.User', related_name='subscription', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    subscriptionType=models.CharField(max_length=20)
    numRequestsLeft=models.IntegerField()
    numItemsCanAdd=models.IntegerField()
    numContainersCanAdd=models.IntegerField()
    # note that this is a soft field, it is only used to check
    # that stripe is working on time, not actually apply payments
    lastUpdateAbsoluteTime=models.FloatField()

    # newSubscriptionType is whether the payment is a renewal or 
    # an upgrade/downgrade
    def update_subscription(amountCharged, newSubscriptionType):
        if newSubscriptionType:
            if amountCharged==2:
                pass
            elif amountCharged==10:
                pass
            elif amountCharged==20:
                pass
            elif amountCharged==50:
                pass
        else:
            if amountCharged==2:
                pass
            elif amountCharged==10:
                pass
            elif amountCharged==20:
                pass
            elif amountCharged==50:
                pass