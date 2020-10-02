from flask import render_template, request, redirect, url_for, Response
from flask_sqlalchemy import get_debug_queries

from corona import app, config
from corona.models import db
from corona.models.UploadedFile import UploadedFile
from corona.models.DailyConfirmed import DailyConfirmed

import os
import csv
import codecs
import shutil
from werkzeug.utils import secure_filename
from hashlib import md5

import pandas as pd
from io import StringIO

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('db_read'))
    
@app.route('/insert/', methods=['GET', 'POST'])
def db_create():
    if request.method == 'GET':
        return render_template("insert.html", msg=request.args.get('msg', ''))
    date = request.form['date'].split()[0]
    today_confirmed = DailyConfirmed(date=request.form['date'], count=request.form['count'])
    db.session.add(today_confirmed)
    db.session.commit()
    return redirect(url_for('db_read'))

@app.route('/read/', methods=['GET'])
def db_read():
    data_list = DailyConfirmed.query.all()
    if not data_list:
        return redirect(url_for('db_create', msg="데이터가 없습니다. 정보를 입력해주세요"))
    for obj in data_list:
        obj.date = obj.date.strftime("%y년 %-m월 %-d일") 
    return render_template("read.html", data_list=data_list)

@app.route('/edit/<date>', methods=['GET'])
def db_update(date):
    target = DailyConfirmed.query.filter_by(date=date).first()
    if not target:
        return redirect(url_for('db_create', msg="해당 날짜의 데이터가 없어 수정이 불가능합니다."))
    target.count = request.args.get('count', target.count)
    db.session.commit()
    return redirect(url_for('db_read'))

@app.route('/remove_all_data/', methods=['GET'])
def db_delete():
    db.session.query(DailyConfirmed).delete()
    db.session.query(UploadedFile).delete()
    db.session.commit()
    shutil.rmtree(app.config['UPLOAD_FOLDER_LOCATION'])
    return redirect(url_for('db_create', msg="초기화를 완료하였습니다."))

@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method != 'POST':
        return redirect(url_for('db_create', msg="올바른 방법으로 파일을 업로드하세요"))
    elif 'file' not in request.files:
        return redirect(url_for('db_create', msg="업로드 할 파일이 없습니다."))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('db_create', msg="업로드 할 파일이 없습니다."))

    if file and config.allowed_file(file.filename):
        # Register real_file_name into db
        checksum = md5(file.read()).hexdigest()
        if UploadedFile.query.filter_by(checksum=checksum).count() != 0:
            return redirect(url_for('db_create', msg="해당 데이터는 이미 등록되었습니다."))
        filename = secure_filename(file.filename)
        usr_upload = UploadedFile(filename=filename, checksum=checksum)
        db.session.add(usr_upload)
        db.session.commit()
        file.stream.seek(0)

        # INSERT CSV Data to DailyConfirmed Table
        # utf-8-sig : utf-8 without bom
        stream = codecs.iterdecode(file.stream, 'utf-8-sig')
        for row in csv.reader(stream, dialect=csv.excel):
            if row:
                if not DailyConfirmed.query.filter_by(date=row[0]).first():
                    db.session.add(DailyConfirmed(date=row[0], count=row[1]))
        db.session.commit()
        file.stream.seek(0)

        # Save User Uploaded File that name changed to index
        file_idx = UploadedFile.query.filter_by(checksum=checksum).first().id
        if not os.path.exists(app.config['UPLOAD_FOLDER_LOCATION']):
            os.mkdir(app.config['UPLOAD_FOLDER_LOCATION'])
        save_path = os.path.join(app.config['UPLOAD_FOLDER_LOCATION'], str(file_idx)+'.csv')

        file.save(save_path)

        # TODO: Delete This CODE
        # file stream still remain bom, so eliminate it
        # I wanna do this at saving
        with open(save_path, 'r', encoding='utf-8-sig') as fin:
            with open(save_path+".edit", 'w', encoding='utf-8') as fout:
                fout.write(fin.read())
        os.remove(save_path)
        os.rename(save_path+".edit", save_path)

        return redirect(url_for('db_read'))
    return redirect(url_for('db_create', msg="파일을 업로드 에러, 다시 시도해주세요."))
    
@app.route('/export/')
def export_csv():
    queryset = DailyConfirmed.query
    # Pandas가 SQL을 읽도록 만들어주기
    df = pd.read_sql(queryset.statement, queryset.session.bind) 
    output = StringIO()
    # 한글 인코딩 위해 UTF-8 with BOM 설정해주기
    output.write(u'\ufeff') 
    df.to_csv(output)
    # CSV 파일 형태로 브라우저가 파일다운로드라고 인식하도록 만들어주기
    response = Response(
        output.getvalue(),
        mimetype="text/csv",
        content_type='application/octet-stream',
    )
    # 다운받았을때의 파일 이름 지정해주기
    response.headers["Content-Disposition"] = "attachment; filename=export.csv" 
    return response