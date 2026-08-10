# PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING

## CHAPTER ONE

## INTRODUCTION

### 1.1 Background of the Study

Digital communication has become integral to education, banking, commerce, government services and everyday social interaction. Email and Short Message Service (SMS) allow information to be exchanged quickly and at relatively low cost, but the same convenience also provides attackers with direct channels to potential victims. A malicious message can be distributed widely, tailored to a particular recipient, and made to resemble a communication from a bank, school, employer, delivery company or technology provider. The security problem therefore extends beyond protecting computers from malicious software; it also involves helping people judge whether apparently legitimate digital communication can be trusted.

Phishing is a form of social engineering in which an attacker uses fraudulent communication or a counterfeit digital identity to induce a victim to reveal sensitive information or perform an unsafe action. The National Institute of Standards and Technology describes phishing as an attempt to acquire sensitive data through fraudulent email or web solicitation in which the perpetrator masquerades as a legitimate business or reputable person (National Institute of Standards and Technology [NIST], n.d.). The intended outcome may be the theft of passwords, one-time passwords (OTPs), personal or banking information, money or access to an organisation’s information systems. When this deception is delivered through SMS or another text-messaging service, it is commonly called smishing.

A phishing message rarely depends on one feature alone. It may combine an urgent subject, a threatening statement, an unexpected reward, a request for credentials, a shortened or obfuscated link, and a sender identity that resembles a known organisation. Other attacks are deliberately restrained and professionally written so that obvious spelling errors and exaggerated claims are absent. Consequently, a dependable assessment cannot be based only on the presence of isolated words such as “urgent” or “verify.” The relationship among the message content, sender identity, links and requested action must also be considered.

Recent evidence indicates that phishing remains persistent and continues to spread across communication channels. The Anti-Phishing Working Group (APWG) recorded 971,181 reported phishing attacks in the first quarter of 2026, representing an increase of 13.8% from the final quarter of 2025. The same report stated that telephone-based fraud, including vishing and smishing, increased by 15% from the preceding quarter (Anti-Phishing Working Group [APWG], 2026). These figures refer to attacks observed through APWG’s reporting arrangements rather than every phishing message sent worldwide, but they demonstrate the continuing scale and changing channel mix of the problem. Verizon’s analysis of more than 22,000 security incidents and 12,195 confirmed breaches for its 2025 Data Breach Investigations Report also identified persistent human involvement in breaches and the importance of social-engineering threats (Verizon, 2025). The evidence supports the need for protective tools that complement user awareness and existing communication-platform controls.

Traditional phishing defences include blocklists, sender filtering, manually written rules and security-awareness training. Each remains valuable, but each has limitations when used alone. A blocklist can identify a previously reported malicious address or domain, yet a newly registered or compromised domain may not appear on the list. A fixed rule can recognise a known pattern, but attackers can change words, spacing or message structure. User education improves awareness, but users may still make mistakes when confronted with time pressure, authority claims or familiar branding. Recent reviews describe a broad shift towards machine learning, deep learning, feature engineering and hybrid or stacked detection approaches because learned models can identify patterns across many examples rather than rely exclusively on fixed signatures (Popescul & Radu, 2025; Wilk-Jakubowski et al., 2025).

Machine learning provides a data-driven way to classify messages. In text classification, a message can be transformed into numeric features and supplied to a classifier that estimates whether it resembles examples from a suspicious or legitimate class. Term Frequency–Inverse Document Frequency (TF-IDF) is a widely used representation that gives greater weight to terms that are important within a document but less common across the collection. Logistic Regression can then learn a decision boundary and estimate class probabilities from those features. This combination is computationally economical, supports sparse text data and offers a practical baseline for a web prototype. Comparative research nevertheless shows that model performance depends strongly on the datasets, evaluation design and distribution of future messages. Studies based on multiple datasets and systematic reviews warn that results obtained from a single source or random within-dataset split may not demonstrate generalisation to new campaigns, organisations, languages or time periods (Alhuzali et al., 2025; Kytidou et al., 2025; Wilk-Jakubowski et al., 2025).

Another important concern is interpretability. A bare label such as “phishing” may not tell a user what was detected or what action should follow. False positives can also cause users to ignore future warnings, while a false negative may create unwarranted confidence. Al-Subaiey et al. (2024) demonstrated the practical value of combining phishing-email classification with a web-based interface and interpretable output. In the SMS context, Wang et al. (2025) found that evidence-based explanations could improve users’ phishing-detection decisions, although their system used a different large-language-model architecture and external contextual sources. These studies support a user-centred design principle: detection output should be accompanied by intelligible evidence and cautious, actionable advice.

This project responds to that need through PhishGuard AI, a practical Django-based prototype for analysing user-supplied email and SMS content. It employs a separate TF-IDF and Logistic Regression model for each communication mode rather than using one model indiscriminately across both channels. The model output is combined with explainable local checks for message content, URLs, sender format, suspicious domain characteristics and inconsistency between a claimed organisation and the supplied sender domain. The analysis engine then aggregates the model and rule evidence into a bounded threat score and a risk-oriented verdict. The user receives the observed indicators, a short explanation and recommendations such as avoiding a suspicious link, refusing to disclose credentials or verifying a payment request through an independent contact method.

The system is intentionally presented as a prototype decision-support tool rather than a production email gateway or a guarantee of safety. Its sender analysis is based only on the text entered by the user. It does not perform live Domain Name System (DNS), WHOIS, Sender Policy Framework (SPF), DomainKeys Identified Mail (DKIM), Domain-based Message Authentication, Reporting and Conformance (DMARC), link-reputation or malware checks. A recognised domain contributes only limited positive context and does not automatically override a serious warning sign. This cautious positioning is important because phishing detection is an evolving and adversarial problem, and the absence of an observed indicator does not prove that a message is legitimate.

### 1.2 Statement of the Problem

Email and SMS users routinely receive transactional alerts, account notices, delivery updates, promotional messages and requests from people or organisations with whom they interact. Phishing messages imitate these familiar forms of communication. The recipient is therefore required to distinguish between legitimate and deceptive content, sometimes within seconds and on a device that displays only limited sender or link information. An incorrect decision may expose login credentials, OTPs, identity information, payment details or organisational data.

Existing platform filters reduce part of this risk, but suspicious messages still reach users. Some recipients also receive messages outside managed corporate environments, where specialist security personnel and enterprise tools are unavailable. Manual judgement is difficult because a legitimate message may contain urgency, a link or a security-related term, while a phishing message may use calm language and an apparently plausible sender. Static keyword matching can therefore create false alarms when it ignores negation and context, as in an awareness notice that says “we will never ask for your password.” Conversely, a classifier that relies only on learned text patterns can assign a high probability without providing evidence that a non-technical user can understand.

A further problem is channel difference. Email commonly includes a sender address, subject and body, whereas SMS is shorter and may use a phone number, short code or alphanumeric sender ID. Applying a single model and one interface to both channels can overlook these distinctions. Research on explainable SMS detection identifies short message length and limited contextual information as particular challenges (Wang et al., 2025). A suitable prototype should therefore treat email and SMS as related but distinct analysis modes.

Many research systems report high accuracy on selected datasets, yet dataset bias, class imbalance, incomplete documentation and limited cross-dataset testing remain recurring concerns (Kytidou et al., 2025; Wilk-Jakubowski et al., 2025). Strong performance on historical or internally split data does not by itself establish safe performance on current real-world messages. This creates a gap between experimental classification results and a transparent tool that can be used cautiously in practice. The problem is not simply to produce a binary model prediction; it is to combine model evidence with observable message characteristics, explain the result, preserve uncertainty and guide the user towards safer verification behaviour.

PhishGuard AI was developed to address this practical gap. The prototype needs to accept the fields appropriate to email and SMS, validate the input, select the correct channel-specific model, examine content and technical indicators, aggregate risk without allowing unexplained model output to dominate, and present understandable findings and recommended actions. At the same time, the system must avoid implying capabilities it does not possess. In particular, it cannot authenticate a sender merely from a typed address, inspect a remote webpage, determine whether an account has been compromised or guarantee that a low-risk message is safe.

Accordingly, this study addresses the following central problem: how can a lightweight, web-based machine-learning prototype support the assessment of phishing risk in email and SMS messages while providing transparent evidence and practical user guidance? The study implements and documents one answer based on channel-specific TF-IDF/Logistic Regression classifiers and local explainable heuristics. Its effectiveness must ultimately be judged through reproducible functional testing and evaluation on sufficiently large, representative and recent datasets; where such evidence is not yet available, no unsupported performance claim is made.

### 1.3 Aim and Objectives of the Study

#### 1.3.1 Aim

The aim of this study is to design and implement a practical web-based system that assesses phishing risk in email and SMS messages by combining machine-learning text classification with explainable content, sender and URL checks.

#### 1.3.2 Objectives

The specific objectives are to:

1. examine the characteristics of email and SMS phishing and review relevant automated detection approaches;
2. represent message text using TF-IDF and apply separate Logistic Regression classifiers to the email and SMS analysis modes;
3. develop a Django-based interface that accepts and validates channel-appropriate sender, subject and message inputs;
4. design a hybrid analysis mechanism that combines machine-learning output with message-content indicators, URL characteristics, sender/domain checks and contextual safeguards;
5. generate risk-oriented verdicts, human-readable reasons and recommended protective actions for analysed messages;
6. persist the submitted scan and analysis outcome for local review within the prototype; and
7. conduct functional testing of the implemented workflow and define an evidence-based evaluation process for subsequent validation on larger, recent and representative real-world datasets.

### 1.4 Significance of the Study

The study is significant because it moves phishing detection from a model-only experiment towards an accessible decision-support prototype. Its value lies not merely in producing a label but in connecting automated analysis to information that a user can inspect and act upon.

**Email and SMS users.** The application gives a user one location in which to examine the sender details and content of a suspicious email or SMS before responding. The displayed reasons can draw attention to credential requests, pressure, threats, money lures, suspicious links or sender inconsistencies. The recommended actions encourage independent verification instead of immediate compliance. The system is not a substitute for professional investigation, but it can support safer first-line decisions.

**Students and educational institutions.** Universities depend heavily on email and mobile messaging for account notices, fee information, registration, learning platforms and administrative communication. This creates opportunities for attackers to imitate institutional or financial messages. A simple explanatory prototype can serve both as an analysis tool and as a practical cybersecurity-awareness resource by showing the indicators that influenced a verdict.

**Small organisations and resource-constrained users.** Not every user has access to an enterprise secure-email gateway or a dedicated security operations team. The project demonstrates how open-source web technologies and conventional machine-learning methods can be combined into a comparatively lightweight prototype. This makes the work relevant to settings where computational cost, ease of deployment and understandable output are important considerations.

**Software developers and cybersecurity practitioners.** The project illustrates a modular approach in which input validation, model selection, rule evidence, risk aggregation, result presentation and persistence are separated. Independent email and SMS models reduce accidental cross-channel use, while explicit safeguards prevent an unexplained model score from being presented as decisive evidence. The local sender-intelligence design also demonstrates the importance of clearly distinguishing heuristic inspection from live authentication or reputation services.

**Researchers.** The study contributes a documented implementation that can be extended and critically evaluated. It provides a basis for comparing classical TF-IDF/Logistic Regression classification with richer text representations, multilingual models, live reputation services or explainable-AI techniques. More importantly, it records current limitations rather than converting incomplete evidence into an accuracy claim. This aligns with recent literature calling for diverse datasets, reproducible evaluation, cross-source validation and cautious interpretation of phishing-detection metrics (Alhuzali et al., 2025; Kytidou et al., 2025; Wilk-Jakubowski et al., 2025).

**User-centred cybersecurity.** Explainability is especially important when a system influences a security decision. By presenting observed indicators and recommendations, the prototype is intended to promote informed verification rather than blind acceptance of an automated label. This design direction is consistent with evidence that usable, evidence-based explanations can help people make better phishing judgements (Wang et al., 2025).

Overall, the study demonstrates the feasibility of a hybrid and explainable detection workflow while preserving the principle that automated output should support, not replace, cautious human judgement.

### 1.5 Scope of the Study

This study covers the design, implementation and documentation of PhishGuard AI as a web-based prototype for the analysis of text supplied by a user. Its scope is defined as follows:

1. **Communication channels:** The prototype supports email and SMS. Email analysis accepts a sender email address, an optional subject and a message body. SMS analysis accepts a phone number, short code or alphanumeric sender ID and a message body; a subject is not used.

2. **Machine-learning method:** Each channel has an independent saved text-classification pipeline based on TF-IDF features and Logistic Regression. The email and SMS model artifacts are loaded separately, and the analysis request selects the artifact that corresponds to the chosen mode.

3. **Content analysis:** The prototype checks the supplied message for locally defined indicators such as urgency, threats, requests for credentials or authentication data, requests for personal or banking information, changed-payment instructions, OTP requests in SMS and unexpected money or reward claims. It includes contextual handling intended to avoid treating negated security advice or genuine awareness wording as a direct request.

4. **URL analysis:** Explicit HTTP and HTTPS links found in the submitted text are inspected locally for selected characteristics, including known shortening services, raw Internet Protocol addresses, a misleading “@” character, punycode hostnames and selected higher-risk top-level domains. The system does not visit the destination or follow redirects.

5. **Sender and domain analysis:** For email, the system validates the address format and examines locally observable domain characteristics, possible one-character brand imitation, use of a public email provider for selected organisation claims and inconsistency between selected claimed brands and known official domains. For SMS, it validates accepted number, short-code and sender-ID formats. These operations are heuristic checks and not cryptographic sender authentication.

6. **Risk aggregation and output:** The application combines model contribution, explainable evidence and limited positive context into a bounded score. Internally, scores from 0–39 are treated as Low Risk, 40–69 as Suspicious and 70–100 as High Risk. Email results expose the three risk-oriented outcomes as Low Risk: Safe, Needs Review: Suspicious and High Risk: Fraudulent. The SMS interface simplifies the presentation to Message Appears Safe or Message Appears Suspicious, while retaining the internal risk analysis. Low risk is expressly not presented as a guarantee of legitimacy.

7. **Explanations and recommendations:** The result identifies triggered indicators or safe signals and provides actions tailored to the evidence, such as not opening a suspicious link, not sharing credentials or OTPs, confirming changed bank details through a known number, and reporting or deleting a high-risk message as appropriate.

8. **Web application and persistence:** The implementation uses Django for request handling, server-side form validation, result rendering and local database persistence. A stored scan may include sender, subject, body, triggered rules, machine-learning label, final label, score and timestamp.

The study does not cover voice phishing, social-media messages as a dedicated input mode, attachment or QR-code inspection, image-based phishing, browser extension deployment, automatic email inbox integration, carrier-level SMS filtering, live website crawling, malware analysis or enterprise incident response.

### 1.6 Limitations of the Study

The following limitations define how the prototype and any later evaluation results should be interpreted:

1. **Prototype status:** PhishGuard AI is a practical academic prototype, not a production-ready cybersecurity service. It has not been demonstrated to meet enterprise requirements for availability, scalability, regulatory compliance, continuous monitoring or formal security assurance.

2. **Manual input:** A user must copy or type the sender and message content into the application. The prototype does not automatically retrieve complete email headers, attachments, inbox metadata, SMS routing information or device telemetry. Relevant evidence may therefore be omitted or altered during submission.

3. **No live sender authentication:** Sender intelligence operates only on supplied text. It does not query DNS or WHOIS, check domain age, validate SPF, DKIM or DMARC, inspect mail-routing headers, determine whether an account has been compromised, or consult a live reputation service. A correctly formatted or recognised domain must not be interpreted as proof of authenticity.

4. **No remote URL investigation:** The URL component performs local string and hostname checks only. It does not open the page, expand every shortened link, inspect Transport Layer Security certificates, analyse webpage content, execute a sandbox, detect malware or query a live threat-intelligence feed. A normal-looking link may still lead to a malicious or subsequently compromised resource.

5. **Dataset and generalisation constraints:** Public phishing, spam and legitimate-message corpora can be outdated, duplicated, imbalanced or unrepresentative of current attacks. The available SMS pipeline is trained from a ham/spam collection and is strengthened with phishing-oriented rules, but this is not equivalent to validation on a large contemporary smishing corpus. The repository does not presently preserve a complete, reproducible set of verified email-model evaluation outputs. Consequently, this chapter makes no claim about the prototype’s accuracy, precision, recall, F1-score or real-world error rates. Verified metrics must be inserted only after a controlled evaluation is completed.

6. **Language and cultural coverage:** The implemented text indicators and current training arrangements are primarily English-language oriented. Nigerian Pidgin, indigenous Nigerian languages, code-switching, abbreviations and region-specific scam narratives may not be represented adequately.

7. **Evolving and adversarial attacks:** Attackers continually modify wording, domains and delivery techniques. Obfuscation, images, QR codes, novel shorteners, compromised legitimate accounts and carefully crafted messages can evade both learned and rule-based signals. Recent reviews identify adversarial adaptation, dataset bias and model drift as continuing problems for machine-learning phishing detection (Kytidou et al., 2025; Wilk-Jakubowski et al., 2025).

8. **Risk-score interpretation:** The displayed threat score is a hybrid prioritisation score, not a calibrated probability that a message is phishing. It combines model output with weighted evidence and contextual safeguards. The thresholds support user-facing triage within this prototype and should not be treated as universal cybersecurity standards.

9. **False positives and false negatives:** A legitimate message can contain suspicious features, and a malicious message can avoid the indicators currently recognised. Human verification through an independently obtained official channel remains necessary, particularly for messages involving credentials, payments or sensitive personal information.

10. **Data protection and access control:** The prototype can store submitted message content and analysis results in its local database. A production deployment would require explicit retention rules, access controls, secure configuration, encryption, audit mechanisms, user consent and procedures for deleting sensitive data. These operational controls are outside the present project scope.

These limitations do not remove the value of the prototype; rather, they establish the conditions under which it can be used and evaluated responsibly. Larger real-world datasets, temporal and cross-dataset testing, multilingual analysis, adversarial evaluation and live security integrations are required before strong claims about general performance or production suitability can be made.

### 1.7 Operational Definition of Terms

#### 1.7.1 Phishing

In this study, phishing means a deceptive digital communication that impersonates or misrepresents a trusted person or organisation in order to induce the recipient to disclose sensitive information, transfer money, open an unsafe link or perform another action that benefits an attacker.

#### 1.7.2 Smishing

Smishing means phishing delivered through SMS or a comparable text-messaging channel. Within PhishGuard AI, the SMS mode analyses the supplied sender number, short code or sender ID and the message body.

#### 1.7.3 Digital Medium

A digital medium is an electronic channel used to create, transmit or receive information. Although phishing can occur through websites, social media, voice services and other channels, the operational scope of “digital medium” in this project is limited to email and SMS.

#### 1.7.4 Machine Learning

Machine learning is the use of computational methods that learn patterns from labelled examples and apply those patterns to new data. In this project, machine learning refers specifically to separate Logistic Regression classifiers trained on TF-IDF representations for email and SMS text.

#### 1.7.5 Term Frequency–Inverse Document Frequency (TF-IDF)

TF-IDF is a numerical text-representation method that assigns weight to a term according to its frequency in a message and its relative rarity across the training collection. The resulting sparse feature vectors are used as input to the Logistic Regression classifiers.

#### 1.7.6 Logistic Regression

Logistic Regression is a supervised classification algorithm that models the probability of a class from a weighted combination of input features. In PhishGuard AI, it is used as the message-text classifier for the independent email and SMS pipelines.

#### 1.7.7 Rule-Based Detection

Rule-based detection refers to explicit, human-readable conditions that identify selected phishing indicators. In this project, the rules cover content patterns, URL characteristics, sender/domain properties and selected claimed-organisation inconsistencies. They complement rather than replace the machine-learning models.

#### 1.7.8 Hybrid Detection

Hybrid detection is the combination of data-driven model output and explicit heuristic evidence in one analysis process. PhishGuard AI uses hybrid detection so that observable warning signs can influence the verdict and be explained to the user.

#### 1.7.9 Sender Intelligence

Sender intelligence means the prototype’s local inspection of a supplied sender string, including format, domain structure, possible typosquatting and selected organisation/domain inconsistencies. The term does not mean live reputation lookup, DNS verification or SPF/DKIM/DMARC authentication.

#### 1.7.10 Risk Score

The risk score is the prototype’s bounded 0–100 aggregation of machine-learning contribution, weighted explainable indicators and limited contextual credit. It is used to assign Low Risk, Suspicious or High Risk bands. It is not a calibrated phishing probability.

#### 1.7.11 Explainability

Explainability is the presentation of understandable reasons that support an automated result. In this project, explainability is provided through triggered indicators, safe signals, analysis details and recommended actions rather than through a label alone.

#### 1.7.12 False Positive and False Negative

A false positive occurs when a legitimate message is classified or flagged as suspicious or fraudulent. A false negative occurs when a phishing message is classified as low risk or safe. Both error types are important because the former can reduce trust in warnings and the latter can expose a user to harm.

#### 1.7.13 Prototype

A prototype is an implemented system used to demonstrate and evaluate a design approach. PhishGuard AI is described as a prototype because further dataset validation, security hardening, privacy controls, live integrations and operational testing are required before production deployment.

### 1.8 Organization of Study

This report is organised into five chapters. Chapter One introduces the study by presenting the background, problem statement, aim, objectives, significance, scope, limitations and operational definitions.

Chapter Two reviews the concepts, theories, detection methods and empirical studies relevant to phishing in email and SMS. It compares at least ten directly related studies, discusses their datasets, methods, findings and limitations, and identifies the gap addressed by PhishGuard AI.

Chapter Three describes the methodology and system-development process. It presents the requirements, architecture, data preparation, TF-IDF and Logistic Regression pipelines, hybrid analysis design, sender and URL checks, database design, interface flow, tools and testing plan. Project-specific diagrams are included in editable formats.

Chapter Four presents the implementation and verified results. It explains the operation of the Django components, channel-specific analysis workflow, interface and output. Screenshots and empirical metrics are included only where verifiable evidence is available; otherwise, numbered placeholders such as “[Insert verified result]” or “[Insert screenshot]” are retained for later replacement. The discussion relates the observed results to the objectives and literature without overstating the prototype’s capability.

Chapter Five summarises the study, states the conclusion, presents recommendations, acknowledges limitations and proposes future work. The final report is followed by the complete reference list and any relevant appendices.

## REFERENCES

Al-Subaiey, A., Al-Thani, M., Alam, N. A., Antora, K. F., Khandakar, A., & Zaman, S. M. A. U. (2024). Novel interpretable and robust web-based AI platform for phishing email detection. *Computers & Electrical Engineering, 120*, 109625. https://doi.org/10.1016/j.compeleceng.2024.109625

Alhuzali, A., Alloqmani, A., Aljabri, M., & Alharbi, F. (2025). In-depth analysis of phishing email detection: Evaluating the performance of machine learning and deep learning models across multiple datasets. *Applied Sciences, 15*(6), 3396. https://doi.org/10.3390/app15063396

Anti-Phishing Working Group. (2026, May 21). *Phishing activity trends report: 1st quarter 2026*. https://docs.apwg.org/reports/apwg_trends_report_q1_2026.pdf

Kytidou, E., Tsikriki, T., Drosatos, G., & Rantos, K. (2025). Machine learning techniques for phishing detection: A review of methods, challenges, and future directions. *Intelligent Decision Technologies*. Advance online publication. https://doi.org/10.1177/18724981251366763

National Institute of Standards and Technology. (n.d.). *Phishing*. Computer Security Resource Center Glossary. Retrieved August 10, 2026, from https://csrc.nist.gov/glossary/term/phishing

Popescul, D., & Radu, L. D. (2025). AI in phishing detection: A bibliometric review. *Frontiers in Artificial Intelligence, 8*, 1496580. https://doi.org/10.3389/frai.2025.1496580

Verizon. (2025). *2025 data breach investigations report*. https://www.verizon.com/business/resources/reports/dbir/

Wang, Y., Zhai, H., Wang, C., Hao, Q., Cohen, N. A., Foulger, R., Handler, J. A., & Wang, G. (2025). Can you walk me through it? Explainable SMS phishing detection using LLM-based agents. In *Proceedings of the Twenty-First Symposium on Usable Privacy and Security (SOUPS 2025)* (pp. 37–56). USENIX Association. https://www.usenix.org/conference/soups2025/presentation/wang

Wilk-Jakubowski, J. L., Pawlik, L., Wilk-Jakubowski, G., & Sikora, A. (2025). Machine learning and neural networks for phishing detection: A systematic review (2017–2024). *Electronics, 14*(18), 3744. https://doi.org/10.3390/electronics14183744
