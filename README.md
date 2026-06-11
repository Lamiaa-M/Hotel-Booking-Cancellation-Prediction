# Hotel Booking Cancellation Prediction

Final Data Science Project — an interactive **dashboard + ML model** that predicts whether a hotel booking will be **canceled**, using real Property-Management-System data from two Portuguese hotels.

> *Completed as part of the [Epsilon AI](https://github.com/Epsilon-AI) Data Science program.*
> *Main Epsilon AI repo: https://github.com/Epsilon-AI*

---

##  Problem statement

> **Can we predict, at booking time, whether a reservation will be canceled (`is_canceled`)?**

A binary classification problem evaluated with **precision and recall**.

---

## Dataset

- **Source:** [Kaggle — mojtaba142/hotel-booking](https://www.kaggle.com/datasets/mojtaba142/hotel-booking) (~119,390 rows × 36 columns)
- **Dirty by design:** missing values, `"Undefined"` categories, `adr` outliers, zero-guest rows, duplicates, and target-leakage columns — all handled in the notebook.

Download `hotel_booking.csv` and place it in the project root.

---

## Project structure

```
.
├── Hotel_Cancellation_Prediction.ipynb   # full analysis notebook
├── Home.py                               # dashboard landing (app entry point)
├── pages/
│   ├── 1_Analysis.py                     #  Analysis page — Q1–Q8 EDA charts
│   └── 2_ML_Model.py                     #  ML Model page — live predictor
├── .streamlit/
│   └── config.toml                       # teal theme
├── requirements.txt
├── hotel_booking.csv                     # raw dataset (download from Kaggle)
├── hotel_booking_clean.csv               # produced by the notebook
├── hotel_cancellation_model.pkl          # saved model (produced by notebook)
├── preprocessor.pkl                      # saved transformer (produced by notebook)
├── feature_columns.pkl                   # saved feature order (produced by notebook)
└── README.md
```

---

##  How to run

```bash
pip install -r requirements.txt        # 1. install deps
# 2. run the notebook to produce the .pkl files + hotel_booking_clean.csv
streamlit run Home.py                  # 3. launch the dashboard
```

The dashboard has **two pages** in the sidebar:
- ** Analysis** — eight business questions (Q1–Q8) answered with interactive charts.
- ** ML Model** — enter a booking's details and get its cancellation probability on a live gauge.

### Deploy online (free)
Push to GitHub → [share.streamlit.io]([https://share.streamlit.io](https://hotel-booking-cancellation-prediction-6exr9x2wtdeh4jxz6oyuat.streamlit.app/)) → connect the repo → set **`Home.py`** as the entry point → paste the public link into your submission.

---

##  Notebook contents

Data cleaning (documented) → feature engineering → EDA (8 business questions, Plotly) → 3 model **pipelines** compared with cross-validation → **class-imbalance handling (SMOTE / SMOTE-Tomek)** → GridSearchCV tuning → validation (train-vs-test cross-validation) → evaluation (precision, recall, F1, ROC-AUC) → embedded feature selection → saved artifacts.


