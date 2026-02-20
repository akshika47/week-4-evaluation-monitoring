# Frontend - Streamlit Chat Interface

Streamlit frontend for the Research Assistant. Deploy to Streamlit Cloud.

## Setup

1. **Create a GitHub repository** for your frontend
2. **Copy these files:**
   - `app.py` - Streamlit application
   - `requirements.txt` - Dependencies

3. **Create `.streamlit/secrets.toml` for local testing:**
   ```toml
   API_URL = "http://localhost:8000"
   ```

## Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click "New app"
3. Configure:
   - **Repository:** Select your frontend repository
   - **Branch:** main (or your default branch)
   - **Main file path:** `app.py`
4. Click "Advanced settings"
5. Add secret:
   - **Key:** `API_URL`
   - **Value:** Your Render backend URL (e.g., `https://your-app.onrender.com`)
6. Click "Deploy"
7. Wait for deployment (1-2 minutes)
8. Get your URL: `https://your-app.streamlit.app`

## Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py

# Make sure your backend is running on http://localhost:8000
```

## Configuration

The app reads the API URL from Streamlit secrets. For local testing, create `.streamlit/secrets.toml`:

```toml
API_URL = "http://localhost:8000"
```

For production (Streamlit Cloud), set it in the app settings.

