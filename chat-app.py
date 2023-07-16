from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# Initialize Firebase app
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-project.firebaseio.com'
})


