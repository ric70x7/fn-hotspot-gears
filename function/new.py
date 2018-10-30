from flask import Flask, render_template, request
#from wtforms import Form, TextAreaField, validators
import pandas as pd
import numpy as np
import json
import sys
import os

# Find machine where the app is being run
with open('where.txt') as _f:
    I_am_in = _f.read()

# Get wd where flask is being run
# This is because I'm not installing it just pulling the code
cwd = os.path.abspath(os.path.dirname('app.py'))
sys.path.append('../disarm-gears/') # Append repo location

from disarm_gears.chain_drives.prototypes import adaptive_prototype_0
from disarm_gears.chain_drives.prototypes import sentinel

app = Flask(__name__)

# This handles the NTD service
@app.route('/ntd', methods=['POST'])
def post_route():
    if request.method == 'POST':
        json_data = request.get_json()
        json_data = json.loads(json_data)
        region_data = pd.DataFrame(json_data['region_definition'])
        train_data = pd.DataFrame(json_data['train_data'])

        x_frame = np.array(region_data[['lng', 'lat']])
        x_id = np.array(region_data['id'])
        x_coords = np.array(train_data[['lng', 'lat']])
        n_trials = np.array(train_data['n_trials'])
        n_positive = np.array(train_data['n_positive'])
        threshold = json_data['request_parameters']['threshold']

        response = adaptive_prototype_0(x_frame=x_frame, x_id=x_id,
                                        x_coords=x_coords,
                                        n_positive=n_positive,
                                        n_trials=n_trials,
                                        threshold=threshold,
                                        covariate_layers=None)
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
