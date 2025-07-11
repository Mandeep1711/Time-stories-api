from flask import Flask
import json
import http.client
from collections import OrderedDict
from flask import Response
import re

app = Flask(__name__)

@app.route('/getTimeStories', methods=['GET'])
def get_time_stories():
    try:
        # Connect to time.com
        conn = http.client.HTTPSConnection("time.com")
        conn.request("GET", "/")
        response = conn.getresponse()
        
        if response.status != 200:
            conn.close()
            return Response({'error': 'Failed to fetch page'}), 500
            
        # Read and decode the HTML
        html = response.read().decode('utf-8')
        conn.close()
     
        unescaped = html.replace('\\"', '"').replace('\\/', '/')
        pattern = r'"title":"(.*?)".*?"path":"(\/[0-9]+\/[^"]+)"'
        matches = re.findall(pattern, unescaped)

        # Build the stories list
        stories = []
        seen_links = set()
        for title, path in matches:
            # Clean title
            title = title.strip()
            if not title or path in seen_links:
                continue
            seen_links.add(path)
            stories.append(OrderedDict([
                ('title', title.strip()),
                ('link','https://time.com' + path)
            ]))
            if len(stories) == 6:
                break

        
        return Response(json.dumps(stories, indent=2), mimetype='application/json')

    except Exception as e:
        return Response({'error': str(e)}), 500

if __name__ == '__main__':
        app.run(debug=True)