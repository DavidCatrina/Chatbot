import pymysql
import datetime
import pandas as pd

digits_to_text = {
        '9_10': 'noua zece', 
        '10_11': 'zece unsprezece', 
        '11_12': 'unsprezece doisprezece',  
        '12_13': 'doisprezece treisprezece',  
        '13_14': 'treisprezece paisprezece',  
        '14_15': 'paisprezece cincisprezece',  
        '15_16': 'cincisprezece saisprezece',  
        '16_17': 'saisprezece saptisprezece'
    }

def dbConnection(host, port, user, password, database):
    # Establish a connection to the database
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    
    return connection

def readDoctorAvailability(df_availability):
    columns = df_availability.columns.tolist()[1:]
    available_times_raw  = []
    for col in columns:
        if  df_availability[col].astype('int').iloc[0]== 1:
            available_times_raw.append(col)
        
    return available_times_raw


def getAvailability(availability_raw):
    availability = []
    for appointment in availability_raw:
        availability.append(digits_to_text[appointment])
    return ', '.join(availability)

def readDbAvailability(doctor_id, todays_date, connection):
    try:
        query = f"SELECT * FROM {todays_date} WHERE Id_Doc = {doctor_id}"
        
        df_availability = pd.read_sql(query, connection)
        # get the raw availability
        availability_raw = readDoctorAvailability(df_availability)
        # convert the raw availability to text format
        availability = getAvailability(availability_raw)
        
        return availability

    except pymysql.Error as e:
        print("Error:", e)

def handler():
    # Database connection parameters 
    host = '127.0.0.1'
    user = 'root'
    password = 'qwertyuiop321!'
    database = 'med_app'
    port = 3306
    # Create a connection to the db
    connection = dbConnection(host, port, user, password, database)
    
    # Read medical appointments availability for doctor_id = 1 (supposedly we are checking for 1 single doctor)
    doctor_id = 1
    # Suppose we need to check for a specific date (format the date to be in MM_DD_YYYY)
    todays_date = '09_03_2023'
    availability =  readDbAvailability(doctor_id, todays_date, connection)
    
    answer = 'Pentru cardiologie, avem disponibile următoarele intervale: '
    final_answer = answer + availability
    
    return final_answer


if __name__ == '__main__':
    handler()