Requirements
============

You need to have installed:
    - the Android SDK
    - Elm
    - Python
    - git


Starting a project
==================

Simply clone this repo and then cd into it.

Build script
============

The script that enables you to build and/or install the app onto the device is ``manage.py``.
It's a single Python script without any dependencies. You can call it like this on the command line::

    $ python manage.py (see next section for commands available)

On Linux you should be able to do simply::

    $ ./manage.py (see next section for commands available)


To build an Elm application (running in a webview)
==================================================

Keystore
--------

First, and this is something  you only have to do once per project, create a debug Android keystore using the command::

    $ ./manage.py create-debug-key

This create a keystore in the current directory under the file name ``debug.keystore``.

Environment variables
---------------------

You need to supply three environment variables to the script::

    - BUILD_TOOLS_DIR: the directory of the Android SDK where reside tools such as `aapt` and `dx`.
      For example, I use `BUILD_TOOLS_DIR=/home/myusername/Android/Sdk/build-tools/29.0.0/`

    - PLATFORM_DIR: the directory of the Android SDK where reside `android.jar`.
      For example I use `PLATFORM_DIR=/home/myusername/Android/Sdk/platforms/android-29/`

    - KEYSTORE_FILE: the keystore file. If you created it by `manage.py create-debug-keystore`,
      then the file is `debug.keystore` and you should use `KEYSTORE_FILE=debug.keystore`

The rest of this tutorial assume you have exported these 3 environment variables using::

    $ export BUILD_TOOLS_DIR=... PLATFORM_DIR=... KEYSTORE_FILE=...

Build the apk
-------------

Build an apk with the command::

    $ ./manage.py build

The apk is created inside the ``build`` directory.

Install the app on an Android device
------------------------------------

Make sure your device is connected to your computer in debug mode
(you can use the command ``adb devices`` to check if your device appear in the list).
Then::

    $ ./manage.py install

You can also install the app and start it automatically using::

    $ ./manage.py install+run


Changing the name of the application
====================================

You change the name of the application exactly like you would in a normal Java only android application.

The name displayed in the icon list of the device is the name you find in the ``AndroidManifest.xml`` in the
``android:label`` attribute of the ``application`` tag. We've used ``"Elm App"`` as an example.

You can change the package name from the original example we've used (``com.example.elmwebviewapp``)
to what you like (say ``net.birdwatchers.birdspot``) by renaming the directories ``java/com/example/elmwebviewapp`` to
``java/net/birdwatchers/birdspot``, then replace the first line ``package com.example.elmwebviewapp;`` in ``MainActivity.java`` with
``package net.birdwatchers.birdspot;``. Then replace the ``package="com.example.elmwebviewapp"`` manifest attribute in ``AndroidManifest.xml``
with ``package="net.birdwatchers.birdspot"``

Changing the icon of the application
====================================

Same as with a normal Java only android application. Refer to Android development documentation.

Viewing the app in the browser using elm-live
=============================================

Before loading the app on the device, you can develop using `elm-live` and see your changes in the browser of your laptop/desktop.
This requires to have installed `elm-live <https://github.com/wking-io/elm-live>`__.

Then::

    $ ./manage.py elm-live

This is just a shortcut for::

    $ elm-live src/Main.elm -d assets -- --output=assets/main.js
