
# 🔐 Digital Identity Graph Detection

This project builds a knowledge graph of users, devices, and IPs to identify synthetic or suspicious identities based on login behavior. It uses graph analysis, community detection, and a custom trust scoring algorithm.

## 📊 Features

- Graph model of users, IPs, and devices
- Louvain community detection
- Flags reused IPs/devices and low-diversity clusters
- Trust scoring algorithm (0 = suspicious, 1 = trusted)
- FastAPI REST API for real-time trust checks
- Streamlit dashboard for visual inspection
- Docker support for easy deployment

## 🚀 Run Locally with Docker

Build the Docker image:

```bash
docker build -t digital-identity-app .
```

Run the app:

```bash
docker run -p 8000:8000 -p 8501:8501 digital-identity-app
```

## 🔌 API Endpoint

POST `/check_trust`

**Request:**

```json
{
  "user_id": "user_042"
}
```

**Response:**

```json
{
  "user_id": "user_042",
  "trust_score": 0.76
}
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## 📊 Streamlit Dashboard

View it at: [http://localhost:8501](http://localhost:8501)

- Select a user ID from the dropdown
- Instantly view their trust score
- Visual risk indicator:
  - ✅ Safe (score > 0.7)
  - ⚠️ Medium Risk (0.4 < score ≤ 0.7)
  - ❌ Suspicious (score ≤ 0.4)

## 📁 Project Structure

```
📁 DigitalIdentityGraphDetection/
├── app.py
├── trust_core.py
├── dashboard.py
├── start.sh
├── Dockerfile
├── requirements.txt
├── users.csv
├── logins.csv
├── devices.csv
└── ip_metadata.csv
```

## 🛠️ Technologies Used

- Python 3.11
- FastAPI
- Streamlit
- NetworkX
- Pandas
- python-louvain
- Docker

## 🧠 Author

Madumita24  
[https://github.com/Madumita24](https://github.com/Madumita24)


