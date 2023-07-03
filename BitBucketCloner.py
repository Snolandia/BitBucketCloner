import requests
import os
from git import Repo
from requests.auth import HTTPBasicAuth

############################################################
# Follow directions here to create a consumer https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/#OAuthonBitbucketCloud-Cloningarepositorywithanaccesstoken
# Set callback url to https://nothing
# Set to a private consumer
# Enable read permissions
# Needs to have something in the box, doesnt matter if its valid or not. 
# Then set the following three variables appropriately, with the new consumer created being the key and secret
############################################################

key = "key"
secret = "secret"
repoFileLocation = "folder location"

keySecret = HTTPBasicAuth(key,secret)
data = { 'grant_type': 'client_credentials'}
accessTokenRequest = requests.post('https://bitbucket.org/site/oauth2/access_token', data=data, auth=(key, secret))
accessToken = accessTokenRequest.json()["access_token"] 
headers={'Authorization': 'Bearer '+ accessToken}

userRepos = "https://api.bitbucket.org/2.0/user/permissions/repositories"

repoList = []
getUserRepos = requests.get(userRepos,headers=headers)
repos = getUserRepos.json()
repoList.append(repos)

while "next" in repos:
    getUserRepos = requests.get(repos["next"], headers=headers)
    repos = getUserRepos.json()
    repoList.append(repos)

if len(repoList) > 0:
    print(" Repos found, attempting to clone, may take a while")
else:
    print("Error, no repos found, Auth correct?")

for repos in repoList:
    for repoName in repos["values"]:
        fullName = repoName["repository"]["full_name"]
        name = repoName["repository"]["name"]
        if os.path.exists(repoFileLocation + "\\" + fullName):
            print(fullName + " already exists, and therefore cloning was skipped.")
        else:
            cloneURLToken = f"https://x-token-auth:{accessToken}@bitbucket.org/{fullName}.git"
            Repo.clone_from(cloneURLToken, repoFileLocation + fullName)
            print(name + " was cloned to this folder : " + repoFileLocation + fullName)
        
print("Cloning of repos has finished")
