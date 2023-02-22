import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer Curated
CustomerCurated_node1676564904667 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://chaolizi-stedi-lakehouse/customer/curated/"],
        "recurse": True,
    },
    transformation_ctx="CustomerCurated_node1676564904667",
)

# Script generated for node Step Training Landing
StepTrainingLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://chaolizi-stedi-lakehouse/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainingLanding_node1",
)

# Script generated for node Renamed keys for Inner Join
RenamedkeysforInnerJoin_node1676571402607 = ApplyMapping.apply(
    frame=CustomerCurated_node1676564904667,
    mappings=[
        ("serialNumber", "string", "`(right) serialNumber`", "string"),
        ("birthDay", "string", "`(right) birthDay`", "string"),
        ("shareWithResearchAsOfDate", "bigint", "shareWithResearchAsOfDate", "long"),
        ("registrationDate", "bigint", "registrationDate", "long"),
        ("customerName", "string", "`(right) customerName`", "string"),
        ("email", "string", "`(right) email`", "string"),
        ("lastUpdateDate", "bigint", "lastUpdateDate", "long"),
        ("phone", "string", "`(right) phone`", "string"),
        ("shareWithPublicAsOfDate", "bigint", "shareWithPublicAsOfDate", "long"),
        ("shareWithFriendsAsOfDate", "bigint", "shareWithFriendsAsOfDate", "long"),
    ],
    transformation_ctx="RenamedkeysforInnerJoin_node1676571402607",
)

# Script generated for node Inner Join
InnerJoin_node2 = Join.apply(
    frame1=StepTrainingLanding_node1,
    frame2=RenamedkeysforInnerJoin_node1676571402607,
    keys1=["serialNumber"],
    keys2=["`(right) serialNumber`"],
    transformation_ctx="InnerJoin_node2",
)

# Script generated for node ValidConsentDate
SqlQuery618 = """
select * from myDataSource
where shareWithResearchAsOfDate < sensorReadingTime
"""
ValidConsentDate_node1676572128038 = sparkSqlQuery(
    glueContext,
    query=SqlQuery618,
    mapping={"myDataSource": InnerJoin_node2},
    transformation_ctx="ValidConsentDate_node1676572128038",
)

# Script generated for node Select Fields
SelectFields_node1676572142908 = SelectFields.apply(
    frame=ValidConsentDate_node1676572128038,
    paths=["sensorReadingTime", "serialNumber", "distanceFromObject"],
    transformation_ctx="SelectFields_node1676572142908",
)

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=SelectFields_node1676572142908,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://chaolizi-stedi-lakehouse/step_trainer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="StepTrainerTrusted_node3",
)

job.commit()
