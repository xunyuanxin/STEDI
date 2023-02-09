# STEDI Human Balance Analytics
This project is for the STEDI team to build a data lakehouse solution for sensor data that trains a machine learning model.
The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:
- trains the user to do a STEDI balance exercise;
- and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
- has a companion mobile app that collects customer data and interacts with the device sensors.
# Project Purpose
- Extract the data produced by the STEDI Step Trainer sensors and the mobile app
- Curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model
# Environments
AWS Glue, AWS S3, Python, and Spark
# Data Source
**STEDI** has three JSON data sources to use from the Step Trainer. You can [download the data from here](https://video.udacity-data.com/topher/2022/June/62be2ed5_stedihumanbalanceanalyticsdata/stedihumanbalanceanalyticsdata.zip) or you can extract it from their respective public S3 bucket locations:

**1. Customer Records (from fulfillment and the STEDI website)**:
<br>AWS S3 Bucket URI - s3://cd0030bucket/customers/
<br>contains the following fields:
- serialnumber
- sharewithpublicasofdate
- birthday
- registrationdate
- sharewithresearchasofdate
- customername
- email
- lastupdatedate
- phone
- sharewithfriendsasofdate

**2. Step Trainer Records (data from the motion sensor)**:
<br>AWS S3 Bucket URI - s3://cd0030bucket/step_trainer/
<br>contains the following fields:
- sensorReadingTime
- serialNumber
- distanceFromObject

**3. Accelerometer Records (from the mobile app)**:
<br>AWS S3 Bucket URI - s3://cd0030bucket/accelerometer/
<br>contains the following fields:
- timeStamp
- serialNumber
- x
- y
- z
# Files
## Landing Zone
- Use Glue Studio to ingest customer and accelerometer landing zone data from S3 bucket.<br>`customer_landing_to_trusted.py`<br>`accelerometer_landing_to_trusted`
- Manually create a Glue Table using Glue Console from JSON data.
<br>`customer_landing.sql`<br>`accelerometer_landing.sql`

## Trusted Zone

## Curated Zone
# Steps

- Create S3 directories for **customer_landing**, **step_trainer_landing**, and **accelerometer_landing** zones
- Copy the data there
- Create two Glue tables for the two landing zones
