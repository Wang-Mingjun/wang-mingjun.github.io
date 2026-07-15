# Synchronized Homepage Mirror Setup

This document configures the existing academic homepage to appear at both:

```text
https://xin-xi-xiao.github.io/
https://wang-mingjun.github.io/
```

The existing `xin-xi-xiao/xin-xi-xiao.github.io` repository remains the only editable source. Every push to its `main` branch triggers a GitHub Actions workflow that publishes the same tracked website files to `wang-mingjun/wang-mingjun.github.io`.

## Current Deployment Status

Status verified on 2026-07-15:

- [x] Organization `Wang-Mingjun` created.
- [x] Public repository `Wang-Mingjun/wang-mingjun.github.io` created.
- [x] Account `xin-xi-xiao` granted Admin access to the target repository.
- [x] Mirror workflow prepared locally in the source repository.
- [x] Independent local Git remote `mirror` configured without changing `origin`.
- [ ] Local source commits pushed to `xin-xi-xiao/xin-xi-xiao.github.io`.
- [ ] Fine-grained mirror token created.
- [ ] Source repository secret `HOMEPAGE_MIRROR_TOKEN` configured.
- [ ] First mirror workflow completed successfully.
- [ ] Target GitHub Pages enabled and returning HTTP 200.

Current remote checks show that the target repository exists but is empty and its Pages endpoint returns 404. This is expected until the first synchronization and Pages activation are complete. The existing homepage returns HTTP 200 and remains unaffected.

## 1. Design and Safety Properties

- The existing homepage is not renamed, transferred, or reconfigured.
- A failed mirror update cannot prevent the existing homepage from publishing.
- The target repository is deploy-only and must not be edited manually.
- The mirror excludes `.github` to prevent recursive workflow execution.
- The mirror excludes `CNAME` to prevent a future custom-domain conflict.
- `.source-commit` records the exact source commit represented by each mirror build.
- The generated HTML keeps `https://wang-mingjun.github.io/` as its canonical URL, making the name-based homepage the preferred result while avoiding duplicate-content ambiguity for search engines.

## 2. Create the GitHub Organization

GitHub account and organization names are case-insensitive. As checked through GitHub's public API on 2026-07-14, no public account named `wang-mingjun` was found. The name is not reserved until GitHub accepts the organization creation form.

While signed in as `xin-xi-xiao`:

1. Open `https://github.com/account/organizations/new`.
2. Select the free organization plan.
3. Enter `wang-mingjun` as the organization name.
4. Use an email address you control as the contact email.
5. Complete GitHub's confirmation steps.

If GitHub reports that the name is unavailable, stop before changing this repository. Recheck the alternatives in `HOMEPAGE_MAINTENANCE.md` and update the target owner in the workflow only after choosing a new name.

## 3. Create the Target Repository

Inside the new `wang-mingjun` organization:

1. Create a **public** repository named exactly `wang-mingjun.github.io`.
2. An initial README is optional because the first successful mirror run replaces the target `main` branch.
3. Do not copy files into the repository manually.
4. Do not configure a custom domain in this target repository.

GitHub requires an organization homepage repository to match `<organization>.github.io`; a repository with this name under any other owner cannot claim `https://wang-mingjun.github.io/`.

## 4. Create a Restricted Fine-Grained Token

The standard `GITHUB_TOKEN` for the source repository cannot write to a different organization repository. Create a dedicated fine-grained personal access token:

Open `https://github.com/settings/personal-access-tokens/new` while signed in as `xin-xi-xiao`.

1. Open GitHub **Settings > Developer settings > Personal access tokens > Fine-grained tokens**.
2. Select **Generate new token**.
3. Use a descriptive name such as `homepage-mirror-writer`.
4. Set a finite expiration date and record a reminder to rotate it.
5. Set **Resource owner** to `wang-mingjun`.
6. Under **Repository access**, select **Only select repositories** and choose only `wang-mingjun.github.io`.
7. Under **Repository permissions**, grant **Contents: Read and write**.
8. Leave unrelated permissions disabled and generate the token.

Treat the token as a password. Do not place it in a source file, shell history, issue, commit, or chat message.

## 5. Store the Token in the Source Repository

In `xin-xi-xiao/xin-xi-xiao.github.io`:

Open `https://github.com/xin-xi-xiao/xin-xi-xiao.github.io/settings/secrets/actions/new`.

1. Open **Settings > Secrets and variables > Actions**.
2. Select **New repository secret**.
3. Set the name exactly to:

```text
HOMEPAGE_MIRROR_TOKEN
```

4. Paste the fine-grained token as the value and save it.

The workflow is intentionally harmless before this secret exists: it exits successfully with a notice and leaves both repositories untouched.

## 6. Publish and Run the First Synchronization

Push the prepared workflow from the authenticated VS Code terminal:

```bash
cd /data0/wangmingjun_homepage
git push -u origin main
```

Then open the source repository's **Actions** tab:

```text
https://github.com/xin-xi-xiao/xin-xi-xiao.github.io/actions/workflows/sync-homepage-mirror.yml
```

1. Select **Sync homepage mirror**.
2. Select **Run workflow** on `main`.
3. Confirm that `Build a clean mirror commit` succeeds.
4. Confirm that `Push the mirror` ends with `Mirror verified at commit ...`.

The same workflow runs automatically after every subsequent push to the source `main` branch.

## 7. Enable GitHub Pages on the Target

After the first mirror commit appears in `wang-mingjun/wang-mingjun.github.io`:

Open `https://github.com/Wang-Mingjun/wang-mingjun.github.io/settings/pages`.

1. Open target repository **Settings > Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch `main` and folder `/(root)`.
4. Save and wait for GitHub Pages to finish deployment.
5. Enable **Enforce HTTPS** if GitHub presents the option.

The new address may take several minutes to become available:

```text
https://wang-mingjun.github.io/
```

## 8. Verify Both Sites

Check the HTTP status:

```bash
curl -I https://xin-xi-xiao.github.io/
curl -I https://wang-mingjun.github.io/
```

Both should return a successful response. Compare important deployed files:

```bash
curl -fsSL https://xin-xi-xiao.github.io/index.html | sha256sum
curl -fsSL https://wang-mingjun.github.io/index.html | sha256sum

curl -fsSL https://xin-xi-xiao.github.io/assets/main.css | sha256sum
curl -fsSL https://wang-mingjun.github.io/assets/main.css | sha256sum
```

Each pair should have the same SHA-256 value after both Pages deployments finish. The target repository also exposes the source revision marker:

```bash
curl -fsSL https://raw.githubusercontent.com/wang-mingjun/wang-mingjun.github.io/main/.source-commit
git -C /data0/wangmingjun_homepage rev-parse HEAD
```

These two commit identifiers should match.

## 9. Normal Update Workflow

Continue editing and publishing only from the existing local workspace:

```bash
cd /data0/wangmingjun_homepage
git pull --ff-only

# Edit index.jemdoc and/or assets/main.css.
python3 tools/render_jemdoc.py index.jemdoc

git add -A
git commit -m "docs: update homepage"
git push -u origin main
```

The source Pages deployment and mirror synchronization then proceed independently. Never make content changes directly in `wang-mingjun/wang-mingjun.github.io`, because the next synchronization force-replaces its `main` branch.

## 10. Troubleshooting

### The workflow reports that the token is missing

Confirm the source repository secret is named exactly `HOMEPAGE_MIRROR_TOKEN`. Repository secrets are not copied between repositories.

### The push returns HTTP 403

Confirm all of the following:

- The token resource owner is `wang-mingjun`.
- The token is authorized for `wang-mingjun.github.io`.
- The token has **Contents: Read and write**.
- The token has not expired.
- The organization has not changed its personal-access-token policy.
- The token owner still has write access to the target repository.

### The new URL returns 404

Confirm the organization and repository names match exactly, the repository is public, and Pages deploys from `main` at `/(root)`. GitHub notes that initial publishing can take several minutes.

### The two pages briefly differ

The source Pages build and mirror Pages build are separate asynchronous deployments. Wait several minutes, then hard-refresh both pages. If the difference persists, inspect the source workflow run and the target Pages deployment status.

## 11. Removing the Mirror Safely

To stop future synchronization without affecting the original homepage:

1. Disable or delete `.github/workflows/sync-homepage-mirror.yml` in the source repository.
2. Delete the source repository secret `HOMEPAGE_MIRROR_TOKEN`.
3. Revoke the fine-grained token in GitHub Developer settings.
4. Optionally archive or delete the target repository or organization.

None of these actions changes `xin-xi-xiao/xin-xi-xiao.github.io` or its Pages settings.
