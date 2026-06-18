from database.db_connection import DBconnection
from database.validations import Checkmissionsdata, check_risk_level


class MissionDB():
    def __init__(self):
        self.mission = DBconnection()

    def create_mission(self, data :Checkmissionsdata):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            level = check_risk_level(data.difficulty, data.importance)
            cursor.execute("""
                    insert into missions (
                        title, description, location, difficulty,
                        importance, status, risk_level, assigned_agent_id)
                    values (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (data.title, data.description, data.location, data.difficulty, data.importance, "NEW", level, None)
                    )
            cursor._connection.commit()
            cursor.close()
        except Exception as e:
            raise Exception(f"the error is: {e}")

    def get_all_missions(self):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from missions
                    """)
            mission = cursor.fetchall()
            return mission
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()       

    def get_mission_by_id(self, id):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from missions
                        where id = %s
                    """, (id,)
                    )
            mission = cursor.fetchone()
            return mission
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close() 

    def assign_mission(self, mission_id, agent_id):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update missions set 
                        assigned_agent_id = %s
                    where id = %s
                    """, (agent_id, mission_id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def update_mission_status(self, id, status):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update missions set
                        status = %s
                    where id = %s
                    """, (status, id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def get_open_missions_by_agent(self, id):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from missions 
                    where status = "ASSIGNED" or status = "IN_PROGRESS"
                    having assigned_agent_id = %s
                    """, (id,)
                    )
            open_mission_by_agent = cursor.fetchall()
            return open_mission_by_agent
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def count_all_missions(self):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from missions
                    """)
            count = cursor.fetchone()
            return count
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def count_by_status(self, status):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from missions
                        where status = %s
                    """, (status,)
                    )
            count = cursor.fetchone()
            return count
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def count_open_missions(self):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select count(*) from missions 
                    where status = "ASSIGNED" or status = "IN_PROGRESS" or status = "NEW"
                    """)
            open_mission = cursor.fetchone()
            return open_mission
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def count_critical_missions(self):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from missions
                        where risk_level = %s
                    """, ("CRITICAL",)
                    )
            count = cursor.fetchone()
            return count
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def get_top_agent(self):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from agents
                        order by completed_missions desc
                        limit 1
                    """)
            top_agent = cursor.fetchone()
            return top_agent
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def check_mission_exists(self, mission_id: int):
        cursor = self.mission.get_connection().cursor(dictionary=True)
        cursor.execute("""
                select id from missions 
                where id = %s
                """, (mission_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        return False