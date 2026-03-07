# Movie Recommendation System

A content-based movie recommendation system built with Python and FastAPI. It uses Natural Language Processing (NLP) techniques to recommend similar movies based on metadata like genres, keywords, cast, crew, overview, and tagline.

## How It Works

1. **Data Preprocessing** — Merges TMDB 5000 movies and credits datasets, extracts features (genres, keywords, top 3 cast, director), and combines them into a single "tags" column.
2. **Model Training** — Applies stemming, vectorizes tags using `CountVectorizer` (bag-of-words), and computes cosine similarity between all movie pairs.
3. **API** — A FastAPI backend loads precomputed similarity matrix and serves top-5 recommendations for a given movie title, enriched with poster/details from the TMDb API.
4. **Frontend** — A simple HTML page where users type a movie name and get visual recommendation cards.

## Project Structure

```
├── main.py                  # FastAPI app with /recommend endpoint
├── index.html               # Frontend UI
├── requirements.txt         # Python dependencies
├── src/
│   ├── preprocessing.py     # Data cleaning & feature extraction
│   └── model.py             # Vectorization, similarity & pickle export
├── data/
│   ├── preprocessed/        # Raw TMDB CSVs
│   └── processed/           # Cleaned CSVs with tags
├── notebooks/
│   ├── data-preprocessing.ipynb
│   └── model_training.ipynb
├── movies.pkl               # Serialized movie DataFrame
├── similarity.pkl           # Cosine similarity matrix
└── vectorizer.pkl           # Fitted CountVectorizer
```

## Setup

### Prerequisites

- Python 3.10+
- A TMDb API key (already configured in `main.py`)

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd movie-prediction

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Generate Model Artifacts

If `movies.pkl` and `similarity.pkl` are not present, run the preprocessing and model scripts (or the notebooks) first:

```bash
python src/preprocessing.py
python src/model.py
```

### Run the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Use the Frontend

Open `index.html` in a browser (e.g. via Live Server on port 5500). Type a movie name and click **Search** to get recommendations.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/recommend?movie=<title>` | Returns top 5 similar movies with title, overview, rating, and poster |

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **ML/NLP:** scikit-learn (CountVectorizer, cosine similarity), NLTK (Porter Stemmer)
- **Data:** pandas, NumPy
- **Frontend:** Vanilla HTML/CSS/JS
- **External API:** TMDb API for movie posters and details
