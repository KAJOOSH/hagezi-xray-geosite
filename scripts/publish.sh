#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-only

set -euo pipefail

artifact_dir=$(cd "${1:?Pass the directory containing the generated files}" && pwd)
branch=generated
ref="refs/heads/$branch"
publish_dir=$(mktemp -d)
trap 'git worktree remove --force "$publish_dir" >/dev/null 2>&1 || rmdir "$publish_dir"' EXIT

report_file=${2:?Pass the successful Xray integration report}
manifest_digest=$(sha256sum "$artifact_dir/manifest.json" | cut -d ' ' -f 1)
if ! jq -e --arg digest "$manifest_digest" --slurpfile candidate "$artifact_dir/manifest.json" '
    .failed == 0 and .passed > 0
    and .manifest_sha256 == $digest
    and .geodata_version == $candidate[0].version
    and .package_count == ($candidate[0].packages | length)
    and (.xray_version | type == "string")
' "$report_file" >/dev/null; then
    echo 'A passing Xray integration report for this exact candidate is required.' >&2
    exit 1
fi
xray_version=$(jq -er '.xray_version' "$report_file")

(cd "$artifact_dir" && sha256sum --check checksums.sha256)

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
manifest="$publish_dir/manifest.json"
new_snapshot=false
if [[ -f "$manifest" ]] && jq -e --slurpfile candidate "$artifact_dir/manifest.json" '
    (.version | type == "string")
    and (.packages | type == "array")
    and .packages == $candidate[0].packages
' "$manifest" >/dev/null; then
    echo 'The generated branch already contains this version.'
else
    new_snapshot=true
    for file in "${files[@]}"; do
        source="$artifact_dir/$file"
        if [[ "$file" == LICENSE ]]; then
            source=LICENSE
        fi
        install -m 0644 "$source" "$publish_dir/$file"
    done
fi

version=$(jq -er '.version' "$manifest")
built_at=$(jq -er '.built_at' "$manifest")
generator_commit=$(jq -er '.generator_commit' "$manifest")
asset_sha256=$(jq -er '.asset_sha256' "$manifest")
source_sha256=$(jq -er '.source_sha256' "$manifest")
if [[ ! "$version" =~ ^v[0-9]{8}\.[0-9]+$ || ! "$generator_commit" =~ ^[0-9a-f]{40}$ ||
    ! "$built_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ||
    ! "$asset_sha256" =~ ^[0-9a-f]{64}$ || ! "$source_sha256" =~ ^[0-9a-f]{64}$ ]]; then
    echo 'Invalid metadata for the generated version.' >&2
    exit 1
fi

(
    cd "$publish_dir"
    sha256sum --check hagezi-tif.dat.sha256
    printf '%s  hagezi-tif.dat\n%s  source-tif-medium.txt\n' "$asset_sha256" "$source_sha256" | sha256sum --check
)

converter_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/tree/$generator_commit"
if [[ "$new_snapshot" == true ]]; then
    git -C "$publish_dir" add -- "${files[@]}"
    git -C "$publish_dir" -c user.name='github-actions[bot]' \
        -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
        commit -m "Publish GeoSite $version ($built_at)" -m "Converter: $converter_url"
    git -C "$publish_dir" push origin "HEAD:$ref"
fi

asset_names=$(jq -er '.packages[].asset' "$manifest")
assets=("$publish_dir/manifest.json" "$publish_dir/LICENSE" "$artifact_dir/checksums.sha256"
    "$artifact_dir/sources.zip" "$publish_dir/hagezi-tif.dat.sha256" "$publish_dir/source-tif-medium.txt")
while IFS= read -r file; do
    assets+=("$artifact_dir/$file")
done <<< "$asset_names"

if release=$(gh release view "$version" --repo "$GITHUB_REPOSITORY" --json isDraft,assets,url 2>/dev/null); then
    if [[ $(jq -r '.isDraft' <<< "$release") == true ]]; then
        gh release upload "$version" "${assets[@]}" --repo "$GITHUB_REPOSITORY" --clobber
        gh release edit "$version" --repo "$GITHUB_REPOSITORY" --draft=false --latest
    else
        for asset in "${assets[@]}"; do
            file=${asset##*/}
            if ! jq -e --arg file "$file" 'any(.assets[]; .name == $file)' <<< "$release" >/dev/null; then
                printf 'Missing asset %s in published release %s\n' "$file" "$version" >&2
                exit 1
            fi
        done
        printf 'Release %s already published: %s\n' "$version" "$(jq -r '.url' <<< "$release")"
    fi
else
    readme_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$generator_commit/README.md"
    persian_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$generator_commit/README.fa.md"
    test_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    notes=$(printf 'Built on `%s` (UTC). Validated with Xray-core `%s`.\n\n[Usage and package list](%s) · [Persian guide](%s) · [Integration results](%s)\n' \
        "$built_at" "$xray_version" "$readme_url" "$persian_url" "$test_url")
    gh release create "$version" "${assets[@]}" --repo "$GITHUB_REPOSITORY" \
        --target "$generator_commit" --latest --title "HaGeZi GeoSite and GeoIP $version" --notes "$notes"
fi
