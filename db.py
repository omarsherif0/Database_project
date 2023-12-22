from pymongo import MongoClient
from bson import json_util, Binary
from db_operations_ import Operations
# from io import BytesIO
# from PIL import Image

class Database:
    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://Omarsherif:Omar01550012774@cluster0.jygrnfl.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.db = self.client['Tourism_Database']

    def get_client(self):
        return self.db

    def get_collection(self, collection_name):
        return self.db[collection_name]

  
if __name__ == "__main__":
    db = Database().get_client()
    collection = db.get_collection('Tour')
    operation = Operations()

    # query = {'Tour_operator': 'Yawan'}

    # with open("E:\\DatabaseProject\\Database_project-1\\static\\images\\post.jpg", "rb") as file:
    #     image_data = file.read()

    # binary_data = Binary(image_data)

    # update_result = collection.update_one(
    #     query,
    #     {"$set": {"image": binary_data}}
    # )

    # if update_result.modified_count > 0:
    #     print("Document updated successfully\n")
    # else:
    #     print("No document was updated\n")

    # Read the updated document
    document = operation.Read(collection)
    print(document)