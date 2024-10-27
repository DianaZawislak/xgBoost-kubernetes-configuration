from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import sys

def test_sharded_mongo_connection():
    """Test connection to sharded MongoDB cluster"""
    try:
        # Connect to MongoDB
        uri = "mongodb://monitoringUser:XZ53GQm9XRxs@10.108.0.15:27017/rentals"
        print(f"Attempting to connect to MongoDB...")
        
        client = MongoClient(uri,
                           serverSelectionTimeoutMS=5000,
                           connectTimeoutMS=2000)
        
        # Test connection
        print("Testing connection...")
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB")
        
        # Test database access
        db = client.rentals
        print("\nTesting database access...")
        print(f"✓ Successfully accessed database")
        
        # Test collection
        collection = db.zip_33131
        print("\nTesting collection access...")
        count = collection.count_documents({})
        print(f"✓ Collection has {count} documents")
        
        # Test query
        print("\nTesting query...")
        doc = collection.find_one()
        if doc:
            print("✓ Successfully retrieved a document")
            print(f"Sample document keys: {list(doc.keys())}")
        
    except ConnectionFailure as e:
        print(f"Connection Error: {e}")
        sys.exit(1)
    except OperationFailure as e:
        print(f"Authentication Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_sharded_mongo_connection()