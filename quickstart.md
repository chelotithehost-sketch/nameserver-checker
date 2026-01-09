# 🚀 Quick Start Guide

Get your .co.za Nameserver Authority Checker running in 5 minutes!

## ⚡ Super Quick Start (3 Commands)

```bash
# 1. Navigate to the folder
cd nameserver-checker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

That's it! Your browser will open automatically to `http://localhost:8501`

## 📝 First Test

Once the app is running, try this test data:

```
google.com, ns1.google.com, ns2.google.com, ns3.google.com
example.com, a.iana-servers.net, b.iana-servers.net
```

1. Paste the above into the text area
2. Click "🔍 Check Nameservers"
3. See the results!

## 🎯 For Your .co.za Domains

Replace the test data with your actual domains:

```
yourdomain.co.za, ns1.yourhost.com, ns2.yourhost.com
anotherdomain.co.za, dns1.provider.com, dns2.provider.com
```

## 📤 Upload a File

You can also upload a CSV file with this format:

```csv
domain.co.za,ns1.example.com,ns2.example.com
mybusiness.co.za,dns1.provider.com,dns2.provider.com
```

See `example_input.csv` for a template!

## 🌐 Deploy to Cloud (Free)

### Streamlit Cloud (Recommended - Takes 2 minutes)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub
   - Select this repository
   - Click Deploy!

Your app will be live at: `https://your-app-name.streamlit.app`

## 🐳 Docker (One Command)

```bash
docker run -p 8501:8501 $(docker build -q .)
```

Then open `http://localhost:8501`

## ❓ Need Help?

- **Setup Issues**: Check `SETUP.md`
- **Full Documentation**: Check `README.md`
- **Can't find Python?**: [Download Python](https://www.python.org/downloads/)
- **Still stuck?**: Create an issue on GitHub

## 💡 Pro Tips

1. **Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

2. **Custom Port**:
   ```bash
   streamlit run app.py --server.port=8080
   ```

3. **Run in Background**:
   ```bash
   nohup streamlit run app.py &
   ```

---

**Ready?** Run the 3 commands above and you're good to go! 🎉
