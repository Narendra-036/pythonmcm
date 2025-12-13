# Render Deployment Guide

## Environment Variables to Set on Render

Go to your Render dashboard → Your service → Environment

Add these environment variables:

### 1. GOOGLE_APPLICATION_CREDENTIALS_JSON
Copy the ENTIRE content of your `config/service-account.json` file and paste it as a single line.

Example:
```
{"type":"service_account","project_id":"adxguard-console","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...","client_email":"...","client_id":"..."}
```

### 2. GAM_NETWORK_CODE
```
23033612553
```

### 3. GAM_SERVICE_ACCOUNT
```
config/googleads.yaml
```

## How to Get service-account.json Content

1. Open `config/service-account.json` in a text editor
2. Copy ALL content (the entire JSON object)
3. Remove ALL line breaks to make it a single line
4. Paste into Render environment variable `GOOGLE_APPLICATION_CREDENTIALS_JSON`

## Alternative: Use Secret Files on Render

1. Go to Render dashboard → Your service → Secret Files
2. Click "Add Secret File"
3. Filename: `config/service-account.json`
4. Contents: Paste your service account JSON content
5. Save

Then update your environment variable:
```
GAM_SERVICE_ACCOUNT=config/googleads.yaml
```

## Test Locally

```bash
# Set environment variable
$env:GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type":"service_account",...}'

# Run the API
python api_fetch.py
```

## Deploy to Render

```bash
git add .
git commit -m "Fix service account authentication"
git push origin main
```

Render will automatically redeploy.
