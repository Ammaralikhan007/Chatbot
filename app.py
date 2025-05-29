#render template is used to render html page
#It automatically looks inside the /templates folder for your .html files.
# requests lets you access data sent from the frontend.
# jsonify converts a Python dictionary or list into a JSON response so the frontend JavaScript can read.


from flask import Flask, render_template, request , jsonify
from chat import get_response

app = Flask(__name__)

#first we need to take user to the main page to make them see what we want to show them
@app.get("/")
def index_get():
    return render_template("base.html")


#when the client or browser send post request to the predict run this function
#when the user will send a message the js will send the post request to predict and flask catches it so this is when it is triggered 
#they will send message from js front end to flask backend 
#this is a backend endpoint
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    #to do : check if text is valid
    response = get_response(text)
    #now send back to the user
    message = {"answer" :response}
    return jsonify(message)



if __name__ == "__main__":
    app.run(debug=True)








