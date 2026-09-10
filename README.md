# AI-Based Emergency Medical Assistance and Rapid Response System

This is a beginner-friendly full-stack Flask project for a college-level AI and Data Science demonstration. It helps elderly people, people living alone, and patients who may need quick medical assistance in an emergency.

## Important safety note

This application is a prototype for emergency assistance and does not replace professional medical advice or emergency services. In a real emergency, contact your local emergency number.

The AI model is for educational demonstration only and should not be used for medical diagnosis.

## Features

- User registration and login
- Role-based access using Flask sessions
- User dashboard with emergency button
- Browser geolocation support
- Simulated emergency alert workflow for demo mode
- SQLite database with SQLAlchemy
- Emergency contacts management
- Medical profile management
- Symptom assessment using a simple scikit-learn model
- Emergency history page
- Admin responder dashboard with emergency status updates
- Simulated ambulance dispatch workflow
- Map link using Google Maps / OpenStreetMap format

## Technology stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite + SQLAlchemy
- AI/ML: scikit-learn, pandas, numpy, joblib
- Security: Werkzeug password hashing
- Demo SMS: simulated service abstraction

## Project structure

```text
emergency_medical_app/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── models/
│   ├── __init__.py
│   └── models.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── user.py
│   ├── emergency.py
│   ├── symptoms.py
│   └── admin.py
├── services/
│   ├── __init__.py
│   ├── sms_service.py
│   ├── location_service.py
│   └── ambulance_service.py
├── ml_model/
│   ├── dataset.csv
│   ├── train_model.py
│   ├── predict.py
│   └── emergency_model.pkl
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── emergency.html
│   ├── symptoms.html
│   ├── contacts.html
│   ├── medical_profile.html
│   ├── history.html
│   ├── profile.html
│   └── admin/
│       ├── dashboard.html
│       ├── emergencies.html
│       ├── emergency_details.html
│       └── users.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   ├── emergency.js
│   │   └── location.js
│   └── images/
├── instance/
│   └── emergency.db
└── .venv/
```

## Installation on Windows (VS Code)

Open the project folder in VS Code terminal.

```bat
cd emergency_medical_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Database initialization

The database is created automatically when the app starts.

## Train the AI model

```bat
python ml_model/train_model.py
```

This script loads the sample dataset, trains a RandomForestClassifier, evaluates accuracy, and saves the model as `ml_model/emergency_model.pkl`.

## Run the application

```bat
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Demo login

Default admin account:

- Username: admin
- Password: admin123

You can also register a normal user account from the registration page.

## How the emergency workflow works

1. The user logs in and reaches the dashboard.
2. The user clicks the large red emergency button.
3. A confirmation dialog appears.
4. The browser asks for location permission.
5. Latitude and longitude are captured.
6. A Google Maps link is generated.
7. An emergency record is stored in SQLite.
8. The app simulates sending alerts to the user’s emergency contacts.
9. A simulated ambulance request is created.
10. The admin can view and update ambulance status from the admin dashboard.

## How the AI model works

The model uses symptoms such as chest pain, shortness of breath, dizziness, fever, and confusion. The project uses a simple RandomForestClassifier.

This is only an educational demo and not a real medical diagnostic tool.

## Configure real SMS later

The app already contains a service abstraction in `services/sms_service.py`. To add a real SMS provider such as Twilio later:

1. Replace the demo sender with an API client.
2. Add credentials in `.env`.
3. Update the `send_alert` method in the SMS service.

## Safety limitations

- This app is not a medical diagnosis system.
- It does not replace emergency services.
- In a real emergency, always contact the local emergency number.
- The ambulance workflow is simulated for the prototype.

## Troubleshooting

If the model file is missing, run:

```bat
python ml_model/train_model.py
```

If the database is not initialized, restart the app and it will create the SQLite tables automatically.

## License

This project is meant for learning and college demonstration purposes.
