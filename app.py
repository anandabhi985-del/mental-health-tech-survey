import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666666;
    margin-bottom: 25px;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e5e5;
}

.section-title {
    font-size: 28px;
    font-weight: 600;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOADING DATA
# =========================================================

df = pd.read_csv("survey.csv")


# =========================================================
# DATA CLEANING
# =========================================================

# Removing comments column
df.drop(
    "comments",
    axis=1,
    inplace=True,
    errors="ignore"
)

# Converting timestamp
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Removing invalid ages
df = df[
    (df["Age"] >= 18) &
    (df["Age"] <= 80)
]

# Cleaning gender
df["Gender"] = (
    df["Gender"]
    .fillna("Other")
    .str.lower()
)

df["Gender"] = df["Gender"].apply(
    lambda x:
    "Female"
    if "female" in x or "woman" in x
    else "Male"
    if "male" in x or "man" in x or "guy" in x
    else "Other"
)

# Filling missing self-employed values
df["self_employed"] = (
    df["self_employed"]
    .fillna("Unknown")
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧠 Mental Health Survey")

st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Filters")

# Gender
gender_options = [
    "All",
    "Male",
    "Female",
    "Other"
]

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)

# Country
country_options = (
    ["All"] +
    sorted(
        df["Country"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_country = st.sidebar.selectbox(
    "Country",
    country_options
)

# Treatment
treatment_options = (
    ["All"] +
    sorted(
        df["treatment"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_treatment = st.sidebar.selectbox(
    "Mental Health Treatment",
    treatment_options
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Use these filters to explore how mental health "
    "responses vary across different groups."
)


# =========================================================
# APPLYING FILTERS
# =========================================================

filtered_df = df.copy()

if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

if selected_treatment != "All":

    filtered_df = filtered_df[
        filtered_df["treatment"] == selected_treatment
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🧠 Mental Health in Tech Survey'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Exploring mental health attitudes and treatment-seeking '
    'behavior in the technology workplace'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# DASHBOARD SUMMARY
# =========================================================

st.header("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)


# Respondents
with col1:

    st.metric(
        "👥 Respondents",
        len(filtered_df)
    )


# Treatment
with col2:

    treatment_count = (
        filtered_df["treatment"] == "Yes"
    ).sum()

    st.metric(
        "🩺 Sought Treatment",
        treatment_count
    )


# Remote workers
with col3:

    remote_count = (
        filtered_df["remote_work"] == "Yes"
    ).sum()

    st.metric(
        "💻 Remote Workers",
        remote_count
    )


# Family history
with col4:

    family_count = (
        filtered_df["family_history"] == "Yes"
    ).sum()

    st.metric(
        "🧬 Family History",
        family_count
    )


st.divider()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Analysis",
        "💡 Key Findings",
        "📌 Recommendations",
        "📋 Dataset"
    ]
)


# =========================================================
# TAB 1 — ANALYSIS
# =========================================================

with tab1:

    st.header("📈 Data Analysis")


    # -----------------------------------------------------
    # AGE DISTRIBUTION
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        age_counts = (
            filtered_df["Age"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        age_counts.columns = [
            "Age",
            "Respondents"
        ]

        fig_age = px.bar(
            age_counts,
            x="Age",
            y="Respondents",
            title="Age Distribution"
        )

        fig_age.update_layout(
            xaxis_title="Age",
            yaxis_title="Number of Respondents"
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )


    # -----------------------------------------------------
    # GENDER DISTRIBUTION
    # -----------------------------------------------------

    with col2:

        gender_counts = (
            filtered_df["Gender"]
            .value_counts()
            .reset_index()
        )

        gender_counts.columns = [
            "Gender",
            "Respondents"
        ]

        fig_gender = px.bar(
            gender_counts,
            x="Gender",
            y="Respondents",
            title="Gender Distribution"
        )

        fig_gender.update_layout(
            xaxis_title="Gender",
            yaxis_title="Number of Respondents"
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )


    # -----------------------------------------------------
    # TREATMENT STATUS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        treatment_counts = (
            filtered_df["treatment"]
            .value_counts()
            .reset_index()
        )

        treatment_counts.columns = [
            "Treatment",
            "Respondents"
        ]

        fig_treatment = px.bar(
            treatment_counts,
            x="Treatment",
            y="Respondents",
            title="Mental Health Treatment Status"
        )

        st.plotly_chart(
            fig_treatment,
            use_container_width=True
        )


    # -----------------------------------------------------
    # TOP COUNTRIES
    # -----------------------------------------------------

    with col2:

        country_counts = (
            filtered_df["Country"]
            .value_counts()
            .head(10)
            .sort_values()
            .reset_index()
        )

        country_counts.columns = [
            "Country",
            "Respondents"
        ]

        fig_country = px.bar(
            country_counts,
            x="Respondents",
            y="Country",
            orientation="h",
            title="Top 10 Countries"
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )


    # -----------------------------------------------------
    # FAMILY HISTORY VS TREATMENT
    # -----------------------------------------------------

    family_treatment = pd.crosstab(
        filtered_df["family_history"],
        filtered_df["treatment"]
    ).reset_index()

    family_treatment.columns = [
        str(col)
        for col in family_treatment.columns
    ]

    fig_family = px.bar(
        family_treatment,
        x="family_history",
        y=[
            col for col in family_treatment.columns
            if col != "family_history"
        ],
        barmode="group",
        title="Family History vs Treatment"
    )

    st.plotly_chart(
        fig_family,
        use_container_width=True
    )


    # -----------------------------------------------------
    # REMOTE WORK VS TREATMENT
    # -----------------------------------------------------

    remote_treatment = pd.crosstab(
        filtered_df["remote_work"],
        filtered_df["treatment"]
    ).reset_index()

    remote_treatment.columns = [
        str(col)
        for col in remote_treatment.columns
    ]

    fig_remote = px.bar(
        remote_treatment,
        x="remote_work",
        y=[
            col for col in remote_treatment.columns
            if col != "remote_work"
        ],
        barmode="group",
        title="Remote Work vs Treatment"
    )

    st.plotly_chart(
        fig_remote,
        use_container_width=True
    )


    # -----------------------------------------------------
    # BENEFITS VS TREATMENT
    # -----------------------------------------------------

    benefits_treatment = pd.crosstab(
        filtered_df["benefits"],
        filtered_df["treatment"]
    ).reset_index()

    benefits_treatment.columns = [
        str(col)
        for col in benefits_treatment.columns
    ]

    fig_benefits = px.bar(
        benefits_treatment,
        x="benefits",
        y=[
            col for col in benefits_treatment.columns
            if col != "benefits"
        ],
        barmode="group",
        title="Mental Health Benefits vs Treatment"
    )

    st.plotly_chart(
        fig_benefits,
        use_container_width=True
    )


# =========================================================
# TAB 2 — KEY FINDINGS
# =========================================================

with tab2:

    st.header("💡 Key Findings")

    st.markdown(
        """
        ### 1. Mental Health Treatment

        Treatment-seeking behavior varies among respondents,
        showing differences in how employees respond to mental
        health conditions.


        ### 2. Family History

        Family history of mental illness is an important factor
        associated with mental health treatment.


        ### 3. Workplace Support

        Workplace factors such as mental health benefits,
        wellness programs, and access to care can influence
        employees' experiences with mental health support.


        ### 4. Remote Work

        Remote work status provides another workplace dimension
        for examining differences in mental health treatment
        patterns.


        ### 5. Workplace Communication

        Employees may have different levels of comfort discussing
        mental health with coworkers, supervisors, and potential
        employers.
        """
    )


# =========================================================
# TAB 3 — RECOMMENDATIONS
# =========================================================

with tab3:

    st.header("📌 Business Recommendations")

    st.markdown(
        """
        ### 🩺 1. Improve Mental Health Benefits

        Organizations should provide clear and accessible mental
        health benefits and communicate these benefits effectively.


        ### 📢 2. Increase Mental Health Awareness

        Companies can conduct awareness programs and employee
        wellness initiatives to reduce hesitation around discussing
        mental health.


        ### 🔒 3. Provide Confidential Support

        Employees should have access to confidential mental health
        resources and understand how their privacy is protected.


        ### 👨‍💼 4. Train Managers and Supervisors

        Managers can be trained to respond appropriately when
        employees raise mental health concerns.


        ### 🤝 5. Create a Supportive Workplace

        Organizations can encourage an environment where employees
        feel comfortable discussing mental health concerns.
        """
    )


# =========================================================
# TAB 4 — DATASET
# =========================================================

with tab4:

    st.header("📋 Dataset Preview")

    st.write(
        f"Showing {min(10, len(filtered_df))} rows from "
        f"{len(filtered_df)} filtered respondents."
    )

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Mental Health in Tech Survey | Exploratory Data Analysis "
    "and Interactive Dashboard"
)