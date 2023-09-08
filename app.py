import streamlit as st
import pandas as pd
import numpy as np

st.title('')

### Postgres 연결
import psycopg2

# 데이터베이스 설정 값
DATABASE = 'your_database_name'
USER = 'your_user_name'
PASSWORD = 'your_password'
HOST = 'localhost'  # or your database host
PORT = '5432'  # default port for PostgreSQL, change if yours is different

# 데이터베이스에 연결
connection = psycopg2.connect(
    dbname=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

# 커서 생성
cursor = connection.cursor()



