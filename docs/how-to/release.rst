==============================
How to cut a Toga release
==============================

The release infrastructure for Toga is semi-automated, using GitHub
Actions to formally publish releases.

This guide assumes that you have an ``upstream`` remote configured on your
local clone of the Toga repository, pointing at the official repository.
If all you have is a checkout of a personal fork of the Toga repository,
you can configure that checkout by running::

    $ git remote add upstream https://github.com/beeware/toga.git

The procedure for cutting a new release is as follows:

#. Check the contents of the upstream repository's main branch::

    $ git fetch upstream
    $ git checkout --detach upstream/main

   Check that the HEAD of release now matches upstream/main.

#. If necessary, update the version number::

    $ ./release.sh bump 1.2.3

#. Tag the release, and push the branch and tag upstream::

    $ git tag v1.2.3
    $ git push upstream main
    $ git push upstream v1.2.3

#. Pushing the tag will start a workflow to create a draft release on GitHub.
   You can `follow the progress of the workflow on GitHub
   <https://github.com/beeware/toga/actions?query=workflow%3A%22Create+Release%22>`__;
   once the workflow completes, there should be a new `draft release
   <https://github.com/beeware/toga/releases>`__, and entries on the TestPyPI
   server for `toga-core <https://test.pypi.org/project/toga-core/>`__,
   `toga-cocoa <https://test.pypi.org/project/toga-cocoa/>`__, etc.

   Confirm that this action successfully completes. If it fails, there's a
   couple of possible causes:

   a. The final upload to TestPyPI failed. TestPyPI doesn't have the same
      service monitoring as PyPI-proper, so it sometimes has problems. However,
      it's not critical to the release process.
   b. Something else fails in the build process. If the problem can be fixed
      without a code change to the Toga repository (e.g., a transient
      problem with build machines not being available), you can re-run the
      action that failed through the Github Actions GUI. If the fix requires a
      code change, delete the old tag, make the code change, and re-tag the
      release.

#. Download the "packages" artifact from the GitHub workflow, and use its wheels
   to build some apps and perform any pre-release testing that may be appropriate.

#. Log into ReadTheDocs, visit the `Versions tab
   <https://readthedocs.org/projects/toga/versions/>`__, and activate the
   new version. Ensure that the build completes; if there's a problem, you
   may need to correct the build configuration, roll back and re-tag the release.

#. Edit the GitHub release. Add release notes. Check the pre-release checkbox if
   necessary.

#. Double check everything, then click Publish. This will trigger a
   `publication workflow on GitHub
   <https://github.com/beeware/toga/actions?query=workflow%3A%22Upload+Python+Package%22>`__.

#. Wait for the packages to appear on PyPI (`toga-core
   <https://pypi.org/project/toga-core/>`__, `toga-cocoa
   <https://pypi.org/project/toga-cocoa/>`__, etc.).

#. Set the version number for the next release::

    $ ./release.sh bump 1.2.4

Congratulations, you've just published a release!

Once the release has successfully appeared on PyPI or TestPyPI, it cannot be
changed. If you spot a problem after that point, you'll need to restart with
a new version number.
