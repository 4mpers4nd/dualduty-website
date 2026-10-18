# GitHub Pages deployment

This project is already static. No npm install or build command is required.

1. Create or use a GitHub repository you control. If replacing an existing website, keep a backup or use a review branch first.
2. Copy all website files from the ZIP’s `dual-duty-junk` directory to the repository root. Include `.nojekyll` and `CNAME`.
3. Commit and push.
4. In the repository’s Pages settings, select branch deployment, the desired branch (usually `main`), and `/ (root)`.
5. Set the Pages custom domain to `dualdutyjunk.com`. `CNAME` already contains exactly that hostname.
6. Check the domain’s existing DNS with the domain owner. If a change is necessary, follow GitHub’s current custom-domain documentation. This project does not change DNS or assume registrar access.
7. After GitHub reports the domain and certificate ready, enable HTTPS enforcement if available.
8. Visit the root and every direct directory URL. Check `/pricing/` after a hard refresh and a nonexistent URL for the 404.
9. Review the manual QA checklist before announcing launch.

The root-relative URLs target a custom-domain root. They will not resolve correctly at an ordinary `/repository-name/` project subpath. Test at the intended domain, an account-root Pages repository, or a local root server.

If hosting somewhere else, serve these exact files and configure your host to use `404.html`. Canonicals and sitemap intentionally point to the business domain, not a temporary preview.

## Routine updates

Edit config and editorial source, run `python3 tools/render.py` for content changes, run the tests, and commit the resulting static files. GitHub Pages serves the committed output. Keep `CNAME` in subsequent updates.

## Rollback

Revert the deployment commit and allow Pages to redeploy the previous files. Local planner storage can survive deployments; normalization discards unsupported item IDs and fields. For a future incompatible planner schema, change the versioned storage key and explain the reset in the privacy policy.

## Local development

```bash
cd dual-duty-junk
python3 -m http.server 8080
```

Visit `http://localhost:8080/`. Do not run from the parent directory, since this project expects to be served at the URL root.
