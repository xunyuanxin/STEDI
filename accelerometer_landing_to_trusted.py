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

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://chaolizi-stedi-lakehouse/accelerometer/landing/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerLanding_node1",
)

# Script generated for node Customer Trusted
CustomerTrusted_node1675889561279 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://chaolizi-stedi-lakehouse/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1675889561279",
)

# Script generated for node Inner Join
InnerJoin_node2 = Join.apply(
    frame1=AccelerometerLanding_node1,
    frame2=CustomerTrusted_node1675889561279,
    keys1=["user"],
    keys2=["email"],
    transformation_ctx="InnerJoin_node2",
)

# Script generated for node ValidConsentDate
SqlQuery564 = """
select * from myDataSource
where shareWithResearchAsOfDate < timestamp
"""
ValidConsentDate_node1675961437747 = sparkSqlQuery(
    glueContext,
    query=SqlQuery564,
    mapping={"myDataSource": InnerJoin_node2},
    transformation_ctx="ValidConsentDate_node1675961437747",
)

# Script generated for node Drop Fields
DropFields_node1675889664225 = SelectFields.apply(
    frame=ValidConsentDate_node1675961437747,
    paths=["user", "timeStamp", "x", "y", "z"],
    transformation_ctx="DropFields_node1675889664225",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node3 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1675889664225,
    connection_type="s3",
    format="json",
    connection_options={
        "path": "s3://chaolizi-stedi-lakehouse/accelerometer/trusted/",
        "partitionKeys": [],
    },
    transformation_ctx="AccelerometerTrusted_node3",
)

job.commit()
