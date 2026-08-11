# PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING

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

Ahmed, T., & Pourmoafil, S. (2026). Adversarial robustness of phishing email detection: A comparative study of TF-IDF + Logistic Regression and fine-tuned DistilBERT. *arXiv*. https://doi.org/10.48550/arXiv.2607.18429

Almeida, T. A., Gómez Hidalgo, J. M., & Yamakami, A. (2011). Contributions to the study of SMS spam filtering: New collection and results. In *Proceedings of the 11th ACM Symposium on Document Engineering* (pp. 259–262). Association for Computing Machinery. https://doi.org/10.1145/2034691.2034742

Anti-Phishing Working Group. (2026, May 21). *Phishing activity trends report: 1st quarter 2026*. https://docs.apwg.org/reports/apwg_trends_report_q1_2026.pdf

Django Software Foundation. (2025). *Django documentation: Release 5.2*. https://docs.djangoproject.com/en/5.2/

Jesutofaye, H. J. (2026). *PhishGuard AI: Email & SMS phishing detection system* [Computer software]. GitHub. https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System

National Institute of Standards and Technology. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* (NIST AI 100-1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.100-1

Nigeria Data Protection Commission. (2025). *Nigeria Data Protection Act (NDP Act) 2023: General application and implementation directive (GAID) 2025* (NDPC/NDP ACT-GAID/01/2025). https://ndpc.gov.ng/wp-content/uploads/2025/07/NDP-ACT-GAID-2025-MARCH-20TH.pdf

Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302

Wang, Y., Zhai, H., Wang, C., Hao, Q., Cohen, N. A., Foulger, R., Handler, J. A., & Wang, G. (2025). Can you walk me through it? Explainable SMS phishing detection using LLM-based agents. In *Proceedings of the Twenty-First Symposium on Usable Privacy and Security (SOUPS 2025)* (pp. 37–56). USENIX Association. https://www.usenix.org/conference/soups2025/presentation/wang
