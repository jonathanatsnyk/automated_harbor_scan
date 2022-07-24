import requests
import json
import os
import subprocess 
from requests.auth import HTTPBasicAuth

#first request gets the projects 
repositories = []
# deepcode ignore AuthOverHttp: <please specify a reason of ignoring this>, deepcode ignore TLSCertVerificationDisabled: <please specify a reason of ignoring this>
# deepcode ignore AuthOverHttp: <please specify a reason of ignoring this>, deepcode ignore TLSCertVerificationDisabled: <please specify a reason of ignoring this>, deepcode ignore TLSCertVerificationDisabled: <please specify a reason of ignoring this>, deepcode ignore TLSCertVerificationDisabled: <please specify a reason of ignoring this>
res = requests.get('http://20.219.64.10/api/v2.0/projects', verify=False, auth=HTTPBasicAuth('admin', 'Test2130!'))


# now loop through the array and make a new request to get repositories for each project.
projects = json.loads(res.text)
for project in projects: 
    requestStr = "http://20.219.64.10/api/v2.0/projects/"+project['name']+"/repositories?page=1&page_size=10"

    # deepcode ignore TLSCertVerificationDisabled: <please specify a reason of ignoring this>
    projectData = requests.get(requestStr, verify=False, auth=HTTPBasicAuth('admin', 'Test2130!'))
    projectData = json.loads(projectData.text)
    for repository in projectData: 
        repositories.append(repository['name'])
  
#now get the artificats 
artifactsToScan = []
for repo in repositories: 

    repoArr = repo.split('/')
    project = repoArr[0]
    repository = repoArr[1]
    artifactRequestStr = "http://20.219.64.10/api/v2.0/projects/"+project+"/repositories/"+repository+"/artifacts"
    artifactData = requests.get(artifactRequestStr, verify=False, auth=HTTPBasicAuth('admin', 'Test2130!'))
   
    artifactData = artifactData.json()

    for artifact in artifactData: 
        tags = artifact['tags']
        #print(tags)
        for tag in tags: 
            if tag['name']=='prod_image':
                #artifactsToScan.append(artifact) 
                artifactsToScan.append({
                    'project':project,
                    'repository':repository,
                    'tag':'prod_image'
                })
              
                

for artifact in artifactsToScan:

    project = artifact["project"]
    repository = artifact["repository"]
    tag = artifact["tag"]

    dockerPullStr = "docker pull 20.219.64.10/"+project+"/"+repository+":"+tag
    snykContainerStr = 'snyk container monitor 20.219.64.10/'+project+'/'+repository+':'+tag 
    
    print('we are monitoring ',artifact)
    os.system(dockerPullStr)
    os.system('sleep 15')
    os.system(snykContainerStr)
