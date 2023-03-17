from motor import motor_asyncio

# The "dnspython" module must be installed to use mongodb+srv:// URIs
class ConnectMongo:
    def __init__(self, url=None):
        self.client = None

        if url is not None:
            self.init_db(url)
    
    def init_db(self, url=None): 
        if url is not None:
            c = motor_asyncio.AsyncIOMotorClient(url)
            self.client = c
        else:
            raise ValueError(
                "You must specify a MONGO URI",
            )

cnct = ConnectMongo()