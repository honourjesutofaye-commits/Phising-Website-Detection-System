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

## CHAPTER TWO

## LITERATURE REVIEW

### 2.1 Introduction

This chapter reviews the literature that informs the design of PhishGuard AI, a machine-learning prototype for assessing phishing risk in email and Short Message Service (SMS) content. The review is organised around the concepts of phishing and smishing, the technical foundations of text classification, rule-based and hybrid detection, sender and URL intelligence, explainable output, and the evaluation of security classifiers. It then examines thirteen directly relevant empirical studies published or revised between 2024 and 2026, compares related systems, identifies unresolved research gaps, and presents the conceptual framework adopted for this project.

Phishing detection is not a single-feature problem. A message can be suspicious because of its language, sender identity, domain, links, requested action, or a combination of these factors. Conversely, legitimate security messages may contain words such as “password,” “urgent,” or “verify.” Recent reviews therefore describe a movement from isolated blacklist or keyword techniques towards machine learning, deep learning, feature engineering, model ensembles and hybrid systems (Kytidou et al., 2025; Popescul & Radu, 2025; Wilk-Jakubowski et al., 2025). However, increasingly complex models do not remove concerns about dataset bias, false positives, adversarial evasion, explanation quality, computational cost and real-world deployment.

The literature is assessed in relation to the actual scope of this project. PhishGuard AI uses separate TF-IDF and Logistic Regression pipelines for email and SMS, combines their output with local content rules, sender/domain checks and URL analysis, and presents a bounded risk score with findings and recommendations. It is a practical Django prototype, not a production email gateway or telecom filter. Consequently, this review pays particular attention to lightweight classification, multi-channel support, transparent evidence, usable guidance and honest limitations rather than treating headline accuracy alone as proof of operational effectiveness.

### 2.2 Conceptual Review

#### 2.2.1 Phishing and Social Engineering

Phishing is a social-engineering attack in which a malicious actor uses fraudulent communication while pretending to be a reputable person or organisation in order to obtain sensitive information or cause an unsafe action. The National Institute of Standards and Technology defines it in terms of deceptive email or web solicitation used to acquire sensitive data while masquerading as a legitimate entity (National Institute of Standards and Technology [NIST], n.d.). The target may be asked to disclose a password, one-time password, payment-card detail or personal record; transfer money; open an attachment; install software; or follow a link to a counterfeit service.

The social-engineering dimension is fundamental. The attacker does not always defeat a technical control directly; instead, the attacker constructs a message that encourages the recipient to override caution. Common persuasive mechanisms include urgency, fear, scarcity, authority, curiosity, reward and familiarity. Generative artificial intelligence has increased concern because grammatically polished, context-aware and personalised messages can be produced at scale. Brissett and Wall (2025) showed that Large Language Models (LLMs) can be considered within the phishing threat model and examined how psychological principles and AI-generated text affect detection. This development weakens the traditional assumption that poor spelling or awkward grammar is a reliable warning sign.

Phishing also changes continuously. Domains can be registered, abandoned or compromised; wording can be paraphrased; and the same campaign can move between email, SMS, social media and voice. The Anti-Phishing Working Group recorded 971,181 phishing attacks in the first quarter of 2026 and reported a 15% quarter-to-quarter increase in telephone-oriented fraud encompassing vishing and smishing (Anti-Phishing Working Group [APWG], 2026). These observed reports do not represent every attack worldwide, but they support the view that phishing is persistent, adaptive and distributed across digital media.

#### 2.2.2 Email Phishing

Email phishing uses electronic mail to impersonate a trusted source or create a misleading transaction. A basic mass campaign distributes substantially similar messages to many recipients, while spear phishing is tailored to a person or organisation. Business Email Compromise may imitate an executive, supplier or colleague to request payment, change account details or obtain confidential records. An email can expose several evidence sources: the visible sender, underlying address, subject, body, links, attachments and complete mail headers. The present project receives only user-supplied sender, subject and body text, so the literature must be interpreted in light of that reduced evidence.

Email detection methods commonly analyse lexical content, structural features, sender and header information, embedded URLs or combinations of these sources. Text-only models are attractive because message bodies are widely available and can be represented efficiently. However, content alone may miss a concise invoice fraud, a compromised legitimate account or a message in which most deception resides on the linked webpage. Alhuzali et al. (2025) demonstrated that strong email-classification results can be obtained across numerous datasets, but they also showed that performance varies with dataset and external evaluation. Khandan et al. (2026) accordingly combined email and URL components rather than assuming that either medium alone provides complete evidence.

#### 2.2.3 SMS Phishing and the Distinction from Spam

Smishing is phishing delivered through SMS or a comparable mobile text channel. It often uses delivery notices, bank alerts, prize claims, unpaid-bill warnings, account suspensions or urgent requests to call a number or open a shortened link. SMS messages are brief, sender information may be a telephone number, short code or alphanumeric identifier, and the display available to the user is constrained. These characteristics reduce context and can make manual judgement difficult.

Spam and smishing overlap but are not identical. Spam is unsolicited bulk communication and may be commercial without attempting credential theft or impersonation. Smishing is deceptive and seeks a harmful security outcome. A binary ham/spam collection can help a classifier learn unwanted-message patterns, but it is not automatically a comprehensive smishing corpus. Munoz and Islam (2025) addressed this distinction through multiclass ham, spam and smishing classification, while Corpuz et al. (2026) focused directly on phishing and legitimate SMS in a language-aware setting. For PhishGuard AI, this distinction is important because the current SMS model originates from a spam collection and is supplemented by phishing-oriented rules; larger contemporary smishing-specific validation is still required.

Human factors also matter. Timko et al. (2024) found that participants were more accurate at identifying fake messages than recognising genuine ones, meaning that scepticism can create false alarms as well as protection. Wang et al. (2025) further showed that evidence-based explanations can improve users’ SMS-phishing decisions. Detection should therefore support calibrated judgement rather than merely encourage the user to distrust every unfamiliar message.

#### 2.2.4 Observable Phishing Indicators

A phishing indicator is an observable characteristic that contributes evidence of deception. Content indicators include pressure to act immediately, threats of account closure, credential or OTP requests, unexpected rewards, changed bank details, requests for sensitive information and instructions to bypass normal procedures. Structural indicators include unusual capitalisation, excessive punctuation, mismatched brand references, obfuscated URLs, raw Internet Protocol addresses, punycode and misleading use of the “@” character in a link. Sender indicators include malformed addresses, look-alike domains, public-mail domains used for formal institutional claims and inconsistency between a claimed organisation and the supplied domain.

No indicator is universally decisive. Urgency is legitimate in some fraud alerts; a public email provider can be appropriate for an individual; and a recognised domain can appear in copied text or be supplied by a compromised account. A robust design treats indicators as cumulative evidence and preserves context. This is one reason PhishGuard AI does not allow an uncorroborated model probability to produce a high-risk verdict by itself and does not treat a locally recognised domain as proof that the message is authentic.

#### 2.2.5 Machine Learning for Message Classification

Machine learning allows a classifier to infer patterns from labelled messages and apply them to previously unseen text. In supervised classification, each training example is associated with a target label such as legitimate or phishing. The typical process consists of data collection, cleaning, transformation into numerical features, model fitting, validation, testing and deployment. Classical algorithms used in phishing research include Naive Bayes, Logistic Regression, Support Vector Machines, decision trees, Random Forest, gradient boosting and ensemble methods. Deep-learning approaches include recurrent networks, convolutional networks and transformer architectures such as BERT, DistilBERT and RoBERTa.

Classical sparse-text methods remain relevant despite the strong results reported for transformers. They require fewer computational resources, train quickly, are simpler to deploy and provide reproducible baselines. Deep models can capture richer semantic context and reduce dependence on manually selected features, but may demand more data, memory, processing time and deployment infrastructure. Alhuzali et al. (2025) found that transformer models led on their balanced merged email dataset, whereas the traditional Stochastic Gradient Descent classifier remained highly competitive on average. Ahmed and Sumesh (2026) also demonstrated that carefully engineered ensemble methods can achieve strong unseen-data results while reducing training and inference cost. The appropriate choice is therefore influenced by the project’s resources, evidence requirements and operational setting, not by model novelty alone.

#### 2.2.6 Natural Language Processing and Text Preprocessing

Natural Language Processing (NLP) supplies methods for converting human language into forms that algorithms can analyse. Common preparation steps include normalising case, handling punctuation, removing or retaining stop words, tokenisation, stemming or lemmatisation, and representing words or sequences numerically. Preprocessing must be selected carefully in phishing detection because punctuation, unusual spelling, currency symbols, URLs and character substitutions may themselves carry evidence. Excessive cleaning can remove precisely the features that distinguish a deceptive message.

Text may be represented through counts, n-grams, TF-IDF weights, dense word embeddings or contextual transformer embeddings. Word and character n-grams help capture recurring phrases and partial patterns. Dense and contextual embeddings can model semantic similarity and surrounding context. Patra et al. (2025), for example, used Dense Passage Retrieval embeddings and vector similarity search, while Uddin et al. (2026) fine-tuned RoBERTa. PhishGuard AI adopts TF-IDF because it is efficient for sparse text, works well with linear classifiers and is appropriate to a lightweight prototype, while recognising that it does not understand meaning in the same way as a contextual language model.

#### 2.2.7 Term Frequency–Inverse Document Frequency

Term Frequency–Inverse Document Frequency assigns each term a weight based on its importance in one document relative to the complete collection. Term frequency reflects how often the term occurs in the message, while inverse document frequency reduces the influence of terms that occur in many messages. In simplified form, the weight of term t in document d is the product of TF(t,d) and IDF(t). The result is a sparse vector in which discriminative words or n-grams can receive greater influence than ubiquitous language (Manning et al., 2008).

TF-IDF is useful for phishing detection because deceptive campaigns often contain recurring lexical patterns, calls to action and combinations of terms. It is computationally economical and can be paired effectively with Logistic Regression, Support Vector Machines and related linear methods. Corpuz et al. (2026) found TF-IDF effective for language-aware SMS classification, and Brissett and Wall (2025) used it with Logistic Regression in the detection of AI-generated phishing emails. Its limitations include sensitivity to vocabulary drift, obfuscation, synonyms and paraphrasing. Ahmed and Pourmoafil (2026) showed that a TF-IDF/Logistic Regression baseline with excellent clean-data performance could still degrade sharply under adversarial modification.

#### 2.2.8 Logistic Regression

Logistic Regression is a supervised linear classifier that estimates the probability of a categorical outcome. For binary classification, it applies the logistic function to a weighted combination of input features. If x represents the TF-IDF vector, w the learned feature weights and b the intercept, the estimated positive-class probability can be expressed as p(y=1|x) = 1 / (1 + exp(-(w·x+b))). A threshold then maps the probability to a class decision (James et al., 2021).

The algorithm is well suited to high-dimensional sparse text. It is relatively fast, supports regularisation and exposes feature coefficients that can assist inspection. Its output probability must nevertheless be interpreted cautiously. A classifier trained on an imbalanced or unrepresentative corpus can be confident and wrong, and a numerical probability is not necessarily calibrated for a new population. In PhishGuard AI, the probability contributes to a hybrid risk score; it is not presented as the literal probability that the submitted message is fraudulent.

#### 2.2.9 Rule-Based and Heuristic Detection

Rule-based detection uses explicit conditions designed by analysts. A rule can recognise a credential request, unexpected OTP demand, raw-IP URL, suspicious shortener or domain imitation. Its main advantages are transparency, speed and direct control. A triggered rule can be presented to the user in ordinary language. Rules also allow security knowledge to be included even when a pattern is underrepresented in a training corpus.

The weaknesses are brittleness and maintenance cost. Attackers can alter wording, place content in images or use a previously unseen shortener. A broad rule can also generate false positives. Context-aware design is therefore necessary. For example, “we will never ask for your password” should not be treated in the same way as “send your password now.” Rules are strongest when they complement learned patterns rather than attempt to enumerate every possible phishing message.

#### 2.2.10 Hybrid Detection and Risk Aggregation

Hybrid detection combines two or more evidence mechanisms. The combination may involve multiple classifiers, content and URL models, machine learning and manually defined rules, or automated detection and human review. Popescul and Radu’s (2025) bibliometric review identified increasing emphasis on hybrid models and classifier stacking. Khandan et al. (2026) used late fusion to combine independent email and URL models, while Zidan et al. (2025) combined machine learning, NLP and generated user guidance.

A hybrid system requires a clear aggregation policy. Scores from unlike components should not be added without considering their scale and meaning. Strong corroborating indicators may justify a higher risk band, whereas limited positive context should not erase dangerous evidence. PhishGuard AI applies a bounded contribution from its classifier, adds weighted explainable findings, applies safeguards, and maps the result to Low Risk, Suspicious or High Risk. This score is a prioritisation mechanism rather than a universally calibrated probability.

#### 2.2.11 Sender and Domain Intelligence

Sender intelligence assesses whether the supplied sender information is structurally and contextually plausible. For email, useful checks include address syntax, domain extraction, visually similar brand names, unusual subdomains, public-mail domains used to claim an official organisation, and disagreement between a claimed brand and an expected official domain. Domain intelligence may also include registration age, DNS records, reputation and mail authentication results in a production system.

There is an important distinction between local inference and live authentication. SPF, DKIM and DMARC require complete headers and DNS information; a typed sender address cannot prove that these checks passed. Similarly, a known domain may be spoofed in display text or used from a compromised account. PhishGuard AI therefore performs only local sender/domain heuristics and describes them as evidence, not authentication. This transparent boundary prevents the user from confusing a plausibly formatted address with a verified identity.

#### 2.2.12 URL Analysis

URLs frequently connect the persuasive message to the attacker’s collection page. Detection can inspect lexical and structural properties such as length, number of subdomains, encoded characters, raw IP hosts, punycode, shortening services, unusual top-level domains and misleading placement of brand terms. More advanced systems resolve redirects, retrieve the webpage, analyse screenshots or Document Object Model content, inspect certificates and consult reputation services. Mishra and Soni (2020) demonstrated the value of combining SMS content analysis with URL behaviour, and Wang et al. (2025) gathered redirect, domain and screenshot context for explainable smishing assessment.

Local URL inspection is safer and easier to deploy but less complete. A normal-looking domain may be newly compromised, a short URL may redirect to a malicious destination, and a page may change after analysis. The current prototype extracts explicit HTTP or HTTPS links and checks selected string and host properties without visiting the destination. The resulting evidence should prompt verification, not be treated as a comprehensive website-security verdict.

#### 2.2.13 Explainable Artificial Intelligence and Security Warnings

Explainability concerns whether a person can understand the basis of a model-assisted decision. Local explanation methods such as LIME approximate the behaviour of a classifier around a particular instance and identify influential features (Ribeiro et al., 2016). SHAP, attention visualisation and feature importance are also used in recent phishing research. Uddin et al. (2026) combined LIME and transformer attribution, while Ahmed and Sumesh (2026) used LIME-supported error analysis.

Technical feature attribution does not automatically produce a useful warning. Miller (2019) argued that explanation is social and selective: people generally need a concise contrastive account of why an outcome occurred. In phishing detection, the user needs to know what was observed, why it matters, what uncertainty remains and what safe action to take. Wang et al. (2025) converted richer LLM reasoning into short evidence-based explanations and found that these improved user detection across age groups. PhishGuard AI follows the same broad user-centred principle but uses deterministic findings and recommendations rather than LLM-generated chain-of-thought. This reduces infrastructure and unpredictability, although the explanations are limited to the indicators that its rules can recognise.

#### 2.2.14 Evaluation Metrics and Validation Design

A phishing classifier is commonly evaluated with a confusion matrix. True positives are phishing messages correctly detected, true negatives are legitimate messages correctly classified, false positives are legitimate messages incorrectly flagged, and false negatives are phishing messages missed. Accuracy is the proportion of all correct decisions. Precision measures how many messages predicted as phishing are actually phishing, recall measures how many actual phishing messages are detected, and F1-score is the harmonic mean of precision and recall. Receiver Operating Characteristic Area Under the Curve summarises ranking performance across thresholds (James et al., 2021).

No single metric is sufficient. Accuracy can be misleading where legitimate messages dominate. A system with low recall may leave dangerous messages undetected, while one with poor precision may overwhelm users with false alarms. Timko et al. (2024) also showed that human judgement can misclassify legitimate messages, reinforcing the importance of examining both error directions. Threshold selection is therefore a security and usability decision.

Validation design is equally important. Randomly splitting one historical dataset may place near-duplicate campaigns in both training and test sets. Cross-dataset, temporal, multilingual, unseen-campaign and adversarial testing provide stronger evidence of generalisation. Alhuzali et al. (2025) reported lower external-set performance than internal results for some models, and Ahmed and Pourmoafil (2026) found severe degradation under adversarial testing despite clean-data accuracy above 98%. Consequently, this project does not invent performance values. Verified accuracy, precision, recall, F1-score, confusion matrices and usability findings will be reported only after the corresponding controlled evaluations are performed.

### 2.3 Theoretical Framework

#### 2.3.1 Statistical Text-Classification Perspective

The first theoretical foundation is supervised statistical classification. A message is treated as an observation x described by numerical features. A learning algorithm estimates parameters from labelled examples and produces a decision function for a new observation. With TF-IDF and Logistic Regression, terms and n-grams define the feature space, while learned coefficients describe their association with the phishing class. Regularisation constrains the coefficients and helps reduce overfitting in a high-dimensional space (James et al., 2021; Manning et al., 2008).

This perspective explains the model component of PhishGuard AI. The email and SMS distributions are not assumed to be identical, so each mode uses a separate learned pipeline. The model estimates textual similarity to its training classes, but its inference remains conditional on that data. Dataset shift, new scam narratives, language variation and adversarial paraphrasing can therefore change performance. The theory supports probabilistic classification while also establishing why a model output should not be confused with verified identity or absolute truth.

#### 2.3.2 Signal Detection Theory and Threshold Trade-offs

Signal Detection Theory distinguishes the underlying evidence from the threshold used to decide whether a signal is present (Green & Swets, 1966). Applied to phishing, suspicious and legitimate messages produce overlapping evidence distributions. Moving the threshold can improve phishing recall but also increase false positives; moving it in the opposite direction may reduce nuisance warnings while increasing false negatives. There is no threshold that removes both errors when the classes overlap.

This theory informs the use of three risk bands in PhishGuard AI rather than a claim of perfect binary separation. Low Risk (0–39) indicates that the observed evidence is limited, Suspicious (40–69) indicates that review is warranted, and High Risk (70–100) indicates strong or combined warning signs. The intermediate band represents uncertainty and encourages independent verification. The bands are prototype triage rules and must be validated; they are not universal standards or calibrated attack probabilities.

#### 2.3.3 Human-Centred Explanation and Decision Support

The third foundation views the system as decision support for a human recipient. Explanation should connect the automated result to observable evidence and a practical response. Miller (2019) emphasised that useful explanations are selective and adapted to human expectations, while Wang et al. (2025) provided empirical evidence that concise, evidence-based smishing explanations can improve detection decisions.

Within this framework, a verdict without reasons is incomplete. PhishGuard AI presents triggered indicators, selected safe signals and recommendations such as avoiding a suspicious link, refusing to disclose an OTP, or confirming payment instructions through an independently obtained contact method. The system is intended to promote verification rather than obedience to an algorithm. This perspective also requires cautious language: a Low Risk result cannot guarantee safety, and a recognised sender string cannot establish authentication.

#### 2.3.4 Integrated Theoretical Position

The three perspectives are complementary. Statistical classification supplies data-driven evidence; Signal Detection Theory explains decision thresholds and unavoidable errors; and human-centred explanation governs how evidence is communicated. Together they support a hybrid architecture in which a classifier is neither used alone nor hidden behind an unexplained label. Explicit rules add inspectable security evidence, aggregation converts diverse evidence into a risk band, and the interface returns reasons and actions to the user. The framework also makes evaluation multidimensional: technical discrimination, error balance, explanation usefulness and practical limitations all matter.

### 2.4 Empirical Review of Selected Studies

#### 2.4.1 Al-Subaiey et al. (2024)

Al-Subaiey et al. (2024) developed an interpretable web-based artificial-intelligence platform for phishing-email detection. The authors sought to address two recurring weaknesses in research systems: dependence on restricted datasets and the absence of an application that an end user could access. Their work used a large public email collection, trained a high-performing machine-learning classifier and integrated explainable AI into a real-time web interface. The study reported an F1-score of 0.99.

The study is closely related to PhishGuard AI because it moves beyond an offline notebook to an interactive detector and treats interpretability as part of deployment. It demonstrates that model output can be translated into a user-facing service. However, the published abstract primarily concerns email, whereas the present project supports distinct email and SMS modes. A high result on the authors’ dataset also does not remove the need for temporal, cross-source and adversarial validation. The study provides a strong deployment precedent but leaves room for lightweight multi-channel analysis and explicit local evidence aggregation.

#### 2.4.2 Timko et al. (2024)

Timko et al. (2024) examined smishing from the user’s perspective rather than proposing another classifier. In an online study, 187 participants judged 16 SMS screenshots and completed a post-survey concerning security attitudes, behaviour and knowledge. Participants achieved 67.1% accuracy on fake messages but only 43.6% on real messages. Attention and security-related behavioural factors influenced performance, and elements such as the sender and URL affected interaction and comfort.

This study is important because automated detection ultimately influences a human decision. The results show that users can distrust legitimate messages as well as accept malicious ones, making false-positive communication a serious usability issue. The use of screenshots and a finite message set limits broad generalisation, and the research did not evaluate an automated detector. Nevertheless, it supports interfaces that expose sender and link evidence, preserve uncertainty and avoid presenting suspicion as certainty. These principles are reflected in PhishGuard AI’s reasons, risk bands and recommendation to verify through an independent channel.

#### 2.4.3 Alhuzali et al. (2025)

Alhuzali et al. (2025) conducted a broad comparison of fourteen machine-learning and deep-learning models across nine public phishing-email datasets and constructed merged variants for additional assessment. The model set included classical methods and neural architectures such as BERT, DistilBERT and RoBERTa. On the balanced merged data, BERT and RoBERTa produced approximately 98.99% and 99.08% accuracy respectively, and the authors reported that deep models generally outperformed classical models. Stochastic Gradient Descent was the strongest traditional method on average, at 98.17% accuracy.

The study’s value lies in its scale and standardised comparison. It shows that model ranking depends on the corpus and that strong classical baselines remain relevant. More importantly, the authors’ external-data results were below their internal merged-data values for some transformer models, illustrating that high within-distribution scores do not guarantee transfer. The study does not provide a dual email/SMS user application, but it strongly informs this project’s insistence on separate validation, multiple metrics and cautious interpretation of any future PhishGuard AI result.

#### 2.4.4 Brissett and Wall (2025)

Brissett and Wall (2025) investigated AI-generated phishing emails through a framework combining supervised classification, unsupervised clustering and watermarking. The work used TF-IDF features with methods including Logistic Regression and K-Means, and considered whether watermarking could support content provenance. It also examined the psychological principles exploited in persuasive phishing and the challenge of paraphrased or contextually manipulated text. Their controlled experiments showed strong supervised performance, while unsupervised clustering misclassified a meaningful portion of LLM-generated phishing in a reported condition.

The study confirms that the TF-IDF/Logistic Regression combination remains useful even in an LLM-era threat landscape, which supports its use as a lightweight baseline in PhishGuard AI. At the same time, dependence on watermark availability and controlled AI-generated corpora limits direct application to arbitrary real-world messages. Attackers are not required to preserve a watermark, and paraphrasing can alter detectable traces. The work therefore supports combining text classification with independent sender, URL and behavioural indicators rather than relying solely on signals of AI authorship.

#### 2.4.5 Patra et al. (2025)

Patra et al. (2025) proposed an email-phishing detector based on transformer-derived Dense Passage Retrieval embeddings and vector similarity search. Email representations were stored in a vector database and compared using similarity measures. Evaluation on the Enron corpus, Nazario phishing corpus and a phishing-validation email dataset produced 98.43% accuracy, 98.44% precision, 98.38% recall, 98.41% F1-score and an Area Under the Curve of 0.984 with cosine similarity.

This approach is significant because it reframes detection as semantic retrieval and reduces dependence on manually designed lexical features. It also offers a route to finding messages similar to previously observed campaigns. Its infrastructure is more complex than a saved TF-IDF/Logistic Regression pipeline, requiring a transformer embedding process and vector storage. Similarity to historical examples may also be less useful for a genuinely novel campaign, and the reported evaluation does not by itself establish adversarial robustness. The study presents a strong alternative architecture but does not directly address SMS, deterministic user guidance or local sender/domain checks.

#### 2.4.6 Zidan et al. (2025)

Zidan et al. (2025) proposed a hybrid email-phishing approach using NLP and three classical classifiers: Logistic Regression, decision tree and Random Forest. Their design considered email attributes including sender, subject, body and URL. A customised ChatGPT component received the classification outcome and produced explanations, highlighted relevant words and offered security tips intended to educate users.

The study is relevant to PhishGuard AI in two ways. First, it supports combining several observable email components rather than analysing the body in isolation. Second, it recognises that user education should accompany classification. The approach, however, depends on a generative component after detection, which introduces external-model cost, availability and output-reliability questions. Its abstract does not provide enough evidence to treat generated explanations as independently validated security facts. PhishGuard AI adopts a more constrained alternative: it maps deterministic findings to predefined recommendations. This is less flexible than generated advice but easier to audit within an academic prototype.

#### 2.4.7 Wang et al. (2025)

Wang et al. (2025) developed SmishX, an explainable SMS-phishing prototype based on LLM agents. Because an SMS provides little context, SmishX gathered external evidence such as domain and brand information, URL redirects and webpage screenshots, used that context in its reasoning process, and converted the result into a short explanation for non-expert users. On real-world SMS datasets, it achieved 98.8% overall accuracy. A user study with 175 participants found improved phishing-detection efficacy across age groups, and participants gave the system a System Usability Scale score of 82.6.

SmishX is one of the strongest related systems because it evaluates technical performance and human use. It demonstrates the value of external context and concise explanations. Its architecture is also substantially heavier than PhishGuard AI: it relies on LLM reasoning, redirect resolution, screenshot acquisition and other external sources. These capabilities can improve evidence but create cost, latency, privacy and dependency concerns. The authors also identified unresolved problems when a human and the AI disagree or the AI is wrong. PhishGuard AI offers a lighter local analysis path while acknowledging that it cannot match SmishX’s remote contextual investigation.

#### 2.4.8 Munoz and Islam (2025)

Munoz and Islam (2025) addressed the multiclass nature of mobile messaging by distinguishing ham, spam and smishing. Their SMS phishing dataset was imbalanced, with ham messages substantially outnumbering spam and smishing. The authors generated synthetic minority-class messages using GPT-2 Medium, used BERT embeddings, and constructed a chained transformer model. Synthetic samples were confined to the training partition to reduce leakage. The reported model exceeded 97% accuracy and achieved 0.98 precision, 0.96 recall and 0.97 F1-score.

The study directly addresses a limitation of treating every unwanted SMS as phishing. It also recognises the challenge of minority smishing examples and the need to protect evaluation data from synthetic-training leakage. Its limitations include dependence on generated examples and transformer resources; synthetic text may not reproduce the full diversity of live adversarial campaigns. PhishGuard AI currently performs a simpler risk-oriented assessment and does not claim validated three-class performance. The study provides a clear direction for future SMS retraining on a phishing-specific multiclass corpus.

#### 2.4.9 Ahmed and Sumesh (2026)

Ahmed and Sumesh (2026) proposed an ensemble phishing-email system designed around performance, computational efficiency and interpretability. They used Enron, SpamAssassin and Nazario data, performed preprocessing, feature engineering and selection, and evaluated hard- and soft-voting ensembles. LIME and prediction-error analysis were used to inspect and improve the models. The authors reported reductions of up to 95% in training time and 78% in inference time, 99.75% accuracy and F1-score on unseen data, an increase in phishing recall, and a 12.5% reduction in false negatives after explanation-guided refinement.

This research is particularly useful because it treats efficiency and error analysis as first-class requirements rather than reporting only a maximum score. It demonstrates that explainability can assist developers in identifying overfitting and misclassification, not merely produce a visual justification for users. However, the system concerns email and uses an ensemble that is more complex than the single linear classifier in each PhishGuard mode. The very high results remain tied to the selected public corpora. The study motivates future unseen-data testing and explanation-assisted error review for the current prototype.

#### 2.4.10 Uddin et al. (2026)

Uddin et al. (2026) fine-tuned RoBERTa for phishing-email classification and reported 98.45% accuracy. To improve transparency, they introduced LITA, a hybrid explanation method combining LIME with Transformers Interpret. The method presented positive and negative feature contributions and was designed to reduce inconsistencies between separate local-attribution techniques.

The study illustrates the current movement towards pairing high-performing contextual models with explanation mechanisms. It is relevant to PhishGuard AI because it recognises that users and developers need more than a label. However, token attribution can still be difficult for a non-expert to convert into a protective action, and the data were stated as available on request rather than supplied as an immediately reproducible benchmark. RoBERTa also demands more resources than the project’s TF-IDF pipelines. LITA is therefore a useful future comparison, while PhishGuard AI prioritises explicit warning statements and recommendations tied to locally observed features.

#### 2.4.11 Corpuz et al. (2026)

Corpuz et al. (2026) developed SMS-phishing detection for the Philippine context, where messages may combine Filipino and English. They collected labelled phishing and legitimate messages from public sources and surveys, applied tokenisation, lemmatisation and TF-IDF, and compared Support Vector Machines, Logistic Regression, Random Forest, K-Nearest Neighbours and Multinomial Naive Bayes. The Support Vector Machine with TF-IDF achieved the best F-score of 99.20%.

The study is important because it challenges Anglocentric detection and demonstrates that language and culture affect the vocabulary of deception. It also confirms that classical TF-IDF-based models can remain highly competitive in a tailored SMS setting. The data and linguistic environment are specific to the Philippines, so the reported result should not be transferred directly to Nigerian users. For PhishGuard AI, the work exposes a localisation gap: Nigerian English, Pidgin, indigenous languages, code-switching, local financial brands and region-specific scam narratives require dedicated collection and evaluation.

#### 2.4.12 Khandan et al. (2026)

Khandan et al. (2026) proposed an explainable multimodal framework with independently trained email-content and URL-feature models. Late fusion combined their outputs, while SHAP, LIME and feature importance identified influential evidence. Detected threats were also passed to an LLM for defensive recommendations based on the MITRE D3FEND framework. Five-fold cross-validation produced approximately 98% email accuracy and 97% URL accuracy, with precision and recall above 97%.

This framework is architecturally close to the hybrid principle used by PhishGuard AI because it preserves specialised components and combines their evidence later. It also connects detection, explanation and recommended action. However, the work concerns email and URL modalities rather than separate email and SMS user workflows, and its LLM/XAI stack is computationally more demanding. Cross-validation is useful, but future cross-dataset and adversarial evidence is still necessary. The study supports modular fusion while leaving space for a lightweight, deterministic and channel-aware implementation.

#### 2.4.13 Ahmed and Pourmoafil (2026)

Ahmed and Pourmoafil (2026) conducted a controlled comparison of TF-IDF with Logistic Regression and a fine-tuned DistilBERT model on 82,255 emails assembled from six public datasets. Both models exceeded 98% accuracy on clean in-distribution data. Under adversarial testing, however, TF-IDF/Logistic Regression fell to 64.00% and DistilBERT to 63.64%. LIME, SHAP and attention-rollout analysis suggested that the models relied on different evidence but had similarly severe vulnerability. The paper was a July 2026 preprint at the time of this review and had not yet undergone peer review.

This is the most direct caution for the model family used in PhishGuard AI. It shows that a transformer’s sophistication does not automatically provide adversarial robustness and that clean-data results can conceal operational weakness. It also suggests partially complementary error patterns, which may support carefully validated hybrid or ensemble approaches. The study does not evaluate the project’s exact pipelines or rule aggregation, so its percentages must not be attributed to PhishGuard AI. Instead, it justifies future adversarial, obfuscation and campaign-shift testing and reinforces the decision not to invent performance claims.

### 2.5 Review of Related Detection Systems

#### 2.5.1 Web-Based Email Detection Platform

The platform by Al-Subaiey et al. (2024) is the closest related work in deployment form. It combines email classification, explainability and a browser-accessible interface. Its principal strength is translating an experimental model into a practical interaction. In comparison, PhishGuard AI extends the interaction to both email and SMS and adds explicit sender, domain and URL heuristics. The trade-off is that the present prototype does not inherit the published platform’s reported model performance and must be evaluated independently.

#### 2.5.2 SmishX

SmishX by Wang et al. (2025) is the strongest related SMS system reviewed. It enriches short messages with live external context and uses LLM agents to explain the verdict. PhishGuard AI shares the goals of explanation and recommended action but operates without webpage screenshots, redirect following, remote threat intelligence or LLM generation. This makes PhishGuard simpler and more locally auditable, but also means it has less contextual evidence and cannot determine the remote behaviour of a submitted link.

#### 2.5.3 Hybrid Email, URL and Guidance Systems

The systems by Zidan et al. (2025) and Khandan et al. (2026) combine classification with several evidence sources and generated guidance. Khandan et al.’s late-fusion architecture is especially relevant because separate components retain specialised roles before aggregation. PhishGuard AI follows a comparable modular principle at a smaller scale: channel-specific text models operate alongside deterministic content, sender and URL checks before a risk score is assigned. Its recommendations are template-driven rather than generated by an LLM, which improves predictability but restricts expressive flexibility.

#### 2.5.4 Position of PhishGuard AI

PhishGuard AI occupies a practical middle position. It is broader than an email-only text classifier and lighter than an LLM-agent system with live browsing. It uses separate TF-IDF/Logistic Regression models for email and SMS, validates mode-specific inputs, performs local sender/domain and URL inspection, aggregates evidence into risk bands, explains relevant findings and persists the scan in Django. It does not authenticate senders, retrieve remote websites, inspect attachments, connect directly to an inbox or telecom provider, or guarantee that a Low Risk result is safe. Its contribution is the integration and transparent presentation of locally available evidence in a modest academic prototype.

### 2.6 Comparative Analysis of Selected Studies

Table 2.1 compares the thirteen empirical studies discussed in Sections 2.4.1–2.4.13. Reported metrics belong to the cited studies and their own evaluation settings; they are not results for PhishGuard AI. Differences in datasets, labels, splits and attack conditions mean that the numbers should not be ranked as though they came from one common benchmark.

[[TABLE 2.1 START]]
| Study | Medium and scope | Data or evaluation | Method | Main reported finding | Explainability or deployment | Limitation and relevance to this project |
| Al-Subaiey et al. (2024) | Email; end-user web detection | Large public email collection | Machine-learning classifier with XAI | F1-score of 0.99 | Real-time web platform; interpretable output | Email only; result remains dataset-dependent. Strong precedent for a usable explanatory interface. |
| Timko et al. (2024) | SMS; human detection behaviour | 187 participants; 16 SMS screenshots | Online judgement task and post-survey | 67.1% accuracy for fake SMS and 43.6% for real SMS | Evaluates user attention, behaviour and message areas of interest | Not an automated detector; finite stimuli. Shows need to manage both unsafe trust and false suspicion. |
| Alhuzali et al. (2025) | Email; broad model benchmark | Nine public datasets plus merged/balanced variants and external testing | Fourteen ML/DL models, including BERT, DistilBERT and RoBERTa | BERT 98.99% and RoBERTa 99.08% accuracy on balanced merged data; SGD strongest traditional model on average | Detailed comparative evaluation rather than a dual-channel application | External performance was lower for some models. Supports multi-dataset validation and strong baselines. |
| Brissett and Wall (2025) | AI-generated phishing email | Controlled human and LLM-generated email conditions | TF-IDF, Logistic Regression, K-Means and watermarking | Strong supervised classification; clustering had substantial AI-phishing errors in a reported condition | Considers provenance and adaptive two-layer detection | Watermarks may be absent or altered; controlled data. Supports combining text evidence with other indicators. |
| Patra et al. (2025) | Email; semantic similarity detection | Enron, Nazario and phishing-validation email data | DPR transformer embeddings, vector database and cosine similarity | 98.43% accuracy and 98.41% F1-score | Designed for efficient similarity search | Requires embedding/vector infrastructure and depends on representative stored examples; no SMS workflow. |
| Zidan et al. (2025) | Email; hybrid classification and education | Email sender, subject, body and URL attributes | Logistic Regression, decision tree, Random Forest, NLP and customised ChatGPT | Demonstrates integrated classification, explanation and security guidance | ChatGPT highlights words and supplies tips | Generative dependence and limited reported evaluation detail. Motivates auditable explanations and recommendations. |
| Wang et al. (2025) | SMS; explainable user-facing detection | Real-world SMS datasets; user study N=175 | LLM agents with domain, brand, redirect and screenshot context | 98.8% overall accuracy; explanations improved user decisions; SUS 82.6 | SmishX prototype with concise evidence-based explanations | Resource-, privacy- and dependency-heavy; human-AI disagreement remains open. Benchmark for explanation usability. |
| Munoz and Islam (2025) | SMS; ham/spam/smishing multiclass detection | Imbalanced SMSPD data; synthetic data restricted to training | GPT-2 Medium augmentation, BERT embeddings and chained transformers | Accuracy above 97%; precision 0.98, recall 0.96 and F1 0.97 | SHAP analysis reported; resource-aware motivation | Synthetic and transformer dependence; corpus representativeness remains a concern. Highlights spam/smishing distinction. |
| Ahmed and Sumesh (2026) | Email; efficient interpretable ensemble | Enron, SpamAssassin and Nazario; unseen-data evaluation | Feature engineering, hard/soft voting, LIME and error analysis | 99.75% accuracy/F1 on unseen data; up to 95% lower training time, 78% lower inference time and fewer false negatives | Interpretability used for both explanations and model refinement | Email only and public-corpus dependent. Supports efficiency and explanation-led error analysis. |
| Uddin et al. (2026) | Email; transformer classification and XAI | Phishing-email dataset with class balancing | Fine-tuned RoBERTa and hybrid LITA explanation | 98.45% accuracy | LITA combines LIME and Transformers Interpret | Higher resource requirement; data available on request; attribution still needs user-centred translation. |
| Corpuz et al. (2026) | SMS; Filipino/English language-aware detection | Public and survey-sourced phishing and legitimate SMS | TF-IDF with SVM, Logistic Regression, Random Forest, KNN and MNB | SVM with TF-IDF achieved 99.20% F-score | Classical, culturally tailored content detector | Country- and language-specific data. Demonstrates need for Nigerian localisation and multilingual validation. |
| Khandan et al. (2026) | Email plus URL multimodal detection | Five-fold cross-validation on email and URL datasets | Independent models, late fusion, SHAP, LIME, feature importance and LLM guidance | About 98% email accuracy and 97% URL accuracy; precision/recall above 97% | Explainable multimodal framework with MITRE D3FEND recommendations | Computationally richer and not an email/SMS workflow. Supports modular evidence fusion. |
| Ahmed and Pourmoafil (2026) | Email; adversarial robustness comparison | 82,255 emails from six datasets; clean, synthetic and adversarial tests | TF-IDF/Logistic Regression versus fine-tuned DistilBERT; LIME, SHAP and attention rollout | Both above 98% on clean data but only 64.00% and 63.64% under adversarial testing | Explanations used to inspect failure patterns | Non-peer-reviewed preprint; controlled adversarial set. Direct warning against inferring robustness from clean accuracy. |
[[TABLE 2.1 END]]

The comparison reveals four consistent patterns. First, both classical and transformer-based models can report very high results on selected datasets. Second, evaluation context matters: external or adversarial testing can produce a markedly different picture from random internal splits. Third, explainability has become a major design objective, but studies vary between technical attribution, generated advice and empirically tested user explanations. Fourth, most systems specialise in either email or SMS; fewer provide one practical interface with separate channel-aware paths and transparent local evidence aggregation.

### 2.7 Identified Research Gaps

#### 2.7.1 Fragmentation by Communication Channel

Most reviewed detectors focus on email or SMS, not both. Email and SMS share deceptive language but differ in available fields, length, sender representation and user context. A single undifferentiated model can conceal these differences. There is room for a practical interface that supports both media while preserving separate validation and model pipelines.

#### 2.7.2 Gap Between Experimental Scores and Practical Use

Several studies report strong model metrics but do not evaluate a complete end-user workflow. Al-Subaiey et al. (2024) and Wang et al. (2025) are notable deployment-oriented exceptions. A useful prototype must accept realistic fields, handle invalid input, route the request correctly, explain the outcome and support a safe next action. PhishGuard AI addresses this integration gap at prototype scale, although its own effectiveness still requires verified evaluation.

#### 2.7.3 Clean-Data and Dataset-Generalisation Gap

High accuracy on an internal test split does not establish performance on a new campaign, later time period, different language or adversarially rewritten message. The external results discussed by Alhuzali et al. (2025) and the adversarial collapse reported by Ahmed and Pourmoafil (2026) make this limitation explicit. Larger real-world, cross-source, temporal and adversarial testing remains necessary for the current project.

#### 2.7.4 Explanation-to-Action Gap

Many XAI studies identify influential tokens, but a recipient also needs meaning and action. SmishX links evidence to a concise explanation and improves user decision-making, but relies on a resource-intensive LLM-agent architecture. There is a gap for lightweight, deterministic explanations that state observable concerns and recommend verification without claiming complete causal insight into the classifier.

#### 2.7.5 Localisation and Language Gap

Corpuz et al. (2026) demonstrated the importance of culture and code-switching in SMS detection. Much public phishing research remains centred on English corpora created outside Nigeria. Nigerian English, Pidgin, local organisations, indigenous languages and regional scam narratives are underrepresented. PhishGuard AI’s current English-oriented resources do not close this gap; they make it a clear priority for future data collection.

#### 2.7.6 Evidence-Fusion and Transparency Gap

Content-only classification can miss sender and URL inconsistency, while isolated rules are easy to evade. Advanced multimodal systems exist, but may rely on heavy transformer, LLM or remote-browser infrastructure. PhishGuard AI explores a smaller hybrid design that combines channel-specific classical models with local rules and makes the aggregation visible through findings and risk bands. Its lightweight nature is a contribution to prototyping, not evidence of superior detection.

#### 2.7.7 Honest Capability-Boundary Gap

User-facing systems can create false confidence when they imply that a sender or webpage has been verified. The current project explicitly distinguishes local format and string checks from DNS, WHOIS, SPF, DKIM, DMARC, redirect, webpage, malware and reputation analysis. This boundary is important for academic validity and safe use. Future integrations can add stronger evidence, but their presence must be demonstrated rather than assumed.

### 2.8 Conceptual Framework for PhishGuard AI

The conceptual framework translates the reviewed literature into the project’s proposed detection flow. The independent variables are the user-selected medium and supplied message evidence: sender, optional email subject, message body and embedded URLs. The processing variables are mode-specific validation, text representation, Logistic Regression classification, content rules, sender/domain inspection, URL inspection and risk aggregation. The dependent outputs are the bounded score, risk band, human-readable findings, safe signals, recommendations and persisted scan record.

[[FIGURE 2.1: PHISHGUARD AI CONCEPTUAL FRAMEWORK]]

**Figure 2.1:** Conceptual framework for PhishGuard AI (author’s design, 2026).

The first stage distinguishes email from SMS so that each request is validated and routed to the appropriate saved pipeline. Email accepts a sender address, optional subject and body; SMS accepts a telephone number, short code or alphanumeric sender ID and body. This separation responds to the channel-fragmentation gap identified in the literature.

The second stage produces parallel evidence. The relevant TF-IDF/Logistic Regression pipeline estimates textual risk. Deterministic content rules identify selected social-engineering patterns. Sender/domain intelligence checks locally observable identity inconsistencies, and URL analysis examines extracted links for selected structural warning signs. These components are complementary; none independently authenticates a message.

The third stage aggregates evidence. The classifier contribution is bounded, weighted findings are added, contextual safeguards are applied and the score is constrained to the 0–100 range. The implemented triage bands are Low Risk from 0 to 39, Suspicious from 40 to 69, and High Risk from 70 to 100. These are design thresholds for the prototype and not empirically established universal standards.

The fourth stage supports the user’s decision. The interface presents the verdict and score, triggered indicators, selected safe signals and recommended actions. The scan can be stored locally for later review. The framework includes an evaluation boundary—confusion-matrix metrics, cross-dataset testing, adversarial testing, multilingual assessment and user evaluation—but these activities must be performed and verified before results are inserted. They are not an automatic self-learning feedback loop in the current implementation.

For editability, Figure 2.1 is constructed in the Word document from native table cells and text. A matching vector source is supplied separately as `PhishGuard_AI_Conceptual_Framework.svg`; it can be inserted into Word and opened or imported into Microsoft Visio for refinement. The separate source preserves individual vector rectangles, text elements and connectors rather than flattening the framework into a screenshot.

### 2.9 Summary of Chapter

This chapter reviewed phishing and smishing as adaptive social-engineering problems involving message content, sender identity, domains, URLs and user judgement. It explained the foundations of NLP, TF-IDF, Logistic Regression, rule-based analysis, hybrid aggregation, sender intelligence, URL inspection, explainability and evaluation. The theoretical framework combined supervised statistical classification, Signal Detection Theory and human-centred explanation to justify a risk-oriented decision-support system rather than an unexplained binary label.

Thirteen recent empirical studies were reviewed individually and compared. The evidence shows that classical, ensemble, transformer, vector-search and multimodal approaches can perform strongly on selected datasets. It also shows that performance depends on the data and test condition, explanations differ in practical usefulness, resource requirements vary substantially, and clean-data accuracy does not demonstrate adversarial robustness. SMS research further highlights the importance of distinguishing spam from smishing, accounting for limited context and supporting users with clear evidence.

The identified gaps concern multi-channel integration, the transition from experimental models to usable systems, generalisation, explanation-to-action, Nigerian localisation, lightweight evidence fusion and transparent capability boundaries. PhishGuard AI responds with separate email and SMS TF-IDF/Logistic Regression pipelines, deterministic content and sender/URL evidence, bounded risk aggregation, findings and recommendations in a Django prototype. It does not resolve all gaps and cannot support strong performance claims until larger real-world, cross-source, multilingual, usability and adversarial evaluations are completed. Chapter Three will describe the methodology, system requirements, data preparation, architecture, implementation tools and testing plan used for the project.

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

## CHAPTER FIVE

## SUMMARY, CONCLUSION AND RECOMMENDATIONS

### 5.1 Introduction

This chapter concludes the study on PhishGuard AI, a web-based prototype for assessing phishing risk in email and SMS messages. It summarises the problem addressed, the design and implementation approach, the evidence obtained, the extent to which the study objectives were achieved, and the contribution of the work. It then states the conclusion that can be defended from the available evidence and presents prioritised recommendations and future research directions.

The need for continued work remains substantial. The Anti-Phishing Working Group (2026) recorded 971,181 phishing attacks in the first quarter of 2026, an increase of 13.8% from the preceding quarter, while observed telephone-based fraud encompassing vishing and smishing rose by 15%. Such figures reinforce the importance of tools that help users pause, inspect evidence and verify a message before surrendering information or following an instruction. They do not, however, imply that any one classifier can cover the changing threat landscape. A responsible conclusion must separate a successfully implemented prototype from a validated production security service.

Accordingly, this chapter retains the evidence boundary established throughout the report. The repository supports conclusions about the implemented Django workflow, the behaviour covered by its automated tests, eight fixed hybrid-analysis scenarios and the saved SMS text classifier on the documented internal data split. It does not support an email performance claim, a complete hybrid-system accuracy claim, a usability score or a claim of production readiness. The recommendations therefore focus first on resolving the specific evidence, engineering, privacy and deployment gaps that prevent stronger claims.

### 5.2 Summary of the Study

#### 5.2.1 Problem, Aim and Scope

The study began from a practical problem: phishing is delivered through more than one digital medium, yet a user who receives a suspicious message often needs more than a binary label. The user needs to know what was observed, why it may matter and what safe action should follow. Model-only output can be difficult to interpret, while rule-only systems can be brittle when attackers alter wording. The project therefore asked how a lightweight web application could combine statistical text classification with transparent local evidence for both email and SMS.

The aim was to design and implement a practical web-based system that assesses phishing risk in email and SMS by combining machine-learning text classification with explainable content, sender and URL checks. The implemented scope accepts manually supplied message data. Email mode uses a sender email address, an optional subject and a body; SMS mode uses a number, short code or alphanumeric sender identifier and a body. Each channel selects its own saved TF-IDF/Logistic Regression artefact. The analyzer then adds locally observable content patterns, sender/domain indicators and URL characteristics before producing a channel-appropriate verdict, explanations and recommended actions.

The scope intentionally excludes autonomous inbox access, carrier-level filtering, attachment and QR-code analysis, malware execution, live webpage crawling, full mail-header authentication, live reputation feeds and enterprise incident response. The system also cannot authenticate an identity from typed sender text or guarantee that a low-risk message is legitimate. These exclusions are not incidental: they determine what the prototype can safely claim.

#### 5.2.2 Research and Development Approach

The study used a design-science-oriented process, moving from problem identification and objective definition through design, development, demonstration, evaluation and communication (Peffers et al., 2007). Chapter One established the problem, aim, objectives, scope and limitations. Chapter Two reviewed email phishing, smishing, text representation, classical and advanced detection methods, hybrid evidence, explainability and directly related studies. Chapter Three translated those findings into requirements, architecture, data flow, model, interface, persistence and testing designs. Chapter Four inspected and evaluated the implemented repository rather than replacing it with an idealised system description.

The technical design, as preserved in the project repository (Jesutofaye, 2026), uses Django for routing, validation, request handling, templates and the local ORM. Statistical text processing is channel-specific: the email and SMS artefacts are separate `(vectorizer, model)` tuples based on TF-IDF and Logistic Regression. The hybrid analyzer combines the selected model output with explicit evidence from message content, URLs and sender/domain text. Contextual safeguards distinguish direct suspicious requests from selected awareness or negated wording, while an unexplained model output is prevented from producing an unsupported warning by itself. The application returns risk-oriented guidance rather than autonomously blocking, accusing or reporting a sender.

Evaluation was evidence-led. The repository’s tests were rerun; model artefacts were loaded and inspected; fixed synthetic examples were passed through the implemented analyzer; the bundled SMS corpus and documented split were reproduced; exact-message overlap was audited; and Django normal, deployment and migration checks were preserved. The study did not substitute a fabricated email dataset, browser screenshot or participant survey when the required evidence was unavailable.

#### 5.2.3 Chapter-by-Chapter Summary

Table 5.1 summarises how the five chapters combine into the complete study.

[[TABLE 5.1 START]]
| Chapter | Principal purpose | Main output |
| One | Define the phishing problem, aim, objectives, significance, scope and limitations | Evidence-bounded project specification for an email/SMS prototype |
| Two | Review concepts, methods and related empirical studies | Theoretical and empirical basis for channel-specific, hybrid and explainable detection |
| Three | Specify the research method, requirements and system design | Project-specific architecture, workflow, data, database, interface and test designs |
| Four | Present implementation, testing, verified results and discussion | Repository-grounded functional evidence, SMS evaluation, diagnostics and limitations |
| Five | Synthesize findings and determine justified next steps | Final conclusion, objective assessment, recommendations and future-work roadmap |
[[TABLE 5.1 END]]

**Table 5.1:** Summary of the study by chapter

The chapters form a traceable sequence. The requirements in Chapter One informed the literature gap in Chapter Two. The gap informed the hybrid and explainable design in Chapter Three. Chapter Four then checked the design against the source code and preserved evidence. This final chapter does not introduce new experimental results; it consolidates what those preceding stages demonstrate and identifies what remains unproven.

### 5.3 Summary of Major Findings

#### 5.3.1 Implementation Findings

The central implementation finding is that PhishGuard AI exists as a coherent, practical academic prototype rather than merely as a model-training notebook. The root route introduces the two supported channels, and the analysis route supplies a mode-aware form. Server-side validation applies the appropriate sender rules, lengths and required fields. SMS subjects are cleared both in the interface behaviour and in backend request handling, reducing accidental cross-channel input. Missing models, corrupt models, invalid forms and unexpected processing errors are separated from risk verdicts so that a failed analysis is not misrepresented as a safe or suspicious result.

The repository contains two independent serialized text-classification artefacts. The saved email vectorizer uses lowercase word features, English stop-word removal, unigram/bigram features and a maximum of 20,000 features; its Logistic Regression estimator uses a maximum of 200 iterations. The saved SMS vectorizer uses lowercase text, Unicode accent stripping, unigram/bigram features, `min_df=1` and a maximum of 15,000 features; its Logistic Regression estimator uses balanced class weights, `random_state=42` and a maximum of 2,000 iterations. The analyzer selects the artefact associated with the submitted channel instead of applying one model indiscriminately to both media.

The statistical output is supplemented with local indicators. Content checks cover selected urgent or threatening language, credential and identity-data requests, OTP requests, changed-payment instructions, money or reward lures and related patterns. URL checks inspect explicit HTTP(S) links for selected shorteners, raw-IP hosts, `@` obfuscation, punycode and selected higher-risk top-level domains without visiting the destination. Email sender intelligence extracts locally observable address and domain parts, checks selected recognised-domain relationships, flags some one-character brand imitations and identifies selected organisational claims made through public email providers. These operations are heuristic observations, not live authentication.

The analyzer maps the combined evidence to bounded internal risk bands: 0–39 for Low Risk, 40–69 for Suspicious and 70–100 for High Risk. Email presents three risk-oriented states, while SMS simplifies the user-facing output to “Message Appears Safe” or “Message Appears Suspicious” and deliberately hides the numerical score. The result page presents named reasons or safe signals and protective actions. This design supports user judgement, but the score remains an engineering decision index rather than a calibrated probability of fraud.

#### 5.3.2 Functional Verification Findings

The preserved automated verification passed all 47 tests in 0.971 seconds. The suite comprised 35 classifier and analyzer tests, six result-layout tests and six view/mode tests. It covered correct channel-model selection, sender validation, body and subject handling, routine notifications, anti-fraud awareness messages, explicit and quiet credential requests, OTP requests, payment-redirection fraud, shortened URLs, public-provider impersonation, look-alike domains, bounded output, result wording and controlled failure behaviour.

Eight fixed synthetic scenarios complemented the test suite. A routine receipt with a high raw model probability remained Low Risk because no explainable warning evidence was found. A recognised-domain awareness notice also remained Low Risk. A shortened URL produced a Suspicious result requiring independent review. A public-provider bank impersonation and a one-character look-alike domain combined with direct demands reached High Risk. In SMS mode, a routine transaction was presented as safe, while an OTP-sharing request and an urgent reward lure were presented as suspicious. These examples demonstrate the intended interaction between model and rule evidence, not a statistical estimate of population performance.

Persistence was only partially verified. The view calls the `ScannedEmail` ORM model with the expected fields after successful analysis, and the relevant automated test uses a mock to verify that call. However, the application migrations directory contains no committed initial migration, and `makemigrations --check --dry-run` reports that `0001_initial.py` is required. Therefore, the software expresses the persistence design, but end-to-end creation and use of the database table is not yet established from a clean deployment.

#### 5.3.3 Quantitative SMS Findings

The bundled SMS corpus, derived from the SMS Spam Collection documented by Almeida et al. (2011), contains 5,574 records: 4,827 ham and 747 spam. The documented stratified 80/20 split with `random_state=42` produces 4,459 training records and 1,115 test records. When the saved SMS artefact was evaluated on that test partition, it correctly classified 1,096 messages and made 19 errors. With spam as the positive class, accuracy was 98.30%, precision was 93.92%, recall was 93.29% and F1-score was 93.60%. The confusion matrix contained 957 true negatives, nine false positives, ten false negatives and 139 true positives.

Those values show that the compact sparse-text baseline fits the documented internal split well, but they require important qualifications. The source labels describe ham and broad spam, not a current phishing-only or smishing-only taxonomy. An exact-message audit found 5,160 unique normalised messages and 414 duplicate rows beyond the first occurrence. Under the documented split, 139 of the 1,115 test rows—12.47%—had exact text present in training. On the 976 exact-text-unseen test rows, F1-score was 91.89%. Removing exact duplicates before a new deterministic split and fit produced an F1-score of 91.95%. These sensitivity results remain useful, but they show why the headline internal result must not be presented as expected real-world detection effectiveness.

The 19 primary errors also illustrate limitations of sparse lexical modelling and the broad corpus labels. False positives included abbreviated conversational or service-like wording; false negatives included premium-rate promotions, warning/complaint language and messages whose isolated label was not obvious. A future phishing-specific evaluation should separate benign notifications, marketing, generic spam, credential phishing, financial fraud, OTP theft and malicious-link smishing rather than treating every positive example as the same operational threat.

#### 5.3.4 Evidence and Readiness Findings

No defensible email accuracy, precision, recall, F1-score or confusion matrix was produced. Although the saved email artefact loads and its structure can be inspected, its training script points to machine-specific external CSV paths and the repository does not preserve the required source datasets, lawful provenance record, immutable split or label manifest. A numerical email result without those materials would be unverifiable and was therefore not invented.

The complete hybrid system also lacks a labelled locked evaluation set. The SMS corpus can assess the SMS text model against its broad labels, but it cannot directly validate final email risk bands, the SMS presentation threshold or the combined effects of sender, URL, content and contextual rules. The fixed scenarios demonstrate selected behaviours only. Similarly, no participant study was conducted, so satisfaction, trust, comprehension, task completion and usability scores remain unknown.

Deployment diagnostics identified six Django security recommendations in the supplied development settings: no HSTS duration, no forced HTTPS redirect, a development-style secret key, non-secure session cookies, non-secure CSRF cookies and `DEBUG=True`. The application also persists full submitted content without a complete user-facing retention notice or implemented deletion controls. The Nigeria Data Protection Commission (2025) emphasises lawfulness and transparency, purpose limitation, data minimisation, storage limitation, confidentiality, integrity, availability, accountability, and privacy by design and default. These principles make data governance a prerequisite rather than an optional enhancement if real messages are to be processed or stored.

Table 5.2 consolidates the principal final findings and their correct interpretation.

[[TABLE 5.2 START]]
| Area | Verified finding | Defensible interpretation | What must not be claimed |
| Implemented workflow | Django routes, validated modes, separate artefacts, hybrid analyzer, explanations and recommendations are present | Core prototype workflow is implemented | Automatic inbox/telecom integration or live threat investigation |
| Functional tests | 47 of 47 tests passed in 0.971 seconds | Covered component and view behaviours worked in the verification environment | Complete absence of software defects or production reliability |
| Fixed scenarios | Eight synthetic cases produced intended low, review and high-risk patterns | Selected hybrid decisions are demonstrable and reproducible | Population accuracy, sensitivity or specificity of the hybrid system |
| SMS text classifier | 98.30% accuracy and 93.60% F1 on the documented 1,115-record hold-out | Strong internal baseline on the available broad spam/ham corpus | Current Nigerian smishing effectiveness or universal phishing accuracy |
| SMS data integrity | 12.47% of test rows had exact training text; stricter F1 was approximately 91.9% | Primary split may be optimistic; sensitivity analysis supports caution | A leakage-free external benchmark |
| Email text classifier | Artefact loads, but source data and reproducible evaluation are unavailable | Implementation presence can be reported | Any email accuracy, precision, recall, F1-score or confusion matrix |
| Persistence | ORM call and fields exist; migration is absent and test is mocked | Persistence design is partially verified | Clean-deployment database readiness |
| Deployment and privacy | Six deployment warnings and incomplete retention disclosure remain | Development prototype requires remediation | Production-ready, compliant or secure public service |
| Usability | Interface structure and cautious wording were inspected | Design intentions can be described | User satisfaction, trust, comprehension or SUS score |
[[TABLE 5.2 END]]

**Table 5.2:** Consolidated findings and evidence boundaries

### 5.4 Achievement of the Aim and Objectives

#### 5.4.1 Achievement of the Aim

The aim was achieved at the level of design and practical prototype implementation. PhishGuard AI provides a web-based workflow for email and SMS, applies separate machine-learning text models, adds explainable local checks and returns risk-oriented guidance. The source code, model artefacts, test suite and controlled scenarios support that conclusion.

The aim was not achieved at the level of validated operational protection. The project has not established email model effectiveness, final hybrid-system performance, contemporary Nigerian generalisation, adversarial robustness, participant usability, complete database deployment, privacy compliance or hardened public operation. The correct final description is therefore: **PhishGuard AI is an implemented and functionally tested academic decision-support prototype with a reproducible internal SMS text-classifier baseline; it is not a production-ready cybersecurity service.**

#### 5.4.2 Assessment of the Specific Objectives

Table 5.3 returns to the seven objectives stated in Chapter One and applies a conservative completion judgement. “Achieved” means that the objective is supported within the declared project scope. “Partially achieved” means that an implementation exists but a material part of the required evidence or operation remains incomplete.

[[TABLE 5.3 START]]
| No. | Specific objective | Evidence of achievement | Final assessment |
| 1 | Examine email/SMS phishing characteristics and relevant automated approaches | Conceptual, theoretical and empirical review; comparative discussion of directly relevant studies | Achieved |
| 2 | Represent text with TF-IDF and apply separate Logistic Regression classifiers to email and SMS | Two independent loadable artefacts and mode-selection tests | Achieved for implementation; effectiveness verified only for SMS |
| 3 | Develop a Django interface with channel-appropriate inputs and validation | Landing page, mode-aware form, server-side validation and view tests | Achieved |
| 4 | Combine machine learning with content, URL, sender/domain and contextual safeguards | Implemented analyzer, targeted tests and fixed scenarios | Achieved for documented local rules; complete hybrid accuracy unmeasured |
| 5 | Generate risk verdicts, readable reasons and protective actions | Channel-specific templates, evidence lists, safe signals and recommendations | Achieved at implementation and functional-test level |
| 6 | Persist submitted scans and outcomes for local review | ORM model and successful-analysis create call exist; test uses a mock; initial migration is absent | Partially achieved |
| 7 | Conduct functional testing and define evidence-led validation for larger real-world data | 47 tests, eight scenarios, reproducible SMS evaluation and explicit external-validation plan | Achieved for functional testing and evaluation design; larger real-world validation remains future work |
[[TABLE 5.3 END]]

**Table 5.3:** Final assessment of the specific objectives

The assessment shows that the project’s primary educational and engineering objectives were substantially achieved, but not every operational implication is complete. In particular, objective six requires an initial migration and clean-database integration test, while the effectiveness part of objectives two, four and seven requires restored email evidence and a representative final-decision benchmark.

### 5.5 Contributions of the Study

The study’s contributions are practical and integrative rather than a claim of a newly invented machine-learning algorithm. TF-IDF and Logistic Regression are established techniques. The value of the project lies in how channel selection, conventional classification, local evidence, result wording and evaluation discipline were assembled into an inspectable prototype.

#### 5.5.1 Technical Contribution

First, the project implements a dual-medium workflow with independent email and SMS artefacts. This prevents accidental reuse of one channel’s vectorizer/model pair for another channel and demonstrates a modular route for adding or replacing channel-specific models.

Second, the hybrid analyzer connects statistical output to explicit content, sender and URL observations. It includes safeguards for selected awareness/negation contexts and limits unexplained model-only warnings. This design illustrates a useful principle: if a security warning is shown to a user, the interface should be able to state at least one observable reason. The contribution is not proof that every resulting decision is correct; it is an implemented pattern for making the basis of a decision inspectable.

Third, the application adapts its interaction to the medium. Email mode accepts a subject and email-form sender, whereas SMS mode removes the subject and accepts telephone numbers, short codes or sender identifiers. SMS also uses simpler result wording and suppresses a numerical score that could imply false precision. The prototype therefore treats channel differences as an interface and analysis concern rather than a cosmetic label.

#### 5.5.2 Evaluation and Reporting Contribution

The study preserves reproducible Chapter Four evidence scripts and machine-readable records instead of reporting only manually transcribed values. It evaluates the saved SMS artefact, records input checksums, audits exact-message overlap, reports unseen-message and deduplicated sensitivity views, and preserves the automated test and deployment-diagnostic outputs. This improves traceability from a report statement back to a repository artefact.

The explicit treatment of unavailable evidence is also a contribution to responsible academic reporting. Email metrics, browser screenshots and user-study outcomes were left as labelled placeholders rather than reconstructed or estimated. The result is less visually complete than a report containing invented values, but it is more scientifically defensible.

#### 5.5.3 Educational and User-Safety Contribution

PhishGuard AI demonstrates how a classifier can be placed within a caution-oriented workflow. Reasons draw attention to suspicious requests and inconsistencies, while recommended actions direct the user to trusted independent channels. This supports the idea that automated detection should assist, not replace, human verification. Wang et al. (2025) similarly emphasise the value of evidence-based walkthroughs in SMS-phishing judgement, although their system and evaluation are considerably broader than this prototype.

Table 5.4 summarises the contributions without overstating novelty.

[[TABLE 5.4 START]]
| Contribution | Practical value | Boundary |
| Channel-separated model use | Reduces cross-channel model confusion and supports modular replacement | Does not establish either model’s external validity |
| Explainable hybrid aggregation | Connects model output to named local evidence and actions | Rules are static and final decisions lack a population benchmark |
| Context safeguards | Reduces selected warnings caused by awareness or negated wording | Does not solve general language understanding |
| Medium-aware interface and result wording | Aligns required fields and presentation with email/SMS use | Has not undergone participant usability evaluation |
| Reproducible SMS evidence package | Preserves metrics, hashes, overlap audit and sensitivity runs | Corpus is old and broadly spam-labelled |
| Transparent limitation reporting | Prevents unsupported performance and readiness claims | Outstanding evidence must still be collected |
[[TABLE 5.4 END]]

**Table 5.4:** Contributions and their boundaries

### 5.6 Conclusion

This study designed, implemented and evaluated PhishGuard AI as a practical web-based prototype for phishing-risk assessment across email and SMS. The system uses Django to collect and validate user-supplied message data, selects a separate TF-IDF/Logistic Regression artefact for each channel, examines selected message, URL and sender/domain indicators, aggregates the evidence into bounded risk output, and presents explanations and recommended protective actions. The project therefore demonstrates that a conventional linear text classifier can be integrated with explicit local checks to produce a more understandable decision-support workflow than a raw class label alone.

The repository evidence supports the conclusion that the implemented core functions are coherent within the tested environment. All 47 automated tests passed, and eight controlled scenarios demonstrated selected safe, review and high-risk behaviours. The saved SMS text classifier produced a strong internal result on the documented hold-out. However, duplicate leakage and broad spam labels weaken the generalisation of that result: 12.47% of test rows had exact text in training, and stricter sensitivity views reduced positive-class F1-score from 93.60% to approximately 91.9%. The value remains a classifier baseline, not a real-world smishing guarantee.

No equivalent email performance conclusion is possible because the repository lacks the source datasets, manifest and reproducible split needed to audit the saved email artefact. Nor can the fixed scenarios be converted into a complete hybrid accuracy measure. The missing application migration, six deployment-security warnings, incomplete persistence disclosure, absence of browser evidence and absence of a participant usability study further limit readiness.

The final conclusion is therefore deliberately bounded. **PhishGuard AI achieves its principal aim as an implemented, explainable and functionally tested academic prototype. It provides a credible foundation for further research and engineering, but it must not yet be represented as production-ready, universally accurate or validated against contemporary real-world Nigerian phishing.** Its strongest contribution is the combination of multi-channel model selection, explicit evidence, cautious user guidance and transparent evaluation boundaries. Its next stage should prioritise data integrity, reproducible email and hybrid evaluation, security and privacy remediation, and supervised real-user validation before feature expansion or public deployment.

### 5.7 Recommendations

The recommendations are prioritised because not all improvements have equal urgency. Evidence integrity, database correctness, security and privacy controls should be resolved before adding impressive but weakly validated functionality. The National Institute of Standards and Technology (2023) organises trustworthy AI risk work around Govern, Map, Measure and Manage. Applied to this project, governance and scope definition should precede measurement; measurement should precede broad claims; and monitored risk management should precede public operation.

#### 5.7.1 Immediate Evidence and Data Recommendations

1. **Restore lawful, reproducible email-model evidence.** The email training datasets should be recovered only where their provenance and permitted use can be documented. A manifest should record source, licence or authority, acquisition date, label definition, preprocessing, duplicate handling, class distribution and checksum. The machine-specific paths in the training script should be replaced with repository-relative or configurable paths. A locked split and external test set should then be created without overwriting the currently deployed artefact until comparison is complete.

2. **Build a contemporary phishing-specific SMS corpus.** The current broad ham/spam collection should remain a historical baseline, not the final benchmark. New data should distinguish benign personal messages, legitimate service alerts, marketing, generic spam, credential phishing, financial fraud, OTP theft, malicious-link smishing and impersonation. Collection and annotation should include Nigerian English, Pidgin, code-switching, locally relevant organisations, telecom patterns and current scam narratives, subject to lawful and ethical processing.

3. **Remove split leakage by design.** Exact and near-duplicate templates should be grouped before splitting. Messages from the same campaign, sender pattern or template family should remain in one partition. In addition to a grouped hold-out, a time-based test should be reserved to estimate performance on later campaigns. Checksums and indices should be preserved so that every published value can be regenerated.

4. **Create a labelled final-decision benchmark.** A separate dataset should exercise complete email and SMS analyzer outputs, not only the text model. Each case should contain the evidence required by the intended scope and an independently reviewed final label. This benchmark should measure the risk bands, rule/model disagreements, explanations and recommendations. Classifier and hybrid metrics should remain separately reported.

5. **Report uncertainty and meaningful error costs.** Future evaluations should include confusion matrices, precision, recall, F1-score, false-positive and false-negative rates, class prevalence and confidence intervals or repeated estimates. Threshold selection should reflect the different harms of missed credential theft and unnecessary user alarm. Performance should be reported by channel, threat type, language and time period instead of as one universal accuracy.

#### 5.7.2 Immediate Engineering and Security Recommendations

1. **Create and test the initial migration.** Generate and review `detector/migrations/0001_initial.py`, apply it to a clean database and add an integration test that verifies an actual `ScannedEmail` record rather than only a mocked call. Define migration and backup procedures before any retained data becomes operationally important.

2. **Separate development and production configuration.** Production settings should load a strong secret from a protected environment or secret manager, set `DEBUG=False`, define controlled hosts, force HTTPS at the correct deployment layer, enable secure session and CSRF cookies, and introduce HSTS only after HTTPS behaviour has been tested. Django’s deployment checklist and `check --deploy` should become release gates (Django Software Foundation, 2025).

3. **Minimise stored message content.** Raw email and SMS text can contain names, account details, transaction information, OTPs and other sensitive data. The preferred default is not to retain raw text after analysis unless a justified purpose requires it. If retention is necessary, implement explicit notice and lawful basis, configurable retention, encryption, access control, deletion, audit logging, redaction or pseudonymisation, and breach/incident procedures in line with the Nigeria Data Protection Commission (2025).

4. **Add operational safeguards.** Introduce rate limiting, request-size controls at the web server, structured security logging without message-body leakage, dependency and vulnerability scanning, model-artefact integrity checks, safe backup procedures, monitoring and tested error recovery. Use a production application server and reverse proxy rather than Django’s development server.

5. **Threat-model the analyzer and administration path.** Review abuse cases such as oversized or adversarial Unicode input, stored-content exposure, log injection, malicious URLs displayed to analysts, model-file replacement, database theft and unauthorised result access. Controls should be verified by security testing rather than inferred from framework use.

#### 5.7.3 Detection and Model Recommendations

1. **Retain the classical baseline.** TF-IDF/Logistic Regression should remain as a transparent, efficient reference model when testing more complex methods. A larger model should be adopted only if it provides meaningful gains on locked, representative data under the same protocol.

2. **Calibrate and version decision logic.** Internal model probabilities and hybrid scores should be calibrated on appropriate validation data if they are to be interpreted quantitatively. Rule weights, thresholds, recognised domains, model hashes and data versions should be version-controlled together so that a result can be traced to the exact decision configuration.

3. **Expand evidence cautiously.** If permitted by scope and governance, email analysis may incorporate parsed headers and SPF, DKIM and DMARC results, while URLs may use controlled redirect expansion, domain-age or reputation evidence and webpage analysis in an isolated service. Such signals should record source, freshness, failure state and uncertainty. A reputation lookup failure must not silently become evidence of safety.

4. **Test adversarial robustness.** Evaluation should cover obfuscated words, homoglyphs, zero-width characters, misspellings, URL redirections, newly registered domains, image-only text, QR codes, attachment lures and prompt-like language intended to manipulate automated analysis. Ahmed and Pourmoafil (2026) show why strong clean-data results should not be assumed to survive adversarial change.

5. **Monitor drift and disagreement.** A governed pilot should record de-identified aggregate error patterns, not unrestricted private content. Analysts should review false positives, false negatives, model/rule disagreement and newly emerging templates. Retraining should require approval, an evaluation report, artefact signing and rollback capability.

#### 5.7.4 Interface, Accessibility and User-Study Recommendations

1. **Capture authentic interface evidence.** Run the repository in a compatible browser and replace Chapter Four screenshot placeholders with actual screens showing the landing page, email and SMS forms, each verdict type, validation feedback and controlled processing errors. Screens should not contain real private messages.

2. **Conduct cross-browser and accessibility testing.** Verify keyboard operation, focus order, labels, error association, colour contrast, responsive layout, zoom behaviour and screen-reader announcements. Automated checks should be complemented by manual testing and users with relevant access needs.

3. **Conduct an approved task-based usability study.** Participants should perform realistic email and SMS review tasks. Measures may include completion rate, time, ability to identify the verdict and evidence, choice of safe next action, comprehension, appropriate trust and error recovery. A standard usability scale may be added, but it must not replace task evidence or be reported before data collection.

4. **Evaluate explanations, not only labels.** Compare label-only output with reason-and-action output to determine whether explanations improve decisions. Study whether users understand that “Low Risk” is not “guaranteed safe,” whether hiding SMS scores reduces false precision, and whether high-risk wording causes appropriate caution without panic.

5. **Provide a clear privacy notice and user control.** Before submission, users should know what is sent to the server, whether it is stored, for how long and how deletion can be requested. The interface should discourage submission of passwords, OTPs or unnecessary personal data even when those items appear in a suspicious message.

#### 5.7.5 Prioritised Implementation Plan

Table 5.5 converts the recommendations into an ordered plan. Priority 0 items are blockers for credible deployment or stronger empirical claims; Priority 1 items establish robust validation and a governed pilot; Priority 2 items extend capability after the foundations are proven.

[[TABLE 5.5 START]]
| Priority | Work package | Principal deliverable | Completion evidence |
| P0 | Database correctness | Initial migration and clean-database persistence integration test | Migration applies from zero; retained record verified and deletable |
| P0 | Production security baseline | Separate hardened settings and resolved deployment checks | Documented deployment review; zero unresolved accepted warnings or formal exception record |
| P0 | Privacy and retention | Minimised storage, clear notice, lawful basis, retention/deletion controls | Approved data map, policy, tests and access review |
| P0 | Email evidence recovery | Lawful manifest, portable training path, locked evaluation | Reproducible script, checksums, split indices and signed report |
| P0 | SMS data integrity | Deduplicated, grouped, contemporary phishing-specific corpus | Label guide, inter-review process, provenance and locked partitions |
| P1 | Complete hybrid benchmark | Independently labelled email/SMS final-decision set | Per-channel confusion matrices, error review and uncertainty |
| P1 | Robustness and security testing | Adversarial, input, artefact and web-security assessment | Resolved findings and regression tests |
| P1 | Accessibility and usability | Cross-browser audit and approved task-based participant study | Protocol, anonymised results and documented design changes |
| P1 | Governed pilot | Limited deployment with monitoring, rollback and incident response | Pilot approval, monitoring report and stop criteria |
| P2 | Advanced evidence and models | Carefully evaluated live signals, multilingual or multimodal methods | Demonstrated improvement over baseline on locked data |
[[TABLE 5.5 END]]

**Table 5.5:** Prioritised recommendation and implementation plan

[[FIGURE 5.1: RESPONSIBLE EVOLUTION ROADMAP]]

**Figure 5.1:** Prioritised roadmap from academic prototype to responsibly governed deployment

Figure 5.1 places evidence and governance before feature expansion. The sequence is intentionally gated: a later phase should proceed only after the previous phase has produced reviewable evidence. This reduces the risk of adding live integrations or complex models to a system whose data, privacy, security or measurement foundations remain unresolved.

### 5.8 Suggestions for Future Research

Future work should test research questions that extend, rather than obscure, the present baseline. Table 5.6 proposes directions and the evidence each would require.

[[TABLE 5.6 START]]
| Research direction | Example question | Required method/evidence |
| Multilingual and Nigerian-context detection | How does the baseline perform on Nigerian English, Pidgin, code-switching and selected indigenous-language messages? | Lawful contemporary corpus, native-speaker annotation, language-stratified locked evaluation |
| Campaign- and time-aware generalisation | How much does performance decline on unseen campaigns and later collection periods? | Grouped and temporal splits, duplicate/near-duplicate controls, confidence intervals |
| Classical versus contextual models | Do transformer or embedding models provide material gains over TF-IDF/Logistic Regression under equal data and latency constraints? | Same locked datasets, tuning budget, calibration, compute and error analysis |
| Hybrid decision evaluation | Which combinations of model, sender, URL and content evidence improve final decisions without excessive false alarms? | Factorial/ablation study on independently labelled complete cases |
| Explanation effectiveness | Do named reasons and protective actions improve safe user choices compared with a label alone? | Randomised task-based user study measuring comprehension, behaviour and appropriate trust |
| Adversarial resilience | Which obfuscations and campaign shifts most seriously affect model and rule performance? | Threat model, controlled attacks, robust metrics and mitigation regression suite |
| Multimodal phishing | Can QR, image text and attachment evidence be added without unacceptable privacy and security risk? | Isolated extraction, multimodal labelled data, malware-safe environment and governance review |
| Privacy-preserving learning | Can useful updates be learned while minimising retention of raw private messages? | De-identification study, differential/privacy risk analysis, utility comparison and DPIA |
| Live intelligence governance | When do DNS, authentication and reputation sources improve decisions, and how should stale or unavailable data be represented? | Source-quality model, freshness tests, failure-state evaluation and audit trail |
| Longitudinal monitoring | How rapidly do error patterns and risk thresholds drift after deployment? | Governed pilot, periodic locked challenge sets, change control and rollback criteria |
[[TABLE 5.6 END]]

**Table 5.6:** Suggested future research directions

A particularly important study would compare four conditions on the same locked data: text model only, rules only, the current hybrid approach and an enhanced hybrid approach with governed external evidence. Such an ablation would show whether each evidence family provides incremental value and where it creates false alarms. It should report results separately for email and SMS and should preserve the existing linear baseline.

A second important study would centre users rather than models. Participants could judge messages first without assistance, then with label-only assistance, and then with explanation-and-action assistance. The outcome of interest would not be whether participants like the interface, but whether they make safer, appropriately calibrated decisions. The design should also test over-reliance: a user should be willing to question an incorrect low-risk output when contradictory evidence is visible.

A third direction is regional and temporal relevance. Contemporary Nigerian scams may use local institutions, mobile-money patterns, Pidgin, compressed abbreviations and cross-channel movement from SMS to calls, messaging applications or websites. A corpus and evaluation programme should therefore record time, campaign and medium while protecting affected individuals. This would allow the project to measure not just random-split performance but resilience to the next campaign.

### 5.9 Final Remarks

Phishing detection is a continuing risk-management problem rather than a one-time classification exercise. Attackers change language, infrastructure, brands and channels; legitimate messages also contain security terms, urgent deadlines and links. A useful system must therefore combine evidence, expose uncertainty, support verification and remain open to correction.

PhishGuard AI provides a sound educational foundation for that work. It demonstrates independent email and SMS model handling, local hybrid evidence, cautious result presentation and reproducible evaluation of the evidence that is actually available. Its current limitations are equally informative: missing email provenance, broad and duplicated SMS data, absent hybrid labels, incomplete persistence deployment, development security settings and no user study show where a prototype ends and responsible operational engineering begins.

The project should proceed by preserving this honesty. Metrics should be regenerated from documented data, screenshots should come from the running application, user findings should come from approved participants, and deployment claims should follow security and privacy verification. If the recommendations in this chapter are followed in priority order, PhishGuard AI can evolve from a credible final-year prototype into a better validated research platform and, only after further governance and assurance, a candidate for limited real-world decision support.

## REFERENCES

Ahmed, R., & Sumesh, E. P. (2026). An intelligent phishing email detection system using ensemble methods and explainable AI. *Knowledge-Based Systems, 337*, 115388. https://doi.org/10.1016/j.knosys.2026.115388

Ahmed, T., & Pourmoafil, S. (2026). Adversarial robustness of phishing email detection: A comparative study of TF-IDF + Logistic Regression and fine-tuned DistilBERT. *arXiv*. https://doi.org/10.48550/arXiv.2607.18429

Al-Subaiey, A., Al-Thani, M., Alam, N. A., Antora, K. F., Khandakar, A., & Zaman, S. M. A. U. (2024). Novel interpretable and robust web-based AI platform for phishing email detection. *Computers & Electrical Engineering, 120*, 109625. https://doi.org/10.1016/j.compeleceng.2024.109625

Alhuzali, A., Alloqmani, A., Aljabri, M., & Alharbi, F. (2025). In-depth analysis of phishing email detection: Evaluating the performance of machine learning and deep learning models across multiple datasets. *Applied Sciences, 15*(6), 3396. https://doi.org/10.3390/app15063396

Almeida, T. A., Gómez Hidalgo, J. M., & Yamakami, A. (2011). Contributions to the study of SMS spam filtering: New collection and results. In *Proceedings of the 11th ACM Symposium on Document Engineering* (pp. 259–262). Association for Computing Machinery. https://doi.org/10.1145/2034691.2034742

Anti-Phishing Working Group. (2026, May 21). *Phishing activity trends report: 1st quarter 2026*. https://docs.apwg.org/reports/apwg_trends_report_q1_2026.pdf

Brissett, A., & Wall, J. (2025). Machine learning and watermarking for accurate detection of AI-generated phishing emails. *Electronics, 14*(13), 2611. https://doi.org/10.3390/electronics14132611

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.

Corpuz, J. E. A., Diaz, S. Q., Palafox, L. B. M., Tan, M. C. T., & Solomon, K. Y. C. (2026). Machine learning-based detection of SMS phishing in the Philippine context. In *Proceedings of the Workshop on Computation: Theory and Practice (WCTP 2025)* (pp. 553–562). Atlantis Press. https://doi.org/10.2991/978-94-6239-638-8_28

Django Software Foundation. (2025). *Django documentation: Release 5.2*. https://docs.djangoproject.com/en/5.2/

Green, D. M., & Swets, J. A. (1966). *Signal detection theory and psychophysics*. Wiley.

James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An introduction to statistical learning: With applications in R* (2nd ed.). Springer. https://doi.org/10.1007/978-1-0716-1418-1

Jesutofaye, H. J. (2026). *PhishGuard AI: Email & SMS phishing detection system* [Computer software]. GitHub. https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System

Khandan, S., Tabatabaei, M., Uzoatul, I. B., Jogunola, O., Tsado, Y., & Dargahi, T. (2026). An explainable multimodal framework for phishing attack detection. In R. Laborde, J. Garcia-Alfaro, A. Yazdinejad, G. Epiphaniou, & H. Abie (Eds.), *Computer security: ESORICS 2025 international workshops* (pp. 75–91). Springer. https://doi.org/10.1007/978-3-032-16165-9_5

Kytidou, E., Tsikriki, T., Drosatos, G., & Rantos, K. (2025). Machine learning techniques for phishing detection: A review of methods, challenges, and future directions. *Intelligent Decision Technologies*. Advance online publication. https://doi.org/10.1177/18724981251366763

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press. https://nlp.stanford.edu/IR-book/

Miller, T. (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence, 267*, 1–38. https://doi.org/10.1016/j.artint.2018.07.007

Mishra, S., & Soni, D. (2020). Smishing detector: A security model to detect smishing through SMS content analysis and URL behavior analysis. *Future Generation Computer Systems, 108*, 803–815. https://doi.org/10.1016/j.future.2020.03.021

Munoz, M. L., & Islam, M. F. (2025). Deep learning approaches for multi-class classification of phishing text messages. *Journal of Cybersecurity and Privacy, 5*(4), 102. https://doi.org/10.3390/jcp5040102

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.100-1

National Institute of Standards and Technology. (n.d.). *Phishing*. Computer Security Resource Center Glossary. Retrieved August 10, 2026, from https://csrc.nist.gov/glossary/term/phishing

Nigeria Data Protection Commission. (2025). *Nigeria Data Protection Act (NDP Act) 2023: General application and implementation directive (GAID) 2025* (NDPC/NDP ACT-GAID/01/2025). https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf

Patra, C., Giri, D., Nandi, S., Das, A. K., & Alenazi, M. J. F. (2025). Phishing email detection using vector similarity search leveraging transformer-based word embedding. *Computers & Electrical Engineering, 124*, 110403. https://doi.org/10.1016/j.compeleceng.2025.110403

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Popescul, D., & Radu, L. D. (2025). AI in phishing detection: A bibliometric review. *Frontiers in Artificial Intelligence, 8*, 1496580. https://doi.org/10.3389/frai.2025.1496580

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). “Why should I trust you?”: Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135–1144). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939778

Saito, T., & Rehmsmeier, M. (2015). The precision–recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432. https://doi.org/10.1371/journal.pone.0118432

scikit-learn developers. (2025). *scikit-learn 1.7 user guide*. https://scikit-learn.org/1.7/user_guide.html

Timko, D., Hernandez Castillo, D., & Rahman, M. L. (2024). A quantitative study of SMS phishing detection. *arXiv*. https://doi.org/10.48550/arXiv.2311.06911

Uddin, M. A., Mahiuddin, M., & Sarker, I. H. (2026). An explainable transformer-based model for phishing email detection: A large language model approach. *Computer Networks, 277*, 112061. https://doi.org/10.1016/j.comnet.2026.112061

Verizon. (2025). *2025 data breach investigations report*. https://www.verizon.com/business/resources/reports/dbir/

Wang, Y., Zhai, H., Wang, C., Hao, Q., Cohen, N. A., Foulger, R., Handler, J. A., & Wang, G. (2025). Can you walk me through it? Explainable SMS phishing detection using LLM-based agents. In *Proceedings of the Twenty-First Symposium on Usable Privacy and Security (SOUPS 2025)* (pp. 37–56). USENIX Association. https://www.usenix.org/conference/soups2025/presentation/wang

Wilk-Jakubowski, J. L., Pawlik, L., Wilk-Jakubowski, G., & Sikora, A. (2025). Machine learning and neural networks for phishing detection: A systematic review (2017–2024). *Electronics, 14*(18), 3744. https://doi.org/10.3390/electronics14183744

Zidan, T., Abu-Amara, F., Hasasneh, A., Sawaftah, M., & Griner, S. (2025). A hybrid approach to phishing email detection: Leveraging machine learning and explainable artificial intelligence. *International Journal of Electrical and Computer Engineering, 15*(5), 4865–4874. https://doi.org/10.11591/ijece.v15i5.pp4865-4874
