import streamlit as st
import boto3
import pandas as pd

st.set_page_config(page_title="Ahmed's SEO Dashboard", layout="wide")
st.markdown("<style>.stDataFrame {border: 2px solid #4CAF50; border-radius: 10px;}</style>", unsafe_allow_html=True)
st.title("🚀 Real-Time Cloud-Automated SEO Dashboard")
st.write("Live System Status: Data synchronized via AWS Cloud infrastructure ( AWS DynamoDB & RDS ).")

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Backlinks') 

def get_data():
    response = table.scan()
    return response['Items']

data = get_data()
df = pd.DataFrame(data)

col1, col2, col3 = st.columns(3)
col1.metric("Total Backlinks", len(df))
if 'Status' in df.columns:
    live_filter = df['Status'].str.contains('Live|Done|yes', case=False, na=False)
    live_count = len(df[live_filter])
    col2.metric("Live Backlinks ✅", live_count)
    col3.metric("Broken Links ❌", len(df) - live_count)

st.subheader("🔗 All Backlinks Details")
desired_columns = ['LinkID', 'URL', 'DA', 'DR', 'Traffic', 'Country', 'SpamScore', 'Status']

existing_columns = [col for col in desired_columns if col in df.columns]

st.dataframe(
    df[existing_columns], 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "status": st.column_config.SelectboxColumn(
            "Link Status",
            help="Show if the link is active or broken",
            width="small",
            options=[
                "🟢 Live", 
                "🔴 Broken", 
                "✅ done", 
                "❌ not work"
            ],
        ),
        "URL": st.column_config.LinkColumn("Destination URL", width="medium"),
        "DA": st.column_config.NumberColumn("DA", format="%d ✨"),
        "Traffic": st.column_config.NumberColumn("Traffic", format="%d 📈")
    }
)
# 5. زر للتحديث
if st.button('🔄 Refresh Data'):
    st.rerun()
