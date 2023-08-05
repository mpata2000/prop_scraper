import os
import time
import logging
import MySQLdb
from dotenv import load_dotenv

logger = logging.getLogger()

class PropertyDatabase:
    def __init__(self):
        load_dotenv()
        try:
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
        except MySQLdb.Error as e:
            logger.error(f"Error connecting to the database: {e}")

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def query(self, query, data=None):
        try:
            if data is not None:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except MySQLdb.Error as e:
            logger.error(f"Error executing query: {e}")
            return None

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
        property_data["pics_urls"] = ",".join(property.pics_urls)

        self.query(query, property_data)

    def get_properties(self):
        query = """
        SELECT property_id,url
        FROM active_properties
        """

        return self.query(query)

    def update_property_last_read_date(self, property_url):
        query = """
        UPDATE active_properties
        SET last_read_date = NOW()
        WHERE url = %s
        """

        self.query(query, (property_url,))

    def delete_inactive_properties(self):
        query = """
        DELETE FROM active_properties
        WHERE last_read_date <= DATE_SUB(NOW(), INTERVAL 3 DAY)
        """

        deleted = self.query(query)
        return self.cursor.rowcount if deleted is not None else 0
