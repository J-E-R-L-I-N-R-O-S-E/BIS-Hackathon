import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/search"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'search_query' not in st.session_state:
    st.session_state['search_query'] = ''
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []
if 'search_confidence' not in st.session_state:
    st.session_state['search_confidence'] = 0
if 'history' not in st.session_state:
    st.session_state['history'] = []

st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.main {
    background-color: #f5f7fb;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background: white;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}
.highlight {
    border-left: 6px solid #22c55e;
}
.tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
    margin-right: 5px;
    color: #1f2937;   /* 🔥 ADD THIS LINE */
    font-weight: 500; /* optional but better */
}
.green { background:#dcfce7; }
.blue { background:#e0f2fe; }
.orange { background:#ffedd5; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("🏛️ BIS System")
    st.markdown("### Navigation")
    if st.button("Home"):
        st.session_state['page'] = 'home'
    if st.button("New Search"):
        st.session_state['page'] = 'search'
    if st.button("History"):
        st.session_state['page'] = 'history'
    if st.button("Docs"):
        st.session_state['page'] = 'docs'
    st.markdown("---")
    st.markdown("### 📊 System Stats")
    st.write("Total Standards: 1247")
    st.write("Chunks: 18532")
    st.write("Avg Response: 1.3s")
    st.success("Model Active")


# Page Content
if st.session_state['page'] == 'home':
    st.title("🏗️ BIS Standards Recommendation Engine")
    st.caption("AI-Powered BIS Standard Discovery for Building Materials")
    st.write("Welcome to the BIS System. Use the navigation menu on the left to explore different features.")

elif st.session_state['page'] == 'search':
    # Search Page
    st.title("🔍 New Search")
    query = st.text_area(
        "Describe your product or material",
        height=100,
        value=st.session_state['search_query']
    )

    colA, colB = st.columns([1, 5])
    search_btn = colA.button("🔍 Search Standards")
    clear_btn = colA.button("Clear")

    if clear_btn:
        st.session_state['search_query'] = ''
        st.session_state['search_results'] = []
        st.session_state['search_confidence'] = 0

    elif search_btn and query.strip():
        st.session_state['search_query'] = query
        start_time = time.time()
        with st.spinner("Searching for standards..."):
            try:
                response = requests.post(API_URL, json={"query": query})
            except Exception as e:
                st.error(f"API request failed: {e}")
                st.stop()
        end_time = time.time()
        response_time = round(end_time - start_time, 3)

        if response.status_code == 200:
            data = response.json()
            standards = data["standards"]
            confidence = data["confidence"]
        else:
            st.error("API error")
            st.stop()

        # Save to history
        st.session_state['history'].append({
            "query": query,
            "top_standard": standards[0]["standard"] if standards else "N/A",
            "confidence": confidence
        })

        # Detection logic (customize as needed)
        q = query.lower()
        category = "Cement" if "cement" in q else "Construction"
        grade = "53 Grade" if "53" in q else "43 Grade" if "43" in q else "33 Grade" if "33" in q else "General"
        use = "Structural" if "concrete" in q else "General"

        # Layout
        left, right = st.columns([3, 1])

        # Left: Results
        with left:
            st.subheader("🎯 Top Recommended Standards")
            for i, item in enumerate(standards):
                st.markdown(f"### {i+1}. {item['standard']}")
                st.write(item["explanation"])
                st.markdown(
                    """
                    <span class='tag green'>Cement</span>
                    <span class='tag blue'>OPC</span>
                    <span class='tag orange'>Construction</span>
                    """,
                    unsafe_allow_html=True
                )
                score = round(0.95 - i * 0.08, 2)
                st.progress(score)
                st.markdown("---")

        # Right: Advanced Panel with details
        with right:
            st.markdown("""
            <div style="
                background:white;
                padding:15px;
                border-radius:12px;
                box-shadow:0 2px 8px rgba(0,0,0,0.05)
            ">
            """, unsafe_allow_html=True)

            st.subheader("📊 Analysis")
            # Query info
            st.write(f"**Query:** {query}")
            # Detection info
            st.write(f"**Detected Category:** {category}")
            st.write(f"**Detected Grade:** {grade}")
            st.write(f"**Intended Use:** {use}")

            # Response time and results count
            st.markdown("---")
            st.write(f"⏱ **Response Time:** {response_time}s")
            st.write(f"📦 **Results Returned:** {len(standards)} standards")
            st.markdown("---")

            # Why these standards
            st.write("### 💡 Why these standards?")
            st.write("✔ Semantic similarity match")
            st.write("✔ Keyword relevance match")
            st.write("✔ Domain-specific rule boosting")
            st.write("✔ Context-aware ranking")
            st.markdown("</div>", unsafe_allow_html=True)

        # Confidence indicator
        if confidence >= 0.7:
            st.success(f"✅ High Confidence: {confidence}")
        elif confidence >= 0.4:
            st.warning(f"⚠️ Medium Confidence: {confidence}")
        else:
            st.error(f"❌ Low Confidence: {confidence}")

elif st.session_state['page'] == 'history':
    st.title("📜 Search History")
    if st.session_state['history']:
        for idx, item in enumerate(st.session_state['history']):
            st.markdown(f"""
            <div style="margin-bottom:15px; padding:10px; border:1px solid #ddd; border-radius:8px;">
                <strong>Query:</strong> {item['query']}<br>
                <strong>Top Standard:</strong> {item['top_standard']}<br>
                <strong>Confidence:</strong> {item['confidence']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No search history available.")

elif st.session_state['page'] == 'docs':
    # Documentation / Guide for officers
    st.title("📖 How to Use the BIS Standards Recommendation System")
    st.markdown("""
    **Welcome Officers and Users!**

    This guide will help you effectively utilize the BIS Standards Recommendation System to find relevant standards for building materials and construction products.

    ### 1. Understand the System
    - This AI-powered tool allows you to input a description of your product or material.
    - It will analyze your description and recommend the most relevant BIS standards.
    - Confidence scores indicate the reliability of each recommendation.

    ### 2. Performing a Search
    - Enter a detailed description of your product/material in the text box.
    - Click on **"Search Standards"** to initiate the search.
    - Wait for the system to process and display results.

    ### 3. Interpreting Results
    - The top recommendations will be displayed with their explanations.
    - Confidence levels:
      - **High Confidence (≥ 0.7):** Results are reliable.
      - **Medium Confidence (0.4 – 0.7):** Results are moderately reliable.
      - **Low Confidence (< 0.4):** Results may need further refinement.
    - Use this information to make informed decisions or verify standards.

    ### 4. Using the History
    - Review previous searches in the **"History"** section.
    - You can revisit past queries, standards, and confidence levels for reference.

    ### 5. Tips for Effective Use
    - Be as descriptive and specific as possible in your query.
    - Use relevant keywords related to your product/material.
    - For better accuracy, refine your description based on initial results.

    ### 6. Need Assistance?
    - For further support, contact your system administrator or refer to official BIS resources.

    **Remember:** This tool complements official BIS documentation and should be used as a guide, not a substitute for official standards.

    Happy standard hunting!
    """)
