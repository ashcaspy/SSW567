# Ashley Foglia
# SSW 567 - Fall 2023
# HW 04a - Develop with the Perspective of the Tester in mind

from datetime import datetime
import requests
import pytest
from tabulate import tabulate
from GetGithubUserReposCommits import get_user_repos_commits

# Define Test Cases

# Test invalid input types
invalidInputTypes = [None, 123, 4.5, ["item1", "item2"], ("item1", "item2")]
@pytest.mark.parametrize("invalid_input_type", invalidInputTypes)
def test_invalid_input_types(invalid_input_type):
    with pytest.raises(TypeError):
        get_user_repos_commits(invalid_input_type, debug=True)

# Test invalid user ID formats
invalidUserIDFormats = ["", "-abc", "abc-", " ", "test with spaces", "test.period", "test&common$special#chars%abc" "thisisaverylongstringthatisgreaterthan38charactersinlength"]
@pytest.mark.parametrize("invalid_user_id_format", invalidUserIDFormats)
def test_invalid_input_types(invalid_user_id_format):
    with pytest.raises(ValueError):
        get_user_repos_commits(invalid_user_id_format, debug=True)

#Test valid user ID formats (not necessarily valid user IDs)
validUserIDFormats = ["ashcaspy", "richkempinski", "user123", ""]
@pytest.mark.parametrize("valid_user_id_format", validUserIDFormats)
def test_valid_user_id(valid_user_id_format):
    try:
        get_user_repos_commits(valid_user_id_format, False, True)
    except ValueError as ve:
        pytest.fail(valid_user_id_format + " raised a ValueError.")
    except Exception as ex: 
        pytest.fail(valid_user_id_format + " raised an unexpected error.")

# Test valid github user IDs
validUserIDs = ["ashcaspy", "public-apis"]
#validUserIDs = ["ashcaspy", "richkempinski", "public-apis"] #Exclude richkempinski due to API request rate limits
@pytest.mark.parametrize("valid_user_id", validUserIDs)
def test_valid_user_id(valid_user_id):
    try:
        get_user_repos_commits(valid_user_id, False)
    except requests.exceptions.HTTPError as err:
        assert err.response.status_code != 404, valid_user_id + " is not a valid user ID."
        assert err.response.status_code != 403, "Access denied. Retry at: " + str(datetime.fromtimestamp(int(err.response.headers["X-RateLimit-Reset"])))
    except Exception as ex: 
        pytest.fail(valid_user_id + " raised an unexpected error.")
        
# Test output values
def test_output_value():
    try:
        repoList = get_user_repos_commits("public-apis", False)
    except requests.exceptions.HTTPError as err:
        assert err.response.status_code != 403, "Access denied. Retry at: " + str(datetime.fromtimestamp(int(err.response.headers["X-RateLimit-Reset"])))
    assert len(repoList) == 1 and repoList[0][0] == "public-apis" and repoList[0][1] >= 1000, "Incorrect data output"

# Test Print Functionality (without making API call)
def test_print_implicit(capfd):
    try:
        get_user_repos_commits("public-apis", debug=True)
    except: pass
    out, err = capfd.readouterr()
    assert out != ""
def test_print_explicit(capfd):
    try:
        get_user_repos_commits("public-apis", True, debug=True)
    except: pass
    out, err = capfd.readouterr()
    assert out != ""
    
def test_print_none(capfd):
    try:
        get_user_repos_commits("public-apis", False, debug=True)
    except: pass
    out, err = capfd.readouterr()
    assert out == ""
