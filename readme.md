Prequisities: 

- Python 3 installed on your machine
- Docker running and installed on your machine 
- You are signed into your harbor container registry after running docker login 

Change the below script values in the app.py file: 

harbor_username ='[your harbor username here]'

harbor_password ='[your harbor password here]'

harbor_instance_url='[url where your harbor server is located]'

harbor_address_tag='[harbor address prefix you use to tag your images when you built them with docker tag harbor_address/project/repo, before they were pushed]'

tag_to_detect='[tag you have attached to the container images you want snyk to scan]'

Description: 

This script will run and cycle through all your projects and repos, and find container images that have a specific tag, e.g snyk_scan or some other value you specify in the tag_to_detect parameter. It will then scan those images using snyk container monitor. Useful for automating the scanning of large number of harbor container registry images without manuallly selecting images to scan. 

You can run the script by cding into the main directory and running: python3 app.py

Make sure you are signed into harbor before running the above script. 

