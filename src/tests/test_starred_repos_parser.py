import unittest
import json
from services.starred_repos_parser import StarredReposParser

class TestStarredReposParser(unittest.TestCase):

    def test_parser_full_info_correct_number_of_repos(self):
        with open ("src/tests/json_files_for_testing/starred_repos_full_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(response["number_of_starred_repositories"], 4)
    
    def test_parser_full_info_correct_number_of_repos_in_list(self):
        with open ("src/tests/json_files_for_testing/starred_repos_full_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        response_starred_repos = response["starred_repositories"]
        self.assertEqual(len(response_starred_repos), 4)
    
    def test_parser_full_info_repo_has_correct_fields(self):
        with open ("src/tests/json_files_for_testing/starred_repos_full_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        
        self.assertEqual(starred_repo.name, "serenity")
        self.assertEqual(type(starred_repo.description), str)
        self.assertEqual(type(starred_repo.license), dict)
        self.assertEqual(type(starred_repo.topics), list)
    
    def test_parser_no_description(self):
        with open ("src/tests/json_files_for_testing/starred_repos_missing_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.description, None)

    def test_parser_no_license(self):
        with open ("src/tests/json_files_for_testing/starred_repos_missing_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.license, {})

    def test_parser_no_topics(self):
        with open ("src/tests/json_files_for_testing/starred_repos_missing_info.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.topics, [])
    
    def test_parser_no_stars_correct_number_of_repos(self):
        with open ("src/tests/json_files_for_testing/starred_repos_empty.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(response["number_of_starred_repositories"], 0)
    
    def test_parser_no_stars_correct_number_of_repos_in_list(self):
        with open ("src/tests/json_files_for_testing/starred_repos_empty.json") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(len(response["starred_repositories"]), 0)