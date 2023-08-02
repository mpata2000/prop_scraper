import os
import time
import MySQLdb
from dotenv import load_dotenv

class PropertyDatabase:
    def __init__(self):
        load_dotenv()
        self.connection = MySQLdb.connect(
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
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_property(self, property):
        query = """
        INSERT INTO active_properties (url, prop_type, price, currency, expenses, total_area,
                                        covered_area, rooms, bedrooms, bathrooms, address,
                                        neighborhood, garage, page, pics_urls)
        VALUES (%(url)s, %(prop_type)s, %(price)s, %(currency)s, %(expenses)s, %(total_area)s,
                %(covered_area)s, %(rooms)s, %(bedrooms)s, %(bathrooms)s, %(address)s,
                %(neighborhood)s, %(garage)s, %(page)s, %(pics_urls)s)
        """

        # Convert enums to their string values
        property_data = property.__dict__
        property_data["prop_type"] = property.prop_type.value
        property_data["currency"] = property.currency.value
        property_data["page"] = property.page.value

        self.cursor.execute(query, property_data)

    def get_properties(self):
        query = """
        SELECT property_id,url
        FROM active_properties
        """

        self.cursor.execute(query)
        properties = self.cursor.fetchall()

        return properties

    def update_property_last_read_date(self, property_url):
        query = """
        UPDATE active_properties
        SET last_read_date = NOW()
        WHERE url = %s
        """

        self.cursor.execute(query, (property_url,))

    def delete_inactive_properties(self):
        query = """
        DELETE FROM active_properties
        WHERE last_read_date <= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """

        self.cursor.execute(query)
        row_count = self.cursor.rowcount

        return row_count