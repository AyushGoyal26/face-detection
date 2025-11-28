# -----------------------------
# 🧠 Age & Gender Prediction App
# -----------------------------

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# -----------------------------
# ✅ Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Age & Gender Prediction", page_icon="🧠", layout="centered")
st.title("🧠 Age & Gender Prediction App")
st.write("Upload or capture an image to predict **Age Group** and **Gender** using a Deep Learning model.")

# -----------------------------
# ✅ Load Pre-Trained Model
# -----------------------------
MODEL_PATH = r"C:\Users\vansh\Downloads\project\python\models\new_testing.h5"  # 🟢 Put your model file name here
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load model. Please check path.\n\n**Error:** {e}")
    st.stop()

# -----------------------------
# ✅ Labels
# -----------------------------
gender_labels = ["Male", "Female"]
age_labels = ["0–10", "11–20", "21–30", "31–40", "41–50", "51–60", "61+"]

# -----------------------------
# ✅ Prediction Function
# -----------------------------
def predict(image):
    try:
        img = image.resize((128, 128))  # resize to model input
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Get model outputs
        preds = model.predict(img_array)
        gender_pred, age_pred = preds[0], preds[1]

        gender = gender_labels[int(round(gender_pred[0][0]))]
        age = age_labels[np.argmax(age_pred[0])]

        return gender, age
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None, None

# -----------------------------
# ✅ Input Options
# -----------------------------
option = st.radio("Choose Input Type:", ["📸 Use Camera", "📁 Upload Image"])

# -----------------------------
# 📸 Camera Input
# -----------------------------
if option == "📸 Use Camera":
    camera_image = st.camera_input("Take a photo")

    if camera_image is not None:
        image = Image.open(io.BytesIO(camera_image.getvalue())).convert("RGB")
        st.image(image, caption="Captured Image", use_container_width=True)
        st.write("⏳ Processing image...")

        gender, age = predict(image)
        if gender and age:
            st.success(f"**Predicted Gender:** {gender}")
            st.success(f"**Predicted Age Group:** {age}")

# -----------------------------
# 📁 Upload Input
# -----------------------------
elif option == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.write("⏳ Processing image...")

        gender, age = predict(image)
        if gender and age:
            st.success(f"**Predicted Gender:** {gender}")
            st.success(f"**Predicted Age Group:** {age}")
    else:
        st.info("Please upload an image to start prediction.")
