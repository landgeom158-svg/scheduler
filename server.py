#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cat — Hardened Python client-server API backend and file server
"""
from __future__ import print_function
import os
import json
import datetime

try:
    # Python 2 imports
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import ThreadingTCPServer
    import urlparse
except ImportError:
    # Python 3 imports
    from http.server import SimpleHTTPRequestHandler
    from socketserver import ThreadingTCPServer
    import urllib.parse as urlparse

PORT = 8000
DB_FILE = 'db.json'

try:
    string_types = (str, unicode)
except NameError:
    string_types = (str,)

def get_relative_date_string(days_offset):
    d = datetime.date.today() + datetime.timedelta(days=days_offset)
    return d.isoformat()

# Initial Default State matching state.js structure
DEFAULT_STATE = {
    "view": "dashboard",
    "timezone": "Asia/Kolkata",
    "meetingTypes": [
        {
            "id": "mt-1",
            "title": "15m Quick Catchup",
            "duration": 15,
            "location": "Google Meet",
            "color": "indigo",
            "description": "Quick sync to align on project updates, resolve blockers, and set weekly goals.",
            "active": True
        },
        {
            "id": "mt-2",
            "title": "30m Discovery Call",
            "duration": 30,
            "location": "Zoom",
            "color": "purple",
            "description": "Introductory call to explore client requirements, project scope, and design choices.",
            "active": True
        },
        {
            "id": "mt-3",
            "title": "60m Tech Consultation",
            "duration": 60,
            "location": "Google Meet",
            "color": "emerald",
            "description": "Deep dive technical architecture review, code audit, and system design recommendations.",
            "active": True
        },
        {
            "id": "mt-4",
            "title": "45m Portfolio Showcase",
            "duration": 45,
            "location": "Phone Call",
            "color": "orange",
            "description": "Presentation of past SaaS designs, visual interactions, and code walkthroughs.",
            "active": True
        }
    ],
    "bookings": [
        {
            "id": "b-1",
            "meetingTypeId": "mt-2",
            "title": "30m Discovery Call",
            "clientName": "Alex Rivers",
            "clientEmail": "alex@designflow.io",
            "date": get_relative_date_string(-2),
            "time": "10:00",
            "duration": 30,
            "notes": "Interested in a new SaaS marketing page redesign with dynamic animations."
        },
        {
            "id": "b-2",
            "meetingTypeId": "mt-3",
            "title": "60m Tech Consultation",
            "clientName": "Marcus Vance",
            "clientEmail": "m.vance@techstack.net",
            "date": get_relative_date_string(-1),
            "time": "14:00",
            "duration": 60,
            "notes": "Need to review system scaling guidelines and Database indexing strategies."
        },
        {
            "id": "b-3",
            "meetingTypeId": "mt-1",
            "title": "15m Quick Catchup",
            "clientName": "Sarah Jenkins",
            "clientEmail": "sarah@vertex.com",
            "date": get_relative_date_string(0),
            "time": "11:00",
            "duration": 15,
            "notes": "Checking in on the visual mockup layout adjustments."
        },
        {
            "id": "b-4",
            "meetingTypeId": "mt-2",
            "title": "30m Discovery Call",
            "clientName": "Diana Prince",
            "clientEmail": "diana@themiscera.co",
            "date": get_relative_date_string(0),
            "time": "15:30",
            "duration": 30,
            "notes": "Explore scheduling API integrations and webhook callbacks."
        },
        {
            "id": "b-5",
            "meetingTypeId": "mt-1",
            "title": "15m Quick Catchup",
            "clientName": "Ethan Hunt",
            "clientEmail": "ethan@impossible.org",
            "date": get_relative_date_string(1),
            "time": "09:30",
            "duration": 15,
            "notes": "Project kickoff sync for the next sprint delivery."
        },
        {
            "id": "b-6",
            "meetingTypeId": "mt-4",
            "title": "45m Portfolio Showcase",
            "clientName": "Bruce Wayne",
            "clientEmail": "bruce@waynecorp.com",
            "date": get_relative_date_string(2),
            "time": "16:00",
            "duration": 45,
            "notes": "Showcasing deep-mode widgets and mobile viewport styling structures."
        }
    ],
    "availability": {
        "start": "09:00",
        "end": "17:00",
        "days": [1, 2, 3, 4, 5]
    },
    "integrations": {
        "googleCalendar": True,
        "outlookCalendar": False,
        "zoomMeetings": True
    },
    "logs": [
        { "id": "l-1", "text": "Sarah Jenkins scheduled a 15m Quick Catchup", "type": "schedule", "time": "10 mins ago" },
        { "id": "l-2", "text": "Diana Prince scheduled a 30m Discovery Call", "type": "schedule", "time": "1 hr ago" },
        { "id": "l-3", "text": "Integration with Zoom successfully connected", "type": "system", "time": "3 hrs ago" },
        { "id": "l-4", "text": "New meeting type \"45m Portfolio Showcase\" created", "type": "create", "time": "5 hrs ago" }
    ]
}

def load_db():
    if not os.path.exists(DB_FILE):
        print("Database file not found. Creating default db.json...")
        save_db(DEFAULT_STATE)
        return DEFAULT_STATE
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print("Error reading database:", e)
        return DEFAULT_STATE

def save_db(data):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("Database successfully written.")
    except Exception as e:
        print("Error writing database:", e)

def validate_state(data):
    try:
        if not isinstance(data, dict):
            return False
            
        required_keys = ["view", "timezone", "meetingTypes", "bookings", "availability", "integrations", "logs"]
        for key in required_keys:
            if key not in data:
                return False
                
        # Type validations
        if not isinstance(data["view"], string_types):
            return False
        if not isinstance(data["timezone"], string_types):
            return False
        if not isinstance(data["meetingTypes"], list):
            return False
        if not isinstance(data["bookings"], list):
            return False
        if not isinstance(data["logs"], list):
            return False
        if not isinstance(data["availability"], dict):
            return False
        if not isinstance(data["integrations"], dict):
            return False
            
        # Validate availability schema
        avail = data["availability"]
        if "start" not in avail or "end" not in avail or "days" not in avail:
            return False
        if not isinstance(avail["start"], string_types) or not isinstance(avail["end"], string_types):
            return False
        if not isinstance(avail["days"], list):
            return False
            
        # Validate integrations schema
        ints = data["integrations"]
        for key, val in ints.items():
            if not isinstance(val, bool):
                return False
                
        # Validate list items
        for mt in data["meetingTypes"]:
            if not isinstance(mt, dict):
                return False
            mt_keys = ["id", "title", "duration", "location", "color", "description", "active"]
            for k in mt_keys:
                if k not in mt:
                    return False
            if not isinstance(mt["id"], string_types) or not isinstance(mt["title"], string_types):
                return False
            if not isinstance(mt["duration"], int) or not isinstance(mt["active"], bool):
                return False

        for b in data["bookings"]:
            if not isinstance(b, dict):
                return False
            essential_b_keys = ["id", "meetingTypeId", "title", "clientName", "clientEmail", "date", "time", "duration"]
            for k in essential_b_keys:
                if k not in b:
                    return False
            if not isinstance(b["id"], string_types) or not isinstance(b["meetingTypeId"], string_types):
                return False
            if not isinstance(b["clientEmail"], string_types) or not isinstance(b["duration"], int):
                return False

        return True
    except Exception as e:
        print("Schema validation failed with exception:", e)
        return False

class CatAPIHandler(SimpleHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Override to suppress default console log pollution
        pass

    def end_headers(self):
        # Injects high-end security response headers before finishing headers dispatch
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; script-src 'self' 'unsafe-inline' https://unpkg.com;")
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)
        path = parsed_url.path

        # Security: Directory Traversal Defense
        translated = self.translate_path(path)
        abs_translated = os.path.abspath(translated)
        abs_root = os.path.abspath(os.getcwd())
        
        if not abs_translated.startswith(abs_root):
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Access Denied")
            print("SECURITY ALERT: Blocked directory traversal attempt: %s" % path)
            return

        if path == '/api/state':
            db_data = load_db()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(db_data).encode('utf-8'))
            return
            
        # Default fallback to serve static files
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        parsed_url = urlparse.urlparse(self.path)
        path = parsed_url.path

        if path == '/api/state':
            content_length = 0
            if 'content-length' in self.headers:
                content_length = int(self.headers['content-length'])
            elif hasattr(self.headers, 'getheader'):
                content_length = int(self.headers.getheader('content-length', 0))
            else:
                content_length = int(self.headers.get('content-length', 0))

            post_body = self.rfile.read(content_length) if content_length > 0 else b''
            if isinstance(post_body, bytes):
                post_body = post_body.decode('utf-8')

            try:
                new_state = json.loads(post_body)
                
                # Security: Validate state schema before saving
                if not validate_state(new_state):
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "Invalid schema"}).encode('utf-8'))
                    print("SECURITY ALERT: Blocked invalid state modification payload")
                    return

                save_db(new_state)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                print("POST /api/state — Saved state updates")
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                print("POST /api/state — Failed to parse state payload:", e)
            return

        self.send_response(404)
        self.end_headers()

# Disable socket address reuse errors
ThreadingTCPServer.allow_reuse_address = True

print("Cat backend server starting on http://localhost:%d" % PORT)
httpd = ThreadingTCPServer(("", PORT), CatAPIHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server.")
    httpd.server_close()
