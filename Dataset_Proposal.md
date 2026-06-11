# Dataset Proposal — Final Data Science Project

**Student:** _[your name]_
**Course:** Epsilon AI — Data Science
**Date:** _[date]_

---

## 1. Chosen dataset

| | |
|---|---|
| **Name** | Hotel Booking Demand |
| **Source** | Kaggle — `mojtaba142/hotel-booking` |
| **Link** | https://www.kaggle.com/datasets/mojtaba142/hotel-booking |
| **Size** | 119,390 rows × 36 columns |
| **Domain** | Hospitality (hotels) |
| **Target** | `is_canceled` (0 = honored, 1 = canceled) — binary classification |

## 2. Description

The dataset contains real booking records from two hotels in Portugal — a **City Hotel** and a **Resort Hotel** — collected from their Property-Management-System between **July 2015 and August 2017**. Each row is a single booking and includes information known at the time of reservation: lead time, arrival date, length of stay, number of guests, meal plan, market segment, distribution channel, deposit type, customer history (previous cancellations, repeated guest), room type, average daily rate (`adr`), special requests, and more.

The original academic source is Antonio, Almeida & Nunes (2019), *"Hotel booking demand datasets"*, Data in Brief. This Kaggle version adds four extra (synthetic) identifier columns.

## 3. Why it simulates a real-time business problem

Booking cancellations directly reduce hotel revenue, distort demand forecasts, and complicate staffing and overbooking decisions. The goal is to predict — **at the moment a booking is made** — whether it is likely to be canceled, so the revenue manager can act (request deposits, adjust overbooking buffers, target retention offers). About **37% of bookings in the data are canceled**, so this is a meaningful, high-impact, real-world problem.

## 4. Proof that the dataset is NOT clean

This dataset requires substantial cleaning, which is the graded "data cleaning" component. The specific issues:

| # | Issue | Evidence / detail |
|---|---|---|
| 1 | **Missing values** | `children`, `country`, `agent`, and `company` all contain nulls. `company` is ~94% missing; `agent` has thousands of nulls. |
| 2 | **`"Undefined"` categories** | `meal`, `market_segment`, and `distribution_channel` contain an `"Undefined"` label that behaves like missing data and must be recoded. |
| 3 | **Invalid numeric values** | `adr` (average daily rate) contains negative values and an extreme outlier above 5,000. |
| 4 | **Impossible records** | Some bookings have `adults + children + babies = 0` — a reservation with zero guests. |
| 5 | **Duplicate rows** | The dataset contains exact duplicate bookings. |
| 6 | **Wrong data types** | `children`, `agent`, and `company` are stored as floats but represent integer counts/IDs. |
| 7 | **Non-predictive / leakage columns** | Synthetic identifier columns (`name`, `email`, `phone-number`, `credit_card`) carry no signal, and `reservation_status` / `reservation_status_date` directly leak the target and must be removed. |

Each of these is documented and handled step-by-step in the project notebook.

## 5. How it matches the recommended-dataset requirements

| Requirement | Recommended | This dataset |
|---|---|---|
| Number of rows | large | 119,390 ✅ |
| Number of columns | ≥ ~10 | 36 ✅ |
| Quality | must be uncleaned | confirmed dirty (see §4) ✅ |
| Simulates a real-time problem | required | cancellation prediction ✅ |

## 6. Planned approach

Clean the data → engineer features (`total_nights`, `total_guests`, `is_family`, `room_changed`) → exploratory analysis → compare three classifiers (Logistic Regression, Random Forest, Gradient Boosting) → tune the best with GridSearchCV → evaluate with **precision and recall** → deploy as an interactive Streamlit dashboard.

---

*Note: this is a dataset I selected and proposed independently (not picked directly from the provided list), in line with the project guidelines.*
