import io
import pandas as pd
import streamlit as st
import streamlit as st

# Yeh code upar ke GitHub links aur niche ke Streamlit logos ko hide kar dega
hide_streamlit_style = """
    <style>
    /* Purane menus aur footer hide karne ke liye */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Streamlit ka floating 'Manage app' / Viewer badge hide karne ke liye */
    [data-testid="stStatusWidget"] {visibility: hidden; display: none;}
    .viewerBadge_container__1QSob {visibility: hidden; display: none;}
    div[class*="viewerBadge"] {visibility: hidden; display: none;}
    #root header {visibility: hidden; display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Yeh HTML head mein manifest link inject karega
st.markdown(
    """
    <link rel="manifest" href="/app/static/manifest.json">
    """,
    unsafe_allow_html=True,
)

# Page Configuration
st.set_page_config(
    page_title="AI Financial Auditor & Fraud Detector", page_icon="📊", layout="wide"
)

st.title("📊 AI-Driven Financial Auditor & Fraud Detector for SMBs")
st.write(
    "Apni business ki monthly sales ya expense ki CSV file upload karein aur"
    " instant automated audit report payein."
)

# File Uploader
uploaded_file = st.file_uploader(
    "Upload your CSV file here", type=["csv"]
)

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)

  st.subheader("📁 Uploaded Financial Data Preview:")
  st.dataframe(df.head(10))

  columns = df.columns.tolist()

  # Target Column (Amount/Price) dhoondna
  target_col = None
  for col in ["Amount", "unit_price", "Price", "Total"]:
    if col in columns:
      target_col = col
      break

  if target_col:
    # Key Financial Metrics
    total_amount = df[target_col].sum()
    total_transactions = len(df)
    avg_transaction = df[target_col].mean()

    st.subheader("💡 Key Financial Metrics Overview:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_transactions)
    col2.metric("Total Value", f"₹{total_amount:,.2f}")
    col3.metric("Avg Transaction", f"₹{avg_transaction:,.2f}")

    # --- FRAUD & ANOMALY DETECTION LOGIC ---
    st.subheader("🚨 Fraud & Anomaly Audit Report:")

    threshold = avg_transaction * 3
    suspicious_df = df[df[target_col] > threshold]

    if not suspicious_df.empty:
      st.error(
          f"⚠️ Alert: {len(suspicious_df)} aisi transactions mili hain jo normal"
          " average se 3x zyada hain aur suspicious ho sakti hain!"
      )
      st.dataframe(suspicious_df)
    else:
      st.success(
          "✅ Sab theek hai! Koi bhi badi unusual ya suspicious transaction nahi"
          " mili."
      )

    # --- CATEGORY ANALYSIS ---
    cat_col = None
    for c in ["Category", "product_category", "Department"]:
      if c in columns:
        cat_col = c
        break

    if cat_col:
      st.subheader(f"📈 Category-wise Breakdown (using {cat_col}):")
      category_summary = df.groupby(cat_col)[target_col].sum()
      st.bar_chart(category_summary)

    # --- AI AUDIT RECOMMENDATION ---
    st.subheader("🤖 AI Auditor Summary & Recommendations:")
    if total_amount > 500000:
      st.warning(
          "💡 **ABHI Dixit Audit Tip:** Transaction volume kaafi high hai. Tax"
          " compliance aur internal control audit karwana zaroori hai."
      )
    else:
      st.info(
          "💡 **ABHI Dixit Audit Tip:** Cash flow stable lag raha hai. Operational"
          " efficiency banaye rakhein."
      )

    # --- DOWNLOAD AUDIT REPORT BUTTON ---
    st.subheader("📥 Export Audit Report:")


    # Function to create a simple text/CSV report for download
    def generate_report():
      report_text = f"""--- AI FINANCIAL AUDITOR REPORT ---
Total Transactions: {total_transactions}
Total Value: ₹{total_amount:,.2f}
Average Transaction: ₹{avg_transaction:,.2f}
Suspicious Transactions Found: {len(suspicious_df)}
Status: {'Risk Detected' if not suspicious_df.empty else 'Safe'}
-----------------------------------
"""
      return report_text


    st.download_button(
        label="Download Audit Summary Report",
        data=generate_report(),
        file_name="AI_Financial_Audit_Report.txt",
        mime="text/plain",
    )

  else:
    st.warning(
        "⚠️ Aapki file mein koi 'Amount' ya 'unit_price' jaisa column nahi mila."
        " Kripya check karein."
    )