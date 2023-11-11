import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import cv2
from cvzone.PoseModule import PoseDetector
import queue
import numpy as np


st.set_page_config(
    page_title="push up counter",
    page_icon=":shark:",
    initial_sidebar_state="collapsed",
    layout="wide",
    menu_items={
        'Get Help': 'https://wa.me/6285536956301',
        'Report a bug': "https://wa.me/6285536956301"
    }
)

st.markdown("""
<style>
.big-font {
    font-size:200px !important;
}

.small-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)
detector = PoseDetector()
result_queue = queue.Queue()
def video_frame_callback(frame: av.VideoFrame)-> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
        # img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
    img = detector.findPose(img, draw= False)
    lmlst, bbox = detector.findPosition(img, draw=False)
    if lmlst:
        a1 = detector.findAngle(img, 12, 14, 16)
        a2 = detector.findAngle(img, 12, 24, 28)
        a3 = detector.findAngle(img, 24, 28, 16)
        per_val1 = int(np.interp(a1,(70,120),(100,0)))
        bar_val = int(np.interp(per_val1, (0,100),(70+350, 70)))
        cv2.rectangle(img, (570, bar_val),(570+35, 70+350), (255, 0, 0), cv2.FILLED)
        cv2.rectangle(img, (570,70), (570+35, 70+350), (), 3)
        # cvzone.putTextRect(img, f"{per_val1} %", (570, 25),1.1, 2, colorT=(255,255,255), colorR=(0, 135, 0),border=3, colorB=())
        result = [a1, a2]
        result_queue.put(result)
        cv2.putText(img, f"{per_val1}%", (560, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_4)
    else:
        cv2.putText(img, f"ANDA TIDAK TERDETEKSI!", (20, 260), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 255), 4, cv2.LINE_4)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

col1, col2 = st.columns([0.6, 0.4])
with st.container():
    with col1:
        webrtc_ctx = webrtc_streamer(
            key="coba",
            mode=WebRtcMode.SENDRECV,
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False}
        )
    with col2:
        # if st.checkbox("Tampilkan perhitungan", value=True):
        if webrtc_ctx.state.playing:
            # false_placeholder = st.empty()
            column1, column2 = st.columns(2)
            with column1:
                st.markdown(f'<center><p class="small-font">BENAR</p></center>', unsafe_allow_html=True)
                benar_placeholder = st.empty()
            with column2:
                st.markdown(f'<center><p class="small-font">SALAH</p></center>', unsafe_allow_html=True)
                salah_placeholder = st.empty()
            push_ups = 0
            no_push_ups = 0
            dir = 0
            while True:
                result = result_queue.get()
                if isinstance(result[0], float):
                    a1, a2 = result
                    if 170 < a2 < 190:
                        if a1 < 70:
                            if dir == 0:
                                push_ups += 0.5
                                dir = 1
                        elif 120 < a1 < 180:
                            if dir == 1:
                                push_ups += 0.5
                                dir = 0
                    elif a2 <= 170 or a2 >= 190:
                        if a1 < 70:
                            if dir == 0:
                                no_push_ups += 0.5
                                dir = 1
                        elif 110 < a1 < 180:
                            if dir == 1:
                                no_push_ups += 0.5
                                dir = 0
                    benar_placeholder.markdown(f'<center><p class="big-font">{int(push_ups)}</p></center>', unsafe_allow_html=True)
                    salah_placeholder.markdown(f'<center><p class="big-font">{int(no_push_ups)}</p></center>', unsafe_allow_html=True)
