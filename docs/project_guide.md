# Project Guide

## A. Project Explanation

### What is AI-powered cybersecurity threat detection?

In simple language:

AI-powered cybersecurity threat detection means using machine learning to automatically identify suspicious digital behavior. Instead of checking every log manually, we train a model to learn the difference between safe activity and risky activity.

In technical language:

It is the application of supervised and unsupervised machine learning on security telemetry such as network flows, authentication logs, endpoint signals, and behavioral metadata to classify known attack types and surface anomalous events that deviate from learned baselines.

### What problems does it solve?

- Too many security logs for humans to review manually
- Slow detection of suspicious activity
- Difficulty spotting patterns spread across multiple systems
- Missed low-and-slow attacks that do not match simple rules
- Alert fatigue caused by noisy monitoring systems

### Why is it important today?

- Companies run on cloud, APIs, IoT, VPN, mobile devices, and remote access
- Attackers move faster and generate more automated attacks
- Security teams need prioritization, not just more raw data
- AI helps convert huge data volumes into explainable alerts

### How companies use such systems

- Intrusion detection: spotting unauthorized access or lateral movement
- Fraud detection: finding abnormal account, payment, or session behavior
- Anomaly detection: flagging unknown or unusual operational patterns
- Malware detection: identifying suspicious beaconing, signatures, or endpoint behavior
- Network security monitoring: tracking spikes, scans, exfiltration, and unusual flows

### Industry examples

- Banks monitor suspicious transactions, repeated login failures, abnormal device changes, and unusual outbound traffic.
- IT companies monitor employee VPN activity, privileged access, internal scans, and server access anomalies.
- Product companies monitor production APIs, application login abuse, abuse bots, and endpoint compromise.
- Logistics companies monitor fleet gateways, warehouse scanners, dispatch consoles, route APIs, and remote warehouse connectivity.

### Complete workflow

1. Data collection: collect logs, network flow records, or simulated telemetry.
2. Preprocessing: handle missing values, invalid records, and duplicates.
3. Feature engineering: create behavior-focused signals like login failure rate or bytes per packet.
4. Anomaly detection / classification: train models for known attacks and unexpected behavior.
5. Model training: fit algorithms on training data.
6. Prediction: score unseen events on the test set or live-like feed.
7. Alert generation: convert scores to severity-based alerts.
8. Visualization/dashboard: present findings in a way that analysts and recruiters can understand quickly.

## B. Tech Stack Options

### Option A: Easiest

- Tools: Python, Pandas, NumPy, Matplotlib, Scikit-learn
- Dataset type: small tabular cybersecurity dataset
- Models: Logistic Regression or Decision Tree
- Difficulty: beginner
- Output: notebook charts and a CSV of predictions
- GPU: not needed

### Option B: Intermediate

- Tools: Python, Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib, Plotly, Streamlit, Joblib
- Dataset type: logistics-company network/security telemetry
- Models: Random Forest + Isolation Forest
- Difficulty: intermediate
- Output: trained models, predictions, alerts, charts, dashboard
- GPU: not needed

### Option C: Advanced

- Tools: Python, PyTorch/TensorFlow, Kafka, FastAPI, SIEM integration, Docker
- Dataset type: streaming logs, enriched threat intel, multi-source enterprise events
- Models: deep learning or ensemble systems
- Difficulty: advanced
- Output: near-real-time detection platform
- GPU: optional to recommended

### Selected approach

Option B is the best choice for a student because it offers:

- strong GitHub proof
- realistic architecture
- practical ML learning
- clean execution on a normal laptop
- a dashboard that looks professional in demos

## C. Selected Approach Summary

This project uses a logistics and transportation company scenario. We generate realistic virtual cybersecurity telemetry for warehouses, hubs, fleet systems, dispatch consoles, and IoT scanners. A Random Forest classifier detects known attack categories, while an Isolation Forest flags unusual behavior. Their outputs are combined into a risk score and severity-based alerts.

## D. Architecture

### Text-based block diagram

```text
Logistics SOC Dataset Generator
        |
        v
Raw CSV Data
        |
        v
Preprocessing
  - missing value handling
  - duplicate removal
  - timestamp validation
        |
        v
Feature Engineering
  - traffic_ratio
  - auth_failure_rate
  - bytes_per_packet
  - session_intensity
  - lateral_movement_score
        |
        v
Model Layer
  - Random Forest Classifier
  - Isolation Forest
        |
        v
Prediction + Risk Scoring
        |
        v
Threat Alerts + Visual Dashboard
```

### Module-wise explanation

- `src/generate_data.py`: creates the logistics dataset and cyberattack patterns
- `src/data_preprocessing.py`: cleans data and creates train/test split
- `src/feature_engineering.py`: adds security-focused derived features
- `src/train_model.py`: trains the classifier and anomaly detector
- `src/detect_threats.py`: computes alert risk scores and severity
- `src/visualize.py`: exports charts
- `dashboard/app.py`: renders the interactive dashboard
- `main.py`: runs the entire pipeline end to end

### Data flow explanation

Raw synthetic telemetry is generated and saved to CSV. The data is cleaned, new security features are created, and the dataset is split into training and testing data. The classifier learns attack labels, the anomaly detector learns normal behavior, and both predictions are merged into a final alert score. The results are stored in reports and presented on the dashboard.

## E. Folder Structure

### Recommended structure

```text
AI-Cybersecurity-Threat-Detection/
├── data/
├── dashboard/
├── docs/
├── models/
├── outputs/
├── src/
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

### Folder purpose

- `data/raw`: generated logistics telemetry
- `data/processed`: train/test files after preprocessing
- `dashboard`: Streamlit dashboard
- `docs`: architecture, README support, GitHub proof strategy
- `models`: serialized trained models and preprocessors
- `outputs/metrics`: JSON evaluation metrics
- `outputs/plots`: charts for screenshots and README
- `outputs/reports`: predictions, alerts, summary CSVs
- `src`: all modular Python source code

## F. Installation And Environment Setup

### Recommended version

- Python: `3.9+`

### Virtual environment setup

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### requirements.txt creation

This project already includes:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- plotly
- streamlit
- joblib

## G. Code Walkthrough

### File: `main.py`

Purpose:

- Runs the full project pipeline in one command.

### File: `src/generate_data.py`

Purpose:

- Creates a transportation-company cybersecurity dataset.
- Simulates normal behavior and attacks such as DoS, brute force, malware beaconing, insider scanning, and data exfiltration.

### File: `src/data_preprocessing.py`

Purpose:

- Loads data, handles missing values, removes duplicates, and splits the dataset.
- Adds light concept drift to the test set so evaluation is closer to real-world conditions.

### File: `src/feature_engineering.py`

Purpose:

- Creates security-focused features:
- `traffic_ratio`
- `auth_failure_rate`
- `bytes_per_packet`
- `session_intensity`
- `lateral_movement_score`

### File: `src/train_model.py`

Purpose:

- Builds preprocessing pipelines
- Trains the Random Forest classifier
- Trains the Isolation Forest anomaly model
- Saves metrics and serialized models

### File: `src/detect_threats.py`

Purpose:

- Converts model outputs into analyst-ready alerts
- Calculates risk score and severity
- Saves predictions and high-priority alerts

### File: `src/visualize.py`

Purpose:

- Saves recruiter-friendly chart images
- Confusion matrix
- Predicted attack distribution
- Confidence vs risk scatter
- Alert timeline
- Threats by logistics site

### File: `dashboard/app.py`

Purpose:

- Displays a metallic, robotic-style SOC dashboard using Streamlit and Plotly.

## H. Virtual Simulation Of Cyber Threats

### How the simulation works

- The dataset acts like security logs from a logistics company.
- Each row represents one event from a logistics site and device.
- Normal records mimic ordinary network behavior.
- Attack records change the distribution of bytes, packets, failed logins, ports, entropy, payload scores, and location/network metadata.

### How attacks are represented

- `dos`: high packet counts, short sessions, many ports, burst traffic
- `brute_force`: many login attempts and failures
- `data_exfiltration`: very high outbound traffic and long sessions
- `malware_beaconing`: repeated DNS activity and suspicious payload scores
- `insider_scan`: high port diversity and lateral movement behavior

### How the model detects suspicious behavior

- Random Forest predicts the likely attack class from feature patterns.
- Isolation Forest checks how unusual an event is compared to normal behavior.
- The project combines both into a risk score for better analyst prioritization.

### Step-by-step simulation workflow

1. Generate the synthetic logistics SOC dataset.
2. Clean records and add engineered features.
3. Train the classifier on labeled attack categories.
4. Train the anomaly detector mainly on normal behavior.
5. Score test records with both models.
6. Convert predictions into `Low`, `Medium`, `High`, and `Critical` alerts.
7. Save reports and generate charts.
8. Run the Streamlit dashboard for demo and screenshots.

### Outputs to generate

- `data/raw/logistics_cyber_threat_dataset.csv`
- `outputs/reports/predictions.csv`
- `outputs/reports/threat_alerts.csv`
- `outputs/metrics/model_metrics.json`
- all PNG charts inside `outputs/plots/`

### Proof students should capture

- dataset preview
- model metrics JSON
- top threat alerts CSV
- confusion matrix chart
- attack distribution chart
- dashboard homepage and alert table

## I. Execution Guide

### Run training and detection

```powershell
python main.py
```

### Run the dashboard

```powershell
streamlit run dashboard/app.py
```

### What successful execution looks like

- dataset CSV appears in `data/raw`
- train/test CSVs appear in `data/processed`
- model files appear in `models`
- metrics JSON appears in `outputs/metrics`
- alert CSVs appear in `outputs/reports`
- charts appear in `outputs/plots`

### Sample result summary

- Accuracy: `0.915`
- Weighted F1: `0.9173`
- Total test events: `800`
- Predicted threats: `352`
- Critical alerts: `16`

## J. GitHub Upload Strategy

### Best repository name

`AI-Cybersecurity-Threat-Detection-System`

### Best short description

AI-powered cybersecurity threat detection project for a simulated logistics enterprise using Python, scikit-learn, anomaly detection, alert scoring, and a Streamlit dashboard.

### Best GitHub topics

- `cybersecurity`
- `machine-learning`
- `threat-detection`
- `anomaly-detection`
- `streamlit`
- `python`
- `soc`
- `data-science`
- `network-security`

### Git commands

```bash
git init
git add .
git commit -m "Initial project scaffold for logistics threat detection system"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Professional repo tips

- add screenshots in README
- keep modular file structure
- write focused commit messages
- avoid dumping everything into one notebook
- include outputs, docs, and a clean explanation of business context

## K. README Content Strategy

Your README should include:

- project overview
- business problem
- why it matters
- architecture
- tech stack
- dataset explanation
- installation
- how to run
- results
- screenshots
- learning outcomes

This repository already includes a recruiter-friendly `README.md`.

## L. Daily Commit Plan

See [github_proof_plan.md](github_proof_plan.md) for the full day-wise plan.

## M. Proof Checklist

- [ ] dataset preview screenshot
- [ ] preprocessing or train/test split screenshot
- [ ] metrics JSON screenshot
- [ ] confusion matrix screenshot
- [ ] threat distribution screenshot
- [ ] dashboard KPI screenshot
- [ ] dashboard alert table screenshot
- [ ] GitHub repo homepage screenshot
- [ ] short demo video or GIF

## Phase-wise Implementation Plan

### Phase 1: Setup

- What to do: create folders, environment, and dependency file
- Why: establishes a stable development base
- Expected output: working project scaffold
- Common mistake: mixing files randomly or skipping virtual environment
- Verify: `python --version` and `pip install -r requirements.txt` work correctly

### Phase 2: Dataset loading

- What to do: generate and read the logistics telemetry dataset
- Why: every ML system starts with data
- Expected output: raw CSV in `data/raw`
- Common mistake: forgetting timestamp parsing
- Verify: open first 5 rows and inspect columns

### Phase 3: Data cleaning

- What to do: remove duplicates, handle nulls, validate types
- Why: noisy data creates unstable training
- Expected output: clean DataFrame
- Common mistake: training directly on dirty data
- Verify: check null counts and duplicate counts

### Phase 4: Feature engineering

- What to do: add behavior-based features
- Why: better features improve detection quality
- Expected output: enriched dataset with derived columns
- Common mistake: division-by-zero errors
- Verify: inspect new columns for invalid values

### Phase 5: Model building

- What to do: train Random Forest and Isolation Forest
- Why: combine known-attack classification with anomaly detection
- Expected output: model files in `models`
- Common mistake: using raw categories without encoding
- Verify: model files are saved and training completes

### Phase 6: Model evaluation

- What to do: compute accuracy, precision, recall, F1, confusion matrix
- Why: shows whether the model generalizes
- Expected output: metrics JSON and confusion matrix chart
- Common mistake: reporting accuracy only
- Verify: confirm `outputs/metrics/model_metrics.json` exists

### Phase 7: Threat detection logic

- What to do: convert predictions into risk and severity
- Why: SOC teams need prioritized alerts, not raw probabilities
- Expected output: predictions and alert CSVs
- Common mistake: treating every anomaly as critical
- Verify: inspect severity distribution

### Phase 8: Visualization

- What to do: export charts and build dashboard
- Why: visuals improve communication and GitHub proof
- Expected output: plot PNGs and Streamlit dashboard
- Common mistake: using unreadable colors or cluttered charts
- Verify: open `outputs/plots` and run the dashboard

### Phase 9: GitHub publishing

- What to do: push source, outputs, docs, and screenshots
- Why: converts work into visible portfolio proof
- Expected output: complete public repository
- Common mistake: uploading code with no explanation
- Verify: README shows project story clearly

### Phase 10: Final output

- What to do: record screenshots, demo video, and polished README sections
- Why: final polish is what recruiters notice
- Expected output: submission-ready project
- Common mistake: stopping after code works
- Verify: a new viewer can understand and run the project without asking questions

