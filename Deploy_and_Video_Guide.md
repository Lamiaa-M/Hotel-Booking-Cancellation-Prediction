# Deployment Guide + Video Script

Everything you need to finish the last steps: get the app live, then record the video.

---

## PART A — Run the notebook to generate artifacts

Before deploying, the `.pkl` files must exist. On your machine:

1. Download `hotel_booking.csv` from Kaggle (mojtaba142/hotel-booking) into the project folder.
2. `pip install -r requirements.txt`
3. Open `Hotel_Cancellation_Prediction.ipynb` and **Run All**.
4. Confirm these files were created: `hotel_cancellation_model.pkl`, `preprocessor.pkl`, `feature_columns.pkl`, `hotel_booking_clean.csv`.
5. Test locally: `streamlit run Home.py` — the dashboard and Prediction page should both work.

---

## PART B — Deploy to Streamlit Community Cloud (free)

### B1. Put the project on GitHub
```bash
cd your-project-folder
git init
git add .
git commit -m "Hotel booking cancellation prediction"
git branch -M main
git remote add origin https://github.com/<your-username>/hotel-cancellation.git
git push -u origin main
```
Make sure the repo contains: `Home.py`, `pages/1_Prediction.py`, `.streamlit/config.toml`, `requirements.txt`, the `.pkl` files, `hotel_booking_clean.csv`, the notebook, and `README.md`.

> If `hotel_booking.csv` is too large for GitHub (>100 MB it will be rejected; this file is ~10 MB so it's fine), you can leave the raw CSV out and keep only the cleaned one — the app only needs `hotel_booking_clean.csv` and the `.pkl` files.

### B2. Deploy
1. Go to **https://share.streamlit.io** and sign in with GitHub.
2. Click **New app** → select your repo and the `main` branch.
3. Set **Main file path** to `Home.py`.
4. Click **Deploy**. Wait ~2–3 minutes for it to build.
5. Copy the public URL (looks like `https://<your-app>.streamlit.app`).

### B3. Update the presentation
Paste that URL into **slide 10** of the PPTX, and replace the representative metrics on **slide 9** with your real numbers from the notebook run.

---

## PART C — Video script (aim for 5–8 minutes)

Record your screen walking through the project. Suggested flow:

**1. Intro (30s)**
> "Hi, I'm [name]. This is my Epsilon AI final project: predicting hotel booking cancellations. I chose the Hotel Booking Demand dataset — 119,000 real bookings from two Portuguese hotels — and the goal is to predict, at booking time, whether a reservation will be canceled."

**2. The data & the problem (45s)**
- Show the dataset / the proposal.
- Explain why it's a real problem (cancellations cost revenue) and that ~37% of bookings cancel.

**3. Data cleaning (1.5 min)** — *the most graded part*
- Open the notebook's cleaning section. Walk through 3–4 concrete steps: dropping leakage columns, filling missing values, recoding `"Undefined"`, removing zero-guest/outlier rows.
- Emphasise: "every change is documented."

**4. EDA insights (1 min)**
- Show 2–3 plots. Call out the findings: longer lead time → more cancellations; non-refundable deposits cancel almost always; more special requests → fewer cancellations.

**5. Feature engineering (30s)**
- Mention the four new features and why each helps.

**6. Modeling (1.5 min)**
- Show the 3-model comparison table.
- Explain GridSearchCV tuning and why tuning matters.
- Show the train-vs-test cross-validation scores (proves no overfitting).
- Show final precision and recall, and that both clear the 0.3 requirement.

**7. Deployment demo (1 min)**
- Open your live Streamlit app.
- On the dashboard page, point to the stats and charts.
- On the Prediction page, enter a booking, hit predict, and show the probability gauge.

**8. Close (15s)**
> "All the code, the notebook, and the deployed app are in my GitHub repo, which references the main Epsilon AI repository. Thanks for watching."

### Recording tips
- Use OBS Studio, Loom, or even PowerPoint's "Record" — all free.
- Do a 1-minute dry run first; keep the pace steady.
- Have the notebook **already run** (outputs visible) so you don't wait on cells.

---

## Final submission checklist
- [ ] Notebook (run, with visible outputs)
- [ ] `Home.py` + `pages/` dashboard, deployed, URL noted
- [ ] Dataset + `preprocessor.pkl` + `model.pkl`
- [ ] PPTX (slides 9 & 10 updated)
- [ ] Dataset proposal
- [ ] Video
- [ ] GitHub repo, mentioning the main Epsilon AI repo
