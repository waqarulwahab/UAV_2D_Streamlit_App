# 🚀 Real-Time Drone Signal Detection and Classification

<div align="center">
  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

</div>

## 📋 Overview

A real-time simulation system for detecting and classifying drone signal anomalies using machine learning. This application provides a visual interface to monitor and analyze potential signal attacks (spoofing and jamming) in real-time.

## ✨ Features

- 🎯 Real-time signal anomaly detection
- 📊 Interactive visualization of drone path and signal patterns
- 🚨 Detection of two types of attacks:
  - Spoofing attacks (signal manipulation)
  - Jamming attacks (signal interference)
- 🎮 Adjustable simulation parameters:
  - Anomaly detection threshold
  - Attack probability
  - Simulation speed
  - Marker lifetime
- 🎨 Multiple theme options for visualization
- 📈 Real-time statistics and event logging

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/drone-signal-detection.git
cd drone-signal-detection
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. In the web interface:
   - Adjust the anomaly threshold and attack probability using the sliders
   - Click "Start Simulation" to begin
   - Monitor the real-time visualization and statistics
   - Use "Reset Simulation" to clear the data and start fresh

## 📊 Visualization Features

- **Planned Path**: Blue line showing the intended drone path
- **Drone Position**: Green dot indicating current position
- **Normal Signals**: Green markers for normal operation
- **Spoofing Attacks**: Red X markers with dashed lines
- **Jamming Attacks**: Yellow star markers
- **Real-time Statistics**: Count of different signal types
- **Event Log**: Timestamped log of all detected events

## 🧠 Machine Learning Models

The system uses two pre-trained models:
1. **Isolation Forest**: For anomaly detection
2. **Random Forest**: For attack classification

## 🔍 System Logic and Implementation Details

### Core Components

1. **Signal Generation and Processing**
   - Generates random samples using normal distribution for drone signals
   - Processes 35 different signal features including noise, velocity, position, and satellite data
   - Updates drone position along a predefined path

2. **Anomaly Detection System**
   - Uses Isolation Forest model to detect abnormal signal patterns
   - Anomaly threshold can be adjusted via slider (0.0 to 10.0)
   - Lower threshold values make the system more sensitive to anomalies
   - Anomaly scores are compared against the negative threshold value

3. **Attack Classification**
   - When an anomaly is detected, the Random Forest classifies it as either:
     - Spoofing Attack (0): Signal manipulation causing path deviation
     - Jamming Attack (1): Signal interference causing position freezing
   - Attack probability slider (0.0 to 1.0) controls the likelihood of attacks
   - When set to 0, no attacks are generated regardless of anomaly detection

4. **Visualization System**
   - Real-time plotting of drone path and signal patterns
   - Color-coded markers for different signal types:
     - Green: Normal signals
     - Red X: Spoofing attacks with dashed path
     - Yellow Star: Jamming attacks
   - Blue line shows planned path
   - Green dot indicates current drone position

5. **Data Management**
   - Maintains a rolling log of signal data
   - Implements marker lifetime system to remove old data points
   - Tracks statistics for different signal types
   - Provides real-time event logging

6. **Simulation Control**
   - Start button initiates the simulation
   - Reset button clears all data and statistics
   - Simulation speed controls the update frequency
   - Theme selection for visualization customization

### Technical Implementation

1. **State Management**
   - Uses Streamlit's session state to maintain simulation state
   - Tracks: simulation running status, data log, attack counts, drone position
   - Preserves visualization settings and theme preferences

2. **Real-time Processing**
   - Continuous loop for signal generation and processing
   - Time-based updates controlled by simulation speed
   - Asynchronous visualization updates

3. **Data Structures**
   - Pandas DataFrames for signal data management
   - Dictionary-based attack count tracking
   - List-based event logging with timestamping

4. **Visualization Pipeline**
   - Plotly for interactive plotting
   - Dynamic figure updates based on real-time data
   - Customizable themes and marker styles
   - Responsive layout with container-based updates

## 🎨 Customization

You can customize the visualization by:
- Changing the plot theme
- Adjusting the simulation speed
- Modifying the marker lifetime
- Fine-tuning the anomaly threshold
- Controlling the attack probability

## 📝 Requirements

- Python 3.8+
- Streamlit
- NumPy
- Pandas
- Plotly
- scikit-learn

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped with this project
- Special thanks to the open-source community for the amazing tools and libraries

---

<div align="center">
  
Made with ❤️ by WAQAR UL WAHAB

</div> 