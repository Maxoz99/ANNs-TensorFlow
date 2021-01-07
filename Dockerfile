FROM tensorflow/tensorflow:latest-gpu-jupyter
RUN pip install tensorflow_datasets
RUN pip install scipy

