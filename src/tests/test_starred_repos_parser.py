import unittest
import json
from services.starred_repos_parser import StarredReposParser


class TestStarredReposParser(unittest.TestCase):

    def test_parser_full_info_correct_number_of_repos(self):
        """Test that the parser returns the correct number of starred repositories
        """
        with open("src/tests/json_files_for_testing/starred_repos_full_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(response["number_of_starred_repositories"], 4)

    def test_parser_full_info_correct_number_of_repos_in_list(self):
        """Test that the parser returns the correct number of starred repositories in the list
        """
        with open("src/tests/json_files_for_testing/starred_repos_full_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        response_starred_repos = response["starred_repositories"]
        self.assertEqual(len(response_starred_repos), 4)

    def test_parser_full_info_repo_has_correct_fields(self):
        """Test that the parser returns the correct fields for a starred repository
        with right types"""
        with open("src/tests/json_files_for_testing/starred_repos_full_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.name, "serenity")
        self.assertEqual(type(starred_repo.description), str)
        self.assertEqual(type(starred_repo.license), dict)
        self.assertEqual(type(starred_repo.topics), list)

    def test_parser_no_description(self):
        """Test that the parser returns None for description if the description is missing
        """
        with open("src/tests/json_files_for_testing/starred_repos_missing_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.description, None)

    def test_parser_no_license(self):
        """Test that the parser returns an empty dictionary for license if the license is missing
        """
        with open("src/tests/json_files_for_testing/starred_repos_missing_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.license, {})

    def test_parser_no_topics(self):
        """Test that the parser returns an empty list for topics if the topics are missing
        """
        with open("src/tests/json_files_for_testing/starred_repos_missing_info.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        starred_repo = response["starred_repositories"][0]
        self.assertEqual(starred_repo.topics, [])

    def test_parser_no_stars_correct_number_of_repos(self):
        """Test that the parser returns the correct number of starred repositories 
        if there are no starred repos
        """
        with open("src/tests/json_files_for_testing/starred_repos_empty.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(response["number_of_starred_repositories"], 0)

    def test_parser_no_stars_correct_number_of_repos_in_list(self):
        """Test that the parser returns the correct number of starred repositories in the list 
        if there are no starred repos
        """
        with open("src/tests/json_files_for_testing/starred_repos_empty.json",
                  encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        parser = StarredReposParser(json_file)
        response = parser.get_starred_repos_response()
        self.assertEqual(len(response["starred_repositories"]), 0)
