# Docker Instructions

**DISCLAIMER**: This guide extends upon the [Tensorflow Docker Guide](https://www.tensorflow.org/install/docker) so following their installation instructions and requirements is mandatory!

## Building the container image

Assuming you have installed docker and cloned this repository, you can build the container using

`docker build -t iannwtf .`

## Run the container

Once the container is done building run it with

`docker run -dp 8888:8888 -v "$PWD":/tf iannwtf`

We use the volume flag `-v "$PWD":/tf` to allow the container access to the current directory with all the homeworks.

If you have an NVIDIA graphics card and installed the respective toolkit you can run the container with GPU support using

`docker run --gpus all -dp 8888:8888 -v "$PWD":/tf iannwtf`

In week 08 Tensorboard was introduced which requires additional setup for our container. By default Tensorboard uses port 6006 so we need to forward that port as well.

`docker run -dp 8888:8888 -p 6006:6006 -v "$PWD":/tf iannwtf`

or

`docker run --gpus all -dp 8888:8888 -p 6006:6006 -v "$PWD":/tf iannwtf`

for the GPU variant.

## Accessing the Jupyter Server

You can find the server running at [localhost:8888](http://localhost:8888)

Get the ID of the currently running container via

`docker ps`

Then execute

`docker exec <your-container id> jupyter notebook list`

and copy the token.

## Permission errors when using the container

You might notice that git will complain when you try to add files to the repo. This is because files created in the container belong to the root user and you will need elevated privilages to work with them. A simple `chown` can help, but it might get tedious to do that everytime you used the container. So we pass the our current user:usergroup to use in the container.

`docker run --gpus all -dp 8888:8888 -p 6006:6006 -v "$PWD":/tf -u $(id -u ${USER}):$(id -g ${USER}) iannwtf`

# Using Tensorboard in Notebooks

Make sure the required port is exposed as described above. If you plan on using multiple Tensorboard instances in the same notebook, you will need to forward more ports in the container.

When calling the tensorboard magic, make sure to pass the `--bind_all` flag. Otherwise the notebook server will not be able to connect to the tensorboard server.

The Homework08 folder contains an example notebook taken from tensorflows documentation to illustrate the process.

# Setting a password

If you want to set custom password for your server instead of having to grab the randomized token everytime, you can pass a token via an docker environment variable when running the container

`-e JUPYTER_TOKEN=my_super_secure_password`

# Quitting the server and container

Once you shutdown the notebook server, the container will close as well.

Alternatively you can shutdown the container via `docker stop <your-container id>`