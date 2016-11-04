#!/bin/bash


function bump {
    echo "BUMP $1 version $2"
    if [ "$1" = "toga" ]; then
        pushd .
        mv setup.py temp
        sed "s/version='.*',/version='$2',/g" temp > setup.py
        rm temp
        git add setup.py
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

function build {
    cd $1
    echo "BUILD $1"
    rm -rf build dist
    python setup.py sdist bdist_wheel
    cd ..
}

function release {
    cd $1
    echo "RELEASE $1 version $2"
    python setup.py sdist bdist_wheel
    if [ "$1" = "toga" ]; then
        twine upload dist/toga-$1-*
        twine upload dist/toga-$1.*
    else
        twine upload dist/toga_$1-$2-*
        twine upload dist/toga-$1-$2.*
    fi
    git tag v$1
    git push
    git push --tags
    cd ..
}

function dev {
    echo "DEV-BUMP $1 version $2"
    if [ "$1" = "toga" ]; then
        pushd .
        mv setup.py temp
        sed "s/version='.*',/version='$2.dev1',/g" temp > setup.py
        git add setup.py
    else
        if [ "$1" = "core" ]; then
            pushd src/$1/toga
        else
            pushd src/$1/toga_$1
        fi
        mv __init__.py temp
        sed "s/^__version__ = '.*'/__version__ = '$2.dev1'/g" temp > __init__.py
        git add __init__.py
    fi
    rm temp
    popd
}

MODULES="toga core cocoa iOS gtk django"

action=$1
shift

if [ "$action" = "" ]; then
    echo "Usage -"
    echo
    echo "  Bump version number for release:"
    echo "    ./release.sh bump 1.2.3"
    echo
    echo "  Build the releases"
    echo "    ./release.sh build"
    echo
    echo "  Release the build products and tag the repo."
    echo "    ./release.sh release 1.2.3"
    echo
    echo "  Bump version number for next version development"
    echo "    ./release.sh dev 1.2.4"

elif [ "$action" = "build" ]; then
    for module in $MODULES; do
        build $module
    done

elif [ "$action" = "release" ]; then
    version=$1
    shift

    for module in $MODULES; do
        $action $module $version
    done

elif [ "$action" = "bump" ]; then
    version=$1
    shift

    git pull

    for module in $MODULES; do
        $action $module $version
    done

    git commit -m "Bumped version number for v$version release."
elif [ "$action" = "dev" ]; then
    version=$1
    shift

    git pull

    for module in $MODULES; do
        $action $module $version
    done

    git commit -m "Bumped version number for v$version development."
fi
