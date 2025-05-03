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
  
Made with ❤️ by [Your Name]

</div> 