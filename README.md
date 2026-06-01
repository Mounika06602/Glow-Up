# GlowUp FastAPI Backend (AI Dermatology Platform)

This is the backend API for **GlowUp**, an AI Dermatology Platform that provides beauty product reviews and skin analysis for all skin types.

## Features
- **Skin Analysis Pipeline (Advanced ML Architecture):**
  - **Face Detection:** Primary detection powered by **MediaPipe**, with **OpenCV Haar** cascades acting as a robust fallback detector.
  - **SkinSegmentationModel:** Uses BiSeNet / U-Net / DeepLabV3+ for precise facial mapping.
  - **SkinToneEstimator:** Combines LAB + HSV with a calibrated ML classifier.
  - **OilinessDrynessAnalyzer:** Uses computer vision heuristics and a lightweight classifier.
  - **SensitivityRednessAnalyzer:** Redness and irritation visual indicator model.
  - **Acne Detection & Heatmap:** Employs **YOLOv8** and **YOLOv9** object detection to generate accurate acne severity reports and visual heatmaps.
  - **QuestionnaireFusionModel:** Fuses visual data with questionnaire inputs using XGBoost / RandomForest / LightGBM.
- **LLM-Powered Chatbot:** An integrated AI chatbot that answers questions regarding skin types and recommends suitable beauty products tailored to those skin types.
- **Local Storage:** Automatically saves uploaded images and generated heatmaps locally.
- **REST API:** Fully functional FastAPI endpoints (`/api/scan`, `/api/health`).

## Prerequisites
- Python 3.9+
- Virtual Environment

## Installation

1. **Clone the repository or navigate to the project directory:**
   ```bash
   cd "glow up fastapi"
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory (using the template provided in your project) to configure your database and storage credentials.

## Running the Application

To start the FastAPI server with auto-reload enabled:
```bash
uvicorn app.main:app --reload
```

## API Documentation
Once the server is running, you can explore and test the API using the interactive Swagger documentation:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure
```text
glow up fastapi/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   └── scan.py
│   │   └── main_router.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── schemas/
│   │   └── analysis.py
│   ├── services/
│   │   ├── image_validator.py
│   │   ├── pipeline.py
│   │   └── storage.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```
