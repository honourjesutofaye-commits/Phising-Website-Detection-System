# Email Training Datasets

These are the labelled email corpora used to train `detector/engine/email_model.joblib`.

Train with:

```
venv\Scripts\python.exe detector\train_multi_csv.py
```

The script reads every `*.csv` in this folder, so adding or removing a file
changes the training data.

## Contents

| File | Rows | Legit (0) | Scam (1) |
|---|---:|---:|---:|
| `CEAS_08.csv` | 39,154 | 17,312 | 21,842 |
| `Enron.csv` | 29,767 | 15,791 | 13,976 |
| `Ling.csv` | 2,859 | 2,401 | 458 |
| `Nazario.csv` | 1,565 | 0 | 1,565 |
| `Nigerian_Fraud.csv` | 3,332 | 0 | 3,332 |
| `SpamAssasin.csv` | 5,809 | 4,091 | 1,718 |
| `phishing_email.csv` | 82,486 | 39,595 | 42,891 |
| **Total** | **164,972** | **79,190** | **85,782** |

Source: the "Phishing Email Dataset" collection on Kaggle, which bundles several
well-known public corpora (CEAS 2008, Enron, Ling-Spam, Nazario's phishing
corpus, a Nigerian fraud/419 collection, and SpamAssassin).

## Format

`label` is required in every file: **0 = legitimate, 1 = phishing/scam**.

Column layouts differ between files, and the training script handles that by
merging whichever of `sender`, `subject`, `body` and `urls` are present into a
single text field:

| Layout | Files |
|---|---|
| `sender, receiver, date, subject, body, label, urls` | `CEAS_08.csv`, `SpamAssasin.csv` |
| `sender, receiver, date, subject, body, urls, label` | `Nazario.csv`, `Nigerian_Fraud.csv` |
| `subject, body, label` | `Enron.csv`, `Ling.csv` |
| `text_combined, label` | `phishing_email.csv` |

> Note: `phishing_email.csv` only has `text_combined`, which is not one of the
> merged columns — so its 82,486 rows currently contribute an empty text field.
> Fixing this means adding `"text_combined"` to the `merge_cols` list in
> `train_multi_csv.py` and retraining.

## How training works

1. Load and concatenate every CSV.
2. Merge the available text columns into one `text` column.
3. **Balance the classes** by downsampling the larger one, so the model isn't
   biased toward whichever label is more common.
4. Split 80/20 into training and test sets.
5. Fit TF-IDF (20,000 features, 1–2 word grams, English stop words removed).
6. Fit Logistic Regression and print a precision/recall report.
7. Save the vectorizer and model together to `engine/email_model.joblib`.

## Note on version control

`.gitignore` excludes `*.csv`, so these files are **not** committed to git. They
live only on disk. If you clone this project elsewhere, copy this folder across
manually or the email training script will not run.
