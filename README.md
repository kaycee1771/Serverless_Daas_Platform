# Serverless Deception-as-a-Service (DaaS) Platform

A cloud-native threat detection platform that uses deception technology to proactively detect attackers **before** they exploit real systems. Designed for serverless environments, it auto-injects fake assets and logs access patterns through a real-time alert pipeline enriched with an ML-based attacker intent classifier.

---

## Purpose

This platform functions as an early-warning system by placing **decoy endpoints, fake credentials, and internal URLs** inside serverless applications (e.g., AWS Lambda). When accessed, these trigger structured alerts to help security teams:

* Identify attacker reconnaissance and credential theft attempts
* Classify intent automatically using machine learning
* Reduce dwell time with real-time alerts

---

## Core Features

| Feature                        | Description                                                              |
| ------------------------------ | ------------------------------------------------------------------------ |
| **Honeypot API**            | Fake API deployed on AWS Lambda + API Gateway to trap attackers          |
| **Real-Time Log Streaming** | CloudWatch Logs subscription directly invokes alert Lambda               |
| **ML Intent Classifier**    | LogisticRegression + Tfidf-based classifier for attack intent prediction |
| **Serverless Architecture** | Fully packaged with AWS SAM for reproducibility                          |
| **Simulation Script**       | CLI tool to simulate attacker behavior (sqlmap, curl, etc.)              |
| **Structured Alerts**       | Alerts include attacker source IP, user agent, and predicted intent      |
| **Deception Assets**        | Fake API keys, internal URLs, endpoints embedded in responses            |

---

## Intelligence Engine

The ML classifier analyzes:

* `User-Agent` (e.g., sqlmap, curl)
* `Query strings` or `headers` (e.g., `?debug=true`, `?id=admin`)
* `Access patterns`

And predicts attacker intent:

* `credential_theft`
* `scanning`
* `probing`
* `unknown`

Trained using labeled attacker simulation logs and saved as a `joblib` model included in the deployment.

---

## Project Structure

```
Serverless-DaaS-Platform/
├── src/
│   ├── honeypots/
│   │   └── fake_api/
│   │       ├── app.py
│   │       ├── template.yaml
│   ├── alerts/
│   │   └── alert_forwarder/
│   │       ├── handler.py
│   │       ├── classifier.py
│   │       ├── intent_classifier.joblib
│   │       ├── template.yaml
│   └── decoy_injector/
│       └── inject.py
├── deploy/
│   └── scripts/
│       └── simulate_attack.py
├── data/samples/intent_training_data.csv
├── model/intent_classifier.joblib
├── train_classifier.py
├── requirements.txt
├── samconfig.toml
└── README.md
```

---

## How to Deploy

### Prerequisites

* AWS CLI configured (`aws configure`)
* SAM CLI installed (`brew install aws-sam-cli` or see AWS docs)

### Deploy the Honeypot

```bash
cd src/honeypots/fake_api
sam build
sam deploy
```

### Deploy the Alert Forwarder

```bash
cd src/alerts/alert_forwarder
sam build
sam deploy
```

### Connect CloudWatch to Alert Forwarder

1. Grant permission:

```bash
aws lambda add-permission \
  --function-name daas-alert-forwarder \
  --statement-id AllowExecutionFromCW \
  --action "lambda:InvokeFunction" \
  --principal logs.amazonaws.com \
  --source-arn arn:aws:logs:<region>:<account-id>:log-group:/aws/lambda/fake-api-honeypot:*
```

2. Add log subscription:

```bash
aws logs put-subscription-filter \
  --log-group-name "/aws/lambda/fake-api-honeypot" \
  --filter-name "DAASTriggerFilter" \
  --filter-pattern '"[DAAS_LOG]"' \
  --destination-arn arn:aws:lambda:<region>:<account-id>:function:daas-alert-forwarder
```

---

## Simulating Attacker Activity

Use the provided script to simulate malicious access:

```bash
python deploy/scripts/simulate_attack.py --url https://your-api-url/Prod/fake --count 3
```

Expected behavior:

* Fake credentials are returned
* \[DAAS\_LOG] entries appear in CloudWatch
* Alert forwarder is invoked

---

## Inspecting Alerts

Check logs for structured alert output:

```bash
aws logs filter-log-events --log-group-name /aws/lambda/daas-alert-forwarder
```

Example output:

```json
[ALERT] {
  "alert_type": "deception_trigger",
  "intent": "credential_theft",
  "user_agent": "sqlmap/1.5.1",
  "source_ip": "203.0.113.10",
  "timestamp": "2025-07-18T10:00:00Z"
}
```

---

## Future Enhancements

* [ ] Azure Functions integration (multi-cloud honeypots)
* [ ] Dashboard for alerts (e.g., S3 static site)
* [ ] Export to Splunk or Sentinel via webhook
* [ ] GitHub Actions CI for model and template validation
* [ ] Auto-remediation triggers

---

## Credits

Built by Kelechi Okpala — focused on cloud-native security, adversary engagement, and intelligent detection pipelines.
