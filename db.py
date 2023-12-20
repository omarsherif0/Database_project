from pymongo import MongoClient
from db_operations_ import Operations
class Database:
    def get_collection(self,collection_name):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb+srv://Omarsherif:Omar01550012774@cluster0.jygrnfl.mongodb.net/?retryWrites=true&w=majority"
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        dbname = client['Tourism_Database']
        #collection = dbname[collection_name]
        return dbname[collection_name]

  
if __name__ == "__main__":
    dbname = Database()
    collection = dbname.get_collection('Tour')
    operation = Operations()
    document = operation.Read(collection)
    print(document)