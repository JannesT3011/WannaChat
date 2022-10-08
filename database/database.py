import motor.motor_asyncio as motor
from datetime import datetime
from config import CONNECTION, CLUSTER, DB, QUEUEDB, GCSERVERDB, EMBED_COLOR

class DbClient:
    """CREATES A CONNECTION TO YOUR DATABASE"""
    def __init__(self):
        cluster = motor.AsyncIOMotorClient(CONNECTION)
        db = cluster[CLUSTER]
        self.collection = db[DB]
        self.queuecollection = db[QUEUEDB]
        self.gcserverscollection = db[GCSERVERDB]

    def __call__(self, *args, **kwargs):
        return self.collection

class Database(DbClient):
    """EXECUTE DATABASE STUFF"""
    async def init_db(self, userid: str):
        """INSERT DOCUMENT"""
        try:
            await self.collection.insert_one(db_layout(userid))
            return
        except:
            raise

    async def delete_db(self, userid: str):
        """DELETE DOCUMENT"""
        try:
            await self.collection.delete_one({"_id": userid})
            return
        except:
            raise

def db_layout(userid: str) -> dict:
    """DEFAULT DATABASE LAYOUT"""
    default_data = {"_id": userid,
                    "age": "-",
                    "language": ["english"],
                    "aboutme": "",
                    "interests": [],
                    "gender": "-",
                    "liked_users": [],
                    "disliked_users": [],
                    "liked_by": [],
                    "color": EMBED_COLOR,
                    "xp": 0,
                    "coins": 0,
                    "emojis": [],
                    "gif": None,
                    "premium": 0,
                    "server_join": str(datetime.utcnow()),
                    }

    return default_data