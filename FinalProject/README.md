# Our Final Project: Artistic Style Transfer

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/15S9DsWTqz4iDyIgUqkdvdC2dL321NhOC)

# Overview

t.b.d.

# Setup the graphical application

Clone the repository 

`git clone https://github.com/Maxoz99/ANNs-TensorFlow.git`

Change into the `FinalProject/style_transfer` folder

`cd ANNs-Tensorflow/FinalProject/style_transfer`

Create the environment

`conda env create -f environment.yml`

Activate the environment

`conda activate style_transfer_env`

Run the application

`python src/main.py`

# Known Issues

When running the application an Autograph warning might occur related to a packaging issue with a Tensorflow dependency. See [this](https://github.com/tensorflow/tensorflow/issues/44146) issue. It is expected to be fixed in Tensorflow 2.5.0. We encountered that bug only in the conda environment but not with the local Python installation.
