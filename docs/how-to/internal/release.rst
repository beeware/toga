=========================
How to cut a Toga release
=========================

The release infrastructure for Toga is semi-automated, using GitHub
Actions to formally publish releases.

This guide assumes that you have an ``upstream`` remote configured on your
local clone of the Toga repository, pointing at the official repository.
If all you have is a checkout of a personal fork of the Toga repository,
you can configure that checkout by running:

.. code-block:: console

    $ git remote add upstream https://github.com/beeware/toga.git

The procedure for cutting a new release is as follows:

#. Check the contents of the upstream repository's main branch:

   .. code-block:: console

       $ git fetch upstream
       $ git checkout --detach upstream/main

   Check that the HEAD of release now matches upstream/main.

#. Ensure that the release notes are up to date. Run:

   .. code-block:: console

     $ tox -e towncrier -- --draft

   to review the release notes that will be included, and then:

   .. code-block:: console

     $ tox -e towncrier

   to generate the updated release notes. After doing any edits that may be
   required, run:

   .. code-block:: console

     $ tox -r -e docs-lint,docs

   to confirm that there are no spelling errors or formatting problems with the
   new release notes, and the docs build using the current documentation tool
   versions.

#. Tag the release, and push the branch and tag upstream:

   .. code-block:: console

     $ git tag v1.2.3
     $ git push upstream HEAD:main
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
      action that failed through the GitHub Actions GUI. If the fix requires a
      code change, delete the old tag, make the code change, and re-tag the
      release.

#. Create a clean virtual environment, install the new release from Test PyPI, and
   perform any pre-release testing that may be appropriate:

   .. code-block:: console

     $ python3 -m venv testvenv
     $ . ./testvenv/bin/activate
     (testvenv) $ pip install --extra-index-url https://test.pypi.org/simple/ toga==1.2.3
     (testvenv) $ toga-demo
     (testvenv) $ #... any other manual checks you want to perform ...

#. Log into ReadTheDocs, visit the `Versions tab
   <https://readthedocs.org/projects/toga/versions/>`__, and activate the
   new version. Ensure that the build completes; if there's a problem, you
   may need to correct the build configuration, roll back and re-tag the release.

#. Edit the GitHub release to add release notes. You can use the text generated
   by Towncrier, but you'll need to update the format to Markdown, rather than
   ReST. If necessary, check the pre-release checkbox.

#. Double check everything, then click Publish. This will trigger a
   `publication workflow on GitHub
   <https://github.com/beeware/toga/actions?query=workflow%3A%22Upload+Python+Package%22>`__.

#. Wait for the packages to appear on PyPI (`toga-core
   <https://pypi.org/project/toga-core/>`__, `toga-cocoa
   <https://pypi.org/project/toga-cocoa/>`__, etc.).

Congratulations, you've just published a release!

Once the release has successfully appeared on PyPI or TestPyPI, it cannot be
changed. If you spot a problem after that point, you'll need to restart with
a new version number.
