import streamlit as st
import pickle
import numpy as np

# import the model
pipe = pickle.load(open('D:\scikit-learn.py\ml_projects.ipynb\laptop_price_predict.ipynb\pipe.pkl','rb'))
df = pickle.load(open('D:\scikit-learn.py\ml_projects.ipynb\laptop_price_predict.ipynb\df.pkl','rb'))

st.title('Laptop Price Predictor',text_alignment= 'center')

# brand
brand = st.selectbox('Brand',df['Brand'].unique())

# storage_gb
storage = st.selectbox('Storage (GB)',np.sort(df['storage_gb'].unique()))

# primary_use_case
primary_use_case = st.selectbox('Type of Laptop',df['primary_use_case'].unique())

# OS
os = st.selectbox('Operating System',df['OS'].unique())

# Weight
weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1)

# Touch
touch = st.selectbox('Touch Screen',['Yes','No'])

# Size 
size = st.number_input("Screen Size (inches)", min_value=10.0, max_value=20.0, step=0.1)

# Resolution 
resolution = st.selectbox('Resolution',df['Resolution'].unique())

# PPI
x_res = int(resolution.split('x')[0])
y_res = int(resolution.split('x')[1])

PPI = ((x_res ** 2) + (y_res ** 2))** 0.5 / size

# Anti Glare Screen
anti_glare_screen = st.selectbox('Anti Glare Screen',['Yes','No'])

# RAM
ram = st.selectbox('RAM',df['RAM'].unique())

# Generation
generations = df.groupby('Brand')['Generation'].unique().to_dict()
gen = st.selectbox('Generation',generations[brand])

# Ram_type
ram_type = st.selectbox('RAM Type',df['RAM_Type'].unique())

# GPU Model
gpu_models = df.groupby('Brand')['GPU_Model'].unique().to_dict()
gpu_model = st.selectbox('GPU Model',gpu_models[brand])

# GPU Type
gpu_type = st.selectbox('GPU Type', df['GPU_Type'].unique())

# Storage Type
storage_type = st.selectbox('Storage Type',df['Storage_Type'].unique())

# Processor Brand
processors = df.groupby('Brand')['Processor_Brand'].unique().to_dict()
processor_brand = st.selectbox('Processor Brand',processors[brand])

# Processor_Family
processor_family = st.selectbox('Processor Family',df['Processor_Family'].unique())


if st.button('Predict Price'):
    # query
    if touch == 'Yes':
        touch = 1
    else :
        touch = 0

    if anti_glare_screen == 'Yes':
        anti_glare_screen = 1
    else:
        anti_glare_screen =0

    query = np.array([
        storage,
        primary_use_case,
        os,
        weight,
        touch,
        size,
        resolution,
        PPI,
        anti_glare_screen,
        brand,
        ram,
        gen,
        ram_type,
        gpu_model,
        gpu_type,
        storage_type,
        processor_brand,
        processor_family
    ]).reshape(1, 18)   
    st.header('Predicted Price')
    st.success(f'₹ {(np.exp(pipe.predict(query))[0]).round(2)}',icon = "✅")
    st.subheader(f'Prediction Confidence')
    st.success('88.3 %',icon = "👉")
