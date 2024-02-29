from models.starred_repo_model import StarredRepoModel


class StarredReposParser:
    def __init__(self, starred_repos: dict):
        self.starred_repos = starred_repos
        self.starred_repos_response: dict = {}

    def get_starred_repos_response(self) -> dict:
        self.count_starred_repos()
        self.parse_starred_repositories()
        return self.starred_repos_response

    def parse_starred_repositories(self):
        starred_repository_list = []
        for starred_repository in self.starred_repos:

            starred_repository_object = StarredRepoModel(
                name=starred_repository["name"],
                description=starred_repository["description"],
                topics=starred_repository["topics"],
                license=starred_repository["license"],
                url=starred_repository["url"]
            )
            starred_repository_list.append(starred_repository_object)
        self.starred_repos_response["starred repositories"] = starred_repository_list

    def count_starred_repos(self):
        self.starred_repos_response["number of starred repositories"] = len(
            self.starred_repos)
