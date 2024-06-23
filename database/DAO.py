from database.DB_connect import DBConnect
from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(`year`)
                    from teams 
                    where year >= 1980"""
        cursor.execute(query, )
        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSquadre(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select ID, teamCode, name
                    from teams
                    where `year` = %s"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(Team(row['ID'],
                           row['teamCode'],
                           row['name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalari(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.ID , sum(s.salary) as salario 
                    from salaries s , people p , appearances a , teams t
                    where s.playerID = p.playerID and p.playerID = a.playerID and t.ID = a.teamID 
                            and a.year =t.year and t.year = %s 
                    group by t.teamCode"""
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append((row['ID'],
                            row['salario']))

        cursor.close()
        conn.close()
        return result