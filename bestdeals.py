from flask import Flask

app = Flask(__name__)

@app.route('/scrap-data', methods=['GET'])
def scrap_data():
    return 'Hello from scrappy service, nice to meet you.'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9020)
