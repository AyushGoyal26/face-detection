# -----------------------------
# 🧠 Age & Gender Prediction App
# -----------------------------

# 🔹 Import libraries
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


st.set_page_config(page_title="Age & Gender Prediction", page_icon="🧠", layout="centered")

# 🔹 App title
st.title("🧠 Age & Gender Prediction App")

# 🔹 Load pre-trained model
MODEL_PATH = r"C:\Users\vansh\Downloads\project\python\models\new_refined.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# 🔹 Define labels
gender_labels = ["Male", "Female"]
age_labels = ["0-5", "6-12", "13-20", "21-30", "31-45", "46-60", "60+"]

# 🔹 Prediction function
def predict(image):
    img = image.resize((128, 128))  # ✅ Match model input
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    # Handle model output structure
    if isinstance(predictions, list) and len(predictions) == 2:
        gender_pred = gender_labels[np.argmax(predictions[0])]
        age_pred = age_labels[np.argmax(predictions[1])]
    else:
        gender_pred = gender_labels[np.argmax(predictions[0, :2])]
        age_pred = age_labels[np.argmax(predictions[0, 2:])]

    return gender_pred, age_pred

# 🔹 Option to choose input type
option = st.radio("Choose Input Type:", ["📸 Use Camera", "📁 Upload Image"])

if option == "📸 Use Camera":
    camera_image = st.camera_input("Take a photo")

    if camera_image is not None:
        image = Image.open(camera_image).convert("RGB")
        st.image(image, caption="Captured Image", use_container_width=True)
        st.write("⏳ Processing image...")

        gender, age = predict(image)

        st.success(f"**Predicted Gender:** {gender}")
        st.success(f"**Predicted Age Group:** {age}")

elif option == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.write("⏳ Processing image...")

        gender, age = predict(image)

        st.success(f"**Predicted Gender:** {gender}")
        st.success(f"**Predicted Age Group:** {age}")

    else:
        st.info("Please upload an image to start prediction.")
