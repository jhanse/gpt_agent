# Antibiotic Concentration Dashboard

This simple Flask application lets users upload CSV files containing antibiotic concentration measurements and dose information.
After uploading, the app displays a line plot of concentration over time with dose markers.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the development server:

```bash
python app.py
```

Then open `http://localhost:5000` in your browser and upload a CSV file with the columns `time`, `concentration`, and `dose`.
