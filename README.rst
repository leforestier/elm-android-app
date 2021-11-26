Requirements
============

You need to have installed:
    - the Android SDK
    - Elm
    - Python
    - git


Starting a project
==================

Clone this repo and cd into it::

    $ git clone https://github.com/leforestier/elm-android-app
    $ cd elm-android-app

Then run::

    $ elm init

That will create an ``elm.json`` file in the current directory.

The entry point of your Elm application is ``src/Main.elm``.
This file contains a basic counter app that you can try to build to test that everything is working on your system.

To create a great app, modify ``src/Main.elm`` and add other Elm source files to the ``src/`` directory .

To install additional elm packages, you can use ``elm install`` just like with any normal Elm project.

Build script
============

The script that enables you to build and/or install the app onto the device is ``manage.py``.
It's a single Python script without any dependencies. You can call it like this on the command line::

    $ python manage.py (see next section for available commands)

On Linux you should be able to do simply::

    $ ./manage.py (see next section for available commands)


To build an Elm application (running in a webview)
==================================================

Keystore
--------

First, and this is something  you only have to do once per project, create a debug Android keystore using the command::

    $ ./manage.py create-debug-key

This creates a keystore in the current directory under the file name ``debug.keystore``.

Environment variables
---------------------

You need to supply three environment variables to the script::

    - BUILD_TOOLS_DIR: the directory of the Android SDK where reside tools such as `aapt` and `dx`.
      For example, I use `BUILD_TOOLS_DIR=/home/myusername/Android/build-tools/30.0.3/`

    - PLATFORM_DIR: the directory of the Android SDK where reside `android.jar`.
      For example I use `PLATFORM_DIR=/home/myusername/Android/platforms/android-30/`

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

The name of our example application is "Elm App" and our package name is ``com.example.elmwebviewapp``.
Here's how to change it, for, say, a bird watching application called "Bird Watch" with package name ``net.birdwatchers.birdspot``.

To change the application name to "Bird Watch":

    - in ``AndroidManifest.xml`` replace ``android:label="Elm App"`` with  ``android:label="Bird Watch"``

To change the package name to ``net.birdwatchers.birdspot``:

    - rename the directory ``java/com/example/elmwebviewapp`` to ``java/net/birdwatchers/birdspot``
    - in ``MainActivity.java``, replace the first line ``package com.example.elmwebviewapp;`` with ``package net.birdwatchers.birdspot;``
    - in ``AndroidManifest.xml``, replace the ``package="com.example.elmwebviewapp"`` manifest attribute  with ``package="net.birdwatchers.birdspot"``

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

Gestures and touch events
=========================

You'll probably want to handle events such as swipes, presses, rotations, pinches etc...

To be able to use event attributes such as ``onSwipe``, ``onSwipeLeft``, ``onPress``, ``onPinch``...
just as easily as you would use ``onClick``, I published a helper library that you can install:

    `leforestier/elm-hammer-events <https://package.elm-lang.org/packages/leforestier/elm-hammer-events/latest/>`_

This helper library relies on the excellent `Hammer.js <https://hammerjs.github.io>`_
Javascript library : it's just a single
file `hammer.min.js <https://hammerjs.github.io/dist/hammer.min.js>`_
to add to your ``assets`` directory.


Alternatively, if you want to deal
with `HTML5 touch events <https://developer.mozilla.org/en-US/docs/Web/API/Touch_events>`_
directly, you can use the

    `Html.Events.Extra.Touch <https://package.elm-lang.org/packages/mpizenberg/elm-pointer-events/latest/Html-Events-Extra-Touch>`_ module from `mpizenberg/elm-pointer-events <https://package.elm-lang.org/packages/mpizenberg/elm-pointer-events/>`_
