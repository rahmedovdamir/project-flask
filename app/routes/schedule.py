from flask import Blueprint, render_template, request, redirect, flash, abort, current_app, url_for, jsonify
from ..functions import generate_group_schedule_url
from ..parser import parsing
from flask_login import current_user, login_required
import requests
import os
import datetime
import json



schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule')
@schedule.route('/schedule/<group_id>', methods=['POST', 'GET'])
@login_required  # Добавьте эту декорацию если нужно
def all(group_id=None):
    if group_id is None:
        if current_user.is_authenticated:
            group_id = current_user.group
        else:
             return redirect(url_for('user.login'))
    
    group = generate_group_schedule_url(str(group_id))
    response = requests.get(group)
    
    if response.status_code != 200:
        flash('Ошибка загрузки расписания', 'error')
        return redirect(url_for('post.all'))
    
    response_data = response.json()
    first_item = response_data['data'][0] 
    file_link = first_item.get('iCalLink')
    response2 = requests.get(file_link, timeout=30)
    
    filename = f"schedule_{group_id}.ics"
    filepath = os.path.join("app/static/json", filename)
    
    with open(filepath, 'wb') as f:
        f.write(response2.content)
    
    ics_path = filepath
    parsing(ics_path, group_id)
    
    return render_template('/schedule/schedule.html', group_number=group_id)

@schedule.route('/api/schedule/<group_id>', methods=['POST', 'GET'])
def get_schedule_perday(group_id):
    first_september = 244   
    counter_day_of_year = int(datetime.datetime.now().strftime("%j"))
    counter_week = (counter_day_of_year - first_september) // 7
    day_name = datetime.datetime.now().strftime("%A") 
    filepath = f"app/static/json/schedule_data_{group_id}.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        week_schedule = data[counter_week]
        day_schedule = week_schedule.get(day_name)
        return jsonify(day_schedule)
