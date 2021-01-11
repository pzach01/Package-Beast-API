# Database Operations
## Overview
```
This document is intended to document database operations such as
1. Migrations
2. Prodution Database Hotfix Procedure
3. Database Recovery from Backup
```

## Migrations Procedure

### Make migrations: 

Database migrations are required when any model is changed.<br> Changes to a serializer do NOT require new migrations.<br> Migrations define database operations from application models. These are made with the development database credentials with the following command prior to pushing to development branch:

```
Activate virtual environment: source venv/bin/activate
python manage.py makemigrations
```

### Migrate (Optional): 
```
Both production and development databases migrate database migrations automatically according to .ebextensions/django.config. Production migrations should (generally) not be made from localhost as the migrations will be automatically applied by production elastic beanstalk environment. Development migrations may be made with the following command below:
```
```
Activate virtual environment: source venv/bin/activate
python manage.py migrate
```

## Production Database Hotfix Procedure: 
```
The production database credentials sensitive and are not included in source control. However, under rare circumstances, the production database may be remotely accessed and modified from localhost with procudure below: 
```
```
In manage.py, set useProductionDatabase=True (line 5)
Set production environment variables by placing set_production_environment_variables.py in project root directory
Activate virtual environment: source venv/bin/activate
python manage.py shell
```

## Database Backup and Recovery
```
THIS IS THE NUCLEAR OPTION. THESE STEPS SHOULD BE TAKEN AS A LAST RESORT. HOTFIX PROCEDURE IS PREFERRED IF POSSIBLE. If for some reason the production database becomes corrupted, the application can be modified to use a database backup with the following procedure:
Modify the following elastic beanstalk environment variables to point to database backup:
    DATABASE_NAME
    DATABASE_USER
    DATABASE_PASSWORD
    DATABASE_HOST
Return github master branch to last stable version of application.
```
