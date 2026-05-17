# marketlens

A small project for market analysis and predictions.

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

- Run the Flask/CLI app:

```powershell
python app.py
```

- Run the Streamlit UI:

```powershell
streamlit run modules/streamlit.py
```

## Files

- `app.py` — application entrypoint
- `modules/` — project modules (data ingestion, preprocessing, models, Streamlit)

## License

This project is licensed under the MIT License. See `LICENSE`."