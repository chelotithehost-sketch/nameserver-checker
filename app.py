import streamlit as st
import pandas as pd
import requests
import time
from io import StringIO
import json

# Page configuration
st.set_page_config(
    page_title=".co.za Nameserver Authority Checker",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def parse_input(text):
    """Parse input text into domain and nameserver pairs"""
    lines = text.strip().split('\n')
    parsed = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # Split by comma or tab
        parts = [p.strip() for p in line.replace('\t', ',').split(',')]
        
        if len(parts) >= 2:
            domain = parts[0].lower().replace('https://', '').replace('http://', '').replace('/', '')
            nameservers = [ns for ns in parts[1:] if ns]
            
            if domain and nameservers:
                parsed.append({
                    'domain': domain,
                    'nameservers': nameservers
                })
    
    return parsed

def check_nameserver_authority(domain, nameservers):
    """Check if nameservers are authoritative for a domain"""
    try:
        # Query Google DNS API
        url = f"https://dns.google/resolve?name={domain}&type=NS"
        response = requests.get(url, timeout=10)
        dns_data = response.json()
        
        # Check if query was successful
        if dns_data.get('Status') != 0 or 'Answer' not in dns_data:
            return {
                'domain': domain,
                'requested_ns': nameservers,
                'actual_ns': [],
                'is_authoritative': False,
                'status': 'error',
                'message': 'Unable to resolve domain nameservers',
                'suggestions': [
                    'Verify the domain is registered and active',
                    'Check if the domain has been delegated properly',
                    'Ensure DNS propagation is complete (can take 24-48 hours)'
                ]
            }
        
        # Extract actual nameservers
        actual_ns = []
        for record in dns_data.get('Answer', []):
            if record.get('type') == 2:  # NS record
                ns = record.get('data', '').lower().rstrip('.')
                actual_ns.append(ns)
        
        # Normalize requested nameservers
        requested_ns_normalized = [ns.lower().rstrip('.') for ns in nameservers]
        
        # Check if all requested nameservers match
        all_match = all(
            any(actual == req or actual in req or req in actual 
                for actual in actual_ns)
            for req in requested_ns_normalized
        )
        
        some_match = any(
            any(actual == req or actual in req or req in actual 
                for actual in actual_ns)
            for req in requested_ns_normalized
        )
        
        # Determine status and suggestions
        if all_match:
            status = 'success'
            message = '✅ All nameservers are authoritative'
            suggestions = [
                '✓ Domain is properly configured',
                '✓ Nameserver changes can be made at the registrar',
                '✓ Any DNS changes will propagate from these nameservers'
            ]
        elif some_match:
            status = 'partial'
            message = '⚠️ Some nameservers match, but not all'
            missing_ns = [ns for ns in actual_ns 
                         if not any(req == ns or req in ns or ns in req 
                                   for req in requested_ns_normalized)]
            suggestions = [
                '→ Update nameservers at your domain registrar to match exactly',
                '→ Remove old/incorrect nameservers',
                f'→ Add missing nameservers: {", ".join(missing_ns)}' if missing_ns else '',
                '→ Wait 24-48 hours for DNS propagation after making changes'
            ]
            suggestions = [s for s in suggestions if s]
        else:
            status = 'mismatch'
            message = '❌ Requested nameservers are NOT authoritative'
            suggestions = [
                f'→ Current authoritative nameservers: {", ".join(actual_ns)}',
                '→ Update nameservers at your domain registrar (e.g., where you bought the domain)',
                '→ For .co.za domains, update via your registrar\'s control panel',
                '→ After updating, wait 24-48 hours for propagation',
                '→ Verify the nameservers you want to use are correctly configured'
            ]
        
        return {
            'domain': domain,
            'requested_ns': nameservers,
            'actual_ns': actual_ns,
            'is_authoritative': all_match,
            'status': status,
            'message': message,
            'suggestions': suggestions
        }
        
    except requests.exceptions.Timeout:
        return {
            'domain': domain,
            'requested_ns': nameservers,
            'actual_ns': [],
            'is_authoritative': False,
            'status': 'error',
            'message': 'Request timeout - DNS server not responding',
            'suggestions': [
                'Check your internet connection',
                'Try again in a few moments',
                'The DNS server may be experiencing issues'
            ]
        }
    except Exception as e:
        return {
            'domain': domain,
            'requested_ns': nameservers,
            'actual_ns': [],
            'is_authoritative': False,
            'status': 'error',
            'message': f'Error: {str(e)}',
            'suggestions': [
                'Check your internet connection',
                'Verify the domain name is correct',
                'Try again in a few moments'
            ]
        }

def display_result(result):
    """Display a single result with appropriate styling"""
    status = result['status']
    
    if status == 'success':
        box_class = 'success-box'
        icon = '✅'
    elif status == 'partial':
        box_class = 'warning-box'
        icon = '⚠️'
    else:
        box_class = 'error-box'
        icon = '❌'
    
    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
    st.markdown(f"### {icon} {result['domain']}")
    st.markdown(f"**{result['message']}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Requested Nameservers:**")
        for ns in result['requested_ns']:
            st.code(ns, language=None)
    
    with col2:
        st.markdown("**Actual Authoritative Nameservers:**")
        if result['actual_ns']:
            for ns in result['actual_ns']:
                st.code(ns, language=None)
        else:
            st.write("*None found*")
    
    st.markdown("**Suggestions:**")
    for suggestion in result['suggestions']:
        st.write(f"• {suggestion}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def convert_results_to_csv(results):
    """Convert results to CSV format"""
    data = []
    for result in results:
        data.append({
            'Domain': result['domain'],
            'Requested Nameservers': '; '.join(result['requested_ns']),
            'Actual Nameservers': '; '.join(result['actual_ns']),
            'Status': result['status'],
            'Message': result['message'],
            'Suggestions': ' | '.join(result['suggestions'])
        })
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

# Main app
def main():
    # Header
    st.markdown('<p class="main-header">🌐 .co.za Nameserver Authority Checker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Bulk check if nameservers are authoritative for your domains</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This tool checks if nameservers are authoritative for .co.za domains.
        
        **Why is this important?**
        - .co.za domains only allow nameserver changes when they are authoritative
        - This ensures proper DNS delegation
        - Helps troubleshoot DNS configuration issues
        """)
        
        st.header("📋 Input Format")
        st.code("""domain.co.za, ns1.example.com, ns2.example.com
anotherdomain.co.za, ns1.host.com, ns2.host.com""")
        st.write("Separate domain and nameservers with commas or tabs")
        
        st.header("🔧 Features")
        st.write("""
        ✓ Bulk checking
        ✓ File upload (CSV/TXT)
        ✓ Real-time DNS verification
        ✓ Export results to CSV
        ✓ Detailed suggestions
        """)
    
    # Input methods
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 📥 Input Methods")
    st.markdown('</div>', unsafe_allow_html=True)
    
    input_method = st.radio(
        "Choose input method:",
        ["Paste Text", "Upload File"],
        horizontal=True
    )
    
    input_text = ""
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload CSV or TXT file",
            type=['csv', 'txt'],
            help="File should contain domain and nameservers separated by commas"
        )
        
        if uploaded_file is not None:
            input_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            with st.expander("Preview uploaded data"):
                st.text(input_text[:500] + ("..." if len(input_text) > 500 else ""))
    else:
        input_text = st.text_area(
            "Paste your domain list here:",
            height=200,
            placeholder="example.co.za, ns1.example.com, ns2.example.com\nanother.co.za, ns1.host.com, ns2.host.com",
            help="Enter one domain per line with its nameservers"
        )
    
    # Check button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        check_button = st.button("🔍 Check Nameservers", type="primary", use_container_width=True)
    
    # Process and display results
    if check_button and input_text.strip():
        # Parse input
        domains = parse_input(input_text)
        
        if not domains:
            st.error("❌ No valid domains found. Please check your input format.")
            return
        
        st.success(f"✅ Found {len(domains)} domain(s) to check")
        
        # Initialize results
        results = []
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Check each domain
        for i, domain_data in enumerate(domains):
            status_text.text(f"Checking {domain_data['domain']}... ({i+1}/{len(domains)})")
            
            result = check_nameserver_authority(
                domain_data['domain'],
                domain_data['nameservers']
            )
            results.append(result)
            
            progress_bar.progress((i + 1) / len(domains))
            time.sleep(0.2)  # Small delay to avoid rate limiting
        
        status_text.text("✅ All checks complete!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # Display summary
        st.markdown("---")
        st.markdown("### 📊 Results Summary")
        
        summary_cols = st.columns(4)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        partial_count = sum(1 for r in results if r['status'] == 'partial')
        mismatch_count = sum(1 for r in results if r['status'] == 'mismatch')
        error_count = sum(1 for r in results if r['status'] == 'error')
        
        with summary_cols[0]:
            st.metric("✅ Authoritative", success_count)
        with summary_cols[1]:
            st.metric("⚠️ Partial Match", partial_count)
        with summary_cols[2]:
            st.metric("❌ Not Authoritative", mismatch_count)
        with summary_cols[3]:
            st.metric("🔴 Errors", error_count)
        
        # Export button
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            csv_data = convert_results_to_csv(results)
            st.download_button(
                label="📥 Download Results (CSV)",
                data=csv_data,
                file_name="nameserver-check-results.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Display individual results
        st.markdown("---")
        st.markdown("### 📋 Detailed Results")
        
        # Filter options
        filter_option = st.selectbox(
            "Filter results:",
            ["All", "Authoritative Only", "Issues Only", "Errors Only"]
        )
        
        filtered_results = results
        if filter_option == "Authoritative Only":
            filtered_results = [r for r in results if r['status'] == 'success']
        elif filter_option == "Issues Only":
            filtered_results = [r for r in results if r['status'] in ['partial', 'mismatch']]
        elif filter_option == "Errors Only":
            filtered_results = [r for r in results if r['status'] == 'error']
        
        if not filtered_results:
            st.info(f"No results match the filter: {filter_option}")
        else:
            for result in filtered_results:
                display_result(result)
                st.markdown("---")
    
    elif check_button:
        st.warning("⚠️ Please enter some data to check")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem 0;'>
        <p>Built with ❤️ for .co.za domain management</p>
        <p style='font-size: 0.8rem;'>Uses Google Public DNS API for nameserver verification</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
