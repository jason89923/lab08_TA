from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)  # 啟用跨域資源共享，允許前端與後端互動
socketio = SocketIO(app)


# 定義根路由
@app.route('/')
def index():
    return render_template('TA.html')  # 返回 TA.html 頁面
# 用於儲存接收到的資料
data_storage = []

# 處理Socket
@socketio.on('connect')
def handle_connect():
    print('Socket connected.')
    emit('message', '已连接到服务器')

@socketio.on('disconnect')
def handle_disconnect():
    print('Socket closed.')

@app.route('/submit', methods=['POST'])
def receive_data():
    try:
        # 確保 Flask 使用 UTF-8 解碼 JSON
        data = request.get_json(force=True)  # 強制解析 JSON
        group = data.get('group')
        link = data.get('link')

        if not group or not link:
            return jsonify({"message": "缺少必要欄位"}), 400

        data_storage.append({"group": group, "link": link})
        
        socketio.emit('message', data_storage)
        
        return jsonify({"message": "資料已接收", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7000)
