from django.db import models
import stripe
from items.models import Item
from containers.models import Container
import time
import os

stripe.api_key = os.getenv('STRIPE_API_SECRET')

# THIS IS TIED TO CURRENT PRODUCTS; WONT BEHAVE CORRECTLY IF THESE FIELDS ARE WRONG
# type, ordering, cost, product id, price id, shipmentsAllowed, itemsAllowed, containersAllowed
# these 'emptyFields' are such to prevent reverse engineering

# production settings and test settings, respectively
if (os.getenv('ENVIRONMENT_TYPE') == 'PRODUCTION'):  
    SUBSCRIPTION_PROFILES=[
        ('trial',0,0,'emptyField741130','emptyField372215',10,10,10),
        ('standard',1,1000,'prod_Io5vXJKuoSljSG','price_1ICTjaJWFTMXIZUonP0TRYCm',50,50,50),
        ('premium',2,3000,'prod_Io5wQO8TZN0K8V','price_1ICTkBJWFTMXIZUoULj8wGsz',300,300,300),
        ('beastMode',3,5000,'prod_Io5w0g0GolhS70','price_1ICTkQJWFTMXIZUoyuuGwYpc',1000,5000,5000),
    ]
else:
    SUBSCRIPTION_PROFILES=[
        ('trial',0,0,'emptyField137824','emptyField329271',10,10,10),
        ('standard',1,1000,'prod_IiXkLvo2tLRuCi','price_1I76eoE5mpXPYa9nlFHK60Ge',50,50,50),
        ('premium',2,3000,'prod_IiXkKw7qe4Dt7l','price_1I76fUE5mpXPYa9ncmIy6tbY',300,300,300),
        ('beastMode',3,5000,'prod_IiXlcdTHpmbQHR','price_1I76gPE5mpXPYa9nzbdm3s9f',1000,5000,5000),
    ]

class SubscriptionManager(models.Manager):
    def create_subscription(self,user):
        stripeCustomer = stripe.Customer.create(
            email=user.email
        )
        subscription=self.create(owner=user,stripeCustomerId=stripeCustomer.id)

        return subscription


class Subscription(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='subscription', on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    stripeCustomerId=models.CharField(max_length=20)
    subscriptionType=models.CharField(max_length=20,default='trial')
    
    shipmentsUsed=models.IntegerField(default=0)
    shipmentsAllowed=models.IntegerField(default=10)

    itemsAllowed=models.IntegerField(default=10)
    containersAllowed=models.IntegerField(default=10)
    subscriptionUpdateInProgress=models.BooleanField(default=False)
    def getItemsUsed(self):
        return Item.objects.filter(owner=self.owner, arrangement__isnull=True).count()
    
    def getContainersUsed(self):
        return Container.objects.filter(owner=self.owner, arrangement__isnull=True).count()
    def getPaymentUpToDate(self):
        if not (self.subscriptionType == 'trial'):
            stripeSubscriptions=StripeSubscription.objects.filter(subscription=self).order_by('-created')
            return stripeSubscriptions[0].currentPeriodEnd+(60*60*24*2)>time.time()
        else:
            # 2 week trial period
            return time.time()<(self.created.timestamp()+(60*60*24*14))
    def getUserCanCreateArrangment(self):
        return (self.getPaymentUpToDate()) and (self.shipmentsUsed<self.shipmentsAllowed)
    def getUserCanCreateItem(self):
        return (self.getPaymentUpToDate()) and (self.getItemsUsed()<self.itemsAllowed)
    def getUserCanCreateContainer(self):
        return (self.getPaymentUpToDate()) and (self.getContainersUsed()<self.containersAllowed)

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
    def choose_upgrade_or_downgrade_with_price_id(self, priceId):
        currentSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[0]==self.subscriptionType][0]
        nextSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[4]==priceId][0]
        return currentSubProfile[1]<nextSubProfile[1]


    def downgrade_subscription(self, priceId):
        nextSubProfile=[sub for sub in SUBSCRIPTION_PROFILES if sub[4]==priceId][0]
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

    def increment_shipment_requests(self):
        self.shipmentsUsed+=1
        self.save()



class StripeSubscription(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    deleted=models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    createdStripe=models.IntegerField(default=0)
    currentPeriodEnd=models.IntegerField(default=0)
    # fields we read during a post to stripe
    stripeSubscriptionId=models.CharField(max_length=50,default="null")
    stripeSubscriptionItemDataPriceId=models.CharField(max_length=50)
    stripeSubscriptionCurrentPeriodEnd=models.CharField(max_length=50)
    stripeSubscriptionCustomer=models.CharField(max_length=50)

class InvoiceId(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    stripeSubscription = models.ForeignKey(StripeSubscription, on_delete=models.CASCADE)
    stripeInvoiceId=models.CharField(max_length=50)