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
- `customer_landing.sql`<br>`accelerometer_landing.sql`<br>SQL DDL scripts that creating Glue Tables from JSON data.
- `customer_landing.png`<br>`accelerometer_landing.png`<br>Screenshots show SELECT statements from Athena showing the **Customer** and **Accelerometer landing data**, where the customer landing data has **multiple rows** where 'shareWithResearchAsOfDate' is blank.
- `customer_landing_to_trusted.py`<br>Sanitize the **Customer** data from the Website (Landing Zone) and only store the Customer Records who **agreed to share** their data from research purposes (Trusted Zone).
- `accelerometer_landing_to_trusted.py`<br>Sanitize the **Accelerometer** data from the Mobile App (Landing Zone) and only store Accelerometer Readings from the customers who **agreed to share** their data for research purposes (Trusted Zone).
- `customer_trusted.png`<br>A screenshot that shows a SELECT * statement from Athena showing the customer landing data, where the resulting **Customer trusted data** has **no rows** where 'shareWithResearchAsOfDate' is blank.
- `customer_trusted_to_curated.py`<br>Santize the **Customer** data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who **have accelerometer data** and have **agreed to share** their data for research.
- `trainer_trusted_to_curated.py`<br>Create an aggregated table that has **each of the Step Trainer readings**, and the **associated accelerometer reading data for the same timestamp**, but only for customers who have **agreed to share** their data.

# ETL Process
## Customer
- Landing Zone - Athena
- Landing to Trusted - Glue Studio/Spark Job
  - Filter protected PII: Drop data that doesn't have data in the 'shareWithResearchAsOfDate' column.
- Trusted Zone - Athena
  - Screenshot shows that results have no rows where 'shareWithResearchAsOfDate' is blank.
- Trusted to Curated - Glue Studeio/Spark Job
  - Only contains only customer data from customer records that aggreed to share data, and is joined with the correct accelerometer data.
## Accelerometer
- Landing Zone - Athena
- Landing to Trusted - Glue Studio/Spark Job
  - Filter out any readings that were prior to the research consent date.
  - Join Privacy tables - Inner joins that join up with the customer_landing table on the 'serialNumber' field.
## Step Trainer
- Landing Zone - Athena
- Landing to Trusted - Glue Studio/Spark Job
  - Inner Join with customer_curated table.
# Curated
- Glue Studio/Spark Job
  - Join trusted data: Inner joins with the customer_trusted table.
  - Anonymize the final curated table: Remove email, and any other personally identifying information up front.

