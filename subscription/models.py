from django.db import models
import stripe
stripe.api_key = 'sk_test_51HB4dCJWFTMXIZUo5d1tlWus4t0NGBLPI6LqHVokCzOyXaYZ6f8rcBqAeWZUdtfdc6tl5EenjpUXWrpFsyRmAwgJ00fRuOxc8b'

# Create your models here.


class SubscriptionManager(models.Manager):
    def create_subscription(self,user):
        stripeCustomer = stripe.Customer.create(
            email=user.email
        )
        subscription=self.create(owner=user,stripeId=stripeCustomer.id)


        # do something with the book
        return subscription





class Subscription(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='subscription', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    stripeCustomerId=models.CharField(max_length=20)


    # fields we read during a post to stripe
    stripeSubscriptionId=models.CharField(max_length=50,default="null")
    stripeSubscriptionItemDataPriceId=models.CharField(max_length=50)
    stripeSubscriptionCurrentPeriodEnd=models.CharField(max_length=50)
    stripeSubscriptionCustomer=models.CharField(max_length=50)
    #stripeInvoiceIds=models.CharField(default='', max_length=250)
    '''
    subscriptionType=models.CharField(max_length=20)
    numRequestsLeft=models.IntegerField()
    numItemsCanAdd=models.IntegerField()
    numContainersCanAdd=models.IntegerField()
    # note that this is a soft field, it is only used to check
    # that stripe is working on time, not actually apply payments
    lastUpdateAbsoluteTime=models.FloatField()
    '''
    objects=SubscriptionManager()
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



class InvoiceId(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    stripeInvoiceId=models.CharField(max_length=50)