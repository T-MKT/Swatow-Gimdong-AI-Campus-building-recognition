# 训练脚本
import os
from ultralytics import YOLO

# 数据集配置文件路径
config_path = 'data/config.yaml'

# 模型路径
model_path = 'models/yolov8n.pt'

# 训练参数
epochs = 100
batch_size = 16
imgsz = 640
workers = 4
optimizer = 'Adam'
learning_rate = 0.01

# 加载预训练模型
model = YOLO(model_path)

# 开始训练
print("开始训练模型...")
train_results = model.train(
    data=config_path,
    epochs=epochs,
    batch=batch_size,
    imgsz=imgsz,
    workers=workers,
    optimizer=optimizer,
    lr0=learning_rate,
    project='runs/train',
    name='exp',
    exist_ok=True
)

# 验证模型
print("验证模型...")
val_results = model.val(
    data=config_path,
    imgsz=imgsz,
    batch=batch_size,
    workers=workers
)

# 保存最佳模型
print("保存最佳模型...")
best_model_path = 'models/best.pt'
os.makedirs(os.path.dirname(best_model_path), exist_ok=True)
model.save(best_model_path)

print("训练完成！")
print(f"最佳模型保存路径: {best_model_path}")
print(f"训练结果: {train_results}")
print(f"验证结果: {val_results}")