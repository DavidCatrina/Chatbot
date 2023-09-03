import pymysql
import datetime
import pandas as pd

# Database connection parameters 
# TODO: change password if needed
host = '127.0.0.1'
user = 'root'
password = 'qwertyuiop321!'
database = 'med_app'
port = 3306

# Read medical appointments availability for doctor_id = 1 (supposedly we are checking for 1 single doctor)
doctor_id = 1

# Suppose we need to check for a specific date (format the date to be in MM_DD_YYYY)
todays_date = '09_03_2023'

answer = 'Pentru cardiologie, avem disponibile următoarele intervale: '

digits_to_text = {
        '9_10': 'nouă zece', 
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
        query = f"SELECT * FROM {todays_date} WHERE Id_Doc = {doctor_id};"
        
        df_availability = pd.read_sql(query, connection)
        # get the raw availability
        availability_raw = readDoctorAvailability(df_availability)
        # convert the raw availability to text format
        availability = getAvailability(availability_raw)
        
        return availability

    except pymysql.Error as e:
        print("Error:", e)
        
        
def checkAppointmentAvailability(question):
    available_times_answer = handler()
    text_to_digits = {value: key for key, value in digits_to_text.items()}
    if question in available_times_answer:
        try:
            time_slot = text_to_digits[question]
            
            connection = dbConnection(host, port, user, password, database)
            cursor = connection.cursor()
            query = f"UPDATE {todays_date} SET {time_slot} = 0 WHERE Id_Doc = {doctor_id};"
            # Execute the query to mark the time slot as booked
            cursor.execute(query)
            # Commit the changes to the database
            connection.commit()           
            return f'Programarea dumneavoastră a fost confirmată pentru ora {question}'
        except:
            return f'A aparut o eroare cand am incercat sa procesam programarea dumneavoastra pentru intervalul {question}. Va rugam încercați din nou !'
    else:
        return 'Acest interval de timp nu este disponibil. Va rugam încercați din nou !'
    

    

def handler():
    # Create a connection to the db
    connection = dbConnection(host, port, user, password, database)
    availability =  readDbAvailability(doctor_id, todays_date, connection)
    final_answer = answer + availability
    return final_answer

if __name__ == '__main__':
    handler()