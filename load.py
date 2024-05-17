from pathlib import Path
import shutil
import ast

from git import Repo


repo_url = "https://github.com/pallets/flask.git"


repo_path = Path(__file__).parent.resolve()
subject_path = repo_path / "subject_repo"
shutil.rmtree(str(subject_path), ignore_errors=True)
subject_path.mkdir(exist_ok=True, parents=True)
Repo.clone_from(repo_url, subject_path)
