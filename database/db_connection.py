import mysql.connector

class DBconnection:
    def __init__(self):
        self.config = {
            "host" : "127.0.0.1",
            "port" : 3306,
            "user" : "root",
            "password" : "1234",
        }
        self._connection = None

    def get_connection(self):
        if self._connection:
            self._connection.close()
        self._connection = mysql.connector.connect(**self.config)
        return self._connection
    
    def create_database(self):
        cursor = self.get_connection().cursor()
        cursor.execute("""
                create database if not exists Intelligence_db
                """)
        cursor._connection.commit()
        cursor.close()
        self.config["database"] = "Intelligence_db"

    def create_tables(self):
        cursor = self.get_connection().cursor()
        cursor.execute("""
                create table if not exists agents (
                    id int auto_increment primary key,
                    name varchar(30) not null,
                    specialty varchar(40) not null,
                    is_active boolean default TRUE,
                    completed_missions int default 0,
                    failed_missions int default 0,
                    agent_rank enum("Junior", "Senior", "Commander") not null)
                """)
        
        cursor.execute("""
                create table if not exists missions (
                    id int auto_increment primary key,
                    title varchar(30) not null,
                    description text not null,
                    location varchar(30) not null,
                    difficulty int not null,
                    importance int not null,
                    status varchar(15) default "NEW",
                    risk_level varchar(10) not null,
                    assigned_agent_id int default null)
                    """)
        cursor._connection.commit()
        cursor.close()