# Flask应用
from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
import cv2
import base64
import numpy as np
from utils.inference import load_model, process_frame, draw_results

app = Flask(__name__)
CORS(app)

# 加载模型
model = None
def init_model():
    global model
    model = load_model('models/best.pt')

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 实时视频流
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # 处理帧
            detected_objects = process_frame(model, frame)
            # 绘制结果
            frame = draw_results(frame, detected_objects)
            
            # 编码为JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # 生成视频流
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 图像识别API
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})
    
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # 处理图像
    detected_objects = process_frame(model, img)
    
    # 构建响应
    results = []
    for obj in detected_objects:
        results.append({
            'class_name': obj['class_name'],
            'confidence': obj['confidence'],
            'bbox': obj['bbox'],
            'suggestion': obj['suggestion']
        })
    
    return jsonify({'results': results})

# 健康检查
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    init_model()
    app.run(debug=True, host='0.0.0.0', port=5000)