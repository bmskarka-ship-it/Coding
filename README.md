# Weather App (Flask + CLI)

Small project demonstrating a Flask web UI for weather lookup and a simple CLI welcome script that fetches current weather using the Open-Meteo APIs.

## Features
- Web frontend served by `app.py` (Flask) using `templates/index.html`.
- API endpoints: `/api/search-cities` and `/api/weather` for city lookup and weather data.
- Simple CLI script `Welcome.py` that prompts for a name and city and prints current weather.

## Prerequisites
- Python 3.8+ installed
- Internet access (uses Open-Meteo geocoding and weather APIs)

## Dependencies
- Flask
- requests

You can install dependencies directly:

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install Flask requests
```

Or create a `requirements.txt` with:

```
Flask
requests
```

and run:

```bash
pip install -r requirements.txt
```

## Run the web app

1. Activate your virtual environment (see above).
2. Start the app:

```bash
python app.py
```

3. Open the browser at `http://127.0.0.1:5000/`.

## Run the CLI script

```bash
python Welcome.py
```

Follow the prompts for your name and city.

## Files
- `app.py` — Flask application, provides frontend and two API endpoints.
- `Welcome.py` — Simple command-line script for greeting and current weather lookup.
- `templates/index.html` — Frontend HTML used by the Flask app.

## Next steps (suggested)
- Add `requirements.txt` for reproducible installs.
- Add error handling and logging for production use.
- Add tests and CI workflow.

---

If you'd like, I can add `requirements.txt` and a simple `.gitignore` next.