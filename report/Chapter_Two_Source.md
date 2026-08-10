# PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING

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

## REFERENCES

Ahmed, R., & Sumesh, E. P. (2026). An intelligent phishing email detection system using ensemble methods and explainable AI. *Knowledge-Based Systems, 337*, 115388. https://doi.org/10.1016/j.knosys.2026.115388

Ahmed, T., & Pourmoafil, S. (2026). Adversarial robustness of phishing email detection: A comparative study of TF-IDF + Logistic Regression and fine-tuned DistilBERT. *arXiv*. https://doi.org/10.48550/arXiv.2607.18429

Al-Subaiey, A., Al-Thani, M., Alam, N. A., Antora, K. F., Khandakar, A., & Zaman, S. M. A. U. (2024). Novel interpretable and robust web-based AI platform for phishing email detection. *Computers & Electrical Engineering, 120*, 109625. https://doi.org/10.1016/j.compeleceng.2024.109625

Alhuzali, A., Alloqmani, A., Aljabri, M., & Alharbi, F. (2025). In-depth analysis of phishing email detection: Evaluating the performance of machine learning and deep learning models across multiple datasets. *Applied Sciences, 15*(6), 3396. https://doi.org/10.3390/app15063396

Anti-Phishing Working Group. (2026, May 21). *Phishing activity trends report: 1st quarter 2026*. https://docs.apwg.org/reports/apwg_trends_report_q1_2026.pdf

Brissett, A., & Wall, J. (2025). Machine learning and watermarking for accurate detection of AI-generated phishing emails. *Electronics, 14*(13), 2611. https://doi.org/10.3390/electronics14132611

Corpuz, J. E. A., Diaz, S. Q., Palafox, L. B. M., Tan, M. C. T., & Solomon, K. Y. C. (2026). Machine learning-based detection of SMS phishing in the Philippine context. In *Proceedings of the Workshop on Computation: Theory and Practice (WCTP 2025)* (pp. 553–562). Atlantis Press. https://doi.org/10.2991/978-94-6239-638-8_28

Green, D. M., & Swets, J. A. (1966). *Signal detection theory and psychophysics*. Wiley.

James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An introduction to statistical learning: With applications in R* (2nd ed.). Springer. https://doi.org/10.1007/978-1-0716-1418-1

Khandan, S., Tabatabaei, M., Uzoatul, I. B., Jogunola, O., Tsado, Y., & Dargahi, T. (2026). An explainable multimodal framework for phishing attack detection. In R. Laborde, J. Garcia-Alfaro, A. Yazdinejad, G. Epiphaniou, & H. Abie (Eds.), *Computer security: ESORICS 2025 international workshops* (pp. 75–91). Springer. https://doi.org/10.1007/978-3-032-16165-9_5

Kytidou, E., Tsikriki, T., Drosatos, G., & Rantos, K. (2025). Machine learning techniques for phishing detection: A review of methods, challenges, and future directions. *Intelligent Decision Technologies, 19*(6), 4356–4379. https://doi.org/10.1177/18724981251366763

Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press. https://nlp.stanford.edu/IR-book/

Miller, T. (2019). Explanation in artificial intelligence: Insights from the social sciences. *Artificial Intelligence, 267*, 1–38. https://doi.org/10.1016/j.artint.2018.07.007

Mishra, S., & Soni, D. (2020). Smishing detector: A security model to detect smishing through SMS content analysis and URL behavior analysis. *Future Generation Computer Systems, 108*, 803–815. https://doi.org/10.1016/j.future.2020.03.021

Munoz, M. L., & Islam, M. F. (2025). Deep learning approaches for multi-class classification of phishing text messages. *Journal of Cybersecurity and Privacy, 5*(4), 102. https://doi.org/10.3390/jcp5040102

National Institute of Standards and Technology. (n.d.). *Phishing*. Computer Security Resource Center Glossary. Retrieved August 10, 2026, from https://csrc.nist.gov/glossary/term/phishing

Patra, C., Giri, D., Nandi, S., Das, A. K., & Alenazi, M. J. F. (2025). Phishing email detection using vector similarity search leveraging transformer-based word embedding. *Computers & Electrical Engineering, 124*, 110403. https://doi.org/10.1016/j.compeleceng.2025.110403

Popescul, D., & Radu, L. D. (2025). AI in phishing detection: A bibliometric review. *Frontiers in Artificial Intelligence, 8*, 1496580. https://doi.org/10.3389/frai.2025.1496580

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). “Why should I trust you?”: Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135–1144). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939778

Timko, D., Hernandez Castillo, D., & Rahman, M. L. (2024). A quantitative study of SMS phishing detection. *arXiv*. https://doi.org/10.48550/arXiv.2311.06911

Uddin, M. A., Mahiuddin, M., & Sarker, I. H. (2026). An explainable transformer-based model for phishing email detection: A large language model approach. *Computer Networks, 277*, 112061. https://doi.org/10.1016/j.comnet.2026.112061

Wang, Y., Zhai, H., Wang, C., Hao, Q., Cohen, N. A., Foulger, R., Handler, J. A., & Wang, G. (2025). Can you walk me through it? Explainable SMS phishing detection using LLM-based agents. In *Proceedings of the Twenty-First Symposium on Usable Privacy and Security (SOUPS 2025)* (pp. 37–56). USENIX Association. https://www.usenix.org/conference/soups2025/presentation/wang

Wilk-Jakubowski, J. L., Pawlik, L., Wilk-Jakubowski, G., & Sikora, A. (2025). Machine learning and neural networks for phishing detection: A systematic review (2017–2024). *Electronics, 14*(18), 3744. https://doi.org/10.3390/electronics14183744

Zidan, T., Abu-Amara, F., Hasasneh, A., Sawaftah, M., & Griner, S. (2025). A hybrid approach to phishing email detection: Leveraging machine learning and explainable artificial intelligence. *International Journal of Electrical and Computer Engineering, 15*(5), 4865–4874. https://doi.org/10.11591/ijece.v15i5.pp4865-4874
