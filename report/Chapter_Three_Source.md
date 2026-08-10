# PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING

## CHAPTER THREE

## RESEARCH METHODOLOGY, SYSTEM ANALYSIS AND DESIGN

### 3.1 Introduction

This chapter presents the methodology used to analyse, design and develop PhishGuard AI, the phishing digital medium detection system introduced in Chapter One and situated within the literature in Chapter Two. The chapter translates the identified problem into a practical software artefact and documents how email and SMS messages move from user input to a risk-oriented decision. It covers the research design, requirements analysis, use cases, system architecture, data flow, database design, dataset preparation, feature extraction, model-development procedure, explainable rule engine, risk aggregation, implementation technologies, security and privacy controls, and testing plan.

The work is an applied computing project rather than a population survey. Its principal research product is a functional prototype that demonstrates how channel-specific statistical text classification can be combined with transparent sender, content and URL checks. Accordingly, the methodology emphasises traceability: each claimed design feature is connected to the implemented repository, each data limitation is stated explicitly, and no unverified model-performance value is supplied. The design does not treat a machine-learning score as certainty. Instead, PhishGuard AI provides decision support through a bounded triage score, named evidence, plain-language guidance and recommended actions.

### 3.2 Research Design

#### 3.2.1 Applied Design-Science Orientation

The project adopted an applied design-science orientation. Design science is appropriate where the study seeks to solve an identified problem by constructing and evaluating an artefact, rather than only observing or describing a phenomenon. Peffers et al. (2007) organise design-science work around problem identification, definition of solution objectives, design and development, demonstration, evaluation and communication. These stages correspond to the present project as follows: the phishing problem and user need were defined in Chapters One and Two; solution requirements were derived from the threat and literature analysis; the PhishGuard AI web prototype was designed and implemented; representative email and SMS inputs support demonstration; functional and model-oriented checks provide evaluation; and Chapters One to Five communicate the work.

This orientation also prevents the software itself from being mistaken for the whole research contribution. The artefact includes the trained channel-specific classifiers, evidence rules, web interface, persistence structure and user guidance, while the research contribution includes the documented design rationale, constraints and evaluation method. The prototype is therefore assessed against explicit requirements and known limitations rather than promoted as a production cybersecurity service.

#### 3.2.2 Iterative and Incremental Development

An iterative and incremental process was used to organise development. Instead of attempting to implement all functions in one pass, the problem was divided into connected increments: input capture and validation; email text classification; SMS text classification; sender and domain inspection; URL and content-rule analysis; risk aggregation; result presentation; persistence; and automated checking. Each increment could be examined against previous behaviour before subsequent components were integrated.

This approach was selected because phishing indicators interact. For example, urgency is not automatically malicious, a legitimate security-awareness notice may contain words such as “password” and “OTP,” and a model can react to routine words such as “bank” or “payment.” Iteration made it possible to refine such cases by adding negation handling, awareness-message checks, context credit and minimum-risk controls. The process therefore prioritised observable user-facing behaviour over uncontrolled addition of keywords.

#### 3.2.3 CRISP-DM-Informed Machine-Learning Workflow

The model-development strand was informed by the Cross-Industry Standard Process for Data Mining (CRISP-DM). CRISP-DM structures data-mining work into business understanding, data understanding, data preparation, modelling, evaluation and deployment (Chapman et al., 2000). In this project, business understanding concerned the need to help a user triage suspicious digital messages. Data understanding involved identifying the available email and SMS fields and label distributions. Data preparation constructed a single text representation per record and normalised the input. Modelling used TF-IDF vectors and Logistic Regression. Evaluation was designed around classification metrics, error analysis and scenario-based behaviour. Deployment serialised the email and SMS vectorizer–classifier pairs for use by the Django application.

CRISP-DM was used as a methodological guide rather than as a claim of complete production machine-learning operations. In particular, the repository does not provide a verified provenance record or portable copy of the external email training CSV files. The SMS corpus is bundled and reproducible, but the email dataset must be documented and revalidated before final performance claims can be made. This limitation is carried forward into the evaluation plan.

[[FIGURE 3.1: DEVELOPMENT METHODOLOGY]]

**Figure 3.1:** Iterative design-science and CRISP-DM-informed methodology for PhishGuard AI

The framework in Figure 3.1 shows two coordinated tracks. The system-development track proceeds from problem definition to requirements, architecture, implementation and verification. The machine-learning track proceeds from channel data understanding to preparation, feature construction, model fitting and evaluation. The tracks converge in the hybrid prototype, after which evidence from testing and evaluation informs refinement. The loop is a human-led development cycle; the deployed prototype does not retrain itself from user submissions.

### 3.3 Requirements Elicitation and System Analysis

#### 3.3.1 Sources of Requirements

Requirements were derived through document and artefact analysis rather than a fabricated questionnaire. The sources comprised the problem statement and objectives in Chapter One, findings and gaps identified in Chapter Two, the operational characteristics of email and SMS, the UCI SMS Spam Collection documentation, and the PhishGuard AI repository’s Django application code, training scripts, templates and automated tests (Jesutofaye, 2026). Direct repository inspection was especially important because it distinguished implemented behaviour from aspirational features. Table 3.1 records the evidence used and its role.

[[TABLE 3.1 START]]
| Evidence source | Information extracted | Design use |
| Chapter One problem and objectives | Need for accessible email/SMS triage, understandable evidence and safety guidance | Defined scope and success criteria |
| Chapter Two literature | Channel shift, explainability need, dataset limitations, robustness and usability gaps | Motivated separate models and hybrid evidence |
| Application forms, views and templates | Actual input fields, validation, result structure and interaction flow | Specified functional and interface requirements |
| Analyzer and sender-intelligence modules | Implemented content, sender, URL, scoring and explanation logic | Documented system decision rules |
| Training scripts and saved artefacts | Text construction, split, balancing, TF-IDF and Logistic Regression settings | Defined reproducible model procedure and limitations |
| SMS corpus documentation | Record count, labels, class distribution, source and licence notice | Established the verifiable SMS data baseline |
| Automated test suite | Expected safe, suspicious, error-handling and presentation behaviour | Informed the verification matrix |
[[TABLE 3.1 END]]

**Table 3.1:** Requirements-evidence sources for PhishGuard AI

No human participant data were collected for this chapter. Future usability testing involving participants would require an approved protocol, informed consent, minimal collection of personal data and appropriate institutional guidance.

#### 3.3.2 Stakeholders and Operating Context

The primary stakeholder is an end user who has received an email or SMS and wants an understandable preliminary assessment before deciding whether to click, reply, pay or disclose information. The user may have limited cybersecurity expertise, so the interface must accept familiar message fields and return plain-language findings rather than only a technical class label. A secondary stakeholder is the project administrator or developer, who installs dependencies, prepares the database, trains or replaces model artefacts, maintains recognised-domain lists and reviews test behaviour. The third stakeholder is an evaluator or researcher who needs traceable methodology, repeatable test cases and clear limits on the meaning of results.

The assumed operating context is a browser accessing a Django web application. The user manually copies a message into the form and selects the email or SMS channel. The system does not connect directly to the user’s mailbox, telecom operator, bank, Domain Name System, threat-intelligence feed or messaging account. It therefore evaluates only the sender text, message text and links supplied by the user. It cannot verify delivery headers, SPF, DKIM, DMARC, DNS ownership, live URL content, certificate history or telephone-network identity.

#### 3.3.3 Analysis of the Existing Approach

Before the proposed system, a non-specialist user commonly depended on manual judgement, generic spam filters or isolated keyword rules. Manual judgement can miss carefully written attacks and may be influenced by branding, urgency or familiarity. Provider-side filters are useful but often conceal their reasoning and may not support a message copied from another channel. Isolated keyword rules can flag legitimate security notices because the same vocabulary appears in both warnings and attacks. A single text classifier can also produce false positives or fail when the incoming channel and distribution differ from its training data.

These limitations informed four design decisions. First, email and SMS are processed as distinct modes because their fields, sender conventions and language distributions differ. Second, the statistical model is combined with independent, named evidence rather than used as the sole verdict source. Third, a warning must have an explanation visible to the user; model evidence without an explainable indicator is capped within the Low Risk band. Fourth, the system returns cautious guidance because neither a low-risk result nor a high model confidence constitutes proof of legitimacy or fraud.

#### 3.3.4 Proposed System Overview

The proposed system is PhishGuard AI, a Django-based academic prototype for detecting phishing indicators in email and SMS. In email mode, it accepts a sender email address, an optional subject and a message body. In SMS mode, it accepts a phone number, short code or alphanumeric sender identifier and a message body; the subject is removed from processing. After validation, the view checks that the corresponding saved model is available and invokes the hybrid analyzer. The analyzer selects the channel-specific TF-IDF/Logistic Regression pair, extracts local rule evidence, combines the evidence under bounded scoring controls, and creates the verdict, explanations and recommendations. The result and selected metadata are stored locally through the `ScannedEmail` model and presented in the browser.

### 3.4 Requirements Specification

#### 3.4.1 Functional Requirements

Functional requirements specify what the system must do. The implemented scope is summarised in Table 3.2. Each identifier is written so it can later be connected to a test case or Chapter Four observation.

[[TABLE 3.2 START]]
| ID | Functional requirement | Verification condition |
| FR-01 | Allow the user to choose email or SMS analysis mode | The selected mode controls the visible fields and backend analysis mode |
| FR-02 | Accept and validate channel-appropriate sender and message fields | Invalid or empty submissions display specific errors and are not analysed |
| FR-03 | Remove the email-only subject from SMS processing | SMS analysis receives an empty subject regardless of stale form content |
| FR-04 | Load a separate saved vectorizer and classifier for each channel | Email and SMS resolve to different artefact paths and objects |
| FR-05 | Calculate phishing-class probability from message text | The selected classifier returns a class-aware probability |
| FR-06 | Inspect content for explainable social-engineering indicators | Triggered requests, pressure, threats or lures are named in the result |
| FR-07 | Inspect email sender syntax, domain form and organisation consistency | Sender findings are returned without claiming live authentication |
| FR-08 | Extract and inspect HTTP(S) links | Shorteners, raw-IP hosts, @ obfuscation, selected TLDs and punycode are identified |
| FR-09 | Aggregate ML and rule evidence into a bounded risk score | Output remains between 0 and 100 and maps to the documented bands |
| FR-10 | Present a verdict, reasons, safe signals and recommended actions | Result wording changes according to channel and risk level |
| FR-11 | Handle missing/corrupt models and unexpected errors without issuing a false verdict | A meaningful error is displayed and analysis is not represented as completed |
| FR-12 | Store the submitted message and analysis metadata locally | A `ScannedEmail` record is created after successful analysis |
| FR-13 | Permit another analysis without requiring user authentication | The analyze-another action returns to the analysis form |
[[TABLE 3.2 END]]

**Table 3.2:** Functional requirements

#### 3.4.2 Non-Functional Requirements

Non-functional requirements define the expected quality and operating constraints of the prototype. They are not all claims of production readiness. Rather, they identify the qualities the prototype supports and the controls needed before public deployment.

[[TABLE 3.3 START]]
| ID | Quality attribute | Requirement |
| NFR-01 | Usability | Use familiar email/SMS labels, readable verdicts, visible field errors and actionable guidance |
| NFR-02 | Explainability | Every warning that reaches the interface must include at least one stated, user-readable reason |
| NFR-03 | Reliability | Reject invalid input, distinguish processing failure from a threat verdict, and keep scores within defined limits |
| NFR-04 | Maintainability | Separate forms, views, classifier, analyzer, sender intelligence, recognised domains and templates into modular components |
| NFR-05 | Performance | Cache loaded model artefacts and perform local inference without calling external threat services |
| NFR-06 | Portability | Use documented Python dependencies, Django conventions and SQLite for a self-contained development prototype |
| NFR-07 | Security | Retain Django CSRF middleware and token, validate lengths and formats, and avoid rendering raw exceptions to the user |
| NFR-08 | Privacy | Clearly disclose server-side processing and persistence, minimise retention, restrict database access and provide deletion controls before real deployment |
| NFR-09 | Auditability | Preserve source-controlled training scripts, scoring constants, artefact names and automated test cases |
| NFR-10 | Responsible use | Present the output as triage assistance, not proof or an autonomous basis for punitive decisions |
[[TABLE 3.3 END]]

**Table 3.3:** Non-functional requirements

#### 3.4.3 Constraints and Assumptions

The first constraint is data availability. The bundled SMS corpus is present and documented, while the external email source files and their portable paths are not included. Consequently, the SMS training route can be reproduced from the repository, but the email dataset provenance, final sample count and achieved hold-out metrics require verified evidence. The second constraint is that the system performs static, local analysis. It does not visit links or query external reputation services. The third is that the recognised-domain map is finite and manually maintained. A domain’s absence is intentionally neutral, and a recognised domain provides only contextual credit rather than a guarantee.

The fourth constraint is language and distribution. The bundled SMS corpus consists of older English-language messages gathered from several public research sources. It is useful for demonstrating spam-oriented text classification but does not by itself represent current Nigerian smishing, multilingual communication, adversarial obfuscation or all legitimate transactional messages. The fifth constraint is the development configuration: SQLite, a development secret key, `DEBUG=True` and local allowed hosts are unsuitable for production. The sixth is that results can contain false positives and false negatives. Users must independently verify consequential requests.

#### 3.4.4 Use-Case Model

[[FIGURE 3.2: USE-CASE MODEL]]

**Figure 3.2:** Use-case model for PhishGuard AI

Figure 3.2 identifies two actors. The end user selects a channel, enters a message, submits it for analysis, reviews the result and chooses a recommended safety action. The administrator/developer maintains model artefacts and reference lists, prepares the database and executes verification procedures. “Validate input” is included in “Analyse message” because analysis cannot proceed without a valid form. “Select channel model,” “inspect explainable evidence” and “aggregate risk” are also included system behaviours. Error presentation extends analysis when a model is missing, corrupt or another controlled failure occurs.

[[TABLE 3.4 START]]
| Use case | Actor and precondition | Main flow | Alternative/exception flow |
| UC-01 Select channel | User; analysis page is available | Select Email or SMS; form adjusts fields | Query-string mode may preselect SMS |
| UC-02 Submit message | User; appropriate fields are available | Enter sender, optional email subject and body; submit | Field error returned for invalid sender, empty body or excessive length |
| UC-03 Analyse message | User; form is valid and channel model exists | Route text to model; extract evidence; aggregate risk | Stop and show model/error message without issuing a verdict |
| UC-04 Review result | User; analysis completed | Read verdict, score where shown, reasons, details and recommendations | Low Risk displays safe signals and caution rather than a guarantee |
| UC-05 Maintain artefacts | Administrator/developer; authorised repository access | Train/replace channel model and update controlled lists | Preserve existing artefact if retraining evidence is incomplete |
| UC-06 Verify system | Administrator/evaluator; test environment prepared | Execute automated tests and documented evaluation protocol | Record failures and refine before release |
[[TABLE 3.4 END]]

**Table 3.4:** Use-case descriptions

### 3.5 System Design

#### 3.5.1 Architectural Design

PhishGuard AI uses a layered server-rendered web architecture. The presentation layer contains the landing page, analysis form and result view. The application-control layer comprises Django URL routing, mode-aware form validation and request handling. The analysis layer contains the model classifier, rule analyzer, sender intelligence, recognised-domain mapping and URL checks. The data/resource layer contains the independent serialized model artefacts, the bundled SMS dataset and SQLite persistence.

[[FIGURE 3.3: SYSTEM ARCHITECTURE]]

**Figure 3.3:** Layered system architecture of PhishGuard AI

A browser request reaches the Django URL dispatcher and then the appropriate view. For a valid POST request, the form supplies cleaned fields to the controller. The controller selects the matching model channel and invokes the analysis service. The analysis service combines four evidence sources: statistical text evidence; content patterns; sender/domain evidence; and URL evidence. It returns a structured Python dictionary containing labels, probabilities, score, evidence features, explanations and recommendations. The view normalises values for presentation, writes a local scan record and renders the result template. Since inference and rule analysis occur on the server, browser-side code does not hold the model.

The architecture is deliberately modular. The classifier does not need to know the presentation structure; the sender-intelligence module does not assign the final verdict; and the view does not encode the feature weights. This separation supports testing and limits the effect of changes. For example, a future classifier can preserve the analyzer interface, while a future database can replace SQLite without rewriting the feature extractors.

[[TABLE 3.5 START]]
| Component | Repository location | Principal responsibility | Interface/output |
| URL configuration | `email_sentinel/urls.py`, `detector/urls.py` | Route landing, analysis and administration requests | Django URL patterns |
| Form validation | `detector/forms.py` | Validate channel, sender, subject and body; remove SMS subject | Cleaned form data or field errors |
| Request controller | `detector/views.py` | Check model state, invoke analyzer, normalise result, persist and render | HTTP response and optional scan record |
| Channel classifier | `detector/engine/classifier.py` | Cache and load model pair; compute class-aware probability and confidence | Prediction dictionary |
| Hybrid analyzer | `detector/engine/analyzer.py` | Extract evidence, apply safeguards, aggregate risk and construct guidance | Structured analysis dictionary |
| Sender intelligence | `detector/engine/sender_intelligence.py` | Parse local sender text, detect format anomalies and brand mismatch | Sender details and weighted findings |
| Recognised domains | `detector/engine/legit_sources.py` | Supply controlled contextual allow-list | Boolean trusted-domain context |
| Persistence model | `detector/models.py` | Define fields for submitted content and analysis metadata | `ScannedEmail` record |
| Presentation templates | `detector/templates/detector/` | Render responsive form, results and guidance | HTML/CSS/JavaScript interface |
| Training scripts | `detector/train_multi_csv.py`, `detector/train_sms_csv.py` | Prepare channel data and serialize vectorizer/classifier pairs | `.joblib` artefacts |
[[TABLE 3.5 END]]

**Table 3.5:** Major system components

#### 3.5.2 Data-Flow Design

[[FIGURE 3.4: DATA-FLOW DIAGRAM]]

**Figure 3.4:** Level-1 data-flow diagram for message analysis

Figure 3.4 follows a submitted message through six processes. Process 1.0 validates and normalises user input. Process 2.0 chooses the email or SMS model. Process 3.0 transforms message text and obtains model evidence. Process 4.0 extracts explainable content, sender and URL evidence. Process 5.0 aggregates all evidence and applies score safeguards. Process 6.0 constructs the result, stores the successful analysis record and sends the response to the user. The saved model files and recognised-domain list are read-only resources during inference; the local scan database is written after successful analysis.

The data-flow boundary is significant. The message is not sent to an external AI or threat-intelligence service by the implemented code. Nevertheless, it is transmitted from the browser to the Django server and then stored in SQLite, so it is inaccurate to describe the present implementation as browser-only or non-persistent. A production privacy notice must disclose this exact flow.

#### 3.5.3 Analysis-Process Design

[[FIGURE 3.5: HYBRID ANALYSIS ACTIVITY]]

**Figure 3.5:** Activity flow for hybrid email and SMS analysis

The analysis activity begins only after validation. If the channel model is unavailable or cannot be loaded, the request terminates with an error state rather than a risk result. When the model is available, the channel text is transformed with its fitted TF-IDF vectorizer, and the classifier supplies the probability of the phishing class and confidence in its predicted class. In parallel at the conceptual level, the analyzer extracts content, sender and URL evidence. Duplicate evidence types are removed so repeated keywords do not multiply the same finding without limit.

The model contribution is then combined with capped evidence points and any permitted trusted-context credit. After the initial arithmetic, decision safeguards impose explanatory floors or caps. A model-only score with no rule evidence cannot leave the Low Risk band. Conversely, an unverifiable link, direct request for sensitive data or strong deceptive combination cannot be diluted into a low-risk result merely because the statistical model is calm. The final bounded score is classified, and channel-appropriate wording is generated.

#### 3.5.4 Database and Persistence Design

The application defines one project-specific persistence entity named `ScannedEmail`. Despite its historical name, the entity may receive both email and SMS analyses. The design stores the user-supplied content and a concise set of analysis fields. Django supplies the primary key automatically through the configured `BigAutoField` default. Figure 3.6 and Table 3.6 document the implemented logical structure.

[[FIGURE 3.6: DATA MODEL]]

**Figure 3.6:** Logical data model for stored scan records

[[TABLE 3.6 START]]
| Field | Implemented type/limit | Purpose | Privacy or integrity note |
| `id` | Automatic primary key | Uniquely identifies a scan | Do not expose predictable identifiers unnecessarily |
| `subject` | Character, maximum 512, blank allowed | Stores email subject; empty for SMS | May contain personal or confidential text |
| `sender` | Character, maximum 255 | Stores supplied email address, number or sender ID | Required persistence field and may constitute contact/identifier data |
| `body` | Text, blank allowed at model layer | Stores submitted message content; form validation requires a non-empty body | May contain credentials, financial data or private correspondence |
| `rules_triggered` | Text, blank allowed | Stores textual explanation of triggered rules | Keep terminology stable for auditability |
| `ml_label` | Character, maximum 50, blank allowed | Stores the machine-learning label | Must not be treated as ground truth |
| `final_label` | Character, maximum 50 | Stores final risk-oriented label | Represents prototype decision support |
| `score` | Float, default 0.0 | Stores bounded aggregate score | Triage score, not calibrated fraud probability |
| `created_at` | Date-time, automatically added | Records when analysis occurred | Apply a defined retention and deletion policy |
[[TABLE 3.6 END]]

**Table 3.6:** Data dictionary for `ScannedEmail`

SQLite was chosen for simple local deployment and minimal configuration. It is appropriate for a single-node academic prototype but not sufficient evidence of production scalability, tenancy isolation, backup governance or access-control maturity. The repository requires migrations to be generated and applied during setup. Before public use, the schema should also include a channel field, explicit retention state and, where justified, pseudonymised or redacted storage rather than full message content.

#### 3.5.5 User-Interface Design

The interface follows a direct input–analysis–feedback sequence. The landing page introduces email and SMS entry points. The analysis page uses channel tabs and a hidden message-type control. Email mode shows sender address, optional subject and message body. SMS mode changes the sender prompt, hides and clears the subject, and accepts a phone number, short code or sender identifier. Validation errors are placed near the relevant field, and the form includes a CSRF token.

Result presentation is channel-aware. Email output can show the three-level risk state, the bounded threat score, reasons, links, sender analysis, safe signals and recommended actions. SMS uses the simpler user-facing verdicts “Message Appears Safe” and “Message Appears Suspicious,” masks numeric sender display, hides the numerical threat score, and organises findings around link, credential, OTP, urgency, threat and money-lure fields. For both channels, Low Risk includes cautionary language because absence of detected evidence is not proof of safety.

Colour reinforces green, amber and red states but is not the only carrier of meaning; each state also has a title, icon and text. Error states are visually and semantically separate from verdict states. This distinction reduces the risk that a failed model load or unexpected exception will be interpreted as a security classification.

### 3.6 Dataset Acquisition and Understanding

#### 3.6.1 SMS Dataset

The SMS model uses the bundled SMS Spam Collection v.1. The repository copy contains 5,574 English SMS messages: 4,827 labelled `ham` and 747 labelled `spam`, corresponding to approximately 86.6% legitimate messages and 13.4% spam messages. Almeida et al. (2011) compiled the collection from several public or research sources, including manually extracted Grumbletext complaints, legitimate messages associated with Caroline Tagg’s research, a subset of the NUS SMS Corpus, and an earlier SMS spam corpus.

The collection provides a reproducible project baseline because both the data file and its readme are present. However, its original `spam` label is broader than phishing. Some promotional or unsolicited messages may be spam without requesting credentials or impersonating an organisation. The collection is also older and geographically mixed. The trained SMS classifier should therefore be described accurately as a spam-informed component within a broader smishing-evidence system, not as proof of comprehensive modern phishing coverage.

#### 3.6.2 Email Dataset

The email training script is designed to combine multiple CSV files. In the merged data frame, it searches for the exact columns `sender`, `subject`, `body` and `urls`, concatenates whichever of those columns are available into a text representation, and requires a `label` column whose values can be converted to integers. It then selects records labelled 0 and 1 and down-samples both groups to the minority-class size before model fitting.

The actual external email CSV files referenced during development and a portable dataset manifest are not versioned in the repository. Their machine-specific paths cannot establish public reproducibility. Therefore, the final source names, licensing terms, original and cleaned record counts, duplicate handling, date range, geography, class balance and final hold-out distribution remain to be supplied from verified records:

- **[Insert verified email dataset title(s), publisher/source URL(s) and licence(s).]**
- **[Insert original record count, excluded record count and final class counts.]**
- **[Insert documented duplicate and leakage-control procedure.]**

No email accuracy, precision, recall, F1-score or confusion-matrix values are asserted in this chapter. The model artefact confirms the implemented estimator form and 20,000-feature vocabulary, but it does not replace dataset provenance or an independently recorded evaluation.

#### 3.6.3 Labels and Unit of Analysis

The unit of analysis is one message. For SMS training, the source labels `ham` and `spam` are explicitly mapped to binary values 0 and 1. For email training, the script requires the merged `label` column to be numeric and uses 0 as legitimate and 1 as scam; it does not implement a mapping for textual label variants. This means externally supplied email CSVs must already use the required binary convention. Although binary harmonisation enables model fitting, it can hide differences between spam, phishing, fraud and benign marketing. A future dataset manifest should preserve the source label alongside the verified binary mapping for audit.

The predicted positive class is treated as the phishing-risk class by the classifier interface. The loader reads `model.classes_` to locate class 1 rather than assuming a fixed probability-column position. This class-aware handling reduces a common implementation error in which confidence in the predicted class is confused with probability of phishing.

### 3.7 Data Preparation

#### 3.7.1 Text Construction and Normalisation

For email records, available sender, subject, body and URL fields are converted to text and concatenated with spaces. This design permits model fitting even when source CSV schemas differ, but it also means the model vocabulary may contain sender or URL tokens as ordinary lexical features. At inference time, the application provides the email subject and body to the model, while sender/domain and URLs receive additional explicit analysis through the rule engine. The training–inference field alignment should therefore be audited when the email datasets are restored.

For SMS, each tab-separated line is parsed into a label and message. Rows with missing values are dropped, consecutive whitespace in message text is collapsed, and any label other than `ham` or `spam` causes training to stop with a validation error. At inference, SMS has no subject, so the message body alone is supplied to the SMS vectorizer. The Django form strips surrounding whitespace and limits the body to 10,000 characters before analysis.

#### 3.7.2 Class Balancing and Data Split

The SMS script divides the corpus into 80% training and 20% test partitions with stratification so both partitions retain the original label proportion. It then relies on `class_weight="balanced"` in Logistic Regression to compensate for class imbalance. The email script first down-samples each class to the size of the minority class, shuffles the balanced set, and applies an 80/20 train–test split. Both scripts use a fixed random state of 42 for repeatability.

These strategies solve different problems and should not be conflated. Class weighting preserves all SMS examples while changing the estimator’s class penalties. Downsampling the email majority class changes the training distribution and can discard useful benign diversity. The eventual evaluation must report metrics on a hold-out set that reflects the intended operating distribution as well as any balanced development set.

#### 3.7.3 Data-Quality and Leakage Controls

Input handling differs by channel. The SMS script drops rows with missing fields and rejects unexpected labels, whereas the email script fills missing cells with empty strings and requires labels that can be cast to integers. Neither script provides a documented near-duplicate analysis, source-grouped splitting procedure or chronological split. Randomly placing duplicate or template-near messages in both training and test partitions can inflate apparent performance. A stronger retraining procedure should compute exact hashes after normalisation, detect high-similarity templates, group records by campaign/source, and perform temporal or source-held-out evaluation where timestamps or source identifiers exist.

Personally identifying content should be minimised during dataset preparation. Public datasets must be used according to their licences, and private operational messages should not be added without a lawful basis, consent where applicable, secure handling and de-identification. Training logs should store aggregate metadata rather than raw messages whenever possible.

### 3.8 Feature Extraction and Model Development

#### 3.8.1 TF-IDF Representation

Both channel models represent text using term frequency–inverse document frequency (TF-IDF). TF-IDF increases the contribution of terms that are important within a message but not ubiquitous across the corpus. Following standard information-retrieval notation (Manning et al., 2008), a simplified weight for term \(t\) in document \(d\) is:

**TF-IDF(t,d) = TF(t,d) × log(N / DF(t))**

where \(TF(t,d)\) is the frequency of term \(t\) in document \(d\), \(N\) is the number of documents, and \(DF(t)\) is the number of documents containing the term. The scikit-learn implementation applies its documented smoothing and normalisation defaults unless a script overrides them (Pedregosa et al., 2011; scikit-learn developers, 2025).

Unigrams capture individual tokens such as “verify,” while bigrams capture short sequences such as “act now” or “account suspended.” The email vectorizer uses unigrams and bigrams, a maximum of 20,000 features, and English stop-word removal. The SMS vectorizer uses unigrams and bigrams and a maximum of 15,000 features without the English stop-word option. Inspection of the serialized artefacts confirms fitted vocabularies of 20,000 and 15,000 features respectively.

#### 3.8.2 Logistic Regression Classifier

Logistic Regression estimates the probability of the positive class from a weighted linear combination of the TF-IDF features. For a feature vector \(x\), coefficient vector \(β\) and intercept \(β₀\), the binary logistic function can be expressed as:

**P(y = 1 | x) = 1 / (1 + e^(−(β₀ + βᵀx)))**

A probability threshold can map the estimate to class 0 or class 1. The PhishGuard AI classifier retains the estimator’s predicted label but separately obtains the probability associated with class 1. It also calculates confidence in the predicted class. If the predicted label is phishing, confidence equals phishing probability; if the predicted label is safe, confidence equals one minus phishing probability. This distinction ensures that a highly confident safe prediction is not accidentally displayed as a high phishing score.

Logistic Regression was selected because it is efficient with sparse high-dimensional text, supplies probabilistic output and produces a relatively compact artefact. Its coefficients are also more inspectable than many deep architectures, although the current user interface explains the rule evidence rather than displaying model coefficient attributions.

#### 3.8.3 Channel Training Configuration

[[TABLE 3.7 START]]
| Parameter | Email model design | SMS model design |
| Source data | External merged CSV files; provenance pending verified manifest | Bundled SMS Spam Collection v.1 |
| Text fields | Available sender + subject + body + URL columns | SMS message body |
| Label handling | Numeric binary labels required: 0=legitimate, 1=scam | `ham`→0; `spam`→1 |
| Balancing | Downsample both classes to minority-class size | Preserve records; class-weighted estimator |
| Split | 80/20 train–test, random state 42 | Stratified 80/20 train–test, random state 42 |
| Vectorizer | TF-IDF; lowercase; (1,2)-grams; maximum 20,000 features; English stop words | TF-IDF; lowercase; Unicode accent stripping; (1,2)-grams; `min_df=1`; maximum 15,000 features |
| Estimator | Logistic Regression; `max_iter=200`; `n_jobs=-1` | Logistic Regression; `max_iter=2000`; `class_weight="balanced"`; `random_state=42` |
| Saved file | `detector/engine/email_model.joblib` | `detector/engine/sms_model.joblib` |
[[TABLE 3.7 END]]

**Table 3.7:** Implemented channel-model training configuration

The fitted vectorizer and classifier are serialized together using Joblib. During application use, the loader resolves the channel name to its artefact path and caches the loaded pair. Caching avoids disk deserialization for every request. The system checks for a missing or unreadable artefact before analysis and shows a controlled message when retraining or restoration is required.

#### 3.8.4 Reproducibility Procedure

A reproducible training run should create a clean virtual environment, install the pinned project dependencies, record the dataset checksum and licence, execute the channel script, capture its random seed and package versions, and save the evaluation report alongside the artefact. The artefact should have a version identifier and cryptographic checksum. For email, machine-specific absolute paths should be replaced by configuration or command-line arguments, and a dataset manifest should be committed without exposing restricted raw data.

The saved models currently establish what the application loads, not a full model card. Before a final release, a model card should record intended use, excluded use, training sources, date range, language, class definitions, split method, metrics, subgroup or source checks, known failure modes and contact for maintenance.

### 3.9 Explainable Evidence Extraction

#### 3.9.1 Content Evidence

The rule engine examines the subject and body for social-engineering patterns. It detects pressure language, threats of loss or account action, explicit requests for credentials or authentication information, personal or banking-data requests, payment redirection and unexpected money, grant or prize claims. SMS receives an additional explicit pattern for requests to share or provide an OTP or verification code. The patterns focus on actions and combinations rather than merely counting security vocabulary.

Evidence is deduplicated by type. If a message repeats “act now” several times, the urgency type contributes once rather than accumulating points for every repetition. This design makes the score represent distinct evidence categories and limits trivial score inflation. Content findings are written in complete phrases for use in the interface.

#### 3.9.2 Negation and Security-Awareness Handling

Legitimate institutions often state that they will never request a PIN or password. A naive keyword system can label such warnings as phishing. PhishGuard AI therefore looks for negation and awareness cues within bounded clauses. Sentence boundaries and contrastive connectors such as “however” or “but” stop an earlier reassurance from suppressing a later demand. Thus, “We will never ask for your PIN” can be treated as awareness content, whereas “We will never ask for your PIN; however, confirm your card number now” is still examined as a demand.

An awareness classification does not suppress technically deceptive links. If an apparent warning contains a shortened, raw-IP, punycode, obfuscated or selected higher-risk link, the link evidence remains active. This prevents an attacker from hiding a request behind copied anti-fraud language.

#### 3.9.3 Sender and Domain Evidence

For email, sender analysis parses the supplied address into username, domain and top-level label. It checks malformed structure, unusually long domains, excessive hyphens, excessive numbers and random-looking consonant-heavy forms. A small Levenshtein-distance routine normalises common digit substitutions and compares domain labels with defined brand names to detect one-edit look-alikes. The module also checks whether message text claims to represent a defined organisation while the supplied domain is inconsistent or uses a public email provider.

These checks are local heuristics. They do not authenticate the sender, query DNS or evaluate SPF, DKIM or DMARC. A syntactically consistent unknown domain is neutral rather than automatically suspicious. A recognised-domain list may support contextual credit, but it does not guarantee safety because sender text can be forged and legitimate accounts can be compromised. For SMS, the form validates numeric numbers, short codes and alphanumeric sender identifiers, while the analyzer does not claim telecom-network verification.

#### 3.9.4 URL Evidence

The analyzer extracts complete HTTP and HTTPS links from the supplied text and strips common sentence punctuation from the end. The hostname is reduced to its registered domain using `tldextract`. The system then checks for a known shortening service, raw IP address in place of a domain, an `@` character in the authority component, selected higher-risk top-level labels and a punycode prefix. The implemented method does not open the URL, execute content, follow redirects or contact reputation providers; this reduces exposure during local analysis but also limits verification.

#### 3.9.5 Evidence Weights

[[TABLE 3.8 START]]
| Evidence category | Implemented point value | Interpretation |
| Unusually long sender domain | 8 | Low-severity domain-form context |
| Urgency; excessive sender hyphens/numbers; random-looking domain | 10 each | Supporting context, insufficient alone for a strong conclusion |
| Threat; money/reward lure | 15 each | Social-engineering pressure or incentive |
| Personal-data request; malformed sender; organisation mismatch; selected risky TLD; punycode URL | 20 each | Strong request, inconsistency or technical concern |
| Credential/OTP request; payment redirection; shortened URL; @ URL obfuscation; typosquatting; public-provider impersonation | 25 each | Direct request or deceptive indicator |
| Raw-IP URL | 30 | Directly suspicious technical indicator |
| Total explainable evidence | Capped at 60 | Prevents unrestricted accumulation |
[[TABLE 3.8 END]]

**Table 3.8:** Implemented explainable-evidence points

The values in Table 3.8 are engineering severity weights, not empirically calibrated likelihood ratios. They provide an auditable decision structure for the prototype. Their calibration should be reviewed against a larger verified validation set and user consequences before operational use.

### 3.10 Hybrid Risk Aggregation and Decision Logic

#### 3.10.1 Model Contribution

The model contributes a maximum of 45 points and only the portion of phishing probability above 0.55. If \(p\) is phishing-class probability, model points \(M\) are:

**M(p) = 0, when p ≤ 0.55**

**M(p) = 45 × (p − 0.55) / (1 − 0.55), when p > 0.55**

This scaling prevents ordinary uncertainty around the decision boundary from dominating the result. The explainable evidence points \(E\) are the sum of unique finding weights capped at 60. A context credit \(C\) may be 15, 20 or 25 points when a recognised sender appears with ordinary, routine-security or safe transactional wording and there is no serious evidence. An awareness notice without serious evidence can receive a 25-point credit. Credit never cancels a serious request, deceptive sender or unverifiable link.

The preliminary score is:

**S₀ = clamp(M + E − C, 0, 100)**

where `clamp` bounds the value to the inclusive range 0–100. The final score applies the safeguards in Section 3.10.2 before a second clamp.

#### 3.10.2 Decision Safeguards and Risk Bands

[[TABLE 3.9 START]]
| Control | Implemented action | Rationale |
| No explainable evidence | Cap score at 39 | Model alone cannot produce an unexplained warning |
| Unverifiable URL evidence | Floor score at 40 | Link requires independent review even if model is calm |
| Credential, OTP, personal-data or payment request | Floor score at 40 | Sensitive unsolicited request must be verified |
| Typosquatting or public-provider impersonation | Floor score at 70 | Sender deception is strong evidence |
| Sensitive-data/payment request plus urgency, threat or money lure | Floor score at 70 | Combined social-engineering pattern indicates high risk |
| Unverifiable link plus pressure/threat/lure or data request | Floor score at 70 | Classic “click or act now” combination |
| Final bound | Clamp to 0–100 | Maintains a stable result range |
[[TABLE 3.9 END]]

**Table 3.9:** Risk-aggregation safeguards

The final bands are 0–39 for **Low Risk**, 40–69 for **Suspicious**, and 70–100 for **High Risk**. Low Risk means that the available text and sender evidence did not produce strong observed indicators; it does not certify the message. Suspicious means the message should be independently verified before action. High Risk means the supplied content contains a strong deceptive indicator or combination and should not be acted on without trusted verification.

The score is a transparent triage index and must not be labelled as the probability that a message is fraudulent. The model’s phishing probability, the model’s confidence in its selected class and the hybrid score are three different quantities. The implementation keeps them separate internally even though the email interface prioritises the hybrid threat score.

#### 3.10.3 Algorithm

The principal procedure can be expressed as the following implementation-aligned pseudocode:

1. Receive `message_type`, `sender`, optional `subject` and `body`.
2. Validate mode, sender format, required body and maximum lengths.
3. If mode is SMS, set `subject` to an empty string.
4. Confirm that the corresponding serialized model exists and can be loaded.
5. Build channel text from subject and body.
6. Transform text with the channel’s fitted TF-IDF vectorizer.
7. Obtain predicted label, phishing-class probability and predicted-class confidence.
8. Extract content evidence with negation and awareness handling.
9. Extract email sender/domain evidence where applicable.
10. Extract URL evidence without visiting the URL.
11. Deduplicate evidence by type and cap its total at 60.
12. Calculate bounded model points above the 0.55 floor.
13. Apply permitted trusted/awareness context credit only when serious evidence is absent.
14. Calculate preliminary score and apply explanatory floors or caps.
15. Map score to Low Risk, Suspicious or High Risk.
16. Build channel-appropriate reasons, safe signals, details and recommended actions.
17. Persist the successful scan record locally.
18. Render the result; on a controlled failure, render an error rather than a verdict.

#### 3.10.4 Output Construction

For email, the result dictionary includes the final label, machine-learning label, phishing probability, model confidence, hybrid score, risk level and colour, evidence descriptions, structured features, sender explanation, detected URLs, user guidance, recommended actions and safe signals. For SMS, the same engine prepares additional plain-language fields for message type, links, masked sender display, credential request, OTP request, urgency, threat, money lure and final verdict.

Recommendations are evidence-sensitive. Link findings advise the user not to open the link and to type or use a saved official address. Credential or OTP findings advise against disclosing secrets. Sender findings recommend independent verification. Payment-redirection findings recommend confirmation using a known contact number. High Risk adds reporting and deletion guidance after necessary evidence is preserved. Low Risk still advises continued caution.

### 3.11 Implementation Environment and Tools

[[TABLE 3.10 START]]
| Technology | Version/role in repository | Justification |
| Python | Project programming language | Mature text-processing and web/ML ecosystem |
| Django | 5.2.8 server-side framework | Forms, routing, templates, ORM, CSRF middleware and structured project organisation |
| scikit-learn | 1.7.2 | TF-IDF, train–test split, Logistic Regression and evaluation utilities |
| pandas | 2.3.3 | CSV loading, field combination, filtering, balancing and shuffling |
| NumPy/SciPy | Numerical and sparse-matrix support | Underpins vectorization and estimator operations |
| Joblib | 1.5.2 | Serializes and restores channel vectorizer–classifier pairs |
| tldextract | 5.3.0 | Separates hostnames into registered-domain components |
| SQLite | Django development database | Low-configuration local persistence for the prototype |
| HTML, CSS and JavaScript | Server-rendered responsive interface | Channel switching, input presentation and readable results |
| Git and GitHub | Source and version control | Traceability of code, report sources and revisions |
[[TABLE 3.10 END]]

**Table 3.10:** Implementation technologies

Django 5.2 is a long-term support series released in 2025, while the pinned repository version is 5.2.8 (Django Software Foundation, 2025). The framework’s conventions support modular request handling and built-in CSRF protection, but framework use does not automatically make an application production-secure. Deployment settings, secrets, HTTPS, logging, database access and operational monitoring still require explicit configuration.

The development workstation must provide a compatible Python interpreter and an isolated environment. Dependencies are installed from the project requirements file. Database migrations are then generated/applied, and the development server may be started for local use. Training scripts are executed separately when model regeneration is needed; inference does not refit the models.

### 3.12 Security, Privacy and Ethical Considerations

#### 3.12.1 Input and Web Security

The form enforces a 10,000-character maximum for the message body, a 512-character maximum for the subject, and mode-aware sender length and syntax constraints. This reduces accidental oversized input and rejects malformed values before model invocation. The POST form includes Django’s CSRF token, and `CsrfViewMiddleware` is enabled. Django documents CSRF protection as a defence that requires correct middleware and token use, with HTTPS and secure deployment settings still necessary (Django Software Foundation, 2025).

The view checks model status before analysis and handles unexpected exceptions with a generic user message. It logs the failure server-side and does not convert an exception into “High Risk” or another verdict. Templates receive text through Django’s normal escaping behaviour. Before public deployment, the system should also add HTTPS redirection, secure cookies, HSTS, rate limiting, request-size limits at the web server, content-security policy, restricted administration access, structured security logging and dependency scanning.

The current settings explicitly identify themselves as development-only: the secret key is embedded, `DEBUG` is enabled and allowed hosts are local. These settings must be replaced by environment-managed secrets, `DEBUG=False`, explicit production hostnames and a production server/database arrangement. The prototype should not be exposed to untrusted public traffic in its current configuration.

#### 3.12.2 Privacy and Data Protection

Submitted messages can contain names, email addresses, telephone numbers, account identifiers, transaction details or private correspondence. The implemented view stores sender, subject, full body, rules, labels and score in SQLite. This persistence creates a privacy obligation. Nigeria’s data-protection framework emphasises fairness and transparency, purpose limitation, data minimisation, storage limitation, security and accountability (Federal Republic of Nigeria, 2023; Nigeria Data Protection Commission, 2025).

Accordingly, a real deployment should provide a clear privacy notice before submission, identify a lawful processing basis, state the purpose and retention period, restrict staff access, encrypt transport and backups, and support deletion or anonymisation. The safest default may be not to retain full message bodies at all unless a user explicitly opts into a defined review purpose. Sensitive tokens, card details and identifiers should be redacted before persistence where technically feasible. Audit logs should record events without duplicating raw message content.

The current interface says analysis is processed in the browser session and on the server for review. That wording should be strengthened to state clearly that a successful submission is stored in the local database in the present prototype. Accurate disclosure is part of ethical system design.

#### 3.12.3 Responsible Machine-Learning Use

NIST’s AI Risk Management Framework describes trustworthy AI characteristics including validity, reliability, safety, security, resilience, transparency, explainability, privacy enhancement and fairness (National Institute of Standards and Technology, 2023). PhishGuard AI supports transparency through named evidence and conservative wording, but full compliance is not claimed. The datasets can contain temporal, geographic, linguistic and class-definition bias. The old English SMS corpus may perform differently on Nigerian Pidgin, local brands, contemporary scam campaigns or adversarial misspellings.

False negatives may expose a user to fraud, while false positives may disrupt legitimate transactions or create unnecessary alarm. The system must therefore remain advisory. It should not block an account, punish a sender, report an individual to law enforcement or make another high-impact decision automatically. Users should be able to review the evidence and verify through an official channel. Evaluation must consider both aggregate metrics and meaningful failure cases.

### 3.13 Testing and Evaluation Methodology

#### 3.13.1 Verification Strategy

Testing was designed at four levels: component, integration, interface and controlled scenario behaviour. Component tests target risk-band mapping, model selection, sender parsing, URL findings, form validation and sender masking. Integration tests check that a valid form invokes the analyzer with the right channel fields, that separate artefacts are available, and that a successful result reaches persistence/rendering boundaries. Interface tests render safe, suspicious, high-risk and SMS result structures to verify that reasons and visual states match the verdict. Error-path tests ensure missing/corrupt models and unexpected failures do not become security verdicts.

[[TABLE 3.11 START]]
| Test area | Representative cases | Expected evidence |
| Validation | Empty body; malformed email; valid SMS number, short code and sender ID; length limits | Field errors; analyzer not called for invalid input |
| Channel routing | Email/SMS model paths; SMS subject clearing | Independent objects and correct analyzer arguments |
| Content logic | Urgency, credential/OTP request, personal-data request, payment redirection, awareness wording | Correct named finding or justified suppression |
| Sender/URL logic | Typosquatting, public-provider claim, neutral unknown domain, short link, raw IP | Explainable finding and appropriate floor where defined |
| Aggregation | Calm model with strong evidence; strong model with no evidence; risk boundaries | Strong evidence not diluted; unexplained warning capped; bands correct |
| Safe-context behaviour | Routine receipt, bank alert, 2FA code, anti-fraud notice | Low-risk caution and safe signals without false guarantee |
| Result layout | Email green/amber/red states; SMS safe/suspicious wording; sender masking | Correct sections shown; incompatible details hidden |
| Failure handling | Missing/corrupt model and unexpected exception | Meaningful error; no false threat verdict |
[[TABLE 3.11 END]]

**Table 3.11:** Verification matrix

The repository contains an automated Django test suite covering these behaviours. The observed execution outcome belongs in Chapter Four, where environment, date, command and result can be reported as implementation evidence rather than being pre-emptively treated as a model-performance claim.

#### 3.13.2 Model Evaluation Metrics

The test partition for each verified dataset should produce a confusion matrix with true positives (TP), true negatives (TN), false positives (FP) and false negatives (FN), taking phishing/spam as the positive class. The principal measures are:

**Accuracy = (TP + TN) / (TP + TN + FP + FN)**

**Precision = TP / (TP + FP)**

**Recall = TP / (TP + FN)**

**F1-score = 2 × (Precision × Recall) / (Precision + Recall)**

Accuracy alone is insufficient where class distributions are imbalanced. Precision reflects how many positive predictions are correct, while recall reflects how many positive cases are detected. For anti-phishing assistance, false negatives are consequential, but excessive false positives can cause alert fatigue. The F1-score balances precision and recall, while the confusion matrix keeps the underlying error counts visible. Precision–recall curves and area under the curve are also useful for imbalanced classification (Saito & Rehmsmeier, 2015).

The verified values are intentionally left open until they are reproduced from controlled data and preserved logs:

- **Email accuracy: [Insert verified result]**
- **Email precision, recall and F1-score: [Insert verified results]**
- **Email confusion matrix: [Insert verified TP, TN, FP and FN]**
- **SMS accuracy: [Insert verified result]**
- **SMS precision, recall and F1-score: [Insert verified results]**
- **SMS confusion matrix: [Insert verified TP, TN, FP and FN]**

Any reported value must identify whether it describes the text classifier alone or the complete hybrid decision system. Metrics generated on balanced email data must not be presented as expected prevalence in real inboxes.

#### 3.13.3 Robustness and External Validation

Internal random-split performance is only an initial check. A credible validation programme should include source-held-out data, temporally newer campaigns, Nigerian email and SMS examples, multilingual and code-switched messages, legitimate transactional messages, security-awareness notices, obfuscated URLs and adversarially altered words. Channel transfer should also be tested explicitly rather than assuming an email model generalises to SMS.

The evaluation set should include low-risk cases that contain security vocabulary and phishing cases that avoid urgency or links. Error analysis should classify failures by source, attack type, language, sender form and rule/model disagreement. Scoring weights and trusted-domain credit should be recalibrated only with held-out evidence. Larger real-world dataset validation is required before strong performance or deployment claims can be made.

#### 3.13.4 Usability and Acceptance Evaluation

A later user study may assess task completion, time to interpret a result, comprehension of reasons, ability to identify the recommended next step, perceived clarity and trust calibration. Participants should include users with varied technical backgrounds. The protocol should avoid exposing participants to active malicious links or collecting their real private messages. Placeholder locations for verified usability evidence will be placed in Chapter Four if such a study is approved and completed.

[[TABLE 3.12 START]]
| Acceptance criterion | Method | Pass condition |
| Channel correctness | Submit equivalent valid email and SMS forms | Each channel uses its own fields, model and output wording |
| Explainable warning | Exercise every warning-producing scenario | At least one specific reason accompanies the warning |
| Safe uncertainty | Submit routine and awareness messages | Output remains cautious and never guarantees legitimacy |
| Failure integrity | Remove/corrupt model or simulate exception | Interface reports inability to analyse, not a threat verdict |
| Score integrity | Test boundary and combined-evidence cases | Score stays 0–100 and bands/floors/caps follow specification |
| Privacy disclosure | Review form wording against actual flow | User is told that server processing and local persistence occur |
| Reproducibility | Repeat documented training/evaluation with manifest | Same configuration and materially consistent results are obtained |
| Prototype limitation | Review all result and report claims | No output presents the artefact as production-ready or infallible |
[[TABLE 3.12 END]]

**Table 3.12:** System acceptance criteria

### 3.14 Deployment and Operational Considerations

For local demonstration, the operator creates an isolated environment, installs dependencies, generates/applies database migrations and starts the Django development server. The email and SMS `.joblib` files must exist in `detector/engine`. This setup is suitable for supervised academic demonstration on a trusted workstation.

A controlled production transition would require a hardened application server, reverse proxy, HTTPS, environment-based secrets, `DEBUG=False`, an explicit host list, a managed database, role-based administrative access, encrypted backups, retention automation, rate limiting, monitoring, incident response and documented model/allow-list updates. The Public Suffix List dependency used by domain extraction should be pinned or configured for deterministic offline behaviour rather than relying unpredictably on network refresh during analysis.

Model monitoring should distinguish service health from prediction quality. Service monitoring covers load failures, latency and request errors. Quality monitoring covers drift in message language, changes in class prevalence, disagreement between model and rules, and reviewed false positives/negatives. User-submitted content must not be silently converted into retraining data. Any retraining pipeline should use separately governed, labelled and de-identified data.

### 3.15 Chapter Summary

This chapter documented the methodology, analysis and design of PhishGuard AI. An applied design-science orientation was combined with iterative development and a CRISP-DM-informed model workflow. Requirements were derived from the research problem, literature and implemented repository rather than an invented survey. The resulting design uses a Django presentation and control layer, independent email and SMS TF-IDF/Logistic Regression artefacts, local content/sender/URL evidence, bounded hybrid risk aggregation, SQLite persistence and channel-specific explanations.

The chapter also established the system’s limits. The SMS corpus is present and reproducible, but it is an older spam-oriented English dataset. The email source datasets and portable provenance manifest are unavailable, so email data counts and model metrics remain explicit placeholders. The risk score is a triage index, not a fraud probability, and no Low Risk result is a guarantee. Finally, the current repository is a development prototype whose full-message persistence, development settings and limited external validation require remediation before public deployment. Chapter Four will present the implemented interfaces, verified test evidence and only those performance results for which reproducible records are available.

## REFERENCES

Almeida, T. A., Gómez Hidalgo, J. M., & Yamakami, A. (2011). Contributions to the study of SMS spam filtering: New collection and results. In *Proceedings of the 11th ACM Symposium on Document Engineering* (pp. 259–262). Association for Computing Machinery. https://doi.org/10.1145/2034691.2034742

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.

Django Software Foundation. (2025). *Django documentation: Release 5.2*. https://docs.djangoproject.com/en/5.2/

Federal Republic of Nigeria. (2023). *Nigeria Data Protection Act, 2023*. Nigeria Data Protection Commission. https://ndpc.gov.ng/

Jesutofaye, H. J. (2026). *PhishGuard AI: Email & SMS phishing detection system* [Computer software]. GitHub. https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press. https://nlp.stanford.edu/IR-book/

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.100-1

Nigeria Data Protection Commission. (2025). *Nigeria Data Protection Act—General application and implementation directive 2025*. https://ndpc.gov.ng/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Saito, T., & Rehmsmeier, M. (2015). The precision–recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432

scikit-learn developers. (2025). *scikit-learn 1.7 user guide*. https://scikit-learn.org/1.7/user_guide.html
