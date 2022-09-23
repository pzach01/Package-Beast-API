#! /bin/bash

# Script to package virtual environment libraries into zip, 
# and move lambda function into zip file for deployment to AWS Lambda
# User may change name of zip file or comment 
# If python packages are already zipped, user may bypass zipping of python packages
# by setting ZIP_PYTHON_PACKAGES="False" 


ZIP_FILE_NAME="my-deployment-package.zip"
ZIP_PYTHON_PACKAGES="False"


if [ "$ZIP_PYTHON_PACKAGES" == "True" ]; then
    echo "yo yo"
    deactivate
    cd venv/lib/python3.8/site-packages
    zip -r ../../../../${ZIP_FILE_NAME} .
    cd ../../../../
fi
zip -g ${ZIP_FILE_NAME} lambda_function.py
source venv/bin/activate