#!/bin/sh

FIRA_TAG=$(cd fonts/fira && git describe --tags `git rev-list --tags --max-count=1`);
HACK_TAG=$(cd fonts/hack && git describe --tags `git rev-list --tags --max-count=1`);

git config --global user.email "logap@me.com";
git config --global user.name "Gary Lo";

if output=$(git status --porcelain) && [ -z "$output" ]; then
  # Working directory clean
  exit 0;
else
  # Uncommitted changes
  GIT_TAG="${HACK_TAG}+fira${FIRA_TAG}"
  git add .
  git commit -m "Update font release Hack@${HACK_TAG}, Fira@${FIRA_TAG}";
  git tag "$GIT_TAG";

  # Remove existing "origin"
  git remote rm origin
  # Add new "origin" with access token in the git URL for authentication
  git remote add origin https://gaplo917:${GITHUB_TOKEN}@github.com/gaplo917/Ligatured-Hack.git > /dev/null 2>&1

  git push origin HEAD:master --quiet;
  git push origin "$GIT_TAG" --quiet
fi
