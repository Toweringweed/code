UPDATE cust_label
SET idcard_area = (
CASE
WHEN (SUBSTRING(id_card,5,1) = '0')
then 
'市区'
when (SUBSTRING(id_card,5,1) IN ('1','2'))
THEN
'偏远区县'
when (SUBSTRING(id_card,5,1) IN ('3','4','5'))
THEN
'村、乡'
when (SUBSTRING(id_card,5,1)='8')
THEN
'县级市'
END)