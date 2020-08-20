from cleanco import cleanco
from flask import Flask, jsonify, request  
app = Flask(__name__) 
@app.route('/') 
def hello_world(): 
    return 'Welcome!'

@app.route('/clean/company',methods = ['POST'])
def classify():
    if not request.json or not 'company' in request.json:
        abort(400)
    print(request.json)
    companyName = request.json['company']
    print(companyName)
    x = cleanco('salesbox llc')

    details = {
        'name': companyName,
        'clean_name': x.clean_name(),
        'business_type': x.type(),
        'country': x.country()
    }
    return jsonify(details),200
# main driver function 
if __name__ == '__main__':
    app.run() 