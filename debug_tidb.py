import pymysql
import os

try:
    conn = pymysql.connect(
        host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        port=4000,
        user='7Y3RshBF8QBknC5.root',
        password='yyWdKSeGH7G9J2rd',
        database='test',
        ssl={'ca': '/etc/ssl/certs/ca-certificates.crt'}
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
