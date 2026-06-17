import db_connection
from validations import Checkmissionsdata, risk_level


class MissionDB():
    def __init__(self):
        self.mission = db_connection.DBconnection()

    def create_mission(self, data :Checkmissionsdata):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            level = risk_level(data.difficulty, data.importance)
            cursor.execute("""
                    insert intu missions (
                        title, description, location, difficulty,
                        importance, status, risk_level, assigned_agent_id)
                    values (%s, %s, %s, %s, %s, %s, %s)
                    """, (data.title, data.description, data.location, data.difficulty, data.importance, "NEW", level, None)
                    )
            cursor._connection.commit()
            mission = self.get_all_missions()
            return mission[-1]
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close() 

    def get_all_missions(self):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from missions
                    """)
            mission = cursor.fetchall()
            return mission
        except Exception as e:
            return f"the error is: {e}"
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
            mission = cursor.fetchall()
            return mission
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close() 

    def assign_mission(self, mission_id, agent_id):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update mission set 
                        assigned_agent_id = %s
                    where id = %s
                    """, (agent_id, mission_id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close()

    def update_mission_status(self, id, status):
        try:
            cursor = self.mission.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update mission set
                        status = %s
                    where id = %s
                    """, (status, id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            return f"the error is: {e}"
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
            return f"the error is: {e}"
        finally:
            cursor.close()

    def count_all_missions(self):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from mission
                    """)
            count = cursor.fetchone()
            return count
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close()

    def count_by_status(self, status):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from mission
                        where status = %s
                    """, (status,)
                    )
            count = cursor.fetchone()
            return count
        except Exception as e:
            return f"the error is: {e}"
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
            return f"the error is: {e}"
        finally:
            cursor.close()

    def count_critical_missions(self):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select count(*) from mission
                        where risk_level = %s
                    """, ("CRITICAL",)
                    )
            count = cursor.fetchone()
            return count
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close()

    def get_top_agent(self):
        try:
            cursor = self.mission.get_connection().cursor()
            cursor.execute("""
                    select * from agents
                        order by completed_missions desc
                        limit 1
                    """)
            top_agent = cursor.fetchone()
            return top_agent
        except Exception as e:
            return f"the error is: {e}"
        finally:
            cursor.close()