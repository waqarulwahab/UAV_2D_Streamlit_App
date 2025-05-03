import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import time
from datetime import datetime, timedelta

# Load models
with open("models/isolation_forest_if.pkl", "rb") as f:
    iso_forest = pickle.load(f)

with open("models/random_forest_model.pkl", "rb") as f:
    rf_classifier = pickle.load(f)

# Feature column names
feature_columns = [
    'noise_per_ms', 'eph', 'timestamp', 's_variance_m_s', 'epv', 'lat_x', 'epv_x', 'evh',
    'alt_ellipsoid_x', 'alt_ellipsoid_y', 'vel_m_s', 'satellites_used', 'hdop', 'vdop', 'y',
    'vel_d_m_s', 'delta_heading', 'c_variance_rad', 'vel_n_m_s', 'z', 'heading_y', 'vy', 'vx',
    'vel_e_m_s', 'q[2]', 'jamming_indicator', 'cog_rad', 'z_deriv', 'vz', 'ay', 'az', 'ax',
    'q[1]', 'terrain_alt_valid'
]

# Initialize session state
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'data_log' not in st.session_state:
    st.session_state.data_log = []
if 'attack_count' not in st.session_state:
    st.session_state.attack_count = {"Normal": 0, "Spoofing": 0, "Jamming": 0}
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []
if 'drone_position' not in st.session_state:
    st.session_state.drone_position = 0
if 'planned_path' not in st.session_state:
    # Create a planned path (a simple line from bottom-left to top-right)
    st.session_state.planned_path = [(0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.4, 0.4), 
                                    (0.5, 0.5), (0.6, 0.6), (0.7, 0.7), (0.8, 0.8), 
                                    (0.9, 0.9)]
if 'last_plot' not in st.session_state:
    st.session_state.last_plot = None

# Streamlit app layout
st.set_page_config(page_title="Real-Time Signal Simulation", layout="wide")
st.title("📡 Real-Time Signal Detection and Classification")

# Create columns for controls and stats
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.sidebar.title("Simulation Controls")
    anomaly_threshold = st.sidebar.slider("Anomaly Threshold", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    attack_probability = st.sidebar.slider("Attack Probability (Spoofing vs Jamming)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    
    # Time controls
    simulation_speed = st.sidebar.slider("Simulation Speed (seconds per step)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    marker_lifetime = st.sidebar.slider("Attack Marker Lifetime (seconds)", min_value=1, max_value=30, value=10, step=1)
    
    # Theme selection
    theme_options = {
        "Dark": "plotly_dark",
        "Light": "plotly_white",
        "Presentation": "presentation",
        "XGrid": "plotly",
        "YGrid": "ggplot2",
        "Minimal": "simple_white"
    }
    selected_theme = st.sidebar.selectbox("Plot Theme", options=list(theme_options.keys()), index=0)
    
    # Control buttons
    if st.sidebar.button("Start Simulation", key="start"):
        st.session_state.simulation_running = True
        st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] Simulation started")
    
    if st.sidebar.button("Reset Simulation", key="reset"):
        st.session_state.data_log = []
        st.session_state.attack_count = {"Normal": 0, "Spoofing": 0, "Jamming": 0}
        st.session_state.log_messages = []
        st.session_state.drone_position = 0
        st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] Simulation reset")

# Main content area
placeholder = st.empty()
stats_placeholder = st.empty()
log_placeholder = st.empty()

# Function to create the plot
def create_plot(df, planned_path_df, current_pos, theme="plotly_dark"):
    fig = go.Figure()

    # Add planned path (static blue line)
    fig.add_trace(go.Scatter(
        x=planned_path_df['x'],
        y=planned_path_df['y'],
        mode='lines',
        name='Planned Path',
        line=dict(color='blue', width=3),
        opacity=0.7
    ))

    # Add current drone position with highlighted green dot
    fig.add_trace(go.Scatter(
        x=[current_pos[0]],
        y=[current_pos[1]],
        mode='markers',
        name='Drone Position',
        marker=dict(
            size=20,
            color='green',
            symbol='circle',
            line=dict(color='white', width=2)
        ),
        opacity=0.8
    ))

    # Add normal path points
    normal_df = df[df['label'] == 'Normal']
    if not normal_df.empty:
        fig.add_trace(go.Scatter(
            x=normal_df['x'],
            y=normal_df['y'],
            mode='markers',
            name='Normal Signal',
            marker=dict(
                size=10,
                color='green',
                symbol='circle',
                opacity=0.6
            )
        ))

    # Add spoofing path points with connecting lines
    spoof_df = df[df['label'] == 'Spoofing']
    if not spoof_df.empty:
        # Add lines connecting spoofing points
        fig.add_trace(go.Scatter(
            x=spoof_df['x'],
            y=spoof_df['y'],
            mode='lines',
            name='Spoofed Path',
            line=dict(color='red', width=2, dash='dash'),
            opacity=0.5
        ))
        # Add spoofing markers
        fig.add_trace(go.Scatter(
            x=spoof_df['x'],
            y=spoof_df['y'],
            mode='markers',
            name='Spoofed Signal',
            marker=dict(
                size=15,
                color='red',
                symbol='x',
                line=dict(color='white', width=2)
            ),
            opacity=0.9
        ))

    # Add jamming points
    jam_df = df[df['label'] == 'Jamming']
    if not jam_df.empty:
        fig.add_trace(go.Scatter(
            x=jam_df['x'],
            y=jam_df['y'],
            mode='markers',
            name='Jamming',
            marker=dict(
                size=15,
                color='yellow',
                symbol='star',
                line=dict(color='white', width=2)
            ),
            opacity=0.9
        ))

    # Update layout
    fig.update_layout(
        title="Drone Path and Signal Visualization",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        showlegend=True,
        width=1000,
        height=600,
        template=theme,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Simulation loop
while True:
    if st.session_state.simulation_running:
        # Generate random sample based on attack probability
        sample = np.random.normal(loc=0.5, scale=0.2, size=(1, len(feature_columns)))
        
        # Create DataFrame with feature names
        sample_df = pd.DataFrame(sample, columns=feature_columns)

        # Update drone position along planned path
        st.session_state.drone_position = (st.session_state.drone_position + 1) % len(st.session_state.planned_path)
        current_pos = st.session_state.planned_path[st.session_state.drone_position]

        # Isolation Forest Prediction with adjusted threshold
        anomaly_score = iso_forest.score_samples(sample_df)
        
        # Adjust anomaly detection to be more sensitive to attacks
        # Lower threshold means more anomalies will be detected
        threshold = -anomaly_threshold  # Remove the 0.3 multiplier to make it more accurate
        
        # Only introduce attacks if attack_probability is greater than 0
        if attack_probability > 0 and np.random.random() < attack_probability:
            # Force an attack
            is_anomaly = True
        else:
            # Use normal anomaly detection
            is_anomaly = anomaly_score < threshold

        if not is_anomaly:
            label = "Normal"
            color = "green"
            # Normal movement - follow planned path
            actual_x, actual_y = current_pos
        else:
            # Predict type of attack (Spoofing or Jamming)
            attack = rf_classifier.predict(sample_df)[0]
            if attack == 0:
                label = "Spoofing"
                color = "red"
                # Spoofing - divert from planned path with larger deviation
                actual_x = current_pos[0] + np.random.normal(0, 0.3)  # Increased deviation
                actual_y = current_pos[1] + np.random.normal(0, 0.3)  # Increased deviation
            else:
                label = "Jamming"
                color = "yellow"
                # Jamming - stay at current position
                actual_x, actual_y = current_pos

        # Increment the counts for labels
        st.session_state.attack_count[label] += 1

        # Log sample data with timestamp
        point = {
            "x": actual_x,
            "y": actual_y,
            "planned_x": current_pos[0],
            "planned_y": current_pos[1],
            "label": label,
            "color": color,
            "timestamp": datetime.now(),
            "attack_count": st.session_state.attack_count.copy()
        }
        st.session_state.data_log.append(point)
        
        # Add log message
        st.session_state.log_messages.append(
            f"[{point['timestamp'].strftime('%H:%M:%S')}] Signal detected: {label} at coordinates ({point['x']:.2f}, {point['y']:.2f})"
        )

        # Remove old attack markers
        current_time = datetime.now()
        st.session_state.data_log = [
            point for point in st.session_state.data_log
            if (current_time - point['timestamp']).total_seconds() <= marker_lifetime  # Remove time limit for all points
        ]

        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.data_log)
        planned_path_df = pd.DataFrame(st.session_state.planned_path, columns=['x', 'y'])

        # Create the main plot
        fig = go.Figure()

        # Add planned path (static blue line)
        fig.add_trace(go.Scatter(
            x=planned_path_df['x'],
            y=planned_path_df['y'],
            mode='lines',
            name='Planned Path',
            line=dict(color='blue', width=3),
            opacity=0.7
        ))

        # Add current drone position with highlighted green dot
        fig.add_trace(go.Scatter(
            x=[current_pos[0]],
            y=[current_pos[1]],
            mode='markers',
            name='Drone Position',
            marker=dict(
                size=20,
                color='green',
                symbol='circle',
                line=dict(color='white', width=2)
            ),
            opacity=0.8
        ))

        # Add normal path points
        normal_df = df[df['label'] == 'Normal']
        if not normal_df.empty:
            fig.add_trace(go.Scatter(
                x=normal_df['x'],
                y=normal_df['y'],
                mode='markers',
                name='Normal Signal',
                marker=dict(
                    size=10,
                    color='green',
                    symbol='circle',
                    opacity=0.6
                )
            ))

        # Add spoofing path points with connecting lines
        spoof_df = df[df['label'] == 'Spoofing']
        if not spoof_df.empty:
            # Add lines connecting spoofing points
            fig.add_trace(go.Scatter(
                x=spoof_df['x'],
                y=spoof_df['y'],
                mode='lines',
                name='Spoofed Path',
                line=dict(color='red', width=2, dash='dash'),
                opacity=0.5
            ))
            # Add spoofing markers
            fig.add_trace(go.Scatter(
                x=spoof_df['x'],
                y=spoof_df['y'],
                mode='markers',
                name='Spoofed Signal',
                marker=dict(
                    size=15,
                    color='red',
                    symbol='x',
                    line=dict(color='white', width=2)
                ),
                opacity=0.9
            ))

        # Add jamming points
        jam_df = df[df['label'] == 'Jamming']
        if not jam_df.empty:
            fig.add_trace(go.Scatter(
                x=jam_df['x'],
                y=jam_df['y'],
                mode='markers',
                name='Jamming',
                marker=dict(
                    size=15,
                    color='yellow',
                    symbol='star',
                    line=dict(color='white', width=2)
                ),
                opacity=0.9
            ))

        # Update layout
        fig.update_layout(
            title="Drone Path and Signal Visualization",
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            showlegend=True,
            width=1000,
            height=600,
            template=theme_options[selected_theme],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Create and store the plot
        st.session_state.last_plot = fig

        # Display the plot
        placeholder.plotly_chart(fig, use_container_width=True, key=f"main_plot_{datetime.now().timestamp()}")

        # Display stats in a cleaner way
        with stats_placeholder.container():
            st.subheader("Attack Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Normal Signals", value=st.session_state.attack_count['Normal'])
            with col2:
                st.metric(label="Spoofing Attacks", value=st.session_state.attack_count['Spoofing'])
            with col3:
                st.metric(label="Jamming Attacks", value=st.session_state.attack_count['Jamming'])

        # Display logs in a cleaner way
        with log_placeholder.container():
            st.subheader("Event Log")
            for msg in st.session_state.log_messages[-10:]:  # Show last 10 messages
                st.text(msg)

        # Add a break in the loop based on simulation speed
        time.sleep(simulation_speed)
    else:
        # When simulation is stopped, show the last plot
        if st.session_state.last_plot is not None:
            placeholder.plotly_chart(st.session_state.last_plot, use_container_width=True, key=f"stopped_plot_{datetime.now().timestamp()}")
        time.sleep(0.1)  # Reduce CPU usage when simulation is stopped
