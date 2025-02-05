from ultralytics import solutions, YOLO
import cv2

status1 = 0
status2 = 0

# 비디오 스트리밍 함수 정의
def generate_frame():
    # cap = cv2.VideoCapture("rtsp://yolo:yolo@192.168.16.92:8080/h264_ulaw.sdp")
    cap = cv2.VideoCapture(0)
    
    # 특정 좌표 설정
    region_points = {
        "Region#01": [(0,0), (600,0), (600, 1080), (0, 1080)],
        "Region#02": [(1250,0), (1920,0), (1920, 1080), (1250, 1080)],
        "Region#03": [(600,0), (1250,0), (1250, 1080), (600, 1080)]
    }

    # 구역 설정
    region = solutions.RegionCounter(
        show=True,
        region=region_points,
       # model='model_train_1/trained_yolo11n.pt'                                # 맥용 경로
        model = 'Pyeongtaek_AI_YOLO_Team/model_train_1/trained_yolo11n.pt'     # 윈도우용 경로
    )
    
    
    while True:
        success, im0 = cap.read()
        if not success:
            print("프레임 확인")
            break
        
        region_results, region_counts, label_names = region.count(im0)
        
        # 탐지된 객체의 수 추출
        global status1, status2, status3
        status1 = region_counts.get("Region#01", 0)
        status2 = region_counts.get("Region#02", 0)
        status3 = region_counts.get("Region#03", 0)
        
        # 프레임을 JPEG 형식으로 인코딩
        _, buffer = cv2.imencode('.jpg', region_results)
        # 인코딩된 이미지를 바이트 형태로 변환
        frame_bytes = buffer.tobytes()
        
        # 실시간으로 비디오 스트리밍 데이터 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + 
               b'\r\n')
        
    cap.release()
    
def get_status1():
    return status1
def get_status2():
    return status2
def get_status3():
    return status3

