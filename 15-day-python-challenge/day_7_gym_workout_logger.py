"""
Gym Workout Logger - Enterprise Edition
========================================
Day 7 of 15 Days Python Challenge

A production-grade workout tracking application built with Streamlit.
Features modular architecture, data validation, and analytics capabilities.

Author: Mohamed Uvais
Date: November 20, 2025
"""

# =============================================================================
# IMPORTS
# =============================================================================
import streamlit as st
import pandas as pd
from dataclasses import dataclass, asdict
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import plotly.express as px

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

class AppConfig:
    """Application configuration constants."""
    APP_TITLE = "Gym Workout Logger"
    APP_ICON = "💪"
    PAGE_LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Data validation constraints
    MIN_WEIGHT = 0.1
    MAX_WEIGHT = 500.0
    MIN_SETS = 1
    MAX_SETS = 50
    MIN_REPS = 1
    MAX_REPS = 500
    
    # UI Constants
    DATE_FORMAT = "%Y-%m-%d"
    CHART_HEIGHT = 400


# =============================================================================
# EXERCISE LIBRARY
# =============================================================================

EXERCISE_LIST = [
    # Chest
    "Bench Press", "Incline Bench Press", "Chest Fly",
    # Back
    "Deadlift", "Lat Pulldown", "Seated Cable Row",
    # Shoulders
    "Overhead Press", "Lateral Raises", "Rear Delt Fly",
    # Biceps
    "Barbell Curl", "Hammer Curl",
    # Triceps
    "Tricep Pushdown", "Dips",
    # Legs
    "Squats", "Leg Press", "Lunges", "Romanian Deadlift",
    "Hip Thrust", "Leg Curl",
    # Core
    "Plank", "Crunches", "Leg Raises",
    # Compound
    "Kettlebell Swing", "Clean and Press", "Farmer's Walk"
]


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class WorkoutEntry:
    """
    Data model representing a single workout entry.
    
    Attributes:
        exercise_name: Name of the exercise performed
        sets: Number of sets completed
        reps: Number of repetitions per set
        weight_kg: Weight used in kilograms
        workout_date: Date when workout was performed
        entry_id: Unique identifier for the entry
    """
    exercise_name: str
    sets: int
    reps: int
    weight_kg: float
    workout_date: date
    entry_id: Optional[str] = None
    
    def __post_init__(self):
        """Generate unique ID if not provided."""
        if self.entry_id is None:
            self.entry_id = f"{self.workout_date}_{self.exercise_name}_{datetime.now().timestamp()}"
    
    def calculate_volume(self) -> float:
        """
        Calculate total workout volume.
        
        Volume = Sets × Reps × Weight
        
        Returns:
            float: Total workout volume in kg
        """
        return self.sets * self.reps * self.weight_kg
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary for DataFrame operations."""
        data = asdict(self)
        data['volume_kg'] = self.calculate_volume()
        return data


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def initialize_session_state() -> None:
    """
    Initialize Streamlit session state with default values.
    
    This function ensures all required state variables exist before
    the application logic runs, preventing KeyError exceptions.
    """
    if 'workout_entries' not in st.session_state:
        st.session_state.workout_entries = []
    
    if 'entry_counter' not in st.session_state:
        st.session_state.entry_counter = 0


# =============================================================================
# DATA VALIDATION
# =============================================================================

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_workout_entry(
    exercise_name: str,
    sets: int,
    reps: int,
    weight_kg: float
) -> tuple[bool, Optional[str]]:
    """
    Validate workout entry inputs against business rules.
    
    Args:
        exercise_name: Name of exercise
        sets: Number of sets
        reps: Number of reps
        weight_kg: Weight in kilograms
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Exercise name validation (now always valid from dropdown)
    if not exercise_name or exercise_name.strip() == "":
        return False, "Exercise name is required"
    
    # Sets validation
    if sets < AppConfig.MIN_SETS or sets > AppConfig.MAX_SETS:
        return False, f"Sets must be between {AppConfig.MIN_SETS} and {AppConfig.MAX_SETS}"
    
    # Reps validation
    if reps < AppConfig.MIN_REPS or reps > AppConfig.MAX_REPS:
        return False, f"Reps must be between {AppConfig.MIN_REPS} and {AppConfig.MAX_REPS}"
    
    # Weight validation
    if weight_kg < AppConfig.MIN_WEIGHT or weight_kg > AppConfig.MAX_WEIGHT:
        return False, f"Weight must be between {AppConfig.MIN_WEIGHT} and {AppConfig.MAX_WEIGHT} kg"
    
    return True, None


# =============================================================================
# BUSINESS LOGIC
# =============================================================================

def add_workout_entry(entry: WorkoutEntry) -> None:
    """
    Add a new workout entry to the session state.
    
    Args:
        entry: WorkoutEntry object to add
    """
    st.session_state.workout_entries.append(entry)
    st.session_state.entry_counter += 1


def get_workout_dataframe() -> pd.DataFrame:
    """
    Convert workout entries to pandas DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing all workout entries
    """
    if not st.session_state.workout_entries:
        return pd.DataFrame(columns=[
            'workout_date', 'exercise_name', 'sets', 'reps', 
            'weight_kg', 'volume_kg'
        ])
    
    data = [entry.to_dict() for entry in st.session_state.workout_entries]
    df = pd.DataFrame(data)
    
    # Ensure proper data types
    df['workout_date'] = pd.to_datetime(df['workout_date']).dt.date
    df['volume_kg'] = df['volume_kg'].round(2)
    
    # Sort by date descending
    df = df.sort_values('workout_date', ascending=False)
    
    return df[['workout_date', 'exercise_name', 'sets', 'reps', 'weight_kg', 'volume_kg']]


def calculate_weekly_volume() -> pd.DataFrame:
    """
    Calculate total workout volume aggregated by day for the past 7 days.
    
    Returns:
        pd.DataFrame: DataFrame with date and total daily volume
    """
    df = get_workout_dataframe()
    
    if df.empty:
        return pd.DataFrame(columns=['workout_date', 'total_volume_kg'])
    
    # Get last 7 days
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    # Filter to last 7 days
    df_filtered = df[df['workout_date'] >= week_ago].copy()
    
    # Group by date and sum volume
    weekly_volume = df_filtered.groupby('workout_date')['volume_kg'].sum().reset_index()
    weekly_volume.columns = ['workout_date', 'total_volume_kg']
    
    # Fill missing dates with zero volume
    date_range = pd.date_range(start=week_ago, end=today, freq='D')
    all_dates = pd.DataFrame({'workout_date': date_range.date})
    
    weekly_volume = all_dates.merge(weekly_volume, on='workout_date', how='left')
    weekly_volume['total_volume_kg'] = weekly_volume['total_volume_kg'].fillna(0)
    
    return weekly_volume.sort_values('workout_date')


def delete_workout_entry(entry_id: str) -> None:
    """
    Remove a workout entry by its ID.
    
    Args:
        entry_id: Unique identifier of the entry to delete
    """
    st.session_state.workout_entries = [
        entry for entry in st.session_state.workout_entries 
        if entry.entry_id != entry_id
    ]


def clear_all_entries() -> None:
    """Clear all workout entries from session state."""
    st.session_state.workout_entries = []
    st.session_state.entry_counter = 0


# =============================================================================
# DATA EXPORT
# =============================================================================

def export_to_csv(df: pd.DataFrame) -> str:
    """
    Export DataFrame to CSV string.
    
    Args:
        df: DataFrame to export
        
    Returns:
        str: CSV formatted string
    """
    return df.to_csv(index=False).encode('utf-8')


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_header() -> None:
    """Render application header with title and description."""
    st.title(f"{AppConfig.APP_ICON} {AppConfig.APP_TITLE}")
    st.markdown("""
    Track your gym workouts with precision. Log exercises, monitor volume, 
    and analyze weekly progress with enterprise-grade data management.
    """)
    st.divider()


def render_input_form() -> None:
    """
    Render workout entry input form.
    
    Handles user input validation and entry creation.
    """
    st.subheader("📝 Log New Workout")
    
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1.5])
        
        with col1:
            exercise_name = st.selectbox(
                "Exercise Name",
                options=EXERCISE_LIST,
                index=0,
                key="input_exercise"
            )
        
        with col2:
            sets = st.number_input(
                "Sets",
                min_value=AppConfig.MIN_SETS,
                max_value=AppConfig.MAX_SETS,
                value=3,
                step=1,
                key="input_sets"
            )
        
        with col3:
            reps = st.number_input(
                "Reps",
                min_value=AppConfig.MIN_REPS,
                max_value=AppConfig.MAX_REPS,
                value=10,
                step=1,
                key="input_reps"
            )
        
        with col4:
            weight_kg = st.number_input(
                "Weight (kg)",
                min_value=AppConfig.MIN_WEIGHT,
                max_value=AppConfig.MAX_WEIGHT,
                value=50.0,
                step=2.5,
                format="%.1f",
                key="input_weight"
            )
        
        with col5:
            workout_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today(),
                key="input_date"
            )
    
    # Submit button
    col_submit, col_clear = st.columns([1, 5])
    
    with col_submit:
        submit_button = st.button("➕ Add Entry", type="primary", use_container_width=True)
    
    # Handle form submission
    if submit_button:
        is_valid, error_message = validate_workout_entry(
            exercise_name, sets, reps, weight_kg
        )
        
        if is_valid:
            entry = WorkoutEntry(
                exercise_name=exercise_name.strip(),
                sets=sets,
                reps=reps,
                weight_kg=weight_kg,
                workout_date=workout_date
            )
            add_workout_entry(entry)
            st.success(f"✅ Added {exercise_name} to workout log!")
            st.rerun()
        else:
            st.error(f"❌ Validation Error: {error_message}")


def render_workout_table() -> None:
    """
    Render the workout entries table with delete functionality.
    """
    st.subheader("📊 Workout History")
    
    df = get_workout_dataframe()
    
    if df.empty:
        st.info("No workout entries yet. Start logging your workouts above!")
        return
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", len(df))
    
    with col2:
        total_volume = df['volume_kg'].sum()
        st.metric("Total Volume", f"{total_volume:,.0f} kg")
    
    with col3:
        unique_exercises = df['exercise_name'].nunique()
        st.metric("Unique Exercises", unique_exercises)
    
    with col4:
        avg_volume = df['volume_kg'].mean()
        st.metric("Avg Volume/Entry", f"{avg_volume:,.0f} kg")
    
    st.divider()
    
    # Display table with improved formatting
    display_df = df.copy()
    display_df.columns = ['Date', 'Exercise', 'Sets', 'Reps', 'Weight (kg)', 'Volume (kg)']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "Weight (kg)": st.column_config.NumberColumn("Weight (kg)", format="%.1f"),
            "Volume (kg)": st.column_config.NumberColumn("Volume (kg)", format="%.1f"),
        }
    )
    
    # Action buttons
    col_delete, col_export, col_spacer = st.columns([1, 1, 3])
    
    with col_delete:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.get('confirm_delete', False):
                clear_all_entries()
                st.session_state.confirm_delete = False
                st.success("All data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("Click again to confirm deletion")
    
    with col_export:
        csv = export_to_csv(df)
        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name=f"workout_log_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )


def render_weekly_analytics() -> None:
    """
    Render weekly progress analytics with volume chart.
    """
    st.subheader("📈 Weekly Progress")
    
    weekly_data = calculate_weekly_volume()
    
    if weekly_data.empty or weekly_data['total_volume_kg'].sum() == 0:
        st.info("Complete some workouts to see weekly analytics!")
        return
    
    # Create bar chart using Plotly
    fig = px.bar(
        weekly_data,
        x='workout_date',
        y='total_volume_kg',
        labels={
            'workout_date': 'Date',
            'total_volume_kg': 'Total Volume (kg)'
        },
        title='Daily Workout Volume - Last 7 Days',
        text='total_volume_kg'
    )
    
    # Customize chart appearance
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textposition='outside',
        marker_color='#1f77b4'
    )
    
    fig.update_layout(
        height=AppConfig.CHART_HEIGHT,
        showlegend=False,
        xaxis_title="Date",
        yaxis_title="Volume (kg)",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly summary metrics
    total_weekly_volume = weekly_data['total_volume_kg'].sum()
    workout_days = (weekly_data['total_volume_kg'] > 0).sum()
    avg_daily_volume = total_weekly_volume / 7 if workout_days > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Weekly Volume", f"{total_weekly_volume:,.0f} kg")
    
    with col2:
        st.metric("Workout Days", f"{workout_days} days")
    
    with col3:
        st.metric("Avg Daily Volume", f"{avg_daily_volume:,.0f} kg")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main() -> None:
    """
    Main application entry point.
    
    Orchestrates the entire application flow:
    1. Configure page settings
    2. Initialize session state
    3. Render UI components
    """
    # Page configuration
    st.set_page_config(
        page_title=AppConfig.APP_TITLE,
        page_icon=AppConfig.APP_ICON,
        layout=AppConfig.PAGE_LAYOUT,
        initial_sidebar_state=AppConfig.INITIAL_SIDEBAR_STATE
    )
    
    # Initialize state
    initialize_session_state()
    
    # Render UI components
    render_header()
    render_input_form()
    
    st.divider()
    
    render_workout_table()
    
    st.divider()
    
    render_weekly_analytics()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
        "Day 7 - 15 Days Python Challenge | Enterprise Gym Workout Logger | "
        "Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
