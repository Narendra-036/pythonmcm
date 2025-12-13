# GAM Child Publisher Monitor

A Python application that monitors Google Ad Manager (GAM) child publisher accounts and sends alerts when accounts are closed due to policy violations, invalid activity, or other reasons.

## Features

- **Automated Monitoring**: Queries GAM for child publishers with closed statuses
- **Smart Deduplication**: Uses Firebase to track previously seen accounts and avoid duplicate alerts
- **Multi-Channel Alerts**: 
  - Email notifications with formatted HTML tables
  - Webhook integration for monitoring systems
- **Configurable**: All settings managed through environment variables
- **Logging**: Comprehensive logging for debugging and audit trails

## Project Structure

```
gam-child-publisher-monitor/
├── config/                    # Configuration files (credentials)
│   ├── .gitkeep
│   ├── service-account.json   # GAM service account (not tracked)
│   └── firebase-credentials.json  # Firebase credentials (not tracked)
├── services/                  # Service classes
│   ├── __init__.py
│   ├── ChildPubService.py     # Main monitoring service
│   ├── EmailService.py        # Email sending service
│   └── FirebaseService.py     # Firebase data storage service
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── helpers.py             # GAM client helper
├── .env                       # Environment variables (not tracked)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Prerequisites

- Python 3.8 or higher
- Google Ad Manager account with MCM (Multi-Client Management) access
- Firebase Realtime Database
- SMTP server access for sending emails

## Setup

### 1. Clone or Download the Project

```bash
cd gam-child-publisher-monitor
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your actual configuration:

```ini
# GAM Configuration
GAM_NETWORK_CODE=123456789
GAM_SERVICE_ACCOUNT=config/service-account.json
GAM_CONSOLE_URL=https://admanager.google.com/123456789#admin/mcm/child_publisher/list

# Email Configuration
EMAIL_RECIPIENTS=admin@example.com,team@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=notifications@example.com

# Escalation Configuration
ESCALATION_WEBHOOK_URL=https://your-monitoring.com/webhook

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=config/firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

# Optional Configuration
PROJECT_NAME=ads
MAX_ENTRIES_TO_CHECK=25
```

### 6. Add Credentials

Place your credential files in the `config/` directory:

- `config/service-account.json` - GAM service account credentials
- `config/firebase-credentials.json` - Firebase Admin SDK credentials

### 7. Run the Application

```bash
python main.py
```

## Configuration Details

### GAM Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a service account with Ad Manager API access
3. Download the JSON key file
4. Place it in `config/service-account.json`

### Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing
3. Enable Realtime Database
4. Go to Project Settings > Service Accounts
5. Generate new private key
6. Save as `config/firebase-credentials.json`

### Email Configuration

For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833):
1. Enable 2-factor authentication on your Google account
2. Generate an App Password
3. Use the app password in `SMTP_PASSWORD`

## Usage

### Manual Execution

```bash
python main.py
```

### Scheduled Execution (Windows Task Scheduler)

Create a scheduled task to run the script periodically:

```powershell
# Run daily at 9 AM
schtasks /create /tn "GAM Monitor" /tr "C:\path\to\venv\Scripts\python.exe C:\path\to\main.py" /sc daily /st 09:00
```

### Scheduled Execution (Linux Cron)

```bash
# Run every hour
0 * * * * /path/to/venv/bin/python /path/to/main.py
```

## Monitoring Statuses

The application monitors these child publisher statuses by default:
- `CLOSED_POLICY_VIOLATION`
- `CLOSED_INVALID_ACTIVITY`
- `CLOSED_BY_PUBLISHER`

You can customize this by modifying the `statuses` parameter in `ChildPubService.fetch_account_status()`.

## Logs

Application logs are written to:
- `app.log` - File-based logging
- Console output - Real-time monitoring

## Troubleshooting

### "Missing configuration" error
- Verify `.env` file exists and contains all required variables

### "Firebase credentials file not found"
- Check that `config/firebase-credentials.json` exists
- Verify the path in `.env` matches the actual file location

### "SMTP credentials not configured"
- Ensure `SMTP_USER` and `SMTP_PASSWORD` are set in `.env`
- For Gmail, verify you're using an App Password

### "Failed to create GAM client"
- Verify service account has proper GAM API permissions
- Check that the network code is correct

## Development

To contribute or modify:

1. Make changes to the code
2. Test thoroughly
3. Update documentation as needed
4. Check logs for any errors

## License

This project is provided as-is for internal use.

## Support

For issues or questions, contact your development team.
