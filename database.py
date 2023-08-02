import os
import MySQLdb
from dotenv import load_dotenv
from datetime import datetime, timedelta

from scraper.property import Property

# Load environment variables from .env file
load_dotenv()

# Connect to the database using the provided configuration
def get_db_connection():
    connection = MySQLdb.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USERNAME_PS"),
        passwd=os.getenv("PASSWORD_PS"),
        db=os.getenv("DATABASE_PROP"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY"
        #ssl={
        #    "ca": "/etc/ssl/cert.pem"
        #}
    )
    return connection

# Insert a property into the database
def insert_property(property:Property):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO active_properties (url, prop_type, price, currency, expenses, total_area,
                                    covered_area, rooms, bedrooms, bathrooms, address,
                                    neighborhood, garage, page, pics_urls,last_read_date)
    VALUES (%(url)s, %(prop_type)s, %(price)s, %(currency)s, %(expenses)s, %(total_area)s,
            %(covered_area)s, %(rooms)s, %(bedrooms)s, %(bathrooms)s, %(address)s,
            %(neighborhood)s, %(garage)s, %(page)s, %(pics_urls)s, %(last_read_date)s)
    """

    # Convert enums to their string values
    property_data = property.__dict__
    property_data["prop_type"] = property.prop_type.value
    property_data["currency"] = property.currency.value
    property_data["page"] = property.page.value
    property_data["last_read_date"] = datetime.now() - timedelta(days=8)

    cursor.execute(query, property_data)
    connection.commit()

    cursor.close()
    connection.close()

# Get all properties ids and urls from the database
def get_properties():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT property_id,url
    FROM active_properties
    """

    cursor.execute(query)
    properties = cursor.fetchall()

    cursor.close()
    connection.close()

    return properties

# Update the last read date of a property
def update_property_last_read_date(property_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE active_properties
    SET last_read_date = NOW()
    WHERE property_id = %s
    """

    cursor.execute(query, (property_id,))
    connection.commit()

    cursor.close()
    connection.close()

# Delete properties that are no longer active
def delete_inactive_properties():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM active_properties
    WHERE last_read_date <= DATE_SUB(NOW(), INTERVAL 7 DAY)
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()
