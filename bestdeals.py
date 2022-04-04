from flask import Flask

app = Flask(__name__)

@app.route('/scrap-data', methods=['GET'])
def scrap_data():
    return 'Hello from scrappy service, nice to meet you.Hii chetan'
    
if __name__ == '__main__':
    app.run()
