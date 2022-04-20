#!/bin/bash
# Force the script to fail on any error
set -e

function bump {
    echo
    echo "************************************************************"
    echo "***** BUMP $1 version $2 *****"
    echo "************************************************************"
    echo
    if [ "$1" = "toga" ]; then
        pushd .
        # Find all the pyproject.toml examples,
        # and update the version of toga required.
        find examples -name pyproject.toml | while read f; do
            mv "$f" temp
            sed "s/^version = \".*\"/version = \"$2\"/g" temp > "$f"
            git add "$f"
        done

    elif [ "$1" = "demo" ]; then
        pushd demo
        mv setup.cfg temp
        sed "s/version = .*/version = $2/g" temp > setup.cfg
        mv setup.cfg temp
        sed "s/toga==.*/toga==$2/g" temp > setup.cfg
        git add setup.cfg

        mv pyproject.toml temp
        sed "s/==.*\"/==$2\"/g" temp > pyproject.toml
        mv pyproject.toml temp
        sed "s/^version = \".*\"/version = \"$2\"/g" temp > pyproject.toml
        git add pyproject.toml

    else
        if [ "$1" = "core" ]; then
            pushd src/$1/toga
        else
            pushd src/$1/toga_$1
        fi

        mv __init__.py temp
        sed "s/^__version__ = '.*'/__version__ = '$2'/g" temp > __init__.py
        git add __init__.py
    fi
    rm temp
    popd
}

function package {
    echo
    echo "************************************************************"
    echo "***** PACKAGE $1"
    echo "************************************************************"
    echo
    if [ "$1" = "toga" ]; then
        rm -rf build dist
        check-manifest -v
        python setup.py sdist bdist_wheel
        python -m twine check dist/*
    elif [ "$1" = "demo" ]; then
        cd demo
        check-manifest -v
        rm -rf build dist
        python setup.py sdist bdist_wheel
        cd ../..
    else
        cd src/$1
        check-manifest -v
        rm -rf build dist
        python setup.py sdist bdist_wheel
        python -m twine check dist/*
        cd ../..
    fi
}


function install {
    echo
    echo "************************************************************"
    echo "INSTALL $1"
    echo "************************************************************"
    echo
    if [ "$1" = "toga" ]; then
        python -m pip install dist/*.whl
    elif [ "$1" = "demo" ]; then
        python -m pip install demo/dist/*.whl
    else
        python -m pip install src/$1/dist/*.whl
    fi
}

function release {
    echo
    echo "************************************************************"
    echo "RELEASE $1 version $2"
    echo "************************************************************"
    echo
    if [ "$1" = "toga" ]; then
        twine upload "dist/toga-$2-py3-none-any.whl"
        twine upload "dist/toga-$2.tar.gz"
    elif [ "$1" = "demo" ]; then
        twine upload "demo/dist/toga_demo-$2-py3-none-any.whl"
        twine upload "demo/dist/toga-demo-$2.tar.gz"
    else
        twine upload "src/$1/dist/toga_$1-$2-py3-none-any.whl"
        twine upload "src/$1/dist/toga-$1-$2.tar.gz"
    fi
}


MODULES="android cocoa core django dummy flask gtk iOS web winforms toga demo"

action=$1
shift

VERSION=$(grep "^__version__ = '.*'$" src/core/toga/__init__.py | cut -f 2 -d \')

if [ "$action" = "" ]; then
    echo "Usage -"
    echo
    echo "  Bump version number for release:"
    echo "    ./release.sh bump 1.2.3"
    echo
    echo "  Package the release"
    echo "    ./release.sh package"
    echo
    echo "  Set up a test environment containing the release"
    echo "    ./release.sh test"
    echo
    echo "  Release the build products and tag the repo."
    echo "    ./release.sh release"
    echo
    echo "  Bump version number for next development version (dev3)"
    echo "    ./release.sh dev 1.2.4 3"

elif [ "$action" = "package" ]; then
    for module in $MODULES; do
        package $module
    done

elif [ "$action" = "test" ]; then
    python -m venv testenv-v$VERSION
    source testenv-v$VERSION/bin/activate
    for module in $MODULES; do
        install $module
    done

elif [ "$action" = "release" ]; then

    for module in $MODULES; do
        $action $module $VERSION
    done

    git tag v$VERSION
    git push upstream release:main
    git push --tags upstream release:main

elif [ "$action" = "bump" ]; then
    version=$1
    shift

    git pull

    for module in $MODULES; do
        $action $module $version
    done

    git commit -m "Bumped version number for v$version release."
elif [ "$action" == "dev" ]; then
    version=$1
    shift
    dev=$1
    shift
    if [ -z "$dev" ]; then
        dev=1
    fi

    git pull

    for module in $MODULES; do
        bump $module $version.dev$dev
    done

    git commit -m "Bumped version number for v$version.dev$dev development."
    git push upstream release:main
fi
