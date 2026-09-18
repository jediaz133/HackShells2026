from flask import Flask, render_template,Response, jsonify, make_response, request, redirect, url_for, stream_with_context
import os, imagezmq, cv2, time
# from tools import *
import tools, agent

app = Flask(__name__)


AIrequest = ""

@app.route("/", methods=["GET","POST"])
def home():
    global AIrequest
    setupTime = not os.path.isfile("/home/puffle/Documents/schoolll/Hackathons/HackShells 2026/static/userdata.json")

    # First time setup stuff
    if setupTime:


        # When they submit stuff
        if request.method == "POST":
            signedUpInfo = []
            for i in ["weight", "age", "height", "sex", "wpw", "workoutTime", "extra"]:
                signedUpInfo.append(request.form.get(i))
            tools.setup(signedUpInfo[0], signedUpInfo[1], signedUpInfo[2], signedUpInfo[3], signedUpInfo[4], signedUpInfo[5], signedUpInfo[6])
            
        toRender = render_template('setup.html')
        # toRender = toRender+"<script>document.getElementById('userRequest').innerHTML = 'Your Request: <br>"+str(requestForAI)+"';</script>"
        return toRender+"</html>"

    # For already joined members
    else:

        if request.method == "POST":
            image = request.files.get('image')

            if not os.path.isfile("image.jpg"):
                None
            else:
                image.save("image.jpg")

            toRender = render_template('general.html')
            
            AIrequest = request.form.get("requestForAI")
            for i in range(50):
                print(str(AIrequest))
            agent.currentRequest = True
        else:            
            toRender = render_template('general.html')
        # toRender = toRender+"<script>document.getElementById('userRequest').innerHTML = 'Your Request: <br>"+str(requestForAI)+"';</script>"
        return toRender+"</html>"    

@app.route('/aiResponse')
# def aiResponse():

def aiResponse():
    global AIrequest
    # Use Flask's Response object to stream the generator directly to the frontend
    if AIrequest != "":
        return Response(
            stream_with_context(agent.askAI(AIrequest)), 
            content_type='text/plain'
        )
    else:
        return ""

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0")
