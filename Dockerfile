FROM tensorflow/tensorflow:latest-gpu-jupyter
LABEL Name=tf Version=0.0.1
RUN pip install tensorflow_datasets

