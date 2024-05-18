
Cut a Release
=============

Create a PR and go through the following steps:

**Preparation**
- Update and check changelog in `CHANGES.rst`
- Bump version in `start_jupyter_cm/__init__.py` (so that the version in the tag is correct and in the Github tarball.)
- (optional) check wheels build. Pushing a tag to a fork will run the release workflow without uploading to pypi

**Tag and release**
:warning: this is a point of no return point :warning:
- push tag (`vx.y.z`) to the upstream repository and the following will be triggered:
  - make the packages (wheel and tarball)
  - test the package
  - upload to pypi
  - creation of a Github Release

**Post-release action**
- Increment the version and set it back to dev: `vx.y.z.dev0`
- Prepare `CHANGES.rst` for development
- Merge the PR

Follow-up
=========

- Tidy up and close corresponding milestone
- A PR to the conda-forge feedstock will be created by the conda-forge bot
