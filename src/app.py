"""Streamlit dashboard for Fitness Center Assistant."""

import sys
from pathlib import Path

# Add project root to Python path for imports to work on Streamlit Cloud
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd
import tempfile

from src.data import plans, class_schedule, promo_codes
from src.logic.messaging import build_welcome
from src.logic.pricing import price_membership
from src.logic.schedule import day_classes, normalized_day
from src.logic.attendance import add_entry, summarize
from src.logic.export import export_text
from src.theme import get_custom_css, PACIFIC_ORANGE, PACIFIC_NAVY

# Page configuration
st.set_page_config(
    page_title="Fitness Assistant",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'attendance_store' not in st.session_state:
    st.session_state.attendance_store = {}

if 'schedule_notes' not in st.session_state:
    st.session_state.schedule_notes = {}


def load_logo():
    """Load and display Pacific logo in sidebar."""
    # Try multiple possible logo file names
    logo_paths = [
        Path("assets/pacific_logo.png"),
        Path("assets/UOP-Logo.jpg"),
        Path("assets/pacific_logo.jpg"),
    ]
    logo_found = False
    for logo_path in logo_paths:
        if logo_path.exists():
            st.sidebar.image(str(logo_path), use_container_width=True, alt="University of the Pacific")
            logo_found = True
            break
    if not logo_found:
        st.sidebar.markdown("### 🏋️ University of the Pacific")


# Sidebar navigation
load_logo()
st.sidebar.title("Fitness Center Assistant")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Pricing Calculator", "Class Schedule", "Attendance", "Summary & Export"],
    label_visibility="collapsed"
)

# Main content area
if page == "Home":
    st.title("🏋️ Welcome to Fitness Center Assistant")
    st.markdown("---")
    
    st.markdown(f"""
    ### Welcome to Baun Fitness Center!
    
    This assistant helps you with:
    - **Personalized greetings** and class reminders
    - **Membership pricing** with discounts and promo codes
    - **Attendance tracking** and summaries
    - **Session summaries** for export
    
    Use the sidebar to navigate to different sections.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("💳 **Pricing Calculator**\n\nCalculate membership costs with discounts")
    with col2:
        st.info("📅 **Class Schedule**\n\nView classes by day of the week")
    with col3:
        st.info("📊 **Attendance**\n\nTrack and visualize attendance data")

elif page == "Pricing Calculator":
    st.title("💳 Membership Pricing Calculator")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        plan = st.selectbox("Select Membership Plan", list(plans.keys()))
        months = st.number_input("Number of Months", min_value=1, value=1, step=1)
        is_student_or_staff = st.checkbox("Student or Staff Member (15% discount)")
        promo = st.text_input("Promo Code (optional)", placeholder="e.g., WELCOME10")
    
    with col2:
        st.markdown("### Pricing Information")
        st.info(f"""
        **Available Plans:**
        - Basic: ${plans['Basic']:.2f}/month
        - Plus: ${plans['Plus']:.2f}/month
        - Premium: ${plans['Premium']:.2f}/month
        
        **Available Promo Codes:**
        - WELCOME10: 10% off
        - FALL5: 5% off
        """)
    
    if st.button("Calculate Price", type="primary"):
        try:
            breakdown = price_membership(
                plan=plan,
                months=months,
                is_student_or_staff=is_student_or_staff,
                promo=promo if promo else None,
                plans=plans,
                promo_codes=promo_codes
            )
            
            # Display breakdown in a styled container
            st.markdown("---")
            st.markdown("### Pricing Breakdown")
            
            breakdown_html = f"""
            <div style="border: 2px solid {PACIFIC_NAVY}; border-radius: 8px; padding: 1.5rem; background-color: #F5F7FA;">
                <p><strong>Plan:</strong> {breakdown['plan']}</p>
                <p><strong>Duration:</strong> {breakdown['months']} month(s)</p>
                <p><strong>Monthly Price:</strong> ${breakdown['monthly_price']:,.2f}</p>
                <p><strong>Base Cost:</strong> ${breakdown['base_cost']:,.2f}</p>
            """
            
            if breakdown['student_staff_discount'] > 0:
                breakdown_html += f"<p><strong>Student/Staff Discount (15%):</strong> -${breakdown['student_staff_discount']:,.2f}</p>"
            
            if breakdown['promo_applied']:
                promo_discount = breakdown['base_cost'] * breakdown['promo_rate']
                breakdown_html += f"<p><strong>Promo Code ({breakdown['promo_applied']}):</strong> -${promo_discount:,.2f}</p>"
            elif promo:
                breakdown_html += "<p style='color: red;'><strong>⚠️ Invalid promo code - not applied</strong></p>"
            
            breakdown_html += f"""
                <hr style="border-color: {PACIFIC_NAVY};">
                <h2 style="color: {PACIFIC_ORANGE}; margin-top: 1rem;">
                    Final Cost: ${breakdown['final_cost']:,.2f}
                </h2>
            </div>
            """
            
            st.markdown(breakdown_html, unsafe_allow_html=True)
            
        except ValueError as e:
            st.error(f"❌ Error: {e}")

elif page == "Class Schedule":
    st.title("📅 Class Schedule")
    st.markdown("---")
    
    day = st.selectbox(
        "Select Day of Week",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    
    day_normalized = normalized_day(day)
    classes = day_classes(day_normalized, class_schedule)
    
    if classes:
        st.markdown(f"### Classes on {day}")
        
        # Display classes in a table
        class_data = []
        for i, cls in enumerate(classes, 1):
            class_data.append({"#": i, "Class": cls})
        
        df = pd.DataFrame(class_data)
        st.table(df)
        
        # Custom note section
        st.markdown("---")
        st.markdown("### Add a Note")
        note_key = f"note_{day_normalized}"
        note = st.text_area(
            f"Add a note for {day}",
            value=st.session_state.schedule_notes.get(note_key, ""),
            key=note_key
        )
        st.session_state.schedule_notes[note_key] = note
        
        if note:
            st.info(f"📝 Note: {note}")
    else:
        st.info(f"No classes scheduled for {day}")

elif page == "Attendance":
    st.title("📊 Attendance Tracking")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        activity = st.text_input("Activity Name", placeholder="e.g., Yoga, Spin Class")
        count = st.number_input("Attendance Count", min_value=0, value=0, step=1)
        
        if st.button("Add Entry", type="primary"):
            if activity.strip():
                try:
                    add_entry(st.session_state.attendance_store, activity.strip(), count)
                    st.success(f"✓ Added {count} to {activity}")
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Activity name cannot be empty")
    
    with col2:
        if st.button("Clear All", type="secondary"):
            st.session_state.attendance_store = {}
            st.rerun()
    
    # Display attendance data
    if st.session_state.attendance_store:
        st.markdown("---")
        st.markdown("### Attendance Summary")
        
        summary = summarize(st.session_state.attendance_store)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Attendance", summary['total'])
        with col2:
            st.metric("Average per Activity", f"{summary['avg_per_activity']:.2f}")
        
        # Table
        st.markdown("#### By Activity")
        attendance_data = [
            {"Activity": activity, "Count": count}
            for activity, count in summary['by_activity'].items()
        ]
        df = pd.DataFrame(attendance_data)
        st.table(df)
        
        # Bar chart
        st.markdown("#### Attendance Chart")
        chart_df = pd.DataFrame({
            "Activity": list(summary['by_activity'].keys()),
            "Count": list(summary['by_activity'].values())
        })
        st.bar_chart(chart_df.set_index("Activity"))
    else:
        st.info("No attendance data yet. Add entries above to get started.")

elif page == "Summary & Export":
    st.title("📋 Summary & Export")
    st.markdown("---")
    
    # Get summary data
    summary = summarize(st.session_state.attendance_store)
    
    st.markdown("### Attendance Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Attendance", summary['total'])
    with col2:
        st.metric("Average per Activity", f"{summary['avg_per_activity']:.2f}")
    
    if summary['by_activity']:
        st.markdown("#### By Activity")
        summary_data = [
            {"Activity": activity, "Count": count}
            for activity, count in summary['by_activity'].items()
        ]
        st.table(pd.DataFrame(summary_data))
    else:
        st.info("No attendance data to summarize.")
    
    st.markdown("---")
    st.markdown("### Export Session Summary")
    
    # Build export content
    lines = [
        "="*60,
        "FITNESS CENTER SESSION SUMMARY",
        "="*60,
        f"Center: Baun Fitness Center",
        "",
        "ATTENDANCE SUMMARY:",
    ]
    
    if summary['by_activity']:
        lines.append(f"  Total Attendance: {summary['total']}")
        lines.append(f"  Average per Activity: {summary['avg_per_activity']:.2f}")
        lines.append("  By Activity:")
        for activity, count in summary['by_activity'].items():
            lines.append(f"    • {activity}: {count}")
    else:
        lines.append("  No attendance data recorded.")
    
    lines.append("")
    lines.append("="*60)
    
    export_content = "\n".join(lines)
    
    st.download_button(
        label="📥 Download Summary",
        data=export_content,
        file_name="fitness_session_summary.txt",
        mime="text/plain",
        type="primary"
    )

