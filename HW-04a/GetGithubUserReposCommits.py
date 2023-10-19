# Ashley Foglia
# SSW 567 - Fall 2023
# HW 04a - Develop with the Perspective of the Tester in mind

from datetime import datetime
import re
import requests
from tabulate import tabulate

def get_user_repos_commits(userId: str, printList: bool = True, debug: bool = False) -> list:
    #Validate user ID input type and format
    if type(userId) != str:
        raise TypeError("Invalid input type: User ID must be a string")
    validUserIDPattern = "^[a-z\\d](?:[a-z\\d]|-(?=[a-z\\d])){0,38}$"
    if not re.search(validUserIDPattern, userId):
        raise ValueError("Invalid User ID format: User ID must match GitHub format")
    else:
        # URL Templates
        repoURL = "https://api.github.com/users/{id}/repos"
        commitURL = "https://api.github.com/repos/{id}/{repo}/commits?per_page=100&page={pagenum}"
        
        #Output variables
        requestStatusCode = 0
        repoList = list()
        try:
            # Get repo list
            if not debug:
                repoResponse = requests.get(repoURL.format(id = userId))
                requestStatusCode = repoResponse.status_code
                repoResponse.raise_for_status()
                repos = repoResponse.json()
            else:
                requestStatusCode = 200
                repos = []
                
            for repo in repos:
                repoName = repo["name"]
                try:
                    # Get commit count for repo
                    got_all = False
                    max_get = 10
                    repoCommits = 0
                    while not got_all and pageNum <= max_get:
                        commitResponse = requests.get(commitURL.format(id = userId, repo = repoName, pagenum = pageNum))
                        requestStatusCode = max(requestStatusCode, commitResponse.status_code)
                        commitResponse.raise_for_status()
                        repoCommits += len(commitResponse.json())
                        pageNum = pageNum + 1
                        if (len(commitResponse.json()) > 0 and len(commitResponse.json()[-1]["parents"]) == 0):
                            got_all = True
                    #Add repo name and commit count to output list
                    repoList.append((repoName, repoCommits))
                except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as error:
                    raise error

            # Print tabulated results if specified
            if printList:
                print(tabulate(repoList, headers=["Repo Name", "Commits"], tablefmt="fancy_outline"))
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.RequestException) as error:
            raise error
        except Exception as ex:
            raise ex
        
        # Return repo list with most severe response status code
        return repoList
