import streamlit as st
from trust_core import compute_trust_score, users_df

st.set_page_config(page_title="Digital Identity Trust Score", layout="centered")

st.title("🔐 Digital Identity Trust Checker")
st.markdown("Enter a `user_id` to get a risk-based trust score.")

user_id = st.selectbox("Select User ID", sorted(users_df['user_id'].unique()))

if st.button("Check Trust Score"):
    score = compute_trust_score(user_id)
    st.metric(label="Trust Score", value=f"{score:.2f}")

    if score < 0.4:
        st.error("⚠️ High Risk: Likely Synthetic Identity")
    elif score < 0.7:
        st.warning("🧐 Medium Risk: Needs Review")
    else:
        st.success("Low Risk")
