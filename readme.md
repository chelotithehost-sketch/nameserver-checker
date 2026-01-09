# 🌐 .co.za Nameserver Authority Checker

A Streamlit web application for bulk checking if nameservers are authoritative for .co.za domains. This tool is essential for domain administrators who need to verify DNS configurations before making nameserver changes.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🎯 Purpose

.co.za domains have a strict requirement: nameserver changes can only be made when the nameservers are authoritative for the domain. This tool helps you:

- ✅ Verify if nameservers are currently authoritative
- 🔍 Identify DNS configuration issues
- 📊 Bulk check multiple domains at once
- 💡 Get actionable suggestions for fixing issues
- 📥 Export results for documentation

## ✨ Features

- **Bulk Checking**: Process multiple domains simultaneously
- **File Upload**: Import domains from CSV or TXT files
- **Real-time Verification**: Uses Google Public DNS API for accurate results
- **Visual Status Indicators**: Color-coded results (green/yellow/red)
- **Detailed Suggestions**: Get specific recommendations for each domain
- **Export Results**: Download comprehensive CSV reports
- **User-Friendly Interface**: Clean, intuitive design

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nameserver-checker.git
   cd nameserver-checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

### Using Docker (Optional)

```bash
docker build -t nameserver-checker .
docker run -p 8501:8501 nameserver-checker
```

## 📝 Usage

### Input Format

Enter your domains and nameservers in one of these formats:

**Format 1: Comma-separated**
```
domain.co.za, ns1.example.com, ns2.example.com
anotherdomain.co.za, ns1.host.com, ns2.host.com
```

**Format 2: Tab-separated**
```
domain.co.za    ns1.example.com    ns2.example.com
anotherdomain.co.za    ns1.host.com    ns2.host.com
```

### Input Methods

1. **Paste Text**: Copy and paste your domain list directly into the text area
2. **Upload File**: Upload a CSV or TXT file containing your domain list

### Example CSV File

```csv
example.co.za,ns1.example.com,ns2.example.com
mybusiness.co.za,ns1.provider.com,ns2.provider.com
testdomain.co.za,dns1.host.net,dns2.host.net
```

## 📊 Understanding Results

### Status Types

- **✅ Authoritative**: All nameservers match - domain is correctly configured
- **⚠️ Partial Match**: Some nameservers match - needs updating
- **❌ Not Authoritative**: No matches - nameservers must be changed at registrar
- **🔴 Error**: Unable to resolve domain - check domain validity

### What Each Status Means

#### ✅ Authoritative (Success)
Your nameservers are properly configured and authoritative for the domain. You can make DNS changes at these nameservers.

**Actions:**
- No action needed
- DNS changes can be made at the nameserver control panel
- Changes will propagate globally

#### ⚠️ Partial Match (Warning)
Some of your specified nameservers match, but not all. This indicates an incomplete configuration.

**Actions:**
- Review the actual authoritative nameservers
- Update your registrar to include all correct nameservers
- Remove any old/incorrect nameservers
- Wait 24-48 hours for DNS propagation

#### ❌ Not Authoritative (Error)
None of your specified nameservers are authoritative. The domain is using different nameservers.

**Actions:**
- Note the current authoritative nameservers shown in results
- Log into your domain registrar's control panel
- Update nameservers to match your desired configuration
- Wait 24-48 hours for propagation
- Re-check using this tool

#### 🔴 Error
The domain could not be resolved or an error occurred.

**Possible Causes:**
- Domain is not registered
- Domain registration has expired
- DNS propagation is still in progress
- Network connectivity issues

## 🛠️ Technical Details

### How It Works

1. **Input Parsing**: Parses your input to extract domains and nameservers
2. **DNS Query**: Queries Google Public DNS API for NS records
3. **Comparison**: Compares requested nameservers with actual authoritative ones
4. **Analysis**: Determines authorization status and generates suggestions
5. **Results**: Displays comprehensive results with actionable recommendations

### API Used

- **Google Public DNS API**: `https://dns.google/resolve`
- **Query Type**: NS (Nameserver) records
- **Rate Limiting**: Built-in delays to prevent API throttling

## 📁 Project Structure

```
nameserver-checker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore file
├── Dockerfile            # Docker configuration (optional)
└── example_input.csv     # Sample input file
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file for custom configuration:

```env
# DNS API endpoint (if using alternative)
DNS_API_URL=https://dns.google/resolve

# Request timeout in seconds
REQUEST_TIMEOUT=10

# Rate limit delay in seconds
RATE_LIMIT_DELAY=0.2
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Roadmap

- [ ] Add support for other TLDs (.com, .net, etc.)
- [ ] Historical tracking of nameserver changes
- [ ] Email notifications for status changes
- [ ] Batch scheduling for regular checks
- [ ] API endpoint for programmatic access
- [ ] Multi-language support

## ❓ FAQ

**Q: Why do I need to check if nameservers are authoritative?**
A: For .co.za domains, you can only make nameserver changes at your registrar when the nameservers are authoritative. This tool helps you verify before attempting changes.

**Q: How long does DNS propagation take?**
A: Typically 24-48 hours, though it can sometimes take up to 72 hours for full global propagation.

**Q: Can I use this for non-.co.za domains?**
A: Yes! While designed for .co.za domains, it works for any domain name.

**Q: Is my data stored anywhere?**
A: No, all checks are done in real-time and no data is stored on our servers.

**Q: What if I get errors for valid domains?**
A: Ensure the domain is registered and active. DNS propagation may still be in progress if you recently made changes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Public DNS API for nameserver resolution
- Streamlit for the amazing web framework
- The .co.za registry for domain management rules

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report a bug](https://github.com/yourusername/nameserver-checker/issues)
- 💡 [Request a feature](https://github.com/yourusername/nameserver-checker/issues)
- 📧 Email: your.email@example.com

## 🌟 Show Your Support

If you find this tool helpful, please consider:
- ⭐ Starring the repository
- 🐦 Sharing on social media
- 🤝 Contributing to the project

---

**Made with ❤️ for the .co.za community**
