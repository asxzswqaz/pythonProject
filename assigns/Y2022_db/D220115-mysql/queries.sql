-- TASK1

-- 2
SELECT AU_ID, AU_FNAME, AU_LNAME
FROM AUTHOR
WHERE AU_ID
NOT IN (SELECT AU_ID FROM WRITES
			  WHERE BOOK_NUM=(SELECT BOOK_NUM FROM BOOK WHERE BOOK_SUBJECT='Programming')
				)
ORDER BY AU_LNAME;



-- 4

SELECT T1.BOOK_NUM, T1.BOOK_TITLE, T1.BOOK_SUBJECT, T1.AU_LNAME,
T2.NUM_BOOKS_BY_AUTHOR
FROM
(
SELECT BOOK.BOOK_NUM, BOOK.BOOK_TITLE, BOOK.BOOK_SUBJECT,
 AUTHOR.AU_LNAME, AUTHOR.AU_ID
FROM BOOK JOIN WRITES ON BOOK.BOOK_NUM=WRITES.BOOK_NUM
JOIN AUTHOR ON AUTHOR.AU_ID=WRITES.AU_ID
) T1
JOIN
(
SELECT AU_ID, COUNT(BOOK_NUM) AS NUM_BOOKS_BY_AUTHOR
WRITES
GROUP BY AU_ID
) T2 ON T1.AU_ID=T2.AU_ID;


-- 5

SELECT T1.LOWEST_AVG_COST, T2.HIGHEST_AVG_COST
FROM
(
SELECT BOOK_SUBJECT, AVG(BOOK_COST) AS LOWEST_AVG_COST
FROM BOOK
GROUP BY BOOK_SUBJECT
ORDER BY AVG(BOOK_COST)
LIMIT 1
) T1,
(
SELECT BOOK_SUBJECT, AVG(BOOK_COST) AS HIGHEST_AVG_COST
FROM BOOK
GROUP BY BOOK_SUBJECT
ORDER BY AVG(BOOK_COST) DESC
LIMIT 1
) T2;


-- TASK2

-- 6

SELECT EMP_FNAME,EMP_LNAME,EMP_EMAIL FROM LGEMPLOYEE
WHERE EMP_HIREDATE>='2005-01-01' AND EMP_HIREDATE<='2014-12-31'
ORDER BY EMP_LNAME, EMP_FNAME;

-- 7

SELECT EMP_FNAME,EMP_LNAME,EMP_PHONE, EMP_TITLE, DEPT_NUM FROM LGEMPLOYEE
WHERE EMP_TITLE LIKE '%CLERK I' OR DEPT_NUM=300
ORDER BY EMP_LNAME, EMP_FNAME;


-- 8


SELECT LGEMPLOYEE.EMP_NUM, EMP_FNAME,EMP_LNAME,SAL_FROM, SAL_END, SAL_AMOUNT
FROM LGEMPLOYEE JOIN LGSALARY_HISTORY ON LGEMPLOYEE.EMP_NUM=LGSALARY_HISTORY.EMP_NUM
WHERE LGEMPLOYEE.EMP_NUM IN ('83731', '83745','84039')
ORDER BY LGEMPLOYEE.EMP_NUM,SAL_FROM;



-- 9

SELECT DISTINCT CUST_FNAME, CUST_LNAME, CUST_STREET, CUST_CITY, CUST_STATE, CUST_ZIP
FROM LGCUSTOMER
JOIN LGINVOICE ON LGCUSTOMER.CUST_CODE= LGINVOICE.CUST_CODE
JOIN LGLINE ON LGLINE.INV_NUM=LGINVOICE.INV_NUM
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGLINE.PROD_SKU
JOIN LGBRAND ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
WHERE LGINVOICE.INV_DATE BETWEEN '2017-07-15' AND '2017-07-31'
AND LGBRAND.BRAND_NAME='FORESTERS BEST' AND LGPRODUCT.PROD_CATEGORY='Top Coat'
ORDER BY CUST_STATE, CUST_LNAME, CUST_FNAME;


-- 10

SELECT LGEMPLOYEE.EMP_NUM, EMP_LNAME,EMP_EMAIL,EMP_TITLE, DEPT_NAME
FROM LGEMPLOYEE JOIN LGDEPARTMENT ON LGEMPLOYEE.DEPT_NUM=LGDEPARTMENT.DEPT_NUM
WHERE EMP_TITLE LIKE '%ASSOCIATE'
ORDER BY DEPT_NAME, EMP_TITLE, LGEMPLOYEE.EMP_NUM;


-- 11


SELECT BRAND_NAME, COUNT(LGPRODUCT.PROD_SKU) AS NUMPRODUCTS
FROM LGBRAND JOIN LGPRODUCT ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
GROUP BY BRAND_NAME
ORDER BY BRAND_NAME;

-- 12
SELECT BRAND_ID, SUM(PROD_QOH) AS TOTALINVENTORY
FROM LGPRODUCT
GROUP BY BRAND_ID
ORDER BY BRAND_ID DESC;

-- 13
SELECT LGBRAND.BRAND_ID, BRAND_NAME, ROUND(AVG(PROD_PRICE),2) AS AVGPRICE
FROM LGBRAND JOIN LGPRODUCT ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
GROUP BY LGBRAND.BRAND_ID,BRAND_NAME
ORDER BY BRAND_NAME;

-- 14
SELECT LGEMPLOYEE.EMP_NUM, EMP_FNAME,EMP_LNAME, MAX(SAL_AMOUNT)
FROM LGEMPLOYEE JOIN LGSALARY_HISTORY ON LGEMPLOYEE.EMP_NUM=LGSALARY_HISTORY.EMP_NUM
WHERE DEPT_NUM=200
GROUP BY LGEMPLOYEE.EMP_NUM, EMP_FNAME,EMP_LNAME
ORDER BY MAX(SAL_AMOUNT) DESC;

-- 15

SELECT LGDEPARTMENT.DEPT_NUM, DEPT_NAME, DEPT_PHONE, LGDEPARTMENT.EMP_NUM, LGEMPLOYEE.EMP_LNAME
FROM LGDEPARTMENT JOIN LGEMPLOYEE ON LGDEPARTMENT.EMP_NUM=LGEMPLOYEE.EMP_NUM
ORDER BY DEPT_NAME;


-- 16

SELECT LGVENDOR.VEND_ID, VEND_NAME, LGBRAND.BRAND_NAME, COUNT(LGSUPPLIES.PROD_SKU) AS NUMPRODUCTS
FROM LGVENDOR
JOIN LGSUPPLIES ON LGSUPPLIES.VEND_ID= LGVENDOR.VEND_ID
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGSUPPLIES.PROD_SKU
JOIN LGBRAND ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
GROUP BY LGVENDOR.VEND_ID, VEND_NAME, LGBRAND.BRAND_NAME
ORDER BY VEND_NAME, LGBRAND.BRAND_NAME;


-- 17
SELECT ROUND(MAX(AVG_PROD_PRICE),2) AS LARGEST_AVERAGE
FROM
(
SELECT BRAND_ID, AVG(PROD_PRICE) AS AVG_PROD_PRICE
FROM LGPRODUCT
GROUP BY BRAND_ID
) T;


-- 18
SELECT T1.*
FROM
(
SELECT LGPRODUCT.BRAND_ID, BRAND_NAME, BRAND_TYPE, ROUND(AVG(PROD_PRICE),2) AS AVGPRICE
FROM LGPRODUCT JOIN LGBRAND ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
GROUP BY LGPRODUCT.BRAND_ID, BRAND_NAME, BRAND_TYPE
) T1,
(
SELECT ROUND(MAX(AVG_PROD_PRICE),2) AS LARGEST_AVERAGE
FROM
(
SELECT BRAND_ID, AVG(PROD_PRICE) AS AVG_PROD_PRICE
FROM LGPRODUCT
GROUP BY BRAND_ID
) T
) T2 WHERE T1.AVGPRICE=T2.LARGEST_AVERAGE
;


-- 19

SELECT LGEMPLOYEE.EMP_NUM, EMP_LNAME, EMP_FNAME, SAL_AMOUNT
FROM LGEMPLOYEE JOIN LGSALARY_HISTORY ON LGEMPLOYEE.EMP_NUM=LGSALARY_HISTORY.EMP_NUM
WHERE DEPT_NUM=300 AND LGSALARY_HISTORY.SAL_END IS NULL
ORDER BY SAL_AMOUNT DESC;


-- 20
SELECT LGEMPLOYEE.EMP_NUM,EMP_LNAME,  EMP_FNAME,SAL_AMOUNT
FROM LGEMPLOYEE JOIN LGSALARY_HISTORY ON LGEMPLOYEE.EMP_NUM=LGSALARY_HISTORY.EMP_NUM
JOIN
(
SELECT EMP_NUM, MIN(SAL_FROM) AS OLDEST_SAL
FROM LGSALARY_HISTORY
GROUP BY EMP_NUM
) T ON T.EMP_NUM=LGEMPLOYEE.EMP_NUM AND T.OLDEST_SAL=LGSALARY_HISTORY.SAL_FROM
ORDER BY LGEMPLOYEE.EMP_NUM;

-- 21

SELECT T1.INV_NUM, T1.LINE_NUM AS "LINE_NUM(S)", T1.PROD_SKU AS "PROD_SKU(S)",
T1.PROD_DESCRIPT AS "PROD_DESCRIPT(S)", T2.LINE_NUM AS "LINE_NUM(T)", T2.PROD_SKU AS "PROD_SKU(T)",
T2.PROD_DESCRIPT AS "PROD_DESCRIPT(T)", T1.BRAND_ID
FROM
(
SELECT LGINVOICE.INV_NUM, LGLINE.LINE_NUM, LGPRODUCT.PROD_SKU, PROD_DESCRIPT, BRAND_ID
FROM LGINVOICE
JOIN LGLINE ON LGLINE.INV_NUM=LGINVOICE.INV_NUM
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGLINE.PROD_SKU
WHERE PROD_CATEGORY='Sealer'
) T1
JOIN
(
SELECT LGINVOICE.INV_NUM, LGLINE.LINE_NUM, LGPRODUCT.PROD_SKU, PROD_DESCRIPT, BRAND_ID
FROM LGINVOICE
JOIN LGLINE ON LGLINE.INV_NUM=LGINVOICE.INV_NUM
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGLINE.PROD_SKU
WHERE PROD_CATEGORY='Top Coat'
) T2 ON T1.INV_NUM=T2.INV_NUM AND T1.BRAND_ID=T2.BRAND_ID
ORDER BY T1.INV_NUM ASC, T1.LINE_NUM ASC, T2.LINE_NUM DESC;

-- 22

SELECT T.*
FROM
(
SELECT LGEMPLOYEE.EMP_NUM,  EMP_FNAME,EMP_LNAME,EMP_EMAIL, SUM(LGLINE.LINE_QTY) AS TOTAL
FROM LGEMPLOYEE JOIN LGINVOICE ON LGEMPLOYEE.EMP_NUM=LGINVOICE.EMPLOYEE_ID
JOIN LGLINE ON LGLINE.INV_NUM=LGINVOICE.INV_NUM
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGLINE.PROD_SKU
JOIN LGBRAND ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
WHERE LGINVOICE.INV_DATE BETWEEN '2017-11-01' AND '2017-12-05'
AND LGBRAND.BRAND_NAME='BINDER PRIME'
GROUP BY LGEMPLOYEE.EMP_NUM,  EMP_FNAME,EMP_LNAME,EMP_EMAIL
) T
WHERE
TOTAL=
(
SELECT MAX(TOTAL)
FROM
(
SELECT LGEMPLOYEE.EMP_NUM,  EMP_FNAME,EMP_LNAME,EMP_EMAIL, SUM(LGLINE.LINE_QTY) AS TOTAL
FROM LGEMPLOYEE JOIN LGINVOICE ON LGEMPLOYEE.EMP_NUM=LGINVOICE.EMPLOYEE_ID
JOIN LGLINE ON LGLINE.INV_NUM=LGINVOICE.INV_NUM
JOIN LGPRODUCT ON LGPRODUCT.PROD_SKU=LGLINE.PROD_SKU
JOIN LGBRAND ON LGBRAND.BRAND_ID=LGPRODUCT.BRAND_ID
WHERE LGINVOICE.INV_DATE BETWEEN '2017-11-01' AND '2017-12-05'
AND LGBRAND.BRAND_NAME='BINDER PRIME'
GROUP BY LGEMPLOYEE.EMP_NUM,  EMP_FNAME,EMP_LNAME,EMP_EMAIL
) TT
)
ORDER BY T.EMP_LNAME;

-- 23


SELECT DISTINCT T1.*
FROM
(
SELECT LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME
FROM LGCUSTOMER
JOIN LGINVOICE ON LGCUSTOMER.CUST_CODE= LGINVOICE.CUST_CODE
WHERE LGINVOICE.EMPLOYEE_ID='83649'
) T1
JOIN
(
SELECT LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME
FROM LGCUSTOMER
JOIN LGINVOICE ON LGCUSTOMER.CUST_CODE= LGINVOICE.CUST_CODE
WHERE LGINVOICE.EMPLOYEE_ID='83677'
) T2 ON T1.CUST_CODE=T2.CUST_CODE
ORDER BY T1.CUST_LNAME, T1.CUST_FNAME;

-- 24

SELECT T1.*
FROM
(
SELECT DISTINCT LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME, CUST_STREET, CUST_CITY,
CUST_STATE, CUST_ZIP, LGINVOICE.INV_DATE, IFNULL(MAX(INV_TOTAL),0) AS LARGEST_INVOICE
FROM LGCUSTOMER
LEFT JOIN LGINVOICE ON LGCUSTOMER.CUST_CODE= LGINVOICE.CUST_CODE
WHERE CUST_STATE='AL'
GROUP BY LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME, CUST_STREET, CUST_CITY,
CUST_STATE, CUST_ZIP, LGINVOICE.INV_DATE
ORDER BY CUST_LNAME, CUST_FNAME
) T1
JOIN
(
SELECT DISTINCT LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME, CUST_STREET, CUST_CITY,
CUST_STATE, CUST_ZIP, IFNULL(MAX(INV_TOTAL),0) AS LARGEST_INVOICE
FROM LGCUSTOMER
LEFT JOIN LGINVOICE ON LGCUSTOMER.CUST_CODE= LGINVOICE.CUST_CODE
WHERE CUST_STATE='AL'
GROUP BY LGCUSTOMER.CUST_CODE, CUST_FNAME, CUST_LNAME, CUST_STREET, CUST_CITY,
CUST_STATE, CUST_ZIP
ORDER BY CUST_LNAME, CUST_FNAME
) T2 ON T1.CUST_CODE=T2.CUST_CODE AND T1.LARGEST_INVOICE=T2.LARGEST_INVOICE;