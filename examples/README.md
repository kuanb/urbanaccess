# Up and running via Docker
Navigate to the root directory of your cloned version of this repo. Typing `ls` should show you all files in the directory, including the `Dockerfile` for this repo. Run `docker build urbanaccess .` to create an image based off of this `Dockerfile`. Once complete, you can now create a container based off of this image.

Let's create a container and leave it running so that we can explore it's contents. To do this, run `docker run -d urbanaccess tail -f /dev/null` in your command line. Now, if you enter `docker ps`, you should be able to see that container listed as running. Under the `NAMES` section, you will see that the container has been given an arbitrary name. The container also has an alphanumeric `CONTAINER ID`. Copy that name and paste it in the following command: `docker rename [container_id] urbanaccess` where `container_id` is the copied alphanumeric id. Running `docker ps` will show you that the arbitrary name has been replaced with `urbanaccess`.

We can now open a bash shell in that Docker container via the following command: `docker exec -it urbanaccess bash`.

Recap of the steps we have taken so far:
```
docker build urbanaccess .
docker run -d urbanaccess tail -f /dev/null
docker rename [container_id] urbanaccess
docker exec -it urbanaccess bash
```

# Executing the script
Feel free to either run `examples/example.py` or follow along and enter in each step yourself to understand the steps involved in running through a typical UrbanAccess workflow.