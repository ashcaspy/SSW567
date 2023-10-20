# Ashley Foglia
# SSW 567 - Fall 2023
# HW 04a - Develop with the Perspective of the Tester in mind

Test functions for the get_user_repos_commits function

"""

import itertools
from unittest.mock import patch, Mock
from tabulate import tabulate
import pytest
import requests
from GetGithubUserReposCommits import get_user_repos_commits

class TestGetGithubUserReposCommits:
    """Tests the get_user_repos_commits function in the GetGithubUserReposCommits module"""
    # Set up mocked json output
    users = [
        {"name":"user1", "commitcounts":[]},
        {"name":"user2", "commitcounts":[1]*5},
        {"name":"user3", "commitcounts":[5]*5},
        {"name":"user4", "commitcounts":[1]*2+[20]*6+[100]*1+[20]*1}
    ]
    userRepos = {}
    repoCommits = {}
    for user in users:
        repoJson = [(cc, {"name": "repo"+str(i+1).zfill(2)})
                    for i, cc in enumerate(user["commitcounts"])]
        userRepos[user["name"]] = [repo[1] for repo in repoJson]
        for repo in repoJson:
            commitJson = []
            for j, c in enumerate(itertools.repeat([repo[0]], repo[0])):
                commitItem = {"sha": j+1, "parents":[] if j == 0 else [j]}
                commitJson.append(commitItem)
            repoCommits[(user["name"], repo[1]["name"])] = commitJson

    invalidInputTypes = [None, 123, 4.5, ["item1", "item2"], ("item1", "item2")]
    invalidUserIDFormats = ["", "-abc", "abc-", " ", "test with spaces", "test.period"
                            , "test&common$special#chars%abc"
                            , "thisisaverylongstringthatisgreaterthan38charactersinlength"]
    validUserIDFormats = ["user1", "user2", "user3", "user4", "testuser123"]
    validUserIDs = ["user1", "user2", "user3", "user4"]

    # Test invalid input types
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("invalid_input_type", invalidInputTypes)
    def test_invalid_input_types(self, mock_get, invalid_input_type):
        """Tests that invalid input types throw a TypeError"""
        mock_get.side_effect = requests.exceptions.HTTPError
        with pytest.raises(TypeError):
            get_user_repos_commits(invalid_input_type)

    # Test invalid user ID formats
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", invalidUserIDFormats)
    def test_invalid_user_id_format(self, mock_get, user_id):
        """Tests that user id strings in an invalid format throw a ValueError"""
        mock_get.side_effect = requests.exceptions.HTTPError
        with pytest.raises(ValueError):
            get_user_repos_commits(user_id)

    #Test valid user ID formats (not necessarily valid user IDs)
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDFormats)
    def test_valid_user_id_format(self, mock_get, user_id):
        """Tests that user id strings in a valid format do not throw a ValueError"""
        if user_id in self.userRepos:
            rc = []
            for user_repo in self.userRepos[user_id]:
                rc.extend([self.repoCommits[repoCommit]
                           for repoCommit in self.repoCommits.items()
                           if repoCommit == (user_id, user_repo["name"])])
            mock_get.side_effects = [self.userRepos[user_id]] + rc
        else:
            mock_get.side_effect = requests.exceptions.HTTPError

        try:
            get_user_repos_commits(user_id, False)
        except ValueError:
            pytest.fail(user_id + " should be a valid user ID format.")
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            pytest.fail(user_id + " raised an unexpected error.")

    # Test valid github user IDs
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDs)
    def test_valid_user_id(self, mock_get, user_id):
        """Tests that the function processes valid user ids successfully"""
        if user_id in self.userRepos:
            commits = []
            for user_repo in self.userRepos[user_id]:
                commits.extend([self.repoCommits[repoCommit]
                                for repoCommit in self.repoCommits.items()
                                if repoCommit == (user_id, user_repo["name"])])
            mock_get.side_effects = [self.userRepos[user_id]] + commits
        else:
            mock_get.side_effect = requests.exceptions.HTTPError
        try:
            get_user_repos_commits(user_id)
        except requests.exceptions.HTTPError:
            pytest.fail(user_id + " should be a valid user ID.")
        except Exception:
            pytest.fail(user_id + " raised an unexpected error.")

    # Test output values
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDs)
    def test_output_value(self, mock_get, user_id):
        """Tests that valid user ids output correct data"""
        mock_get.side_effect, mock_get.return_value = self._build_mock_values(user_id)
        try:
            repo_list = get_user_repos_commits(user_id)
        except StopIteration:
            pytest.fail(user_id + " made more API calls than expected.")

        expected = [(r[1], len(self.repoCommits[r]))
                    for r in set(rc
                                 for rc in self.repoCommits
                                 if user_id == rc[0])]
        assert sorted(repo_list) == sorted(expected), "Incorrect data output."

    # Test Print Functionality
    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDs)
    def test_print_implicit(self, mock_get, user_id, capfd):
        """Tests that the default function call prints correct tabulated data"""
        mock_get.side_effect, mock_get.return_value = self._build_mock_values(user_id)
        get_user_repos_commits(user_id)
        out = capfd.readout()
        expected = sorted([(r[1], len(self.repoCommits[r]))
                           for r in set(rc
                                        for rc in self.repoCommits
                                        if user_id == rc[0])])
        assert out.strip() == tabulate(expected,
                                       headers=["Repo Name", "Commits"],
                                       tablefmt="fancy_outline").strip()

    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDs)
    def test_print_explicit(self, mock_get, user_id, capfd):
        """Tests that the explicit print parameter prints correct tabulated data when True"""
        mock_get.side_effect, mock_get.return_value = self._build_mock_values(user_id)
        get_user_repos_commits(user_id, True)
        out = capfd.readout()
        expected = sorted([(r[1], len(self.repoCommits[r]))
                           for r in set(rc
                                        for rc in self.repoCommits
                                        if user_id == rc[0])])
        assert out.strip() == tabulate(expected,
                                       headers=["Repo Name", "Commits"],
                                       tablefmt="fancy_outline").strip()

    @patch("GetGithubUserReposCommits.requests.get")
    @pytest.mark.parametrize("user_id", validUserIDs)
    def test_print_none(self, mock_get, user_id, capfd):
        """Tests that the explicit print parameter does not print any data when False"""
        mock_get.side_effect, mock_get.return_value = self._build_mock_values(user_id)
        get_user_repos_commits(user_id, False)
        out = capfd.readout()
        assert out == ""

    # Helpers
    def _mock_response(self, json_data=None):
        """Builds a slim mock of the Response object with a response status and json data"""
        mock_resp = Mock()
        if not json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
            mock_resp.status_code = 404
        else:
            mock_resp.json = Mock(
                return_value=json_data
            )
            mock_resp.status_code = 200
        return mock_resp

    def _build_mock_values(self, user_id):
        """Builds the mock's side effect iterables and return value for a given user id"""
        if user_id in self.userRepos:
            side_effects = []
            mock_resp = self._mock_response(json_data = [self.userRepos[user_id]][0])
            side_effects.append(mock_resp)
            for user_repo in self.userRepos[user_id]:
                mock_resp = self._mock_response(
                    json_data = list(reversed([self.repoCommits[repoCommit]
                                                for repoCommit in self.repoCommits.items()
                                                if repoCommit == (user_id, user_repo["name"])][0])))
                side_effects.append(mock_resp)
            side_effect = side_effects
        else:
            side_effect = [requests.exceptions.HTTPError]
        return_value = requests.exceptions.HTTPError
        return side_effect, return_value
