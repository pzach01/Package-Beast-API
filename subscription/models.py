from django.db import models
import stripe
stripe.api_key = 'sk_test_51HB4dCJWFTMXIZUo5d1tlWus4t0NGBLPI6LqHVokCzOyXaYZ6f8rcBqAeWZUdtfdc6tl5EenjpUXWrpFsyRmAwgJ00fRuOxc8b'

# THIS IS TIED TO CURRENT PRODUCTS; WONT BEHAVE CORRECTLY IF THESE FIELDS ARE WRONG
# type, ordering, cost, product id, price id, shipmentsAllowed, itemsAllowed, containersAllowed
SUBSCRIPTION_PROFILES=[
    ('standard',0,1000,'prod_HzHvyINf9uyaxv','price_1HPJLlJWFTMXIZUoMH26j2EB',50,50,50),
    ('premium',1,3000,'prod_HzHxDGJSZDQ8GI','price_1HPJNoJWFTMXIZUo60gNaXlm',300,300,300),
    ('beast_mode',2,5000,'prod_HzHy8kP263Pqzp','price_1HPJOLJWFTMXIZUoGcXhTnax',1000,1000,1000),
]

class SubscriptionManager(models.Manager):
    def create_subscription(self,user):
        stripeCustomer = stripe.Customer.create(
            email=user.email
        )
        subscription=self.create(owner=user,stripeCustomerId=stripeCustomer.id)


        # do something with the book
        return subscription





class Subscription(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='subscription', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    stripeCustomerId=models.CharField(max_length=20)
    subscriptionType=models.CharField(max_length=20,default='none')
    
    shipmentsUsed=models.IntegerField(default=0)
    shipmentsAllowed=models.IntegerField(default=0)

    itemsAllowed=models.IntegerField(default=0)
    itemsUsed=models.IntegerField(default=0)

    containersAllowed=models.IntegerField(default=0)
    containersUsed=models.IntegerField(default=0)

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

    # if upgrade then increment required values and change subscriptionType else just change subscriptionType
    # DESIGN DECISION: subscriptionType holds the type corresponding to last paid invoice, but because we dont limit
    # permissions immediately upon downgrading sub type, this may not correspond to the permissions profile (ie. requests allowed)
    # for the subscription until next month (in general case)
    def upgrade_or_downgrade(self, productId):
        currentSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[0]==self.subscriptionType][0]
        nextSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[3]==productId][0]
        # upgrade
        if currentSubProfile[1]<nextSubProfile[1]:
            self.shipmentsAllowed=nextSubProfile[5]
            self.itemsAllowed=nextSubProfile[6]
            self.containersAllowed=nextSubProfile[7]
        # update subscriptionType
        self.subscriptionType=nextSubProfile[0]
        self.save()
    # reset used values and set to desired
    def initialize_or_refill(self, productId):
        nextSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[3]==productId][0]

        self.shipmentsUsed=0

        self.shipmentsAllowed=nextSubProfile[5]
        self.itemsAllowed=nextSubProfile[6]
        self.containersAllowed=nextSubProfile[7]
        # update subscriptionType
        self.subscriptionType=nextSubProfile[0]
        self.save()

class StripeSubscription(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    deleted=models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    # fields we read during a post to stripe
    stripeSubscriptionId=models.CharField(max_length=50,default="null")
    stripeSubscriptionItemDataPriceId=models.CharField(max_length=50)
    stripeSubscriptionCurrentPeriodEnd=models.CharField(max_length=50)
    stripeSubscriptionCustomer=models.CharField(max_length=50)

class InvoiceId(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    stripeSubscription = models.ForeignKey(StripeSubscription, on_delete=models.CASCADE)
    stripeInvoiceId=models.CharField(max_length=50)