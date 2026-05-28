# Smart Campus Lab Web App

This project integrates the lab programs with a simple FastAPI backend and Streamlit frontend.

## Run the API

```powershell
uvicorn backend.main:app --reload
```

## Run the Streamlit App

Open a second terminal:

```powershell
streamlit run app.py
```

All application data is stored in CSV files inside the `backend` folder.
