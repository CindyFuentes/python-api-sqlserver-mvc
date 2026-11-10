import pyodbc
from flask import current_app
def db():
    c=current_app.config
    s=f"DRIVER={{{c['SQL_DRIVER']}}};SERVER={c['SQL_SERVER']};DATABASE={c['SQL_DATABASE']};Encrypt=yes;TrustServerCertificate=yes;"
    s += "Trusted_Connection=yes;" if c["SQL_TRUSTED"] else f"UID={c['SQL_USERNAME']};PWD={c['SQL_PASSWORD']};"
    return pyodbc.connect(s, timeout=10)
def init_db():
    sql="""
    IF OBJECT_ID('dbo.Municipios','U') IS NULL CREATE TABLE dbo.Municipios(id INT IDENTITY PRIMARY KEY,nombre NVARCHAR(150) UNIQUE NOT NULL,subregion NVARCHAR(150));
    IF OBJECT_ID('dbo.Tipos','U') IS NULL CREATE TABLE dbo.Tipos(id INT IDENTITY PRIMARY KEY,nombre NVARCHAR(150) UNIQUE NOT NULL);
    IF OBJECT_ID('dbo.Atractivos','U') IS NULL CREATE TABLE dbo.Atractivos(id INT IDENTITY PRIMARY KEY,id_api NVARCHAR(100) UNIQUE NULL,municipio_id INT NULL,tipo_id INT NULL,nombre NVARCHAR(300) NOT NULL,ubicacion NVARCHAR(300),descripcion NVARCHAR(MAX),origen NVARCHAR(20) DEFAULT 'LOCAL',fecha_importacion DATETIME2,FOREIGN KEY(municipio_id) REFERENCES dbo.Municipios(id),FOREIGN KEY(tipo_id) REFERENCES dbo.Tipos(id));
    IF OBJECT_ID('dbo.Resenas','U') IS NULL CREATE TABLE dbo.Resenas(id INT IDENTITY PRIMARY KEY,atractivo_id INT NOT NULL,calificacion TINYINT NOT NULL CHECK(calificacion BETWEEN 1 AND 5),comentario NVARCHAR(1000) NOT NULL,fecha DATETIME2 DEFAULT SYSDATETIME(),FOREIGN KEY(atractivo_id) REFERENCES dbo.Atractivos(id) ON DELETE CASCADE);
    """
    with db() as c: c.cursor().execute(sql); c.commit()
