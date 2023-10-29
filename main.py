import streamlit as st
import time
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np


st.set_page_config(
    page_title="push up counter",
    page_icon=":shark:",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://wa.me/6285536956301',
        'Report a bug': "https://wa.me/6285536956301"
    }
)
st.markdown("<h1 style='text-align: center;'>Push-Up Counter</h1>", unsafe_allow_html=True)

frame_placeholder = st.empty()
stop_button_pressed = st.button("Stop")

cap = cv2.VideoCapture(0)
detector = PoseDetector()
ptime = 0
ctime = 0
dir = 0
push_ups = 0

while cap.isOpened() and not stop_button_pressed:
    ret, img = cap.read()

    img = detector.findPose(img)
    lmlst, bbox = detector.findPosition(img, draw=False)
    if lmlst:
        a1 = detector.findAngle(img, 12, 14, 16)
        a2 = detector.findAngle(img, 15, 13, 11)
        per_val1 = np.interp(a1, (85, 175), (100, 0))
        per_val2 = np.interp(a2, (85, 175), (100, 0))

        if 20 <= per_val1 <= 100 and 20 <= per_val2 <= 100:
            if dir == 0:
                push_ups += 0.5
                dir = 1
                color = (0, 255, 0)
        elif 0 <= per_val1 < 20 and 0 <= per_val2 < 20:
            if dir == 1:
                push_ups += 0.5
                dir = 0
                color = (0, 255, 0)
        else:
            color = (0, 0, 255)
    cvzone.putTextRect(img, f"Jumlah : {int(push_ups)}", (440, 442), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),
                       border=3, colorB=())
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cvzone.putTextRect(img, f"FPS : {int(fps)}", (20, 440), 1.6, 2, colorT=(255, 255, 255), colorR=(0, 135, 0),
                       border=3, colorB=())


    if not ret:
        st.write("The video capture is ended")
        break


    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(img, channels="RGB")

    if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
        break

cap.release()
cv2.destroyAllWindows()










#
# import streamlit as st
# import time
# import cv2
# import cvzone
# from cvzone.PoseModule import PoseDetector
# import numpy as np
#
#
# st.set_page_config(
#     page_title="push up counter",
#     page_icon=":shark:",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://wa.me/6285536956301',
#         'Report a bug': "https://wa.me/6285536956301"
#     }
# )
# st.markdown("<h1 style='text-align: center;'>Push-Up Counter</h1>", unsafe_allow_html=True)
#
# frame_placeholder = st.empty()
# stop_button_pressed = st.button("Stop")
#
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()
# ptime = 0
# ctime = 0
# dir = 0
# push_ups = 0
#
# while cap.isOpened() and not stop_button_pressed:
#     ret, img = cap.read()
#
#     img = detector.findPose(img)
#     lmlst, bbox = detector.findPosition(img, draw=False)
#     if lmlst:
#         a1 = detector.findAngle(img, 12, 14, 16)
#         a2 = detector.findAngle(img, 15, 13, 11)
#         per_val1 = np.interp(a1, (85, 175), (100, 0))
#         per_val2 = np.interp(a2, (85, 175), (100, 0))
#
#         if 20 <= per_val1 <= 100 and 20 <= per_val2 <= 100:
#             if dir == 0:
#                 push_ups += 0.5
#                 dir = 1
#                 color = (0, 255, 0)
#         elif 0 <= per_val1 < 20 and 0 <= per_val2 < 20:
#             if dir == 1:
#                 push_ups += 0.5
#                 dir = 0
#                 color = (0, 255, 0)
#         else:
#             color = (0, 0, 255)
#     cvzone.putTextRect(img, f"Jumlah : {int(push_ups)}", (440, 442), 2, 2, colorT=(255, 255, 255), colorR=(255, 0, 0),
#                        border=3, colorB=())
#     ctime = time.time()
#     fps = 1 / (ctime - ptime)
#     ptime = ctime
#     cvzone.putTextRect(img, f"FPS : {int(fps)}", (20, 440), 1.6, 2, colorT=(255, 255, 255), colorR=(0, 135, 0),
#                        border=3, colorB=())
#
#
#     if not ret:
#         st.write("The video capture is ended")
#         break
#
#
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     frame_placeholder.image(img, channels="RGB")
#
#     if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
#         break
#
# cap.release()
# cv2.destroyAllWindows()






# frame_window = st.image([])
# cap = cv2.VideoCapture(0)
# detector = PoseDetector()
# ptime = 0
# ctime = 0
# dir = 0
# push_ups = 0
# while True:
#     _, img = cap.read()
#     img = detector.findPose(img)
#     lmlst, bbox = detector.findPosition(img, draw=False)
#     if lmlst:
#         a1 = detector.findAngle(img,12,14,16)
#         a2 = detector.findAngle(img, 15, 13, 11)
#         per_val1 = np.interp(a1,(85,175),(100,0))
#         per_val2 = np.interp(a2, (85, 175), (100, 0))
#
#         if 20 <= per_val1 <= 100 and 20 <= per_val2 <= 100:
#             if dir == 0:
#                 push_ups += 0.5
#                 dir = 1
#                 color = (0, 255, 0)
#         elif 0 <= per_val1 < 20 and 0 <= per_val2 < 20:
#             if dir == 1:
#                 push_ups += 0.5
#                 dir = 0
#                 color = (0, 255, 0)
#         else:
#             color = (0, 0, 255)
#     cvzone.putTextRect(img, f"Jumlah : {int(push_ups)}", (440,442),2,2,colorT=(255,255,255), colorR=(255,0,0), border=3, colorB=())
#     ctime = time.time()
#     fps = 1/(ctime-ptime)
#     ptime = ctime
#     cvzone.putTextRect(img, f"FPS : {int(fps)}",(20,440),1.6,2,colorT=(255,255,255),colorR=(0,135,0),border=3, colorB=())
#     # cv2.imshow("Coba", img)
#     frame_window.image(img)
#     # if cv2.waitKey(1) == ord("q"):
#     #     break