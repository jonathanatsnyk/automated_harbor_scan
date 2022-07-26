import requests
import json
import os
import subprocess 
from requests.auth import HTTPBasicAuth

#set required credentials and initial variables
harbor_username ='<your harbor username here>'


harbor_password ='<your harbor password here>'

harbor_instance_url='<url where your harbor server is located>'

harbor_address_tag='<harbor address prefix you use to tag your images when you built them with docker tag harbor_address/project/repo>'

tag_to_detect='<tag you have attached to the container images you want snyk to scan>'

#first request gets the projects 
repositories = []


res = requests.get(harbor_instance_url+'/api/v2.0/projects', auth=HTTPBasicAuth(harbor_username, harbor_password))


# now loop through the array and make a new request to get repositories for each project.
projects = json.loads(res.text)
for project in projects: 
    requestStr = harbor_instance_url+"/api/v2.0/projects/"+project['name']+"/repositories?page=1&page_size=10"

    
    projectData = requests.get(requestStr, auth=HTTPBasicAuth(harbor_username, harbor_password))
    projectData = json.loads(projectData.text)
    for repository in projectData: 
        repositories.append(repository['name'])
  
#now get the artificats 
artifactsToScan = []
for repo in repositories: 

    repoArr = repo.split('/')
    project = repoArr[0]
    repository = repoArr[1]
    artifactRequestStr = harbor_instance_url+"/api/v2.0/projects/"+project+"/repositories/"+repository+"/artifacts"
    artifactData = requests.get(artifactRequestStr, auth=HTTPBasicAuth(harbor_username, harbor_password))
   
    artifactData = artifactData.json()

    for artifact in artifactData: 
        tags = artifact['tags']
        #print(tags)
        for tag in tags: 
            if tag['name']==tag_to_detect:
                #artifactsToScan.append(artifact) 
                artifactsToScan.append({
                    'project':project,
                    'repository':repository,
                    'tag':tag_to_detect
                })
              
                

for artifact in artifactsToScan:

    project = artifact["project"]
    repository = artifact["repository"]
    tag = artifact["tag"]

    dockerPullStr = "docker pull "+harbor_address_tag+"/"+project+"/"+repository+":"+tag
    snykContainerStr = "snyk container monitor "+harbor_address_tag+'/'+project+'/'+repository+':'+tag 
    
    print('we are monitoring ',artifact)
    os.system(dockerPullStr)
    os.system('sleep 15')
    os.system(snykContainerStr)
