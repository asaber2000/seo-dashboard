import streamlit as st
import boto3
import pandas as pd

# 1. إعداد الصفحة وتصميمها
st.set_page_config(page_title="Ahmed's SEO Dashboard", layout="wide")
st.title("🚀 Real-Time Cloud-Automated SEO Dashboard")
st.write("Live System Status: Data synchronized via AWS Cloud infrastructure ( AWS DynamoDB & RDS ).")

# 2. جلب البيانات من DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Backlinks') # اسم جدولك

def get_data():
    response = table.scan()
    return response['Items']

data = get_data()
df = pd.DataFrame(data)

# 3. عرض إحصائيات سريعة (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Total Backlinks", len(df))
if 'Status' in df.columns:
    live_filter = df['Status'].str.contains('Live|Done|yes', case=False, na=False)
    live_count = len(df[live_filter])
    col2.metric("Live Backlinks ✅", live_count)
    col3.metric("Broken Links ❌", len(df) - live_count)

# 4. عرض الجدول التفاعلي
st.subheader("🔗 All Backlinks Details")
# 1. قائمة الأعمدة اللي إحنا عاوزينها بالترتيب
# 1. قائمة الأعمدة بالترتيب (تأكد من كتابة status بنفس حالة الأحرف في ملفك)
desired_columns = ['LinkID', 'URL', 'DA', 'DR', 'Traffic', 'Country', 'SpamScore', 'Status']

# 2. التأكد من وجود الأعمدة في الملف لتجنب الأخطاء
existing_columns = [col for col in desired_columns if col in df.columns]

# 3. تفعيل عرض الصفحة بالكامل (Wide Mode) وإظهار الـ Scroll
st.dataframe(
    df[existing_columns], 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "URL": st.column_config.LinkColumn("URL", width="medium"),
        "status": st.column_config.TextColumn("Status", width="small")
    }
)
# 5. زر للتحديث
if st.button('🔄 Refresh Data'):
    st.rerun()
