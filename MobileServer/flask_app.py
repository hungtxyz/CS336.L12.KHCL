import base64
import json
import os
from flask import Flask, request, flash, send_file, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from config import app, db
from models import Task
from task import AudioProcessor

db.create_all()


@app.route('/')
def hello():
    return "https://drive.google.com/drive/folders/1a48MTG34rfSHQ9gYY2DFk7lo6UQusctu?usp=sharing"


@app.route('/sendstr', methods=['GET', 'POST'])
def response():
    data = request.data
    return data


@app.route('/audio/test', methods=['POST', 'GET'])
def ahihi():
    data = request.data
    return data


# --------------------- OLDVERSION---------------------
# @app.route('/audio/sendaudio', methods=['POST', 'GET'])
# def receiveAudio():
#     audioFile = request.files['audioFile']
#     file_name = secure_filename(audioFile.filename)
#     print(audioFile.filename)
#     task = Task()
#     db.session.add(task)
#     db.session.commit()
#
#     audioFile.save("./q_"+str(task.id)+file_name)
#
#     db.session.flush()
#     return str(task.id)

#
# @app.route('/audio/request4result', methods=['GET', 'POST'])
# def checkStatus():
#     request_id = request.data
#     print("Request status of id: ", request_id)
#     request_id = request_id.decode("utf-8")
#     task = Task.query.filter_by(id=request_id).first_or_404()
#     return str(task.result)


@app.route('/audio/sendaudio', methods=['POST', 'GET'])
def receiveAudio():
    raw_body = request.get_data().decode('utf-8')
    data: dict = json.loads(raw_body)

    # Save audio to file
    bytes = data.get("audio", None);
    if not bytes:
        raise ValueError("Invalid image data")

    task = Task()
    db.session.add(task)
    db.session.commit()

    db.session.flush()

    file = './q_' + str(task.id) + "audio.mp3"
    bin_data = base64.b64decode(bytes)

    with open(file, "wb") as wb:
        wb.write(bin_data)

    return jsonify({
        "task_id": task.id
    })


@app.route('/audio/request4result', methods=['GET'])
def checkStatus():
    task_id = int(request.args.get("id"))
    task = Task.query.filter_by(id=task_id).first()

    if task.status:
        return jsonify({
            "status": True,
            "song_name": task.result,
        })
    return jsonify({
        "status": False,
        "song_name": None,
    })


if __name__ == "__main__":
    image_processor = AudioProcessor(db)
    image_processor.start()

    app.run(host="0.0.0.0", port=8000)
