import os
import sys

from flask import Flask, request, render_template, jsonify

from db.db import Crud
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData

# redundant assignment because of AWS deployment
application = Flask(__name__)
app = application

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # else part is going to be POST request
        # fetching data from form
        
        # form validation
        try:
            carat_value = float(request.form.get("carat"))
            depth_value = float(request.form.get("depth"))
            table_value = float(request.form.get("table"))
            x_value = float(request.form.get("x"))
            y_value = float(request.form.get("y"))
            z_value = float(request.form.get("z"))
            
        except Exception as e:
            return render_template("form.html", exception = e) 
        
        
        data = CustomData(
            carat = carat_value,
            depth = depth_value,
            table = table_value,
            x = x_value,
            y = y_value,
            z = z_value,
            cut = request.form.get("cut"),
            color = request.form.get("color"),
            clarity = request.form.get("clarity")
        )
        
        final_df = data.get_data_as_dataframe()
        prediction_pipeline = PredictPipeline
        
        pred = prediction_pipeline.predict(self=prediction_pipeline, features=final_df)
        result = [round(pred[0],2), final_df]

        db_dict_result = {
            result[1].columns[0] : final_df.iloc[0][0],
            result[1].columns[1] : final_df.iloc[0][1],
            result[1].columns[2] : final_df.iloc[0][2],
            result[1].columns[3] : final_df.iloc[0][3],
            result[1].columns[4] : final_df.iloc[0][4],
            result[1].columns[5] : final_df.iloc[0][5],
            result[1].columns[6] : final_df.iloc[0][6],
            result[1].columns[7] : final_df.iloc[0][7],
            result[1].columns[8] : final_df.iloc[0][8],
            'price' : result[0]   
       }

        # db integrated database push code here
        db_object = Crud
        db_object.insert(self=db_object, result=db_dict_result)

        return render_template("result.html", final_result=result)
    
    else:
        return render_template("form.html")
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6969, debug=True)