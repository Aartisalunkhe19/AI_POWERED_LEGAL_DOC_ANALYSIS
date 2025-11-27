import firebase_admin
from firebase_admin import credentials, auth, firestore, storage

# Initialize Firebase
def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Load the Firebase service account key
            cred = credentials.Certificate("firebase_service_account_key.json")  # Replace with your service account key path
            # Initialize Firebase with the credentials and Storage bucket
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'your-storage-bucket-url'  # Replace with your Storage bucket URL
            })
            print("Firebase initialized successfully!")
        else:
            print("Firebase already initialized.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

# Call the function to initialize Firebase
initialize_firebase()

# Firestore client for database operations
db = firestore.client()

# Storage client for file uploads
bucket = storage.bucket()