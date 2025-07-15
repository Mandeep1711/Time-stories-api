rom flask import Flask, Response
import json
import http.client
from collections import OrderedDict

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
            return Response(json.dumps({'error': 'Failed to fetch page'}), status=500, mimetype='application/json')

      
        html = response.read().decode('utf-8')
        conn.close()

       
        unescaped = html.replace('\\"', '"').replace('\\/', '/')

        
        stories = []
        seen_links = set()
        index = 0

        while len(stories) < 6:
            title_start = unescaped.find('"title":"', index)

            if title_start == -1:
                break
            title_end = unescaped.find('"', title_start + 9)
            title = unescaped[title_start + 9:title_end].strip()

            path_start = unescaped.find('"path":"', title_end)
            if path_start == -1:
                break
            path_end = unescaped.find('"', path_start + 8)
            path = unescaped[path_start + 8:path_end]

            index = path_end  

            
            if not title or not path or path in seen_links:
                continue

            seen_links.add(path)
            stories.append(OrderedDict([
                ('title', title),
                ('link', 'https://time.com' + path)
            ]))

        return Response(json.dumps(stories, indent=2), mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
