# 🌿 Cannabis Deployment System - README
=============================================

**Complete automated deployment sync for 3 Streamlit cannabis applications**

## 🚀 One-Command Setup

After 72 hours awake, you deserve automation that just works:

```bash
python fix_everything.py
```

That's it! Your entire cannabis app ecosystem will be configured automatically.

## 🌿 Your Cannabis Applications

1. **🧠 Green Hill GPT** - AI-powered strain recommendation system
   - Streamlit: https://greenhillgpt.streamlit.app
   - LangGraph: https://green-hill-gpt-ai-a1b2c3d4e5f6.us.langgraph.app

2. **🌱 Digital Roots** - Cannabis cultivation management platform  
   - Streamlit: https://digital-roots.streamlit.app
   - LangGraph: https://digital-roots-cultivation-g7h8i9j0k1l2.us.langgraph.app

3. **🎮 Ground Control** - Cannabis operations command center
   - Streamlit: https://ground-control.streamlit.app
   - LangGraph: https://ground-control-a0ae430fa0b85ca09ebb486704b69f2b.us.langgraph.app

## 📋 Quick Setup Steps

1. **Set Environment Variables:**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

2. **Required API Keys:**
   - `LANGSMITH_API_KEY` - From https://smith.langchain.com/
   - `GITHUB_TOKEN` - From GitHub Settings > Personal Access Tokens
   - `OPENAI_API_KEY` - From https://platform.openai.com/api-keys
   - `STREAMLIT_SHARING_EMAIL` - Your Streamlit Cloud account email

3. **Run Deployment:**
   ```bash
   python fix_everything.py
   ```

4. **Check Status:**
   ```bash
   python check_status.py
   ```

## 🔧 What Gets Automated

✅ **GitHub Repositories**
- Creates/configures 3 repos: `greenhillgpt`, `digital-roots`, `ground-control`
- Sets up GitHub Actions workflows for auto-deployment
- Configures proper .gitignore for cannabis industry compliance

✅ **LangSmith Integration**
- Connects repos to your LangSmith org: `3d60abf5-78b5-4d90-8b55-2f69b0f53557`
- Auto-syncs on every git push
- Manages API keys securely

✅ **Streamlit Cloud**
- Configures deployment from GitHub
- Sets up secrets.toml templates
- Creates requirements.txt for each app

✅ **Monitoring & Logging**
- Creates comprehensive logging system
- Generates monitoring dashboard
- Provides status checking tools

## 🌿 Cannabis Industry Features

- **HIPAA Compliance** - Medical cannabis data protection
- **Regulatory Compliance** - Built-in compliance tools
- **Data Privacy** - Secure patient information handling
- **Medical Cannabis Support** - Specialized features for medical use

## 📊 Monitoring Your Apps

After deployment, monitor everything with:

```bash
# Quick status check
python check_status.py

# Full monitoring dashboard
streamlit run cannabis_monitor.py
```

## 🔐 Security Features

- All API keys stored securely in environment variables
- Secrets never committed to Git
- HIPAA-compliant data handling
- Cannabis industry security standards

## 📞 Support

**Zaki Baydoun** (Pharmacist & AI Developer)
- 📧 Email: zakibaydoun@msn.com  
- 🐙 GitHub: @zakibaydoun
- 🏢 Organization ID: 3d60abf5-78b5-4d90-8b55-2f69b0f53557

## 🎯 Troubleshooting

**If deployment fails:**
1. Check your API keys in `.env` file
2. Verify GitHub token has proper permissions
3. Ensure LangSmith org ID is correct
4. Run `python check_status.py` for diagnostics

**Common Issues:**
- 403 errors → Check API keys
- Connection timeouts → Check internet/firewall
- GitHub Actions failing → Verify repo permissions

## 🌿 Cannabis Compliance Notes

This system is designed specifically for the legal cannabis industry:
- All data handling follows medical cannabis regulations
- Built-in HIPAA compliance features
- Secure patient data management
- Regulatory reporting capabilities

---

*Built with 💚 for the cannabis industry. After 72 hours of work, you deserve automation that just works.*