# PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING

## CHAPTER FOUR

## SYSTEM IMPLEMENTATION, TESTING, RESULTS AND DISCUSSION

### 4.1 Introduction

This chapter presents the implemented PhishGuard AI prototype and evaluates the evidence that can be reproduced from its repository. It moves from the design specified in Chapter Three to the actual Django routes, forms, analysis modules, model artefacts, result templates, persistence call and automated tests. It then reports controlled hybrid-analysis scenarios and the independently reproduced performance of the bundled SMS text classifier. The purpose is not to convert implementation activity into unsupported performance claims, but to distinguish clearly among three kinds of evidence: what is present in the source code, what the automated suite verifies, and what the available dataset permits to be measured.

The evaluation was conducted on 11 August 2026 using the source-controlled application and pinned Python dependencies. The Django suite was rerun, the two serialized model artefacts were loaded, fixed synthetic messages were passed through the real hybrid analyzer, and the SMS evaluation was regenerated from the bundled corpus and documented split. Small machine-readable evidence records and scripts were preserved under `report/evidence/` and `report/tools/` respectively (Jesutofaye, 2026). Application screenshots could not be captured in the current report-generation environment because a compatible browser-rendering facility was unavailable. Consequently, this chapter uses clearly numbered, editable screenshot placeholders and does not present reconstructed mock-ups as observed screens.

The results must be read within the prototype boundary. The verified SMS measures describe the saved TF-IDF/Logistic Regression text classifier on an internal random hold-out from an older spam-labelled corpus. They do not measure the complete hybrid decision system, present-day Nigerian smishing, email detection, live-domain verification or public deployment performance. Email dataset provenance and evaluation data are not available in the repository, so all email metric fields remain explicit placeholders. Larger, contemporary, independently labelled real-world validation is required before strong performance claims can be made.

### 4.2 Implementation Environment

#### 4.2.1 Hardware and Software Context

PhishGuard AI was implemented as a server-rendered Python web application. The application does not require a graphics-processing unit for inference because both channel models are sparse linear text classifiers. The verification environment used an isolated Python virtual environment and the dependency versions pinned in the repository. Table 4.1 records the versions associated with the reproduced quantitative evidence. This environment record is important because serialized scikit-learn objects and numerical optimisation can be affected by library-version differences.

[[TABLE 4.1 START]]
| Item | Verified version or state | Role in implementation/evaluation |
| Python | 3.11.2 | Application runtime and report evidence scripts |
| Django | 5.2.8 | URL routing, form handling, templates, ORM and test framework |
| scikit-learn | 1.7.2 | TF-IDF transformation, Logistic Regression and classification metrics |
| pandas | 2.3.3 | SMS corpus loading, label mapping and split preparation |
| NumPy | 2.3.4 | Numerical arrays and consistency comparisons |
| SciPy | 1.16.3 | Sparse numerical support used by scikit-learn |
| Joblib | 1.5.2 | Loading the serialized email and SMS model pairs |
| tldextract | 5.3.0 | Local registered-domain parsing for URL/sender evidence |
| Database design | SQLite through Django ORM | Intended local prototype persistence; initial app migration is not committed |
| Evaluation date | 11 August 2026 | Date of the preserved test and classifier evidence |
[[TABLE 4.1 END]]

**Table 4.1:** Verified implementation and evaluation environment

The application dependencies are version-pinned, which improves repeatability. Django 5.2 is an LTS release line, while the repository uses version 5.2.8 (Django Software Foundation, 2025). The verification used the development settings supplied by the project rather than a hardened deployment profile. Therefore, successful development checks and functional tests should not be interpreted as evidence that the application is ready for exposure to untrusted internet traffic.

#### 4.2.2 Implemented Project Structure

The implementation follows Django’s separation of project configuration and application logic. `email_sentinel/` contains project-level settings and URL inclusion. `detector/` contains the form, view, persistence model, templates, template filter, inference and analysis modules, datasets, training scripts, tests and saved model artefacts. Table 4.2 connects the design responsibilities from Chapter Three to concrete implementation points.

[[TABLE 4.2 START]]
| Implemented element | Repository location | Observed responsibility |
| Project routing | `email_sentinel/urls.py` | Includes detector routes and Django administration route |
| Application routing | `detector/urls.py` | Maps the root landing page and `/analyze/` analysis page |
| Mode-aware form | `detector/forms.py` | Validates email or SMS sender, body and lengths; discards SMS subject |
| Request controller | `detector/views.py` | Selects mode, checks model state, invokes analyzer, normalises output, requests persistence and renders response |
| Model interface | `detector/engine/classifier.py` | Resolves artefact path, caches vectorizer/model pair and returns class-aware probability |
| Hybrid analyzer | `detector/engine/analyzer.py` | Extracts content/URL evidence, coordinates sender evidence, scores risk and builds guidance |
| Sender intelligence | `detector/engine/sender_intelligence.py` | Parses email sender text and detects local format or organisation inconsistencies |
| Recognised domains | `detector/engine/legit_sources.py` | Supplies bounded trusted-context information |
| Persistence model | `detector/models.py` | Defines the `ScannedEmail` record structure |
| Presentation | `detector/templates/detector/` | Implements landing, channel form, validation, results and recommendations |
| Test suite | `detector/tests.py` | Contains component, view-mode and rendered-layout checks |
| Training/evidence | `detector/train_sms_csv.py`; `report/tools/evaluate_chapter_four.py` | Documents SMS training and reproduces report metrics without replacing the artefact |
[[TABLE 4.2 END]]

**Table 4.2:** Mapping of implemented components to repository evidence

This modular arrangement supports traceability. For example, changing a visual label in the template does not require refitting the model, while replacing a model artefact does not require placing training logic inside a request handler. The analyzer remains the integration point at which statistical evidence, local sender/domain checks, content patterns and URL evidence are combined.

### 4.3 User-Interface Implementation

#### 4.3.1 Landing Page and Channel Entry

The root route renders `landing.html`. Its principal heading identifies email and SMS phishing as the user problem, and it provides three links into the analysis page: an email-detection card, an SMS-detection card and a general start-analysis button. The email and SMS cards append `?mode=email` and `?mode=sms` respectively. This allows the analysis view to initialise the matching channel without requiring a separate controller for each medium.

The landing page is implemented as responsive HTML and CSS. Its visual hierarchy places the PhishGuard AI brand, task statement and entry options before explanatory benefits. The system remains a manual copy-and-paste tool: no button connects to an inbox, SMS application or telecom network. This boundary reduces integration complexity but means the user must transfer the relevant sender and message text accurately.

[[FIGURE 4.1: LANDING PAGE SCREENSHOT]]

**Figure 4.1:** Editable placeholder for the PhishGuard AI landing page screenshot

Figure 4.1 is reserved for a browser-captured image of the implemented landing page. The final image should show the project brand, email and SMS entry cards, and the start-analysis action. It should be captured from the actual running repository rather than replaced by a redesigned mock-up.

#### 4.3.2 Channel-Aware Analysis Form

The `/analyze/` route renders one form for both media. A hidden `message_type` choice stores either `email` or `sms`, while visible tabs allow the user to switch modes. In email mode, the form requests a sender email address, an optional subject and the message body. In SMS mode, the sender prompt accepts a telephone number, short code or alphanumeric sender identifier; the subject control is hidden and cleared. The backend repeats this protection by setting SMS subject to an empty string even if a stale or manipulated value is posted.

Server-side validation is implemented in `EmailForm`. The sender and body are required. The sender has a maximum of 255 characters, the email subject is limited to 512 characters, and the body is limited to 10,000 characters. Django’s email validator handles email mode. SMS mode removes spaces, parentheses and hyphens for numeric validation, then accepts an optional leading plus followed by 3–15 digits, or an alphanumeric sender identifier beginning with a letter and containing no more than 32 characters. Invalid data remains on the form with a specific message, and the analyzer is not called.

The template adds presentation behaviour without replacing backend enforcement. JavaScript changes field labels and visibility, clears stale cross-channel values only when the user deliberately changes channel, and disables duplicate submission after the form passes native browser validity checks. The form includes Django’s CSRF token. Table 4.3 summarises the principal interface controls.

[[TABLE 4.3 START]]
| Interface element | Email behaviour | SMS behaviour | Verification basis |
| Channel tabs | Selects email and displays subject | Selects SMS and hides subject | Template inspection and mode tests |
| Sender input | Requires syntactically valid email address | Accepts phone number, short code or sender ID | Form tests |
| Subject input | Optional; maximum 512 characters | Cleared and excluded from analyzer call | Form and view-mode tests |
| Message input | Required; maximum 10,000 characters | Required; maximum 10,000 characters | Form tests |
| Submit action | POST with CSRF token; duplicate submission disabled client-side | Same | Template inspection |
| Validation feedback | Field-specific visible errors | Field-specific visible errors | Invalid-form test |
| Privacy note | States browser-session and server processing | Same | Template inspection; wording requires stronger persistence disclosure |
[[TABLE 4.3 END]]

**Table 4.3:** Implemented analysis-form controls

[[FIGURE 4.2: EMAIL FORM SCREENSHOT]]

**Figure 4.2:** Editable placeholder for the email-analysis form screenshot

[[FIGURE 4.3: SMS FORM SCREENSHOT]]

**Figure 4.3:** Editable placeholder for the SMS-analysis form screenshot

Figures 4.2 and 4.3 should be replaced with screenshots from the running analysis page after selecting each channel. They should make the field differences legible and should not contain a real private message, live credential, personal telephone number or active malicious URL.

#### 4.3.3 Accessibility and Feedback Features

The implementation uses text, icons and colour together rather than relying on colour alone. Validation and processing errors use an alert role. Result headings state Low Risk, Suspicious or High Risk for email, while SMS uses the simpler visible wording “Message Appears Safe” or “Message Appears Suspicious.” Responsive style rules reorganise the form and result panels on smaller screens. These are useful implementation features, but code inspection is not a substitute for a user-based accessibility audit. Keyboard order, screen-reader interpretation, contrast under real rendering and comprehension by non-specialists remain to be evaluated with appropriate tools and participants.

The privacy line below the form currently states that analysis is processed in the browser session and on the server for review. Since the view also calls the ORM after a successful analysis, the wording does not clearly state that sender and message content are intended to be stored. This is reported as an acceptance limitation rather than silently treated as complete privacy disclosure.

### 4.4 Backend and Analysis Implementation

#### 4.4.1 Request Handling and Failure Separation

The `index` view obtains the requested channel from the query string or posted hidden field and falls back to email if an unsupported value is supplied. On POST, analysis proceeds only after form validation. The view calls `model_error(message_type)` before invoking the analyzer. A missing or unreadable model produces an error message and leaves the result object empty. An unexpected exception is logged and converted to the generic message “Unable to complete the analysis right now. Please try again.” It is not converted into a phishing verdict.

This separation is important in a security-facing interface. A processing failure does not demonstrate that a message is safe or malicious. The corresponding automated tests verify that a missing SMS model, a corrupt model and an unexpected analyzer exception cannot appear as a High Risk result.

#### 4.4.2 Channel-Specific Model Loading and Inference

The model interface maps email and SMS modes to different `.joblib` files and restores each file as a `(vectorizer, model)` tuple. Both inspected classifiers expose classes `[0, 1]`. The application locates class 1 in `model.classes_` before reading the positive-class probability, rather than assuming that it occupies a fixed column. It also distinguishes positive-class probability from confidence in the selected class.

Email inference uses the saved 20,000-feature TF-IDF vectorizer and Logistic Regression classifier. SMS inference uses the separate 15,000-feature vectorizer and class-weighted Logistic Regression classifier. The loader caches restored objects, reducing repeated deserialization overhead during a running process. No request triggers model training, and user-submitted text is not automatically added to a learning set.

#### 4.4.3 Explainable Evidence Extraction

After statistical inference, the hybrid analyzer examines the supplied content for bounded categories of social-engineering evidence. These include urgency, threat of loss or account action, credential or authentication requests, personal/banking-data requests, payment redirection, reward/grant/money lures and, for SMS, a direct request to share an OTP or verification code. Clause-level negation and security-awareness checks reduce false alarms where a legitimate warning states that an organisation will never ask for a PIN or OTP.

Email sender checks parse the text supplied as the sender address. They identify malformed structure, domain-form anomalies, selected one-edit look-alikes, public-provider organisation claims and inconsistencies between a named organisation and the supplied domain. URL checks identify shortened links, raw-IP hosts, `@` authority obfuscation, punycode and selected higher-risk top-level labels. These checks are local. They do not authenticate mail headers, verify a telephone-network identity, query DNS ownership, follow redirects or open a linked webpage.

#### 4.4.4 Risk Aggregation and Result Construction

The implementation combines a maximum 45-point model contribution with explainable evidence capped at 60 points and limited context credit. Safeguards then cap or floor the result. Model output with no explainable evidence is capped at 39, while a deceptive link or sensitive-data request reaches at least Suspicious. Strong sender deception or a serious combination reaches at least High Risk. The final value is bounded between 0 and 100 and mapped to 0–39 Low Risk, 40–69 Suspicious and 70–100 High Risk.

The email template displays the resulting numerical threat score, risk state, reasons where triggered, technical details and recommended actions. It displays safe signals for Low Risk rather than showing an empty warning panel. The SMS template deliberately hides the numerical score and emphasises a two-label user verdict, masked numeric sender, links, credentials, OTP, urgency, threat, money lure and channel-appropriate recommendations. The internal score still exists for consistent risk mapping and persistence; it is simply not exposed in the SMS result panel.

[[FIGURE 4.4: LOW-RISK EMAIL RESULT SCREENSHOT]]

**Figure 4.4:** Editable placeholder for a Low Risk email result screenshot

[[FIGURE 4.5: WARNING EMAIL RESULTS SCREENSHOT]]

**Figure 4.5:** Editable composite placeholder for Suspicious and High Risk email result screenshots

[[FIGURE 4.6: SMS RESULT STATES SCREENSHOT]]

**Figure 4.6:** Editable composite placeholder for safe and suspicious SMS result screenshots

Figures 4.4–4.6 should be populated with the actual rendered outputs for non-sensitive test messages. A composite in Figure 4.5 should show the amber Suspicious state beside the red High Risk state. Figure 4.6 should show that both SMS states use plain-language verdicts and that the numerical threat score is absent.

#### 4.4.5 Persistence Implementation and Current Constraint

After a successful analyzer response, the view calls `ScannedEmail.objects.create` with the sender, subject, full body, comma-joined rule descriptions, machine-learning label, final label and hybrid score. This confirms that persistence is implemented in the request path. However, the repository’s `detector/migrations/` directory contains only `__init__.py`. A dry-run migration check reports that `0001_initial.py` would need to be created for `ScannedEmail`, and no local `db.sqlite3` file is part of the evaluated checkout.

The automated view test mocks `ScannedEmail.objects.create`, and all test classes inherit from `SimpleTestCase`. Django therefore reported “Skipping setup of unused database(s): default.” The suite verifies the call boundary but does not establish that a fresh database can persist and retrieve a record end to end. FR-12 is consequently classified as partially verified. Before a demonstration that exercises storage, the initial migration must be generated, reviewed, committed and applied. Before any real deployment, retention, access controls, redaction and deletion policy must also be defined.

[[FIGURE 4.7: VALIDATION AND ERROR STATES SCREENSHOT]]

**Figure 4.7:** Editable composite placeholder for validation and controlled processing-error screenshots

Figure 4.7 is intended to show one field-validation error and one model/processing error. The images must make clear that neither error is a risk verdict.

### 4.5 System Testing

#### 4.5.1 Testing Procedure

The application suite was executed from the repository root with:

**`.report-work/venv/bin/python manage.py test --verbosity 2`**

The preserved run on 11 August 2026 discovered 47 tests, completed them in 0.971 seconds and returned `OK`. Django’s normal system check reported no issues. One expected error-path test deliberately raises `RuntimeError("model failed")`; the view logs the exception, returns the generic failure message and the test still passes. The traceback in the test log is therefore evidence that the controlled failure path was exercised, not an unhandled suite failure.

The suite is organised into 35 classifier/analyzer/form tests, six rendered result-layout tests and six view/mode/error tests. All use Django’s `SimpleTestCase`; this keeps the suite fast but explains why a test database is not created. Table 4.4 reports the exact summary.

[[TABLE 4.4 START]]
| Test group | Number executed | Passed | Failed/error | Main behaviours covered |
| `ClassifierTests` | 35 | 35 | 0 | Model separation, risk bands, evidence, safe contexts, sender/URL rules, forms and SMS wording |
| `ResultLayoutTests` | 6 | 6 | 0 | Green/amber/red structures, SMS details, safe signals, sender masking and hidden SMS score |
| `ViewModeTests` | 6 | 6 | 0 | Query mode, SMS subject removal, invalid form, missing/corrupt model and unexpected exception |
| Total | 47 | 47 | 0 | Functional and rendered-output verification |
| Execution | 0.971 seconds | `OK` | Exit status 0 | Normal system check identified no issues |
[[TABLE 4.4 END]]

**Table 4.4:** Automated Django test results on 11 August 2026

The result establishes that the tested behaviours passed in the recorded environment. It does not mean that every possible input was tested, that database migration works, that browsers render identically, or that classifier accuracy is 100%. Unit/functional test pass rate and statistical detection performance are separate quantities.

#### 4.5.2 Functional Requirement Verification

Table 4.5 traces the Chapter Three functional requirements to current evidence. “Pass” means that a relevant automated check and/or direct implementation inspection supports the stated behaviour. “Partial” is used where the implementation exists but the available verification does not cover the complete operational path.

[[TABLE 4.5 START]]
| ID | Evidence used | Status | Evaluation comment |
| FR-01 | Query-mode test and channel tabs | Pass | Email/SMS mode controls input and output path |
| FR-02 | Form validation tests | Pass | Required fields, syntax and length limits are exercised |
| FR-03 | SMS subject view test | Pass | Posted SMS subject is replaced with an empty string |
| FR-04 | Independent-artefact test and artefact inspection | Pass | Email and SMS resolve to different saved pairs |
| FR-05 | Class-aware probability code and model tests | Pass | Positive class is identified from classifier classes |
| FR-06 | Content-rule tests | Pass | Urgency, requests, threats, payment and lures are named |
| FR-07 | Sender-intelligence tests | Pass | Neutral unknown, public-provider claim and look-alike cases are checked |
| FR-08 | URL tests and analyzer inspection | Pass | Shortened URL and other local URL indicators are implemented |
| FR-09 | Boundary and evidence tests | Pass | Score bounds, bands, floors and cap behaviour are exercised |
| FR-10 | Layout tests | Pass | Verdict, reason/safe signal and recommendations are conditional |
| FR-11 | View error tests | Pass | Missing/corrupt artefacts and exceptions do not become verdicts |
| FR-12 | ORM call inspection and mocked view test | Partial | Persistence call exists, but no initial migration or real database test is present |
| FR-13 | Landing/analyse links and template inspection | Implemented | Analyze-another navigation requires no authentication; no dedicated automated assertion |
[[TABLE 4.5 END]]

**Table 4.5:** Functional requirement verification status

The trace shows that the core triage flow is implemented and tested more extensively than deployment and persistence. This is appropriate for an academic prototype, provided the limitations remain explicit.

#### 4.5.3 Controlled Hybrid-Analysis Scenarios

Eight fixed synthetic scenarios were evaluated through the real `analyze` function and saved as `report/evidence/chapter_four_scenarios.json`. They were selected to test disagreement between the model and rules, legitimate security vocabulary, link review, sender deception, routine SMS, quiet OTP requests and money/reward lures. They are functional scenarios rather than a statistically representative sample. Table 4.6 reports the exact outputs. “Model positive output” is the classifier’s class-1 score expressed as a percentage; it is not the final risk score or a calibrated probability of real fraud.

[[TABLE 4.6 START]]
| ID | Scenario | Model positive output | Internal hybrid score | Final user outcome | Principal observed evidence |
| E1 | Routine payment receipt; unknown clean sender | 87.3% | 32.3 | Low Risk | No rule; unexplained model evidence capped below warning |
| E2 | Recognised-domain anti-fraud notice | 56.5% | 0.0 | Low Risk | Awareness wording and trusted routine context; no rule |
| E3 | Email containing a shortened URL | 64.6% | 40.0 | Suspicious | Shortened URL detected |
| E4 | Zenith Bank claim from Gmail with urgent password demand | 99.3% | 100.0 | High Risk | Public-provider impersonation, urgency, threat and credential request |
| E5 | Zenith Bank claim from `zen1thbank.com` | 96.2% | 100.0 | High Risk | Look-alike domain, organisation mismatch and credential request |
| S1 | Routine bank credit notification | 43.6% | 0.0 | Message Appears Safe | No rules; ordinary transaction wording |
| S2 | Quiet SMS asking recipient to share an OTP | 61.3% | 56.3 | Message Appears Suspicious | Credential/authentication and explicit OTP request |
| S3 | Grant/prize claim with 24-hour deadline | 92.0% | 62.0 | Message Appears Suspicious | Urgency and reward/money lure |
[[TABLE 4.6 END]]

**Table 4.6:** Controlled hybrid-analysis scenario results

The E1 result demonstrates the explanation safeguard. Although the text classifier produced a high class-1 output for routine payment language, the absence of an explainable indicator prevented an amber or red warning. E2 demonstrates that anti-fraud vocabulary is not automatically treated as a credential demand. E3 demonstrates the independent link-review floor. E4 and E5 demonstrate two distinct sender-consistency mechanisms. S2 confirms that a phishing-like request need not contain a URL or overt threat to receive a warning, while S3 shows that a reward/deadline combination can be surfaced without being forced into High Risk by model output alone.

These outputs also reveal an important design choice: the same internal three-band score is translated into two visible SMS verdicts. S2 and S3 are internally Suspicious and appear to the user as “Message Appears Suspicious.” The numerical value is hidden in the SMS interface, reducing the chance that a non-calibrated engineering score is interpreted as percentage certainty.

### 4.6 SMS Classifier Evaluation

#### 4.6.1 Evaluation Scope and Data Integrity

The SMS evaluation is reproducible because the dataset file, training script and saved artefact are present. The normalized corpus contains 5,574 records: 4,827 ham and 747 spam, representing approximately 86.6% and 13.4% of the data respectively. The dataset SHA-256 checksum recorded for this evaluation is `7d039a24a6083ed9ef0f806ebad56bbb976e3aeb8de05669173bfdc4996c239d`. The saved SMS artefact checksum is `4fc2195d6667bb2efb4de768432b4e27f5a1aff7541439b220867f918a9368d2`.

The labels originate from the SMS Spam Collection assembled by Almeida et al. (2011). The positive label is `spam`, not a narrower verified `smishing` class. Therefore, the classifier detects language associated with the corpus’s unsolicited/premium-rate messages and is used only as one component of PhishGuard AI’s phishing-oriented hybrid analysis.

The documented split is an 80/20 stratified random hold-out with `random_state=42`, implemented with the pinned scikit-learn toolchain (scikit-learn developers, 2025). It produces 4,459 training records and 1,115 test records. The training partition contains 3,861 ham and 598 spam messages; the test partition contains 966 ham and 149 spam messages. The saved vectorizer has 15,000 features, and the classifier exposes classes `[0, 1]`. Table 4.7 presents the data and split evidence.

[[TABLE 4.7 START]]
| Evidence item | Value | Interpretation |
| Total records | 5,574 | Corpus after file loading and missing-row removal |
| Ham records | 4,827 (86.6%) | Negative class 0 |
| Spam records | 747 (13.4%) | Positive class 1 |
| Training partition | 4,459: 3,861 ham; 598 spam | Stratified 80% split |
| Test partition | 1,115: 966 ham; 149 spam | Stratified 20% hold-out |
| Random state | 42 | Fixed by training script |
| Representation | TF-IDF unigram/bigram; maximum 15,000 | Saved vocabulary size confirmed as 15,000 |
| Estimator | Logistic Regression; balanced class weights | `max_iter=2000`; positive class 1 |
[[TABLE 4.7 END]]

**Table 4.7:** SMS classifier dataset and deterministic split

The primary calculation loaded the deployed saved artefact and evaluated it on the deterministic test indices. A second fit using the documented current code produced identical discrete test predictions and the same confusion matrix. Positive-class probabilities differed by at most approximately 0.999 percentage point, which may reflect small fitting or vocabulary-order differences between artefact creation and the current numerical environment. For this reason, the saved artefact—not a newly substituted model—is the source of the headline values.

#### 4.6.2 Primary Hold-Out Results

Taking spam as the positive class, the saved classifier correctly classified 1,096 of 1,115 test messages and made 19 errors. It achieved 98.30% accuracy, 93.92% positive-class precision, 93.29% positive-class recall and a 93.60% positive-class F1-score. Table 4.8 presents values to two decimal places while the evidence JSON preserves full precision.

[[TABLE 4.8 START]]
| Measure | Verified value | Calculation/meaning |
| Accuracy | 98.30% | 1,096 correct predictions divided by 1,115 test records |
| Precision for spam | 93.92% | 139 true positives divided by 148 predicted positives |
| Recall for spam | 93.29% | 139 true positives divided by 149 actual positives |
| F1-score for spam | 93.60% | Harmonic mean of positive-class precision and recall |
| Correct ham | 957 | True negatives |
| Incorrect ham flagged as spam | 9 | False positives |
| Spam missed as ham | 10 | False negatives |
| Correct spam | 139 | True positives |
[[TABLE 4.8 END]]

**Table 4.8:** Verified SMS text-classifier results on the documented hold-out

[[FIGURE 4.8: SMS METRIC SUMMARY]]

**Figure 4.8:** Verified primary hold-out metrics for the saved SMS text classifier

[[FIGURE 4.9: SMS CONFUSION MATRIX]]

**Figure 4.9:** Confusion matrix for the saved SMS text classifier

Figure 4.9 uses actual classes as rows and predicted classes as columns. Of 966 ham messages, 957 were correctly classified and nine were false alarms. Of 149 spam messages, 139 were detected and ten were missed. The associated false-positive rate was approximately 0.93%, while the false-negative rate among positive examples was approximately 6.71%.

Accuracy is reported because it is familiar, but the positive-class precision, recall, F1-score and raw counts are essential under the imbalanced distribution. Saito and Rehmsmeier (2015) similarly argue that precision–recall-oriented interpretation is more informative than relying only on aggregate accuracy for imbalanced classification. In this prototype, a false negative may permit a risky message to appear benign at the model layer, while a false positive may unnecessarily alarm a user. Hybrid evidence can correct some cases, but no complete hybrid confusion matrix can be claimed without a separately labelled evaluation set and a fixed final-decision protocol.

#### 4.6.3 Error Analysis

Inspection of the 19 errors showed patterns that are consistent with the corpus and sparse lexical representation. The nine false positives included short, highly abbreviated conversational messages and legitimate-looking telecom, job or customer-service wording. One duplicated ham message about receiving a landline call appeared twice in the false-positive set. The ten false negatives included premium-rate or ringtone promotions written in conversational style, complaint/warning texts that discussed scams rather than directly delivering a lure, and a small number of records whose spam label was not obvious from the isolated sentence.

These cases identify three limitations. First, a unigram/bigram model can over-weight abbreviations and service language without broader context. Second, corpus labels combine several forms of spam, so a message may be correctly labelled `spam` by the dataset while not resembling credential phishing. Third, duplicate messages can influence both error counts and internal hold-out estimates. The local rule engine addresses selected phishing actions such as credentials, OTPs, links and payment redirection, but it is not evaluated by simply reusing the corpus’s broad spam label.

#### 4.6.4 Duplicate and Split Sensitivity

An exact-message audit found 5,160 unique normalized messages and 414 rows beyond the first occurrence of a message. No repeated message had conflicting labels. Under the documented random split, 123 unique message strings occurred in both partitions, and 139 of the 1,115 test rows (12.47%) had exact text already present in training. This is a leakage risk because a random message-level split can reward memorisation of duplicate templates.

Two supplementary analyses were therefore performed. First, the saved artefact was scored only on the 976 test rows whose exact text did not occur in training. Second, exact normalized duplicates were removed before a new stratified 80/20 split and model fit. These are sensitivity checks, not replacements for the deployed artefact’s primary result.

[[TABLE 4.9 START]]
| Evaluation view | Test records | Accuracy | Precision | Recall | F1-score | Confusion counts: TN, FP, FN, TP |
| Saved artefact; documented test split | 1,115 | 98.30% | 93.92% | 93.29% | 93.60% | 957, 9, 10, 139 |
| Saved artefact; exact-text-unseen test subset | 976 | 98.16% | 92.73% | 91.07% | 91.89% | 856, 8, 10, 102 |
| Deduplicate first; new deterministic split and fit | 1,032 | 97.97% | 90.23% | 93.75% | 91.95% | 891, 13, 8, 120 |
[[TABLE 4.9 END]]

**Table 4.9:** SMS duplicate/leakage sensitivity analysis

The sensitivity values remain high, but positive-class F1-score falls from 93.60% to approximately 91.9% under both stricter views. The difference supports a cautious interpretation of the primary hold-out and confirms the Chapter Three recommendation to deduplicate and group related templates before future splitting. It also demonstrates why a single headline accuracy should not be treated as expected real-world effectiveness.

#### 4.6.5 Comparison and Interpretation

Recent studies reviewed in Chapter Two have reported high values for phishing and smishing classifiers, including larger neural systems and systems enriched with external evidence. However, direct ranking would be invalid because their datasets, labels, dates, channels and evaluation protocols differ. Alhuzali et al. (2025), for example, compared numerous models across multiple email datasets, while Wang et al. (2025) combined SMS analysis with external evidence and a user study. PhishGuard AI’s verified value concerns one older SMS spam corpus and a local sparse linear classifier.

The result nevertheless supports the technical feasibility of the chosen baseline. TF-IDF and Logistic Regression produced a compact, fast and reproducible channel model, and the complete Django test suite executed in under one second in the verification environment. Its strengths are simplicity, local inference and interpretable integration. Its weaknesses are lexical sensitivity, corpus age, broad spam labels, duplicate leakage and lack of external Nigerian validation. The literature also shows that high clean-data results can decline sharply under adversarial change; Ahmed and Pourmoafil (2026) reported such degradation for both TF-IDF/Logistic Regression and a transformer. The present 98.30% internal value must therefore not be advertised as a guarantee against contemporary or adversarial smishing.

### 4.7 Email Classifier Evidence Status

The repository contains a loadable email `(vectorizer, model)` artefact with a 20,000-feature TF-IDF vocabulary and binary classes `[0, 1]`. The application tests confirm that email and SMS use independent artefacts. However, the external email CSV paths in the training script are machine-specific, and the corresponding datasets, manifest and split records are not versioned. A serialized model cannot reconstruct trustworthy source provenance, licensing, deduplication, label mapping or test membership.

Consequently, no email accuracy, precision, recall, F1-score or confusion matrix is reported. Values mentioned in development notes were not used because their underlying scratch corpora are unavailable for independent verification. Table 4.10 and Figure 4.10 remain intentionally editable. They must be populated only after the email sources and deterministic evaluation records are supplied.

[[TABLE 4.10 START]]
| Required email evidence | Current report entry | Condition for replacement |
| Dataset titles, publishers and licences | [Insert verified email dataset provenance] | Portable manifest and lawful source record supplied |
| Original and final record counts | [Insert verified counts and class distribution] | Reproducible preparation log supplied |
| Duplicate/leakage controls | [Insert verified procedure and overlap audit] | Hash/group analysis completed before split |
| Training/test distribution | [Insert verified split counts] | Deterministic indices or split manifest preserved |
| Accuracy | [Insert verified result] | Reproduced from held-out email data |
| Precision, recall and F1-score | [Insert verified results] | Positive class and averaging method stated |
| Confusion matrix | [Insert verified TN, FP, FN and TP] | Actual/predicted orientation stated |
| External/temporal test | [Insert verified result or “not conducted”] | Independent contemporary data evaluated |
[[TABLE 4.10 END]]

**Table 4.10:** Explicit placeholders for unavailable email classifier evidence

[[FIGURE 4.10: EMAIL CLASSIFIER RESULT PLACEHOLDER]]

**Figure 4.10:** Editable placeholder for a verified email classifier confusion matrix and metric summary

This evidence gap does not make the implemented email workflow nonexistent: email forms, inference loading, sender checks, URL checks, risk aggregation and result rendering are present and exercised by tests/scenarios. It does mean that the statistical effectiveness of the email model is unknown from reproducible repository evidence. The distinction must be maintained in the abstract, conclusion and any oral defence.

### 4.8 Deployment and Security Diagnostics

#### 4.8.1 Django Checks

The normal Django system check completed with no issue. The deployment-oriented check, `manage.py check --deploy`, returned six warnings: HSTS was not configured; SSL redirect was not enabled; the development secret key was weak/insecure; session cookies were not marked secure; CSRF cookies were not marked secure; and `DEBUG` remained enabled. These warnings align with Django’s documented distinction between development defaults and deployment controls (Django Software Foundation, 2025).

The dry-run migration check returned status 1 because it would create `detector/migrations/0001_initial.py` for `ScannedEmail`. This is a concrete setup deficiency rather than a theoretical future concern. Table 4.11 records the diagnostics.

[[TABLE 4.11 START]]
| Diagnostic | Observed result | Meaning/action required |
| `manage.py check` | No issues; exit 0 | Development configuration is internally consistent |
| `manage.py check --deploy` | Six security warnings; exit 0 | Harden HTTPS, cookies, secret management and debug setting before deployment |
| `makemigrations --check --dry-run` | Initial `ScannedEmail` migration would be created; exit 1 | Generate, review, commit and apply migration before persistence demonstration |
| Migration directory inspection | Only `__init__.py` | No application schema migration currently tracked |
| Test database report | Default database skipped | Automated suite does not verify real record persistence |
[[TABLE 4.11 END]]

**Table 4.11:** Deployment and database diagnostics

The application should therefore remain a supervised local prototype. Production transition requires environment-managed secrets, `DEBUG=False`, explicit hosts, HTTPS and secure cookies, a committed migration, controlled administration, retention/deletion controls, rate limiting, monitoring and a managed data-store arrangement. Domain extraction should also be configured with a pinned local Public Suffix List for deterministic offline behaviour rather than depending on a network refresh.

#### 4.8.2 Privacy and Ethical Result Presentation

The user supplies potentially private sender and message data. The current persistence call stores the full text, while the form notice does not plainly state local database retention. This fails the complete privacy-disclosure acceptance condition even though the statement acknowledges server processing. Remediation should either disable raw-message storage by default or provide an explicit notice, lawful purpose, retention period, access control, redaction and deletion mechanism.

Result wording is more cautious than a simple binary accusation. Low Risk is accompanied by normal-caution language, Suspicious recommends independent verification, and High Risk recommends avoiding interaction and using trusted channels. The system does not autonomously block accounts or report senders. This decision-support positioning is appropriate because false positives and false negatives remain possible.

### 4.9 Evaluation Against Project Objectives

Table 4.12 evaluates the objectives stated in Chapter One using only implementation and test evidence. The assessment separates fulfilment of a software function from validation of its effectiveness.

[[TABLE 4.12 START]]
| Project objective | Evidence in this chapter | Assessment |
| Analyse email and SMS through one accessible prototype | Landing route, channel form, independent models and mode tests | Implemented and functionally verified |
| Apply machine learning to message text | Two saved TF-IDF/Logistic Regression pairs; classifier loading tests | Implemented; SMS effectiveness verified internally; email effectiveness pending |
| Examine sender/domain, URLs and content indicators | Sender, URL and content modules plus targeted tests/scenarios | Implemented and functionally verified for documented local checks |
| Aggregate evidence into understandable risk output | Three-band email score, two-label SMS output, named reasons and actions | Implemented; controlled scenario behaviour verified |
| Reduce unexplained or misleading warnings | Model-only cap, awareness handling and controlled failure states | Verified by automated tests and E1/E2 scenarios |
| Evaluate system behaviour | 47 passing tests and eight fixed hybrid scenarios | Completed for implemented functional scope |
| Evaluate statistical classifier performance | Reproduced SMS metrics, confusion matrix and leakage sensitivity | Completed for bundled SMS classifier only |
| Provide responsible, deployment-ready protection | Deploy check, migration and privacy findings | Not achieved; prototype requires security, data and operational remediation |
[[TABLE 4.12 END]]

**Table 4.12:** Evaluation of project objectives

The central objective—a practical prototype that combines channel-specific models with explainable evidence—was achieved at implementation level. The evidence does not justify describing the system as production-ready or universally accurate. The SMS classifier has a reproducible internal baseline; email and complete hybrid performance remain open evaluation tasks.

### 4.10 Discussion of Findings

#### 4.10.1 Functional Findings

The 47 passing tests demonstrate coherent behaviour across forms, analyzer logic, rendered layouts and failure handling. The suite goes beyond a single happy path: it includes routine bank alerts, payment receipts, anti-fraud notices, direct credential requests, quiet OTP requests, payment-redirection fraud, shortened URLs, sender look-alikes, public-provider claims and model failures. This coverage is especially useful because many phishing detectors are vulnerable to legitimate messages containing words such as “password,” “bank” or “OTP.”

The controlled scenarios show that the hybrid layer can resolve some disagreements. E1 would be alarming if the raw model output were displayed as the final result, but the no-evidence cap retains Low Risk and still avoids claiming certainty. E3 is raised to review because a short link prevents visual destination verification. E4 and E5 combine sender inconsistency with an explicit demand, producing a High Risk state with reasons. This behaviour reflects the project’s emphasis on transparent triage rather than opaque class output.

However, the same safeguards can create new errors. A malicious message that contains no covered rule and receives a calm model score can remain Low Risk. A legitimate message with a shortened link can become Suspicious. The recognised-domain map may become stale, and local sender text can be forged. The score is therefore an engineering decision index, not an empirically calibrated fraud probability.

#### 4.10.2 Statistical Findings

The SMS classifier’s 98.30% accuracy and 93.60% F1-score show that the selected sparse text baseline fits the documented internal split well. The confusion matrix is more informative than accuracy alone: ten of 149 spam test messages were missed, and nine of 966 ham messages were flagged. The positive-class recall of 93.29% means that approximately 6.71% of positive examples in this particular test partition were not detected by the text model.

The duplicate audit changes the interpretation. More than twelve per cent of test rows had exact message text in training, and stricter sensitivity views reduced F1 to approximately 91.9%. This does not invalidate the implementation, but it limits the evidential strength of the primary number. Future work should preserve deduplicated, campaign-grouped and temporal test sets and should report uncertainty across multiple splits or an independent locked test corpus.

The corpus also represents spam rather than phishing exclusively. A premium-rate entertainment message and a credential-stealing bank impersonation can share the positive label even though user harms and appropriate explanations differ. A modern evaluation should use explicit categories such as ham, benign marketing, generic spam, financial fraud, credential phishing, OTP theft and malicious-link smishing, then report both multiclass and operational binary results.

#### 4.10.3 Explainability and Usability

Named reasons and recommended actions address an important gap between detection and safe user response. Wang et al. (2025) found value in walking users through SMS evidence rather than returning only a label. PhishGuard AI follows this direction at a smaller prototype scale by explaining the observed sender, content and URL indicators and recommending trusted verification. Its local implementation does not gather external webpage or brand evidence, so its explanations are narrower.

No participant usability study was conducted for this chapter. It would be inaccurate to infer satisfaction, trust, comprehension or System Usability Scale scores from template inspection. Figure 4.11 remains a placeholder for a future approved study. A defensible protocol should measure whether users can identify the verdict, evidence and next action; whether score hiding in SMS improves understanding; and whether warnings create appropriate caution without over-trust.

[[FIGURE 4.11: USABILITY RESULT PLACEHOLDER]]

**Figure 4.11:** Editable placeholder for verified user-based usability and comprehension results

#### 4.10.4 Threats to Validity

Internal validity is limited by duplicate leakage in the SMS random split and by the absence of a locked hybrid-labelled evaluation set. Construct validity is limited because the corpus positive class is spam while the project construct is phishing/smishing risk. External validity is limited by the corpus age, English language, mixed non-Nigerian sources and absence of contemporary Nigerian brands, Pidgin, code-switching and telecom patterns. Statistical conclusion validity is limited by one fixed split and the lack of confidence intervals or repeated external samples.

Implementation validity is also bounded. Most tests are component-oriented and use `SimpleTestCase`; persistence is mocked, browser rendering was not captured, and production configuration fails six deployment recommendations. The email model’s source evidence is missing. Finally, adversarial validity is untested: spelling manipulation, Unicode confusables, image-only lures, QR codes, redirected links and previously unseen campaign templates may alter performance. Recent robustness evidence suggests that clean-data results can conceal severe degradation under adaptive attack (Ahmed & Pourmoafil, 2026).

### 4.11 Limitations and Outstanding Evidence

Table 4.13 consolidates what should not be inferred from this chapter. Each limitation is paired with a concrete evidence requirement so that future updates can replace a placeholder rather than invent a value.

[[TABLE 4.13 START]]
| Limitation | Consequence for current claim | Required next evidence/action |
| Email dataset and split unavailable | No email performance value is defensible | Restore lawful data manifest; reproduce held-out and external evaluation |
| SMS labels are broad spam/ham | SMS metric is not direct modern smishing effectiveness | Build contemporary phishing-specific labelled corpus |
| Exact duplicates cross SMS split | Primary internal metric may be optimistic | Deduplicate/group campaigns before locked split |
| One historical English corpus | Limited Nigerian, multilingual and temporal generalisation | Evaluate Nigerian English, Pidgin and current campaign data |
| No browser capture facility in report environment | UI figures are placeholders, not fake screenshots | Capture real application screens in a compatible browser |
| No participant study | No usability, satisfaction or trust score can be claimed | Conduct approved task-based study and report raw protocol/results |
| No committed initial migration | Persistence is not end-to-end verified | Generate/apply migration and add database integration test |
| Development security settings | Public deployment is unsafe | Resolve six deployment warnings and add operational controls |
| No live header/domain/telecom verification | Local text findings cannot authenticate identity | Integrate governed reputation/authentication evidence if in scope |
| Static rules and allow-list | New attacks and brands may be missed | Version, test and review rule/reference updates |
[[TABLE 4.13 END]]

**Table 4.13:** Current limitations and evidence required for stronger claims

These constraints do not negate the educational contribution. They define the boundary within which the implementation and results are valid. Reporting the boundary is particularly important for a cybersecurity tool, because exaggerated confidence can itself increase user risk.

### 4.12 Chapter Summary

This chapter presented the implementation, testing, results and discussion of PhishGuard AI. The prototype uses Django routes, a mode-aware validated form, independent email and SMS TF-IDF/Logistic Regression artefacts, local content/sender/URL checks, bounded hybrid risk aggregation, channel-specific results and an ORM persistence call. The interface supplies named reasons and recommended actions, while errors remain separate from threat verdicts.

The preserved automated run passed all 47 tests in 0.971 seconds with no normal Django system-check issue. Eight fixed synthetic scenarios further demonstrated the model-only cap, security-awareness handling, URL review, sender deception, routine SMS behaviour, OTP detection and reward/deadline detection. Persistence remains only partially verified because the test mocks the ORM and no initial application migration is committed.

The saved SMS classifier was independently evaluated on the deterministic 1,115-message hold-out. It achieved 98.30% accuracy, 93.92% precision, 93.29% recall and 93.60% F1-score for the positive spam class, with 957 true negatives, nine false positives, ten false negatives and 139 true positives. Duplicate analysis showed that 12.47% of test rows had exact text in training; stricter sensitivity results reduced F1 to approximately 91.9%. Accordingly, the primary value is an internal baseline, not a real-world guarantee. Email performance remains an explicit placeholder because its source data and evaluation split are unavailable.

Finally, deployment diagnostics identified six Django security warnings and the missing initial migration. No user usability score or browser screenshot was invented. PhishGuard AI should be described as a practical academic prototype whose core functions are implemented and tested, but whose email evidence, external validation, privacy controls, migration, security hardening and real-user evaluation must be completed before production use. Chapter Five will summarise the study, state the defensible conclusions and present recommendations for improvement and future research.

## REFERENCES

Ahmed, T., & Pourmoafil, S. (2026). Adversarial robustness of phishing email detection: A comparative study of TF-IDF + Logistic Regression and fine-tuned DistilBERT. *arXiv*. https://doi.org/10.48550/arXiv.2607.18429

Alhuzali, A., Alloqmani, A., Aljabri, M., & Alharbi, F. (2025). In-depth analysis of phishing email detection: Evaluating the performance of machine learning and deep learning models across multiple datasets. *Applied Sciences, 15*(6), 3396. https://doi.org/10.3390/app15063396

Almeida, T. A., Gómez Hidalgo, J. M., & Yamakami, A. (2011). Contributions to the study of SMS spam filtering: New collection and results. In *Proceedings of the 11th ACM Symposium on Document Engineering* (pp. 259–262). Association for Computing Machinery. https://doi.org/10.1145/2034691.2034742

Django Software Foundation. (2025). *Django documentation: Release 5.2*. https://docs.djangoproject.com/en/5.2/

Jesutofaye, H. J. (2026). *PhishGuard AI: Email & SMS phishing detection system* [Computer software]. GitHub. https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System

Saito, T., & Rehmsmeier, M. (2015). The precision–recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432

scikit-learn developers. (2025). *scikit-learn 1.7 user guide*. https://scikit-learn.org/1.7/user_guide.html

Wang, Y., Zhai, H., Wang, C., Hao, Q., Cohen, N. A., Foulger, R., Handler, J. A., & Wang, G. (2025). Can you walk me through it? Explainable SMS phishing detection using LLM-based agents. In *Proceedings of the Twenty-First Symposium on Usable Privacy and Security (SOUPS 2025)* (pp. 37–56). USENIX Association. https://www.usenix.org/conference/soups2025/presentation/wang
