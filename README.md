# Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application  
**Django REST Framework · React · PyQt5 · Pandas · SQLite**

---

## 1. Overview

The Chemical Equipment Parameter Visualizer is a hybrid analytics platform that processes CSV files containing chemical equipment information and generates:

- Statistical summaries  
- Equipment-type distribution charts  
- Structured analytical insights  
- Downloadable PDF reports  

Both the **web client (React)** and **desktop client (PyQt5)** consume a shared **Django REST API**, ensuring consistency and centralized data handling.  
The project demonstrates full-stack API design, desktop integration, and modern UI/UX principles.

### Screenshots
<img width="1878" height="872" alt="image" src="https://github.com/user-attachments/assets/34ee58b4-73a0-4f56-909b-950322230295" />
<img width="1218" height="765" alt="image" src="https://github.com/user-attachments/assets/f7eac680-3ed4-4b2f-8217-aa3c72143353" />
<img width="670" height="770" alt="image" src="https://github.com/user-attachments/assets/02b8ff79-5be3-421d-936b-d56d50873916" />
<img width="1428" height="952" alt="image" src="https://github.com/user-attachments/assets/0f706db9-4b9e-412d-b5bb-01609dac4d67" />



---

## 2. System Architecture

    Backend (Django REST API)
    │
    ├── CSV Processing (Pandas)
    ├── Statistical Summary Generation
    ├── PDF Report Builder
    ├── SQLite Database (Last 5 datasets)
    │
    ├── Web Client (React + Chart.js)
    │ ├── CSV Upload
    │ ├── Dataset History View
    │ ├── Inline Analytics Section
    │ └── Bar Charts Visualization
    │
    └── Desktop Client (PyQt5 + Matplotlib)
    ├── CSV Upload
    ├── Structured Summary Viewer
    └── Chart Visualization


---

## 3. Technology Stack

### Backend
- Python  
- Django  
- Django REST Framework  
- Pandas  
- ReportLab  
- SQLite  

### Web Client
- React.js  
- Chart.js  
- Fetch API  

### Desktop Client
- PyQt5  
- Matplotlib  
- Requests  

---

## 4. Key Features

### Backend
- CSV upload REST endpoint  
- Automatic CSV parsing  
- Summary and distribution computation  
- PDF report generation  
- Retains last five datasets in database  

### Web Frontend
- CSV upload UI  
- Authentication fields  
- Dataset history display  
- Click-to-expand analytics section  
- Chart.js bar chart visualization  
- PDF report viewer  
- Clean professional interface  

### Desktop Client
- CSV upload via native dialog  
- Sidebar-based dashboard layout  
- Structured summary output  
- Matplotlib chart  
- Shared API authentication  

---

## 5. Project Structure
    Chemical Equipment Parameter Visualizer/
    │
    ├── backend/
    │ ├── equipment/
    │ ├── api/
    │ ├── media/reports/
    │ ├── db.sqlite3
    │ └── manage.py
    │
    ├── web-frontend/
    │ ├── src/App.js
    │ ├── package.json
    │ └── public/
    │
    └── desktop-client/
    └── main.py


---

## 6. Setup Instructions

### 6.1 Backend Setup (Django)

```bash
    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```
### 6.2 Web Frontend Setup (React)

    cd web-frontend
    npm install
    npm start

### 6.3 Desktop Application Setup (PyQt5)

    cd desktop-client
    pip install PyQt5 matplotlib requests
    python main.py

### 7. Authentication

The backend uses HTTP Basic Authentication.

Each request must include:

    Authorization: Basic base64(username:password)


Both clients (React + PyQt5) have built-in fields for credentials.

### 8. API Endpoints

Method	Endpoint	Description
  - POST	/api/upload/	Upload a CSV file
  - GET	/api/datasets/	Retrieve last five datasets
  - GET	/api/datasets/<id>/summary/	Get summary for a dataset
  - GET	/media/reports/<file>.pdf	Download PDF report

### 9. Data Insights Generated

### Summary Statistics

- Total equipment count
- Mean Flowrate
- Mean Pressure
- Mean Temperature

### Visualizations

- Bar chart of equipment type distribution (React + Chart.js)
- Matching bar chart in desktop app (PyQt5 + Matplotlib)

### PDF Report Includes

- Uploaded dataset table
- Summary table
- Distribution breakdown
- Clean enhanced layout

### 10. Learning Outcomes

- Designing REST APIs
- Hybrid application architecture
- Data processing with Pandas
- Chart rendering in both web and desktop environments
- Report generation using ReportLab
- Maintaining UI/UX consistency across different platforms

### 11. License

This project is created for evaluation and educational purposes.
