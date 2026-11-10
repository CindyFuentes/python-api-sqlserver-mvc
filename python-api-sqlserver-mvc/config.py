import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY=os.getenv("SECRET_KEY","change-this-key")
    DEBUG=os.getenv("FLASK_DEBUG","false").lower()=="true"
    API_URL=os.getenv("API_URL","https://www.datos.gov.co/api/v3/views/2fsd-7enq/query.json")
    SQL_SERVER=os.getenv("SQL_SERVER",r"localhost\SQLEXPRESS")
    SQL_DATABASE=os.getenv("SQL_DATABASE","AtlanticoTuristico")
    SQL_DRIVER=os.getenv("SQL_DRIVER","ODBC Driver 18 for SQL Server")
    SQL_TRUSTED=os.getenv("SQL_TRUSTED_CONNECTION","true").lower()=="true"
    SQL_USERNAME=os.getenv("SQL_USERNAME","")
    SQL_PASSWORD=os.getenv("SQL_PASSWORD","")
