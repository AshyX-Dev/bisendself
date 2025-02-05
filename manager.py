from interface import Session, Dict, Union, json
import sqlite3
import time

class BisendDatabaseManager(object):
    def __init__(self):
        self.bisend = sqlite3.connect("session.bss", check_same_thread=False)
        self.setup()

    def setup(self):
        self.bisend.execute(
            """
            CREATE TABLE IF NOT EXISTS session (
                sid INTEGER PRIMARY KEY,
                uptime TEXT,
                locks TEXT,
                alpha_range INTEGER
            )
            """
        )

        pre_session = self.getManagerProperty()
        if pre_session['status'] != "OK":
            self.bisend.execute(
                """
                INSERT INTO session ( sid, uptime, locks, alpha_range ) VALUES ( ?, ?, ?, ? )
                """,
                (
                    0,
                    time.ctime(time.time()),
                    "[]",
                    10
                )
            )

    def getManagerProperty(self) -> Dict[str, Union[str, Session]]:
        sessions = self.bisend.execute("SELECT * FROM session")
        for session in sessions.fetchall():
            session = Session(session)
            if session.exists:
                return { "status": "OK", "session": session }
            
        return { "status": "CANNOT_GET_MANAGER", "session": Session() }

    def addLock(
        self,
        uid: int
    ):
        
        manager = self.getManagerProperty()
        if manager['status'] == "OK":
            if not uid in manager['session'].locks:
                manager['session'].locks.append(uid)
                self.bisend.execute("UPDATE session SET locks = ? WHERE id = ?", (
                    json.dumps(
                        manager['session'].locks
                    ),
                    0
                ))
                self.bisend.commit()

                return { "status": "OK" }
            
            else: return { "status": "USER_ALREADY_LOCKED" }
        
        else: return { "status": manager['status'] }

    def removeLock(
        self,
        uid: int
    ):
        
        manager = self.getManagerProperty()
        if manager['status'] == "OK":
            if uid in manager['session'].locks:
                manager['session'].locks.remove(uid)
                self.bisend.execute("UPDATE session SET locks = ? WHERE id = ?", (
                    json.dumps(
                        manager['session'].locks
                    ),
                    0
                ))
                self.bisend.commit()

                return { "status": "OK" }
            
            else: return { "status": "USER_NOT_LOCKED" }
        
        else: return { "status": manager['status'] }

    def setAlphaRange(
        self,
        arange: int = 10
    ):
        
        manager = self.getManagerProperty()
        if manager['status'] == "OK":
            self.bisend.execute("UPDATE session SET locks = ? WHERE id = ?", (
                arange,
                0
            ))
            self.bisend.commit()

            return { "status": "OK" }
        
        else: return { "status": manager['status'] }
