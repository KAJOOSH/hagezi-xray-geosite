#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-only

set -euo pipefail

artifact_dir=$(cd "${1:?Pass the directory containing the generated files}" && pwd)
branch=generated
ref="refs/heads/$branch"
publish_dir=$(mktemp -d)
trap 'git worktree remove --force "$publish_dir" >/dev/null 2>&1 || rmdir "$publish_dir"' EXIT

cd "$artifact_dir"
sha256sum --check hagezi-tif.dat.sha256
cd - >/dev/null

gh auth setup-git --hostname github.com
if git ls-remote --exit-code origin "$ref" >/dev/null; then
    git fetch --no-tags --depth=1 origin "$ref"
    git worktree add --detach "$publish_dir" FETCH_HEAD
else
    status=$?
    if [[ "$status" != 2 ]]; then
        exit "$status"
    fi
    git worktree add --detach "$publish_dir" HEAD
    git -C "$publish_dir" switch --orphan "$branch"
fi

files=(hagezi-tif.dat hagezi-tif.dat.sha256 source-tif-medium.txt manifest.json LICENSE)
for file in "${files[@]}"; do
    source="$artifact_dir/$file"
    if [[ "$file" == LICENSE ]]; then
        source=LICENSE
    fi
    install -m 0644 "$source" "$publish_dir/$file"
done

git -C "$publish_dir" add -- "${files[@]}"
if git -C "$publish_dir" diff --cached --quiet; then
    echo 'Published files are up to date.'
    exit 0
fi
git -C "$publish_dir" -c user.name='github-actions[bot]' \
    -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
    commit -m "Update HaGeZi TIF Medium ($(date -u +%F))" \
    -m "Converter: $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/tree/$GITHUB_SHA"
git -C "$publish_dir" push origin "HEAD:$ref"
