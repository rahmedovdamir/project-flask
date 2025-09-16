import icalendar
from datetime import datetime
from pathlib import Path
import json

def count_par(time):
    array = ["0900","1040", "1240", "1420", "1620","1800","1940"]
    return str(array.index(time) + 1)

def clean_text(text):
    if "\\n" in text:
        return text.replace('\\n', ' ').replace('  ', ' ').strip()
    return text

def parsing(ics_path, group_number):
    ics_file = Path(ics_path)
    calendar = icalendar.Calendar.from_ical(ics_file.read_bytes())
    events = []
    for event in calendar.events:
        week = dict()
        if ("неделя" in event.get("SUMMARY")):
            week["week_count"] = str(event.get("SUMMARY"))
            week["dstart"] = str(event.get('DTSTART').dt)
            week["dend"] = str(event.get('DTEND').dt)
            week["Monday"] = {}
            week["Tuesday"] = {} 
            week["Wednesday"] = {} 
            week["Thursday"] = {}
            week["Friday"] = {}
            week["Saturday"] = {} 
        else:
            if ((str(event.get("CATEGORIES").to_ical().decode())) != "ЛАБ"):
                dstart = event.get("DTSTART").dt
                count_pars = count_par(str(dstart.strftime("%H%M")))
                day_week = str(dstart.strftime("%A"))
                dend = event.get("DTSTART").dt
                interval = event.get("RRULE").get("INTERVAL")
                type_lesson = event.get("CATEGORIES").to_ical().decode()
                teacher = clean_text(event.get("DESCRIPTION").to_ical().decode())
                name_lesson = clean_text(event.get("SUMMARY").to_ical().decode())
                location = clean_text(event.get("LOCATION").to_ical().decode())
                first_september = 244
                counter_week_day = int(dstart.strftime("%j"))
                counter_week = (counter_week_day - first_september) // 7 
                while counter_week < 18:
                    events[counter_week][day_week][count_pars] = {}
                    events[counter_week][day_week][count_pars]["type_lesson"] = type_lesson
                    events[counter_week][day_week][count_pars]["name_lesson"] = name_lesson
                    events[counter_week][day_week][count_pars]["teacher"] = teacher
                    events[counter_week][day_week][count_pars]["locatiton"] = location
                    events[counter_week]["week_number"] = counter_week + 1
                    counter_week+=2
            elif((str(event.get("CATEGORIES").to_ical().decode())) == "ЛАБ") : 
                dstart = event.get("DTSTART").dt
                count_pars = count_par(str(dstart.strftime("%H%M")))
                day_week = str(dstart.strftime("%A"))
                dend = event.get("DTSTART").dt
                interval = event.get("RRULE").get("INTERVAL")
                type_lesson = event.get("CATEGORIES").to_ical().decode()
                teacher = clean_text(event.get("DESCRIPTION").to_ical().decode())
                name_lesson = clean_text(event.get("SUMMARY").to_ical().decode())
                location = clean_text(event.get("LOCATION").to_ical().decode())
                first_september = 244
                counter_week_day = int(dstart.strftime("%j"))
                counter_week = (counter_week_day - first_september) // 7 
                events[counter_week][day_week][count_pars] = {}
                events[counter_week][day_week][count_pars]["type_lesson"] = type_lesson
                events[counter_week][day_week][count_pars]["name_lesson"] = name_lesson
                events[counter_week][day_week][count_pars]["teacher"] = teacher
                events[counter_week][day_week][count_pars]["locatiton"] = location
        events.append(week)
    with open(f'app/static/json/schedule_data_{str(group_number)}.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)