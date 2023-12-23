class Operations:
    def __init__(self) -> None:
        pass
    def Read(self,collection):
        document_list = [document for document in collection.find()]
        return document_list
    def Update(self,collection):
        document_list = [document for document in collection.find()]
        return document_list
    def Create(self,collection, document_data):
        try:
            collection.insert_one(document_data)
            return 'Success'
        except Exception as e:
            return f'Insertion failed with error: {e}'
    def Delete(self,collection):
        document_list = [document for document in collection.find()]
        return document_list