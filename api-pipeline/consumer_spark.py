from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as F
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4

spark = SparkSession.builder.appName('Weather-api').config('spark.sql.warehouse.dir','/user/hive/warehouse').config('hive.metastore.uris','thrift://localhost:9083').enableHiveSupport().getOrCreate()
spark.sparkContext.setLogLevel("WARN")
#read json schema from a test file
json_schema = spark.read.format('json').load('file:////home/nhobbs/BigData2020/task6/test.txt').schema

df = spark.readStream.format('kafka')\
    .option('kafka.bootstrap.servers','localhost:9093')\
    .option('subscribe','realtime')\
    .load()

df_data = df.select(from_json(col("value")\
              .cast("string"), json_schema)\
                    .alias('weather')).selectExpr('weather.*')
nested_cols = [c[0] for c in df_data.dtypes if c[1][:6] == 'struct']

df_clean = df_data.select([F.col('lat'),F.col('lon')]+list(map(lambda x: F.col(x).value.alias(x),nested_cols)))

def write_hive(df,epoch_id):
	df.show()
	df.write.mode('append').saveAsTable('bigdata2020.weatherdata')
	

out=df_clean.writeStream.foreachBatch(write_hive).start()

out.awaitTermination()

