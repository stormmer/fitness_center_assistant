"""University of the Pacific theme colors and styling."""

# University of the Pacific Brand Colors
PACIFIC_ORANGE = "#F15A22"
PACIFIC_NAVY = "#002D62"
WHITE = "#FFFFFF"
GRAY = "#F5F7FA"
BLACK = "#000000"


def get_custom_css() -> str:
    """
    Get custom CSS for Streamlit app with Pacific theme.
    
    Returns:
        CSS string to inject via st.markdown
    """
    return f"""
    <style>
        /* Primary button styling */
        .stButton > button {{
            background-color: {PACIFIC_ORANGE};
            color: {WHITE};
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: background-color 0.3s;
        }}
        
        .stButton > button:hover {{
            background-color: #D14A1A;
            color: {WHITE};
        }}
        
        /* Header styling */
        h1, h2 {{
            color: {PACIFIC_NAVY};
            font-weight: 700;
        }}
        
        h3 {{
            color: {PACIFIC_NAVY};
            font-weight: 600;
        }}
        
        /* Card/container styling */
        .card {{
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 1.5rem;
            background-color: {WHITE};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background-color: {GRAY};
        }}
        
        /* Metric styling */
        [data-testid="stMetricValue"] {{
            color: {PACIFIC_ORANGE};
        }}
    </style>
    """

