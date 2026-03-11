from flask import Flask, request, jsonify
from myglobal import logger
import arduinocomm
import threading

"""
usage:
curl -X POST -H "Content-Type: application/json" \
  -d '{"action":"set_pompe","p":0,"t":16}' \
  http://localhost:5001/command
"""


app = Flask(__name__)

@app.route('/command', methods=['POST'])
def handle_command():
    """
    Handle REST API commands and forward them to Arduino.
    
    Expected JSON payload:
    {
        "action": "set_pompe",
        "p": 0,
        "t": 16
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "No JSON payload"}), 400
        
        action = data.get("action")
        
        if action == "set_pompe":
            p = data.get("p")
            t = data.get("t")
            
            if p is None or t is None:
                return jsonify({
                    "status": "error", 
                    "message": "Missing parameters: p and t required"
                }), 400
            
            command = f"/setpompe?p={p}&t={t}"
            logger.info(f"REST API: forwarding command to Arduino: {command}")
            arduinocomm.send_cmd(command)
            
            return jsonify({
                "status": "success",
                "command": command
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Unknown action: {action}"
            }), 400
            
    except Exception as e:
        logger.error(f"REST API error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def run_api(host='0.0.0.0', port=5001, debug=False):
    """Run the Flask REST API server in a separate thread."""
    logger.info(f"Starting Arduino REST API on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    # setup can be commented out if we want to fake the command 
    #arduinocomm.setup()
    run_api(port=5001, debug=True)