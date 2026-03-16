import subprocess
from pathlib import Path
from ..exceptions import GitOperationError
from ..logger import Console, logger


class GitService:
    @classmethod
    def _run(cls, cmd: list[str], silent: bool = True) -> subprocess.CompletedProcess:
        """Internal helper for executing Git commands."""
        logger.debug(f"Git CMD: {' '.join(cmd)}")
        return subprocess.run(cmd, capture_output=silent, text=True)

    @classmethod
    def ensure_repo(cls):
        """Checks for repository initialization and Detached HEAD state."""
        if not Path(".git").exists():
            Console.warning("Git not initialized. Initializing now...")
            cls._run(["git", "init"])

        res = cls._run(["git", "branch", "--show-current"])
        if not res.stdout.strip():
            raise GitOperationError(
                "You are in a DETACHED HEAD state. Process stopped for safety."
            )

    @classmethod
    def get_current_branch(cls) -> str:
        return cls._run(["git", "branch", "--show-current"]).stdout.strip()

    @classmethod
    def switch_branch(cls, branch: str):
        """Safely switches to the target branch or creates it."""
        current = cls.get_current_branch()
        if current != branch:
            Console.info(f"🌿 Switching branch: {current} ➔ {branch}")
            has_commits = cls._run(["git", "rev-parse", "HEAD"]).returncode == 0

            if not has_commits:
                res = cls._run(["git", "branch", "-M", branch])
            else:
                res = cls._run(["git", "checkout", "-B", branch])

            if res.returncode != 0:
                error_msg = res.stderr.strip() or res.stdout.strip()
                raise GitOperationError(f"Failed to switch branch: {error_msg}")

    @classmethod
    def has_any_changes(cls) -> bool:
        """Checks if there are any staged, unstaged, or untracked changes."""
        res = cls._run(["git", "status", "--porcelain"])
        return bool(res.stdout.strip())

    @classmethod
    def has_staged_changes(cls) -> bool:
        """Checks if there are files already in the staging area."""
        res = cls._run(["git", "diff", "--cached", "--quiet"])
        return res.returncode != 0

    @classmethod
    def smart_stage(cls):
        """Intelligent file staging."""
        if cls.has_staged_changes():
            Console.info("Staged files detected. Committing current index only.")
        else:
            Console.warning("No files in the staging area.")
            ans = (
                input("Would you like to stage all changes (git add .)? [y/N]: ")
                .strip()
                .lower()
            )
            if ans == "y":
                cls._run(["git", "add", "."])
            else:
                raise GitOperationError("Nothing to commit. Operation cancelled.")

    @classmethod
    def commit(cls, message: str):
        """Commits changes and extracts Git output if it fails."""
        res = cls._run(["git", "commit", "-m", message])
        if res.returncode != 0:
            error_msg = res.stderr.strip() or res.stdout.strip()
            raise GitOperationError(f"Commit failed. Git says:\n{error_msg}")

    @classmethod
    def push_with_retry(cls, branch: str):
        """Pushes to remote, attempting a pull --rebase if rejected."""
        Console.info(f"Pushing to branch: {branch}...")
        res = cls._run(["git", "push", "-u", "origin", branch])

        if res.returncode == 0:
            Console.success(f"Code successfully pushed to origin/{branch}!")
            return

        Console.warning("Push rejected. Remote changes detected.")
        Console.info("Synchronizing (pull --rebase)...")
        pull_res = cls._run(["git", "pull", "origin", branch, "--rebase"])

        if pull_res.returncode != 0:
            error_msg = pull_res.stderr.strip() or pull_res.stdout.strip()
            raise GitOperationError(
                f"🛑 Rebase conflict detected!\nGit says: {error_msg}"
            )

        Console.success("Sync successful. Retrying push...")
        push_retry = cls._run(["git", "push", "-u", "origin", branch])

        if push_retry.returncode != 0:
            error_msg = push_retry.stderr.strip() or push_retry.stdout.strip()
            raise GitOperationError(f"Final push failed after rebase:\n{error_msg}")
