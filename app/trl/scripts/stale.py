"""
Script to close stale issue. Taken in part from the AllenNLP repository.
https://github.com/allenai/allennlp.
"""
import os
from datetime import datetime as dt
from datetime import timezone

from github import Github


LABELS_TO_EXEMPT = [
    "good first issue",
    "good second issue",
    "feature request",
]


def main():
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo("huggingface/trl")
    open_issues = repo.get_issues(state="open")

    for issue in open_issues:
        comments = sorted([comment for comment in issue.get_comments()], key=lambda i: i.created_at, reverse=True)
        last_comment = comments[0] if len(comments) > 0 else None
        if (
            last_comment is not None
            and last_comment.user.login == "github-actions[bot]"
            and (dt.now(timezone.utc) - issue.updated_at).days > 7
            and (dt.now(timezone.utc) - issue.created_at).days >= 30
            and not any(label.name.lower() in LABELS_TO_EXEMPT for label in issue.get_labels())
        ):
            issue.edit(state="closed")
        elif (
            (dt.now(timezone.utc) - issue.updated_at).days > 23
            and (dt.now(timezone.utc) - issue.created_at).days >= 30
            and not any(label.name.lower() in LABELS_TO_EXEMPT for label in issue.get_labels())
        ):
            issue.create_comment(
                "This issue has been automatically marked as stale because it has not had "
                "recent activity. If you think this still needs to be addressed "
                "please comment on this thread.\n\n"
            )


if __name__ == "__main__":
    main()
