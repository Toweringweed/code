# #%%
# from pyspark import  SparkContext as sc

# # conf = SparkConf().setMaster("local[*]")
# # conf = conf.setAppName('APP_NAME')

# # sc = SparkContext(conf=conf)
# df = sc.textFile(name="D:\code\hoomsun_data\analysis\Tele data.csv")
# print(df)

import os
import sys
spark_name = os.environ.get('SPARK_HOME',None)
if not spark_name:
    raise ValueErrorError('spark环境没有配置好')
sys.path.insert(0,os.path.join(spark_name,'python'))
sys.path.insert(0,os.path.join(spark_name,'python/lib/py4j-0.10.4-src.zip'))
exec(open(os.path.join(spark_name,'python/pyspark/shell.py')).read())

