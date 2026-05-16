# 🚀 Deployment Guide - Smart Data Analyst Agent

This guide covers deploying the Smart Data Analyst Agent to various platforms.

---

## 📋 Table of Contents

1. [Streamlit Cloud](#streamlit-cloud)
2. [Heroku](#heroku)
3. [AWS EC2](#aws-ec2)
4. [Docker](#docker)
5. [Local Production Server](#local-production-server)
6. [Troubleshooting](#troubleshooting)

---

## ☁️ Streamlit Cloud (Easiest)

### Prerequisites
- GitHub account
- Project pushed to GitHub

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select repository, branch, and file (app.py)
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to App settings → Secrets
   - Add your secrets:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```

4. **Your app is live!**
   - Share the public URL
   - App automatically updates on git push

### Advantages
- ✅ Free tier available
- ✅ Automatic SSL/HTTPS
- ✅ Easy CI/CD with GitHub
- ✅ No server management
- ✅ Shareable public link

### Disadvantages
- ❌ Limited computational resources
- ❌ Sleeps after 1 hour of inactivity
- ❌ Rate limiting

---

## 🔴 Heroku Deployment

### Prerequisites
- Heroku account
- Git installed
- GitHub repository

### Steps

1. **Create Heroku App**
```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create your-app-name
```

2. **Create Procfile**
```bash
# In project root
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

3. **Create setup.sh**
```bash
mkdir -p ~/.streamlit
echo "[general]" > ~/.streamlit/config.toml
echo "email = \"your-email@example.com\"" >> ~/.streamlit/config.toml
```

4. **Deploy**
```bash
git add .
git commit -m "Add deployment files"
git push heroku main
```

5. **Add Environment Variables**
```bash
heroku config:set GEMINI_API_KEY="your_key_here"
```

6. **View Logs**
```bash
heroku logs --tail
```

### Custom Procfile Example
```
web: sh setup.sh && streamlit run app.py
```

---

## 🟠 AWS EC2 Deployment

### Prerequisites
- AWS Account
- EC2 instance (Ubuntu 20.04+)
- SSH access to instance

### Steps

1. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. **Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install other dependencies
sudo apt install -y build-essential libssl-dev libffi-dev
```

3. **Clone Repository**
```bash
cd /home/ubuntu
git clone https://github.com/your-username/ai-data-analyst.git
cd ai-data-analyst
```

4. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Set Environment Variables**
```bash
cp .env.example .env
nano .env  # Edit and add your API key
```

6. **Run with Gunicorn**
```bash
pip install gunicorn

# Run in background
nohup streamlit run app.py --server.port 8501 &
```

7. **Setup Nginx Reverse Proxy**
```bash
sudo apt install -y nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/default
```

Example Nginx config:
```nginx
server {
    listen 80 default_server;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

8. **Enable HTTPS with Let's Encrypt**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Create .dockerignore

```
__pycache__
*.pyc
.git
.gitignore
.env
*.log
.streamlit/cache
.pytest_cache
venv/
.vscode/
```

### 3. Build Docker Image

```bash
docker build -t ai-data-analyst:1.0 .
```

### 4. Run Docker Container

```bash
# Local development
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your_key" \
  ai-data-analyst:1.0

# With volume mount for data
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY="your_key" \
  ai-data-analyst:1.0
```

### 5. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

### 6. Deploy to Docker Hub

```bash
# Tag image
docker tag ai-data-analyst:1.0 your-username/ai-data-analyst:1.0

# Login to Docker Hub
docker login

# Push image
docker push your-username/ai-data-analyst:1.0
```

---

## 🖥️ Local Production Server

### Setup with Systemd Service

1. **Create Service File**
```bash
sudo nano /etc/systemd/system/data-analyst.service
```

Add:
```ini
[Unit]
Description=Smart Data Analyst Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/ai-data-analyst
Environment="PATH=/home/your-username/ai-data-analyst/venv/bin"
Environment="GEMINI_API_KEY=your_key"
ExecStart=/home/your-username/ai-data-analyst/venv/bin/streamlit run app.py --server.port 8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable data-analyst
sudo systemctl start data-analyst
```

3. **Monitor Service**
```bash
sudo systemctl status data-analyst
sudo journalctl -u data-analyst -f
```

---

## 🔧 Production Best Practices

### Performance Optimization

1. **Cache Data**
```python
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
```

2. **Optimize Visualizations**
- Use `use_container_width=True` for better layout
- Limit data points in plots
- Use sampling for large datasets

3. **Resource Management**
```bash
# Limit memory usage
streamlit run app.py --logger.level=warning --client.maxMessageSize=200
```

### Security

1. **Never commit secrets**
```bash
# .gitignore
.env
.streamlit/secrets.toml
```

2. **Use secrets properly**
```python
import streamlit as st
api_key = st.secrets["GEMINI_API_KEY"]
```

3. **Enable CORS protection**
```bash
# In .streamlit/config.toml
[server]
enableCORS = false
```

4. **Add authentication** (Optional)
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
authenticator.login()
```

### Monitoring

1. **Setup Logging**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

2. **Monitor Resources**
```bash
# Check memory usage
ps aux | grep streamlit

# Monitor CPU
top -p $(pgrep -f streamlit)
```

### Backup Strategy

```bash
# Backup data and configs
crontab -e

# Add daily backup:
0 2 * * * tar -czf /backups/data-analyst-$(date +\%Y\%m\%d).tar.gz /home/user/ai-data-analyst/
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Out of Memory
```bash
# Increase available memory
# Or limit data size in app

@st.cache_data(max_entries=1)
def load_data(file):
    return pd.read_csv(file)
```

### API Key Issues
```bash
# Verify key is valid
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"
```

### Slow Performance
```bash
# Profile app
streamlit run app.py --logger.level=debug

# Reduce data size for testing
df = df.sample(frac=0.1)  # Use 10% of data
```

### Connection Issues
```bash
# Test connectivity
ping api.example.com

# Check firewall rules
sudo ufw status

# Allow port
sudo ufw allow 8501
```

---

## 📊 Performance Metrics

| Platform | Cold Start | Memory | Cost/month | Uptime |
|----------|-----------|--------|------------|--------|
| Streamlit Cloud | <2s | 1GB | Free | 99.9% |
| Heroku | 5-10s | 512MB | $7-50 | 99.95% |
| AWS EC2 | <1s | Custom | $5-100 | 99.9% |
| Docker | <1s | Custom | Variable | High |

---

## 📚 Additional Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Heroku Deploy Guide](https://devcenter.heroku.com/)
- [AWS Deployment](https://aws.amazon.com/solutions/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

## ✅ Pre-Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Environment variables configured
- [ ] API keys secured
- [ ] .env in .gitignore
- [ ] README updated with deployment info
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Backup strategy in place

---

Happy Deploying! 🚀
