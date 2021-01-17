from django.utils.crypto import get_random_string

# If random string is used as environment variable, characters should be compatible with elastic beanstalk environment variable values
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html
chars = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789'
randomm_string = get_random_string(100, chars)
print(randomm_string)