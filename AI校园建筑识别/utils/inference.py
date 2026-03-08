# 推理逻辑
import cv2
from ultralytics import YOLO

# 加载模型
def load_model(model_path):
    return YOLO(model_path)

# 垃圾分类建议
def get_garbage_suggestion(class_id):
    suggestions = {
        5: "可回收垃圾：建议投放到蓝色垃圾桶",
        6: "厨余垃圾：建议投放到绿色垃圾桶",
        7: "有害垃圾：建议投放到红色垃圾桶",
        8: "其他垃圾：建议投放到灰色垃圾桶"
    }
    return suggestions.get(class_id, "")

# 处理单帧图像
def process_frame(model, frame, conf_threshold=0.5):
    # 模型推理
    results = model(frame, conf=conf_threshold)
    
    # 处理结果
    detected_objects = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 获取类别ID和置信度
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            # 获取边界框
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # 获取类别名称
            class_name = model.names[class_id]
            
            # 获取垃圾分类建议
            suggestion = get_garbage_suggestion(class_id)
            
            detected_objects.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2],
                "suggestion": suggestion
            })
    
    return detected_objects

# 绘制识别结果
def draw_results(frame, detected_objects):
    for obj in detected_objects:
        x1, y1, x2, y2 = obj["bbox"]
        class_name = obj["class_name"]
        confidence = obj["confidence"]
        suggestion = obj["suggestion"]
        
        # 绘制边界框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 绘制标签
        label = f"{class_name}: {confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # 绘制垃圾分类建议
        if suggestion:
            cv2.putText(frame, suggestion, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    return frame

# 实时摄像头识别
def run_realtime(model, camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 处理帧
        detected_objects = process_frame(model, frame)
        
        # 绘制结果
        frame = draw_results(frame, detected_objects)
        
        # 显示结果
        cv2.imshow('AI校园建筑识别', frame)
        
        # 按ESC键退出
        if cv2.waitKey(1) == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()