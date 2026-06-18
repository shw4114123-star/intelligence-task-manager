from database.db_connection import DBconnection
from database.validations import Checkagentdata


class AgentDB():
    def __init__(self):
        self.agent = DBconnection()

    def create_agent(self, data: Checkagentdata):
        try:
            cursor = self.agent.get_connection().cursor()
            cursor.execute("""
                    insert into agents (
                        name, specialty, is_active, completed_missions,
                            failed_missions, agent_rank) values (%s, %s, %s, %s, %s, %s)
                    """, (data.name, data.specialty, True, 0, 0, "Junior")
                    )
            cursor._connection.commit()
            cursor.close()
        except Exception as e:
            raise Exception(f"the error is: {e}")

    def get_all_agents(self):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from agents
                    """)
            all = cursor.fetchall()
            return all
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def get_agent_by_id(self, id):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    select * from agents
                        where id = %s
                    """, (id,)
                    )
            agent = cursor.fetchone()
            return agent
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()
        
    
    def update_agent(self, id, data: Checkagentdata):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update agents set 
                        name = %s,
                        specialty = %s,
                        is_active = %s,
                        completed_missions = %s, 
                        failed_missions = %s,
                        agent_rank = %s
                    where id = %s
                    """, (data.name, data.specialty, data.is_active, data.completed_missions,
                        data.failed_missions, data.agent_rank, id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def deactivate_agent(self, id):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update agents set 
                        is_active = %s
                    where id = %s
                    """, (False, id)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def ncrement_completed(self, id):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update agents set
                        completed_missions = completed_missions + 1
                    where id = %s
                    """, (id,)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def increment_failed(self, id):
        try:
            cursor = self.agent.get_connection().cursor(dictionary=True)
            cursor.execute("""
                    update agents set
                        failed_missions = failed_missions + 1
                    where id = %s
                    """, (id,)
                    )
            cursor._connection.commit()
            return True
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def get_agent_performance(self, id):
        try:
            cursor = self.agent.get_connection().cursor()
            cursor.execute("""
                    select completed_missions, failed_missions from agents where id = %s
                    """, (id,)
                    )
            a = cursor.fetchone()
            total = a[0] + a[1]
            success_rate = (a[0] / total) * 100
            return {"completed" : a[0], "failed" : a[1], 
                    "total": total, "success_rate" : success_rate}
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()
    
    def count_active_agents(self):
        try:
            cursor = self.agent.get_connection().cursor()
            cursor.execute("""
                    select count(*) from agents
                        where is_active = True 
                    """)
            a = cursor.fetchone()
            return a[0]
        except Exception as e:
            raise Exception(f"the error is: {e}")
        finally:
            cursor.close()

    def check_agent_exists(self, agent_id: int):
        cursor = self.agent.get_connection().cursor(dictionary=True)
        cursor.execute("""
                select id from agents 
                where id = %s
                """, (agent_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        return False
