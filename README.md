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

# ETL Process
## Customer
- Landing Zone
  - (Athena)SQL script - `customer_landing.sql`
  - (Athena)Glue Table - **customer_landing**
  - (Athena)Screenshot - `customer_landing.png`
    - Multiple rows where 'shareWithResearchAsOfDate' is blank
- Trusted Zone
  - (Glue Studio/Spark Job)Python script - `customer_landing_to_trusted.py`
    - Customers who agreed to share their data from research purposes.
  - (Athena)Glue Table - **customer_trusted**
  - (Athena)Screenshot - `customer_trusted.png`
    - No rows where 'shareWithResearchAsOfDate' is blank
- Curated Zone
  - (Glue Studio/Spark Job)Python script - `customer_trusted_to_curated.py`
    - Customers who have accelerometer data
    - Customers who agreed to share their data for research
  - (Athena)Glue Table - **customer_curated**
## Accelerometer
- Landing Zone
  - (Athena)SQL script - `accelerometer_landing.sql`
  - (Athena)Glue Table - **accelerometer_landing**
  - (Athena)Screenshot - `accelerometer_landing.png`
- Trusted Zone
  - (Glue Studio/Spark Job)Python script - `accelerometer_landing_to_trusted.py`
    - Accelerometer Readings from the customers who agreed to share their data for research purposes
  - (Athena)Glue Table - **accelerometer_trusted**
## Step Trainer
- Landing Zone
- Trusted Zone
  - (Glue Studio/Spark Job)Python script - `step_trainer_landing_to_trusted.py`
    - Step Trainer Records for customers who have accelerometer data
    - Step Trainer Records for customers who have agreed to share their data for research
  - (Athena)Glue Table - **step_trainer_trusted**
## Machine Learning
- Curated Zone
  - (Glue Studio/Spark Job)Python script - `aggregation.py`
    - Each of the Step Trainer Readings
    - Associated accelerometer reading data for the same timestamp
    - Only for customers who have agreed to share their data
  - (Athena)Glue Table - **machine_learning_curated**
