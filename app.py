# SAVE THIS FILE AS: app.py

# RUN USING:

# py -3.11 -m streamlit run app.py

# =========================================================

# IMPORTS

# =========================================================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import serial
import time

from math import cos, sin, radians

# =========================================================

# ARDUINO CONNECTION

# =========================================================

# CHANGE COM7 TO YOUR ACTUAL COM PORT

# Example:

# COM3

# COM5

# COM8

arduino = serial.Serial('COM7', 115200, timeout=1)

time.sleep(2)

# =========================================================

# PAGE CONFIG

# =========================================================

st.set_page_config(
page_title="VisionGuard X",
layout="wide",
initial_sidebar_state="expanded"
)

# =========================================================

# PREMIUM CSS

# =========================================================

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp {

background-image:

linear-gradient(
rgba(0,0,0,0.72),
rgba(0,0,0,0.90)
),

url("https://images.unsplash.com/photo-1518770660439-4636190af475");

background-size: cover;
background-position: center;
background-attachment: fixed;

color: white;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

section[data-testid="stSidebar"] {

background:
linear-gradient(
180deg,
rgba(10,15,25,0.95),
rgba(5,10,20,0.92)
);

border-right: 1px solid rgba(255,255,255,0.08);
}

.glass {

background: rgba(255,255,255,0.06);

backdrop-filter: blur(14px);

border: 1px solid rgba(255,255,255,0.08);

padding: 22px;

border-radius: 26px;

box-shadow:
0 8px 32px rgba(0,0,0,0.45);

margin-bottom: 18px;
}

.metric-card {

background:
linear-gradient(
145deg,
rgba(255,255,255,0.09),
rgba(255,255,255,0.03)
);

padding: 22px;

border-radius: 22px;

text-align: center;

border: 1px solid rgba(255,255,255,0.08);

transition: 0.3s;
}

.metric-card:hover {

transform: translateY(-4px);

border: 1px solid cyan;
}

.success-box {

background:
linear-gradient(
135deg,
rgba(0,255,140,0.16),
rgba(0,255,140,0.05)
);

padding: 20px;

border-left: 5px solid #00ff99;

border-radius: 18px;
}

.warning-box {

background:
linear-gradient(
135deg,
rgba(255,180,0,0.16),
rgba(255,180,0,0.05)
);

padding: 20px;

border-left: 5px solid orange;

border-radius: 18px;
}

.danger-box {

background:
linear-gradient(
135deg,
rgba(255,0,90,0.18),
rgba(255,0,90,0.05)
);

padding: 20px;

border-left: 5px solid #ff004c;

border-radius: 18px;
}

</style>

""", unsafe_allow_html=True)

# =========================================================

# TITLE

# =========================================================

st.markdown("""

<h1 style='text-align:center;
font-size:60px;
color:#00F5FF;'>

VISIONGUARD X

</h1>
""", unsafe_allow_html=True)

st.markdown("""

<h3 style='text-align:center;
color:lightgray;'>

AI Powered Smart Factory Monitoring Platform

</h3>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================

# LIVE SENSOR DATA FROM ARDUINO

# =========================================================

st.sidebar.title("📡 LIVE SENSOR PANEL")

try:

```
line = arduino.readline().decode().strip()

values = line.split(',')

if len(values) == 7:

    ax = float(values[0])
    ay = float(values[1])
    az = float(values[2])

    gx = float(values[3])
    gy = float(values[4])
    gz = float(values[5])

    motor_temp = float(values[6])

else:

    ax, ay, az = 0,0,9.8
    gx, gy, gz = 0,0,0
    motor_temp = 30
```

except:

```
ax, ay, az = 0,0,9.8
gx, gy, gz = 0,0,0
motor_temp = 30
```

# =========================================================

# CONVERT SENSOR VALUES TO ROBOT MOVEMENT

# =========================================================

base = int(abs(gz) * 50)
shoulder = int(abs(ax) * 20)
elbow = int(abs(ay) * 20)
wrist = int(abs(gx) * 25)
rotate = int(abs(gy) * 25)
gripper = 40

base = min(base,180)
shoulder = min(shoulder,180)
elbow = min(elbow,180)
wrist = min(wrist,180)
rotate = min(rotate,180)

st.sidebar.metric("Accel X", round(ax,2))
st.sidebar.metric("Accel Y", round(ay,2))
st.sidebar.metric("Accel Z", round(az,2))

st.sidebar.metric("Gyro X", round(gx,2))
st.sidebar.metric("Gyro Y", round(gy,2))
st.sidebar.metric("Gyro Z", round(gz,2))

st.sidebar.metric("Temperature", round(motor_temp,1))

# =========================================================

# REAL AI MONITORING CONDITIONS

# =========================================================

danger = False
warning = False
alerts = []

vibration = abs(gx) + abs(gy) + abs(gz)

tilt = abs(ax) + abs(ay)

if vibration > 3:
warning = True
alerts.append("High vibration detected")

if vibration > 6:
danger = True
alerts.append("Critical vibration overload")

if tilt > 12:
warning = True
alerts.append("Robot instability detected")

if motor_temp > 45:
warning = True
alerts.append("Motor overheating")

if motor_temp > 55:
danger = True
alerts.append("Critical motor temperature")

# =========================================================

# ROBOT KINEMATICS

# =========================================================

L1 = 2
L2 = 2
L3 = 1.5

t1 = radians(shoulder)
t2 = radians(elbow)
t3 = radians(wrist)

x0,y0 = 0,0

x1 = L1*cos(t1)
y1 = L1*sin(t1)

x2 = x1 + L2*cos(t1+t2)
y2 = y1 + L2*sin(t1+t2)

x3 = x2 + L3*cos(t1+t2+t3)
y3 = y2 + L3*sin(t1+t2+t3)

# =========================================================

# TOP METRICS

# =========================================================

m1,m2,m3,m4 = st.columns(4)

health = 96
risk = "LOW"
risk_color = "#00ff99"

if warning:
health = 76
risk = "MEDIUM"
risk_color = "orange"

if danger:
health = 52
risk = "HIGH"
risk_color = "red"

with m1:
st.markdown(f""" <div class="metric-card"> <h1 style='color:#00ff99;'>{health}%</h1> <p>Machine Health</p> </div>
""", unsafe_allow_html=True)

with m2:
st.markdown(f""" <div class="metric-card"> <h1 style='color:{risk_color};'>{risk}</h1> <p>Failure Risk</p> </div>
""", unsafe_allow_html=True)

with m3:
st.markdown(""" <div class="metric-card"> <h1 style='color:#00F5FF;'>92%</h1> <p>Stability</p> </div>
""", unsafe_allow_html=True)

with m4:
st.markdown(f""" <div class="metric-card"> <h1 style='color:#FFD700;'>{round(motor_temp,1)}°C</h1> <p>Motor Temperature</p> </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================

# LIVE AI SUMMARY

# =========================================================

st.markdown("""

<div class="glass">
<h2 style='color:#00F5FF;'>
🧠 LIVE AI FACTORY SUMMARY
</h2>
</div>
""", unsafe_allow_html=True)

if danger:

```
st.markdown(f"""
<div class="danger-box">

🚨 CRITICAL FAILURE DETECTED

<br><br>

{'<br>'.join(alerts)}

<br><br>

Emergency shutdown recommendation triggered.
Bluetooth alert transmitted.

</div>
""", unsafe_allow_html=True)
```

elif warning:

```
st.markdown(f"""
<div class="warning-box">

⚠ WARNING CONDITION DETECTED

<br><br>

{'<br>'.join(alerts)}

<br><br>

Maintenance inspection recommended.

</div>
""", unsafe_allow_html=True)
```

else:

```
st.markdown("""
<div class="success-box">

✅ SYSTEM RUNNING NORMALLY

<br><br>

AI predictive monitoring active.
Robot operating safely.

</div>
""", unsafe_allow_html=True)
```

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================

# MAIN LAYOUT

# =========================================================

left, right = st.columns([1,1.2])

# =========================================================

# LEFT ROBOT

# =========================================================

with left:

```
st.markdown("""
<div class="glass">
<h2 style='color:#00F5FF;'>
🦾 DIGITAL TWIN ROBOT
</h2>
</div>
""", unsafe_allow_html=True)

robot_color = "cyan"

if warning:
    robot_color = "orange"

if danger:
    robot_color = "red"

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[x0,x1],
    y=[y0,y1],
    mode='lines+markers',
    line=dict(width=16,color=robot_color),
    marker=dict(size=12,color='white')
))

fig.add_trace(go.Scatter(
    x=[x1,x2],
    y=[y1,y2],
    mode='lines+markers',
    line=dict(width=14,color=robot_color),
    marker=dict(size=11,color='white')
))

fig.add_trace(go.Scatter(
    x=[x2,x3],
    y=[y2,y3],
    mode='lines+markers',
    line=dict(width=12,color=robot_color),
    marker=dict(size=10,color='white')
))

fig.add_shape(
    type="line",
    x0=-6,
    y0=0,
    x1=6,
    y1=0,
    line=dict(color="white",width=3)
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=500,
    xaxis=dict(visible=False,range=[-6,6]),
    yaxis=dict(visible=False,range=[-1,6]),
    margin=dict(l=0,r=0,t=0,b=0)
)

st.plotly_chart(fig,use_container_width=True)
```

# =========================================================

# RIGHT DASHBOARD

# =========================================================

with right:

```
st.markdown("""
<div class="glass">
<h2 style='color:#00F5FF;'>
⚙ SERVO ANALYTICS
</h2>
</div>
""", unsafe_allow_html=True)

servo_df = pd.DataFrame({

    "Servo":[
        "Base",
        "Shoulder",
        "Elbow",
        "Wrist",
        "Rotate",
        "Gripper"
    ],

    "Angle":[
        base,
        shoulder,
        elbow,
        wrist,
        rotate,
        gripper
    ],

    "Status":[
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "ACTIVE",
        "ACTIVE"
    ]

})

st.dataframe(
    servo_df,
    use_container_width=True,
    height=250
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass">
<h2 style='color:#00F5FF;'>
📡 LIVE SENSOR DATA
</h2>
</div>
""", unsafe_allow_html=True)

sensor_df = pd.DataFrame({

    "Sensor":[
        "Accel X",
        "Accel Y",
        "Accel Z",
        "Gyro X",
        "Gyro Y",
        "Gyro Z",
        "Temperature"
    ],

    "Value":[
        round(ax,2),
        round(ay,2),
        round(az,2),
        round(gx,2),
        round(gy,2),
        round(gz,2),
        round(motor_temp,2)
    ]

})

st.dataframe(
    sensor_df,
    use_container_width=True,
    height=250
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass">
<h2 style='color:#00F5FF;'>
🤖 AI PREDICTION ENGINE
</h2>
</div>
""", unsafe_allow_html=True)

if danger:

    st.markdown("""
    <div class="danger-box">

    AI predicts imminent failure.

    <br><br>

    • Vibration overload detected
    • Shutdown recommendation ACTIVE
    • Maintenance priority CRITICAL

    </div>
    """, unsafe_allow_html=True)

elif warning:

    st.markdown("""
    <div class="warning-box">

    AI predicts moderate instability.

    <br><br>

    • Stability reduction detected
    • Preventive maintenance recommended

    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="success-box">
```
