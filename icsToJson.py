import json
import hashlib
from datetime import datetime
from icalendar import Calendar

def hash_data(data):
    # Convert the data to a JSON string and hash it using SHA256
    json_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_string.encode()).hexdigest()

def parse_ics_to_json(ics_file_path, output_json_path):
    """
    Convert ICS file to JSON format matching the required structure
    """
    with open(ics_file_path, 'rb') as f:
        calendar = Calendar.from_ical(f.read())
    
    classes = []
    
    # Slovenian day names mapping
    day_names = {
        'Monday': 'Ponedeljek',
        'Tuesday': 'Torek',
        'Wednesday': 'Sreda',
        'Thursday': 'Četrtek',
        'Friday': 'Petek',
        'Saturday': 'Sobota',
        'Sunday': 'Nedelja'
    }
    
    for component in calendar.walk():
        if component.name == "VEVENT":
            # Extract event details
            summary = str(component.get('summary', ''))
            description = str(component.get('description', ''))
            location = str(component.get('location', ''))
            if summary.strip().lower() == 'rezervacija':
                continue
            dtstart = component.get('dtstart')
            dtend = component.get('dtend')
            
            # Description lines: "Predavatelji: A, B" / "Skupine: X, Y"
            izvajalec = ''
            skupina = ''
            for line in description.splitlines():
                label, sep, value = line.partition(':')
                if not sep:
                    continue
                label = label.strip().lower()
                if label.startswith('predavatelj'):
                    izvajalec = value.strip()
                elif label.startswith('skupin'):
                    skupina = value.strip()
            
            # Extract date and time
            sort_key = ''  # For sorting purposes
            if dtstart:
                dt = dtstart.dt
                if isinstance(dt, datetime):
                    dan_english = dt.strftime('%A')
                    dan = day_names.get(dan_english, dan_english)
                    datum = dt.strftime('%d.%m.%Y')
                    ura_od = dt.strftime('%H:%M')
                    # Create sort key in format YYYYMMDD-HHMM
                    sort_key = dt.strftime('%Y%m%d-%H%M')
                else:
                    dan = ''
                    datum = str(dt)
                    ura_od = ''
            else:
                dan = ''
                datum = ''
                ura_od = ''
            
            if dtend:
                dt = dtend.dt
                if isinstance(dt, datetime):
                    ura_do = dt.strftime('%H:%M')
                else:
                    ura_do = ''
            else:
                ura_do = ''
            
            # Combine time range
            ura = f"{ura_od}-{ura_do}" if ura_od and ura_do else ''
            
            # Create entry matching the required format
            entry = {
                "Dan": dan,
                "Datum": datum,
                "Ura": ura,
                "Prostor": location,
                "Skupina": skupina,
                "Izvajalec": izvajalec,
                "Opis": summary,
                "_sort_key": sort_key  # Temporary field for sorting
            }
            
            classes.append(entry)
    
    # Sort by date and time using the sort key
    classes.sort(key=lambda x: x.get('_sort_key', ''))
    
    # Remove the temporary sort key from all entries
    for entry in classes:
        entry.pop('_sort_key', None)
    
    # Create JSON structure with Hash
    json_data = {
        "Hash": hash_data(classes),
        "Classes": classes
    }
    
    # Write to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent=4)
    
    print(f"Converted {len(classes)} events from {ics_file_path} to {output_json_path}")
    return json_data

if __name__ == '__main__':
    ics_file = 'timetable.ics'
    output_file = 'school.json'
    parse_ics_to_json(ics_file, output_file)
