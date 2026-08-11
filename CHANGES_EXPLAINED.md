# What Was Wrong and How It Was Fixed — A Plain-English Guide

This document explains every change made to PhishGuard AI in simple language.
You do not need to be a programmer to follow it. If a technical word appears, it
is explained the first time it is used.

---

## Table of Contents

1. [The Problem in One Sentence](#1-the-problem-in-one-sentence)
2. [Two Words You Need: False Positive and False Negative](#2-two-words-you-need-false-positive-and-false-negative)
3. [How the App Decides if a Message Is Phishing](#3-how-the-app-decides-if-a-message-is-phishing)
4. [Part One — Fixing Email](#4-part-one--fixing-email)
5. [Part Two — Fixing SMS](#5-part-two--fixing-sms)
6. [Part Three — Fixing the Frontend](#6-part-three--fixing-the-frontend)
7. [How We Proved It Works](#7-how-we-proved-it-works)
8. [How Links Are Checked (and What That Cannot Tell You)](#8-how-links-are-checked-and-what-that-cannot-tell-you)
9. [Where the Training Data Lives](#9-where-the-training-data-lives)
10. [Files That Changed](#10-files-that-changed)
11. [Glossary](#11-glossary)

---

## 1. The Problem in One Sentence

The app was calling **real, harmless messages "suspicious"** — a bank's own
safety notice, a payment receipt, a login alert from Google — while some genuine
scams slipped through as "safe".

The goal was to make the app **accurate in both directions**: stop crying wolf,
without letting real wolves through.

---

## 2. Two Words You Need: False Positive and False Negative

These two terms are used constantly below, so here they are up front:

| Term | What it means | Real-world example | Why it's bad |
|---|---|---|---|
| **False positive** | The app says "danger" but the message is actually fine | Your bank's real receipt is marked "Suspicious" | Users stop trusting the app and start ignoring *all* its warnings |
| **False negative** | The app says "safe" but the message is actually a scam | A real scam is marked "Low Risk" | The user gets robbed |

The tricky part is that **fixing one usually breaks the other**. If you make the
app more suspicious, you catch more scams (fewer false negatives) but you also
flag more innocent messages (more false positives). Making it more relaxed does
the opposite.

Getting both down at once is what this work was about. The way to do it is not
to turn a single "sensitivity" dial, but to make the app **understand the
message better** — so it becomes more suspicious of the *right* things and more
relaxed about the *wrong* things.

---

## 3. How the App Decides if a Message Is Phishing

The app gives every message a **score from 0 to 100**. Higher = more dangerous.

| Score | Verdict shown to the user |
|---|---|
| 0 – 39 | 🟢 Low Risk |
| 40 – 69 | 🟠 Suspicious |
| 70 – 100 | 🔴 High Risk |

That score comes from **two separate sources** that are added together:

### Source A — The machine learning model ("the model")

A **machine learning model** is a program that was shown thousands of example
messages labelled "scam" or "safe", and learned the statistical patterns that
tend to appear in each. It doesn't truly understand English — it just knows that
certain word combinations *tend to* appear in scams.

Its output is a **probability**, e.g. "I'm 72% sure this is phishing."

**Its weakness:** it reacts to vocabulary, not meaning. Words like *bank*,
*account*, *payment*, *verify* and *security* appear constantly in scams — but
they also appear in every legitimate bank email ever written. So the model gets
nervous about perfectly normal mail.

### Source B — The rules ("evidence" / "indicators")

These are explicit checks written by hand, each looking for one specific
suspicious thing:

- Does the message contain a **shortened link** (like `bit.ly/xyz`) where you
  can't see where it really goes?
- Does the link use a **raw IP address** (`http://192.168.4.10/`) instead of a
  domain name?
- Does the sender's domain **imitate a real brand** (`paypa1.com` instead of
  `paypal.com`)?
- Does the message **ask you for a password, PIN or OTP**?
- Does it **pressure you** ("within 24 hours", "act now")?
- Does it **threaten you** ("your account will be suspended")?

Each rule that fires adds points. Rules are called "evidence" because, unlike
the model, each one can be **shown to the user as a reason**: *"Shortened URL
detected."*

**The key principle behind the whole fix:**

> Every warning the app shows must have a reason it can state out loud.

---

## 4. Part One — Fixing Email

### Problem 4.1 — The model could raise an alarm all by itself

**What was happening:** the model's probability was being converted into points
and added to the score with no restrictions. A completely ordinary email —
*"Your monthly bank statement is ready in online banking"* — made the model 80%
nervous purely because of the words *bank*, *statement* and *banking*. That
alone pushed the score into the "Suspicious" band.

The result was a warning with **no explanation underneath it**. The "Why was
this flagged?" panel was empty. That's the worst possible user experience: the
app is alarming you and cannot tell you why.

**The fix — three rules for the model:**

1. **A confidence floor.** Below 55% certainty, the model contributes **zero**
   points. A model that is 30% or 50% sure is basically guessing, and guesses
   shouldn't move the score at all.
2. **A weight cap.** Even at 100% certainty, the model can only ever add 45
   points out of 100. It is one opinion, not the verdict.
3. **The unexplained cap.** If **no rule fired at all**, the score is forced
   down to a maximum of 39 — the very top of the green "Low Risk" band.

Rule 3 is the important one. It's a hard guarantee: **the app can never show a
warning it cannot justify.** If it says "Suspicious", there is always at least
one reason listed underneath.

In the code (`analyzer.py`) this is just a few lines:

```python
MODEL_WEIGHT = 45          # most the model can ever add
MODEL_FLOOR = 0.55         # below this, the model says nothing
UNEXPLAINED_SCORE_CAP = 39 # no evidence = cannot leave the green band
```

---

### Problem 4.2 — The app couldn't tell a warning *about* phishing from phishing itself

This was the most interesting bug, and the most damaging one.

Banks regularly send genuine safety notices that read like this:

> *"Zenith Bank would **NEVER** ask you for your card details, PIN or Internet
> Banking login details. We would also **NEVER** ask you to click on a link to
> update your bank information."*

That is the most anti-phishing message imaginable. But the app looked at it and
saw the phrases *"card details"*, *"PIN"*, *"login details"* and *"click on a
link"* — and confidently reported it as a phishing attempt. 🤦

**Why it happened:** the rules were doing a plain keyword search. They looked
for the words and never noticed the word **"NEVER"** sitting right in front of
them, which reverses the entire meaning.

**The fix — negation awareness.** In grammar, a **negation** is a word that
flips meaning: *never, not, don't, won't, cannot*. Two things were added:

1. **A negation check.** Before accepting any keyword match as evidence, the app
   now looks backwards a short distance and asks: *"is there a negation in front
   of this?"* If yes, the match is ignored. *"We will never ask for your PIN"*
   no longer counts as asking for your PIN.

2. **An awareness detector.** If the whole message is written in the style of a
   security-education notice ("we will never...", "do not share...", "report
   such messages..."), it's recognised as an awareness bulletin and gets a
   **credit** that pulls the score down, rather than penalties that push it up.

---

### Problem 4.3 — Scammers copy that exact wording (the trap in the fix above)

Here's where it gets subtle, and where a careless fix creates a **security
hole**.

Real scammers know that "we will never ask for your details" sounds reassuring,
so they paste it at the top of their scam and *then* make their demand:

> *"We will never ask for your details, **however** to protect your account you
> must confirm your internet banking login details within 24 hours or access
> will be blocked. Verify now: `https://bit.ly/secure-bank-verify`"*

If the negation fix from 4.2 were naive, that single "never" at the start would
excuse **the entire rest of the message** — and this obvious scam would be
waved straight through as safe. We would have fixed false positives by creating
a false negative. That's not progress; it's a trade.

**The fix — the look-back has boundaries.** When the app checks for a negation
in front of a suspicious phrase, it stops looking at:

- the end of the previous **sentence** (a full stop, `!`, `?`, `;` or a line
  break), **and**
- any **contrastive connective** — the pivot words English uses to change
  direction: *however, but, although, nevertheless, therefore, so, to protect,
  in order to*.

In plain terms: **a reassurance only protects the clause it's actually in.** The
moment the sentence turns on the word "however", the protection is over and the
demand that follows is judged on its own.

Three extra safeguards were added on top:

- An "awareness notice" **loses that status** if any clause in it makes a live
  demand or applies pressure.
- An awareness notice that contains a **deceptive link** is not an awareness
  notice. Real safety bulletins tell you *not* to click links; they don't ship
  a `bit.ly` link of their own.
- Technical red flags — shortened links, IP-address links, punycode, brand
  imitation — are **never** suppressed by negation, ever. You cannot talk your
  way out of a `bit.ly` link, because the reader genuinely cannot see where it
  leads.

---

### Problem 4.4 — Genuine security keywords were too twitchy

Two rules were rewritten to be more precise instead of more paranoid:

**Credential requests.** The old rule fired on any security-ish word. The new
one requires an actual **request verb + secret**: *"enter your password"*,
*"reply with your OTP"*, *"send your card number"*. Merely mentioning the word
"password" (as in *"your password was changed successfully"*) is no longer
evidence of anything.

**Urgency.** The word *"immediately"* on its own is ordinary business English —
*"contact support immediately"* appears in countless legitimate emails. It now
only counts when paired with a phishing-style action: *"verify immediately"*,
*"pay immediately"*, *"click now"*.

---

### Problem 4.5 — Known-good senders got no credit

The app keeps a list of recognised organisation domains (`legit_sources.py`).
That list was expanded, and more importantly it's now actually *used* to balance
the score:

When a message comes from a recognised domain **and** shows no serious red flag,
it earns a **context credit** that is subtracted from the score:

| Situation | Credit |
|---|---|
| Recognised sender + routine transactional wording ("receipt", "no action required") | −25 |
| Recognised sender + routine security wording ("new login", "if this was you") | −20 |
| Recognised sender writing ordinary prose | −15 |
| Any message recognised as a security-awareness notice | −25 |

**Critically, this credit is switched off entirely** the moment any serious
indicator appears — a deceptive link, an imitated sender, or a request for your
data. A trusted-looking name can never launder a genuine red flag. This matters
because sender names are easy to fake.

A related fix: an email from `@zenithbank.com` that mentions "Zenith Bank" was
being flagged for *impersonating Zenith Bank*. Recognised domains are now exempt
from the impersonation check when they name their own organisation.

---

### Problem 4.6 — Making sure real scams still get caught

Every change above **lowers** scores, so each one is a chance to create a false
negative. To guarantee that didn't happen, **score floors** were added. A floor
is a minimum: no matter how calm the model is or how many credits apply, the
score cannot drop below it.

| Evidence found | Score floor | Resulting verdict |
|---|---|---|
| Any link the reader can't verify (shortened, raw IP, `@`-trick, punycode) | 40 | at least 🟠 Suspicious |
| A request for your secrets, identity data, or a payment | 40 | at least 🟠 Suspicious |
| Sender imitates a brand (`paypa1.com`) or a public account claims to be a company | 70 | 🔴 High Risk |
| A data request **combined with** pressure, a threat, or a prize lure | 70 | 🔴 High Risk |
| An unverifiable link **combined with** pressure, a threat, a lure, or a data request | 70 | 🔴 High Risk |

The effect: **strong evidence alone can reach High Risk even if the model is
completely relaxed.** The rules and the model act as independent safety nets —
either one can raise the alarm, so a failure in one doesn't sink the whole
system.

---

## 5. Part Two — Fixing SMS

The same engine handles text messages, but SMS is a different beast:

- Messages are tiny — often one sentence, so there's very little for the model
  to work with.
- The sender is a phone number or a short name ("GTBank"), not an email address,
  so most sender checks don't apply.
- Legitimate SMS traffic is *dominated* by exactly the words scams use: balance,
  account, OTP, expires, blocked.

Two test sets were built to measure it: 30 real-looking legitimate texts (bank
alerts, delivery updates, OTP codes, appointment reminders) and 20 realistic
scams.

**The good news:** false positives were already at zero. Everyday bank alerts,
receipts and OTP codes were all correctly marked safe.

**The bad news:** four scams were being marked "Low Risk". All four were
**quiet** scams — no link, no shouting, no urgency. Just a calm, polite request.
Those are the hardest kind to catch and, unfortunately, very common.

### Fix 5.1 — Requests for an unnamed secret

**Missed message:** *"Good day, please share the code sent to your phone so we
can complete your registration."*

The rule was looking for named secrets — the literal words *OTP*, *PIN*,
*password*. This scammer never used any of them. They said **"the code sent to
your phone"**, which is exactly the same thing described in plain English.

**Fix:** the rule now also recognises a request for an unnamed code when it's
tied to how it arrived — *"the code **sent** to your phone"*, *"the number we
**texted** you"*, *"the 6-digit code you **received**"*.

### Fix 5.2 — Requests for identity and banking data

**Missed message:** *"Kindly send your account number and BVN for verification
of your salary payment."*

No link. No urgency. No password requested. The app found almost nothing to
report — yet handing over your BVN and account number is precisely how identity
fraud starts.

**Fix:** a new indicator, `personal_data_request`, fires on requests for
identity or banking data — account number, BVN, NIN, date of birth, card
details. It carries a floor of 40 on its own (🟠 Suspicious) and 70 if it's
paired with pressure or a threat.

The reasoning is simple: **an organisation that genuinely holds your account
already knows your account number.** It never needs to text you asking for it.

### Fix 5.3 — Payment redirection fraud

**Missed message:** *"This is your landlord. My bank account has changed, send
this month's rent to 0123456789 immediately."*

This scored **zero**. Not one rule fired, because there is no link, no
credential request and no brand being imitated. It's just a sentence.

Yet this is one of the most financially devastating scams that exists — it's how
businesses lose entire invoice payments and how people lose their rent money.

**Fix:** a new indicator, `payment_redirect`, recognises the pattern of "the
account has changed, send money to the new one": phrases like *"my bank account
has changed"*, *"send payment to the new account"*, and *"transfer to"* followed
by a 10-digit account number.

It also comes with its own tailored advice: *"Confirm any change of bank details
by calling the person or organisation on a number you already have."*

### Fix 5.4 — Two negation words were too greedy

While testing, two scams were escaping through the negation system from
section 4.2 — but for a silly reason. The negation list contained the bare
words `not` and `avoid`, and they were matching **inside other words and
phrases**:

| Scam text | What matched | Why it was wrong |
|---|---|---|
| *"Please **not**e my bank account has changed..."* | `not` inside "note" | "Please note" is not a negation — it's an *introduction* |
| *"...confirm your card number now **to avoid** a block."* | `avoid` | "to avoid a block" is a **threat**, not a reassurance |

Both innocent-looking words were acting as a free pass for the scam that
followed.

**Fix:**
- `not` must now be a **standalone word** (the pattern `\bnot\b`), so it no
  longer matches inside *note*, *notice* or *nothing*.
- `avoid` only counts as a negation when it's genuinely warning you off
  something: *"avoid **sharing** your PIN"*, *"avoid **clicking** links"*. The
  bare word — as in *"to avoid a block"* — no longer excuses anything.

This is a good illustration of a general lesson: **when you search for a word,
be precise about where it's allowed to match.** A pattern that's slightly too
loose will quietly do the opposite of what you intended.

---

## 6. Part Three — Fixing the Frontend

**The bug you reported:** type an email into the form, click the **SMS** tab,
and your email text is still sitting there in the SMS box.

**Why it happened:** the Email/SMS tabs don't load a new page. They just relabel
the same form — the "Sender Address" label becomes "Sender Phone Number", and
the Subject field hides itself, because SMS has no subject line. But **nothing
ever emptied the boxes.** The old content just stayed put under the new labels.

**Why it actually matters:**

- An email address is not a phone number. Leaving `user@example.com` in a field
  now labelled "Sender Phone Number" produces a nonsense analysis.
- A 500-word email is not a text message. The SMS model was trained on short
  messages; feeding it an email body gives an unreliable result.
- It's simply confusing to see content you didn't type into the form you're
  looking at.

**The fix** (in `index.html`): switching tabs now clears the sender, subject and
message boxes, and also removes any leftover red validation errors — since those
errors belonged to the message you just discarded.

One important detail: the clearing only happens on a **deliberate tab click**.
When the page first loads it must *not* clear anything, because that's when the
server sends your submitted message back along with its result. The code
distinguishes the two by passing a flag:

```javascript
// Deliberate click by the user → clear the form
selectType(tab.dataset.messageType, { clearOnChange: true });

// Initial page load → set up labels only, keep what the server sent
selectType(initialMode);
```

And it only clears if the type genuinely *changed* — clicking "SMS" when you're
already on SMS does nothing, so you can't wipe your own work by accident.

---

## 7. How We Proved It Works

Changing detection logic without measuring it is guesswork. Two things were used
to verify every change.

### 7.1 Test corpora (a labelled collection of messages)

Four sets of messages were assembled, each one labelled in advance with the
answer:

| Set | Legit | Scam | Purpose |
|---|---|---|---|
| Email — everyday | 16 | 13 | Ordinary mail from real services |
| SMS — everyday | 20 | 12 | Bank alerts, OTPs, receipts, common smishing |
| SMS — hard | 10 | 8 | Deliberately borderline cases |
| **Total** | **46** | **33** | **79 messages** |

The "hard" set is the valuable one. It contains messages designed to fool a
detector in each direction:

- **Legitimate but alarming:** a real fraud alert from your bank (*"We detected
  a login from a new device"*), a card genuinely blocked after wrong PIN
  attempts, a subscription that really does expire today.
- **Scam but calm:** a polite request for a code, a landlord changing their bank
  details, a plain ask for your BVN.

Any detector can classify obvious cases. The hard set is where you find out if
it actually understands anything.

**Final result: 79 out of 79 correct — 0 false positives, 0 false negatives.**

For comparison, the starting point was **7 false positives** on the email set
alone.

### 7.2 Automated tests

The corpora were scratch scripts, used during development and then deleted. To
keep the fixes from silently breaking later, the important cases were written
into the project's permanent test suite (`detector/tests.py`).

An **automated test** is a small piece of code that runs the app on a known
input and fails loudly if the answer isn't what it should be. Run them any time
with:

```
venv\Scripts\python.exe manage.py test detector
```

The suite grew from 42 tests to **47, all passing**. The new ones lock in
exactly the behaviours that were broken:

- A bank's awareness notice must be **Low Risk**
- A scam *disguised* as an awareness notice must be **High Risk**
- The model alone must **never** produce an unexplained warning
- Strong evidence alone must reach **High Risk** even with a calm model
- Routine bank SMS (alerts, OTP codes) must be **Low Risk**
- A quiet SMS credential request must **not** be Low Risk
- A request for account number and BVN must be **detected**
- A "my bank account has changed" email must be **detected**

Two pre-existing test failures were also repaired along the way. They were
checking for text that no longer matched how the template writes it — the
templates were fine; the tests were out of date.

---

## 8. How Links Are Checked (and What That Cannot Tell You)

This question comes up a lot, so it's worth stating plainly:

> **The app never opens, visits, or contacts any link. It never connects to the
> internet at all.**

Everything you paste stays on your machine. There is no HTTP request, no DNS
lookup, and no query to any external blocklist service anywhere in the code.
The only URL-related tools used are `urlparse` (which splits an address into its
parts as plain text) and `tldextract` (which works out which piece of a domain
is the registered name).

### What it *can* tell from reading the address

The app judges a link the way a careful person would judge it by eye — from how
the address is written:

| Check | Example | Why it's suspicious |
|---|---|---|
| Shortened link | `https://bit.ly/xyz` | The real destination is hidden from you |
| Raw IP address | `http://45.13.98.2/pay` | Real companies use domain names, not bare numbers |
| Risky TLD | `.xyz`, `.top`, `.gq`, `.tk`, `.ml`, `.cf` | Cheap or free endings, heavily used by scammers |
| Punycode | `xn--pypal-4ve.com` | Non-English characters that render as a lookalike domain |
| `@` obfuscation | `http://paypal.com@evil.xyz` | Everything before the `@` is ignored by browsers — the real host is `evil.xyz` |
| Sender mismatch | A "PayPal" email linking to `paypal-verify.top` | The link doesn't belong to the organisation being claimed |

### What it *cannot* know

Because it never looks at the page, the app cannot tell you:

- whether the domain is currently live or already taken down,
- who registered it, or how recently,
- what the page actually does when it loads,
- whether it appears on a known-scam blocklist,
- or whether a normally-legitimate site was hijacked yesterday.

### Why this is a deliberate choice, not a missing feature

1. **Opening a phishing link to "test" it is genuinely dangerous.** Many scam
   pages attack the moment they load. Some show the fake login only to visitors
   who arrive from the scam message, so an automated fetch sees an innocent
   page and reports a false "safe" — worse than not checking at all.
2. **It tells the attacker they hit a live target.** Fetching the page reveals
   the checker's IP address and confirms someone read the message.
3. **Your data never leaves the machine.** Nothing you paste is transmitted
   anywhere. There is no telemetry and no third party involved.
4. **"I don't recognise that domain, so I won't click it" is the correct
   response anyway** — regardless of what the page turns out to contain.

### If live checking is ever wanted

The safe way to add it is **not** to fetch the page, but to look up the domain
name against a reputation service such as Google Safe Browsing or URLhaus. That
would catch domains already reported by others while still never touching the
page. The trade-offs: it needs an API key, it adds a network call to every scan,
your scanned domains would be sent to a third party, and it only knows about
*already-reported* sites — so brand-new scam domains still slip through.

**Current status: deliberately not implemented. The app is fully offline.**

---

## 9. Where the Training Data Lives

The two models were trained on separate datasets, both now stored inside the
project.

### Email — `detector/datasets/`

Seven labelled CSV files totalling **164,972 emails**, from the Kaggle
"Phishing Email Dataset" collection (CEAS 2008, Enron, Ling-Spam, Nazario's
phishing corpus, a Nigerian fraud/419 set, and SpamAssassin). Trained by
`detector/train_multi_csv.py`. See `detector/datasets/README.md` for the
per-file breakdown.

These files originally lived outside the project, so the training script could
not be run. They have been copied in, and the script's paths — which were
hardcoded to a folder that no longer existed — now resolve relative to the
project.

### SMS — `detector/datasets_sms/`

The **UCI SMS Spam Collection**: 5,574 real text messages, 4,827 legitimate and
747 spam. Trained by `detector/train_sms_csv.py`. The `spam.csv` downloaded
from Kaggle is the same corpus in a different format and sits in the same
folder for reference.

### One thing to be aware of

`.gitignore` excludes `*.csv`, so the email datasets are **not** committed to
git — they exist only on this machine. If the project is copied elsewhere, that
folder must be copied manually or email training will not run.

Also noted while documenting: `phishing_email.csv` (82,486 rows, half the email
corpus) stores its text in a `text_combined` column, which is not one of the
columns the training script merges. Those rows currently contribute empty text.
Fixing it is a one-line change plus a retrain — left alone for now, because
retraining would replace the model the accuracy figures above were measured
against.

---

## 10. Files That Changed

| File | What changed |
|---|---|
| `detector/engine/analyzer.py` | The main work: negation and awareness handling, the rewritten credential rule, the two new indicators (`personal_data_request`, `payment_redirect`), the model floor and cap, the unexplained-score cap, the score floors, and the trusted-sender credits |
| `detector/engine/sender_intelligence.py` | Recognised domains are exempt from the impersonation check when they name their own organisation |
| `detector/engine/legit_sources.py` | Expanded the list of recognised organisation domains |
| `detector/templates/detector/index.html` | Tab switching now clears the form fields and stale validation errors |
| `detector/tests.py` | 5 new regression tests; 2 outdated assertions repaired |
| `detector/train_multi_csv.py` | Paths were hardcoded to a folder that no longer exists; they are now relative to the project, with a clear error if the data is missing |
| `detector/datasets/` | **New.** The 7 email training CSVs, copied in, plus a README documenting them |
| `detector/datasets_sms/spam.csv` | **New.** The Kaggle copy of the SMS corpus, kept for reference |

Nothing was changed in the machine learning models themselves — no retraining
was involved. All of this is in how the model's opinion is *weighted* and how
the surrounding evidence is *interpreted*.

---

## 11. Glossary

**BVN** — Bank Verification Number, a Nigerian banking identity number. Highly
sensitive; a frequent target of scams.

**Blocklist** — a published list of web addresses already reported as malicious.
Checking one requires an internet connection, which this app deliberately does
not make (see section 8).

**Corpus (plural: corpora)** — a collection of example messages used to test a
system. Ours are *labelled*, meaning we already know the right answer for each
one, so we can count exactly how many the app gets wrong.

**DNS lookup** — asking the internet "which computer does this domain name point
to?" It's the smallest possible network request, and the app doesn't make even
that one.

**Evidence / indicator / rule** — a specific, explainable check ("this message
contains a shortened link"). Unlike the model's opinion, evidence can be shown
to the user as a reason.

**False negative** — a scam the app said was safe. Dangerous.

**False positive** — a safe message the app said was a scam. Erodes trust.

**Machine learning model** — a program that learned patterns from thousands of
labelled examples. Good at spotting statistical patterns, bad at understanding
meaning — which is why it needs rules alongside it.

**Negation** — a word that reverses meaning: *never, not, don't, cannot*.
Handling these correctly was central to the whole fix.

**OTP** — One-Time Password, the short code texted to you to confirm a login or
payment. Never share it; no legitimate organisation will ever ask you for it.

**Phishing** — a fake message pretending to be from someone you trust, designed
to steal information or money. Over SMS it's sometimes called *smishing*.

**Punycode** — an encoding that lets non-English characters be used in web
addresses. Scammers use it to register domains that *look* identical to real
ones but aren't. Such addresses begin with `xn--`.

**Regular expression (regex)** — a compact pattern for matching text. Powerful,
but easy to make slightly too loose — which is exactly the bug in section 5.4.

**Score floor** — a minimum score applied when specific evidence is found, so
the verdict can't be watered down by other factors.

**Static analysis** — judging something by reading it, without running or opening
it. This app analyses links statically: it reads the address, never visits it.

**TLD (top-level domain)** — the ending of a web address: `.com`, `.org`, `.ng`.
Some endings are free or near-free to register, which makes them popular with
scammers.

**Typosquatting** — registering a domain that's one character off a real one
(`paypa1.com` vs `paypal.com`) to fool people who read too quickly.
