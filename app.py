from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
import time

app = Flask(__name__)

# --- Home & Main Pages ---
@app.route("/")
@app.route("/index")
def index():
    data = {"header": "true"}
    return render_template("home/index.html", **data)

@app.route("/contact")
def contact():
    data = {"header": "true", "footer": "true"}
    return render_template("contact.html", **data)

@app.route("/privacy-policy")
def privacyPolicy():
    data = {"header": "true"}
    return render_template("privacyPolicy.html", **data)

@app.route("/service-single2")
def serviceSingle2():
    return render_template("serviceSingle2.html")

@app.route("/service-single3")
def serviceSingle3():
    return render_template("serviceSingle3.html")

@app.route("/service-single4")
def serviceSingle4():
    return render_template("serviceSingle4.html")

@app.route("/terms")
def terms():
    data = {"header": "true"}
    return render_template("terms.html", **data)

# --- Pages ---
@app.route("/about")
def about():
    data = {"footer": "true"}
    return render_template("pages/about.html", **data)

@app.route("/book-demo")
def bookDemo():
    data = {"header": "true"}
    return render_template("pages/bookDemo.html", **data)

@app.route("/faq")
def faq():
    data = {"header": "true"}
    return render_template("pages/faq.html", **data)

@app.route("/free")
def free():
    data = {"header": "true"}
    return render_template("pages/free.html", **data)

@app.route("/predict")
def predict():
    data = {"header": "true"}
    return render_template("pages/predict.html", **data)

@app.route("/page-error")
def pageError():
    data = {}
    return render_template("pages/pageError.html", **data)

@app.route("/pricing")
def pricing():
    data = {"header": "true", "footer": "true"}
    return render_template("pages/pricing.html", **data)

@app.route("/team")
def team():
    data = {"footer": "true"}
    return render_template("pages/team.html", **data)

# --- Blog ---
@app.route("/blog")
def blog():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blog.html", **data)

@app.route("/blog-details")
def blogDetails():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blogDetails.html", **data)

@app.route("/blog-grid")
def blogGrid():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blogGrid.html", **data)

@app.route("/blog-grid-2")
def blogGrid2():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blogGrid2.html", **data)

@app.route("/blog-grid-3")
def blogGrid3():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blogGrid3.html", **data)

@app.route("/blog-left-Sidebar")
def blogLeftSidebar():
    data = {"header": "true", "footer": "true"}
    return render_template("blog/blogLeftSidebar.html", **data)

# --- Services ---
@app.route("/emailMarketing")
def emailMarketing():
    data = {"header": "true", "footer": "true"}
    return render_template("services/emailMarketing.html", **data)

@app.route("/influencerMarketing")
def influencerMarketing():
    data = {"header": "true", "footer": "true"}
    return render_template("services/influencerMarketing.html", **data)

@app.route("/service")
def service():
    data = {"header": "true", "footer": "true"}
    return render_template("services/service.html", **data)

@app.route("/serviceSingle")
def serviceSingle():
    data = {"header": "true", "footer": "true"}
    return render_template("services/serviceSingle.html", **data)

@app.route("/socialMediaMarketing")
def socialMediaMarketing():
    data = {"header": "true", "footer": "true"}
    return render_template("services/socialMediaMarketing.html", **data)

# --- Work ---
@app.route("/caseStudies")
def caseStudies():
    data = {"footer": "true"}
    return render_template("work/caseStudies.html", **data)

@app.route("/singleCaseStudies")
def singleCaseStudies():
    data = {"header": "true", "footer": "true"}
    return render_template("work/singleCaseStudies.html", **data)

# --- Error Handler ---
@app.errorhandler(404)
def page_not_found(error):
    return render_template("pages/pageError.html"), 404

# Model paths and details
MODEL_PATHS = {
    'brain-tumor': r'C:/Users/Batu/Documents/mediainbeta/models/effvb1/effvb1.h5',
    'pneumonia': r'C:/Users/Batu/Documents/mediainbeta/models/resnet50_1/resnet50_best_model_09_0.9954.h5',
    'skin-cancer': r'C:/Users/Batu/Documents/mediainbeta/models/resnet50_2/resnet50_best_model.h5',
    'diabetic-retinopathy': r'C:/Users/Batu/Documents/mediainbeta/models/effvb4/effvb4_best_model_05_0.5913.h5'
}
MODEL_INPUTS = {
    'brain-tumor': (224, 224),
    'pneumonia': (224, 224),
    'skin-cancer': (224, 224),
    'diabetic-retinopathy': (380, 380)
}
MODEL_TYPE = {
    'brain-tumor': 'binary',
    'pneumonia': 'binary',
    'skin-cancer': 'binary',
    'diabetic-retinopathy': 'categorical'
}
DR_CLASSES = ['Healthy', 'Mild DR', 'Moderate DR', 'Proliferate DR', 'Severe DR']

# --- Model Loading at Startup ---
print('Loading models...')
LOADED_MODELS = {}
for key, path in MODEL_PATHS.items():
    try:
        LOADED_MODELS[key] = tf.keras.models.load_model(path)
        print(f"{key.replace('-', ' ').title()} model loaded.")
    except Exception as e:
        print(f"Error loading {key} model: {e}")
        LOADED_MODELS[key] = None

# --- Model-specific Prediction Functions ---
def predict_brain_tumor(img):
    start_time = time.time()
    try:
        img = img.resize((224, 224)).convert('RGB')
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        pred = LOADED_MODELS['brain-tumor'].predict(arr)[0][0]
        label = 'Tumor' if pred >= 0.3 else 'Healthy'
        return {
            'probability': float(pred),
            'classification': label,
            'prediction_time': round(time.time() - start_time, 2)
        }
    except Exception as e:
        print(f"Brain tumor prediction error: {str(e)}")
        return {'error': str(e)}

def predict_pneumonia(img):
    start_time = time.time()
    try:
        img = img.resize((224, 224)).convert('RGB')
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        pred = LOADED_MODELS['pneumonia'].predict(arr)[0][0]
        label = 'Pneumonia Detected' if pred >= 0.3 else 'Healthy'
        return {
            'probability': float(pred),
            'classification': label,
            'prediction_time': round(time.time() - start_time, 2)
        }
    except Exception as e:
        print(f"Pneumonia prediction error: {str(e)}")
        return {'error': str(e)}

def predict_skin_cancer(img):
    start_time = time.time()
    try:
        img = img.resize((224, 224)).convert('RGB')
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        pred = LOADED_MODELS['skin-cancer'].predict(arr)[0][0]
        label = 'Malignant' if pred >= 0.3 else 'Benign'
        return {
            'probability': float(pred),
            'classification': label,
            'prediction_time': round(time.time() - start_time, 2)
        }
    except Exception as e:
        print(f"Skin cancer prediction error: {str(e)}")
        return {'error': str(e)}

def predict_diabetic_retinopathy(img):
    start_time = time.time()
    try:
        img = img.resize((380, 380)).convert('RGB')
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        preds = LOADED_MODELS['diabetic-retinopathy'].predict(arr)[0]
        idx = int(np.argmax(preds))
        conf = float(np.max(preds))
        stages = ['Normal', 'Mild', 'Moderate', 'Severe', 'Proliferative']
        return {
            'class': stages[idx],
            'confidence': conf,
            'class_index': idx,
            'classification': stages[idx],
            'prediction_time': round(time.time() - start_time, 2)
        }
    except Exception as e:
        print(f"Diabetic retinopathy prediction error: {str(e)}")
        return {'error': str(e)}

@app.route('/predict', methods=['POST'])
def predict_api():
    try:
        if 'medical_image' not in request.files or 'selected_model' not in request.form:
            return jsonify({'error': 'Image and model selection required.'}), 400
        
        file = request.files['medical_image']
        model_key = request.form['selected_model']
        
        if model_key not in LOADED_MODELS:
            return jsonify({'error': 'Invalid model selection.'}), 400
        
        if LOADED_MODELS[model_key] is None:
            return jsonify({'error': f"Model '{model_key}' failed to load. Please contact the administrator."}), 500
        
        img = Image.open(file.stream)
        
        # Model tahminini yap
        if model_key == 'brain-tumor':
            result = predict_brain_tumor(img)
        elif model_key == 'pneumonia':
            result = predict_pneumonia(img)
        elif model_key == 'skin-cancer':
            result = predict_skin_cancer(img)
        elif model_key == 'diabetic-retinopathy':
            result = predict_diabetic_retinopathy(img)
        else:
            return jsonify({'error': 'Unknown model.'}), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
