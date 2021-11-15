#!/usr/bin/env python
import os
import os.path
from os.path import join
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

def usage():
    return (
        "manage.py "
        + '|'.join((
            'create-debug-key',
            'create-key',
            'build',
            'install',
            'install+run',
            'elm-live'
        ))
    )

def quit_error(message):
    sys.stderr.write(message)
    sys.stderr.write('\n')
    sys.stderr.flush()
    sys.exit(1)


class Project:

    @classmethod
    def from_current_dir_and_env(cls):
        try:
            build_tools_dir = os.environ['BUILD_TOOLS_DIR']
        except KeyError:
            quit_error(
                "You need to supply a BUILD_TOOLS_DIR environment variable.\n"
                "Example: BUILD_TOOLS_DIR=/home/user/Android/Sdk/build-tools/29.0.0/"
            )

        if not os.path.isdir(build_tools_dir):
            quit_error("%s is not a directory" % repr(build_tools_dir))
        try:
            platform_dir = os.environ['PLATFORM_DIR']
        except KeyError:
            quit_error(
                "You need to supply a PLATFORM_DIR environment variable.\n"
                "Example: PLATFORM_DIR=/home/user/Android/Sdk/platforms/android-29/"
            )

        if not os.path.isdir(platform_dir):
            quit_error("%s is not a directory" % repr(platform_dir))

        manifest_tree = ET.parse('AndroidManifest.xml')
        root = manifest_tree.getroot()
        package = root.attrib['package']
        application = root.find('application')
        android_label = application.attrib['{http://schemas.android.com/apk/res/android}label']
        return cls(
            build_tools_dir,
            platform_dir,
            package,
            android_label,
            keystore = KeyStore.from_current_dir_and_env()
        )

    def __init__(self, build_tools_dir, platform_dir,
      package, android_label, keystore):
        self.build_tools_dir = build_tools_dir
        self.platform_dir = platform_dir
        self.package = package
        self.android_label = android_label
        self.keystore = keystore
        self.aapt = join(self.build_tools_dir, 'aapt')
        self.dx = join(self.build_tools_dir, 'dx')
        self.zipalign = join(self.build_tools_dir, 'zipalign')
        self.apksigner = join(self.build_tools_dir, 'apksigner')
        splitted_package = self.package.split('.')
        assert all(s.isalpha() for s in splitted_package)
        self.package_dir = join(*splitted_package)
        self.apk_name = re.sub(r'\W', '-', self.android_label)

    def makedirs(self):
        for d in ('gen', 'obj', 'apk'):
            os.makedirs(join('build', d), exist_ok=True)

    def elm_make(self):
        if not os.path.exists('elm.json'):
            quit_error("No elm.json file in the current directory. Please run `elm init`.")
        subprocess.check_call(['elm',
            'make', join('src', 'Main.elm'), '--output', join('assets', 'main.js')
        ])

    def build_apk(self):
        for command in (
            [self.aapt,
                'package', '-f', '-m', '-J', join('build', 'gen' + os.path.sep), '-A',
                 'assets', '-S', 'res', '-M', 'AndroidManifest.xml',
                 '-I', join(self.platform_dir, "android.jar")
            ],
            ['javac',
                '-source', '1.7', '-target', '1.7', '-bootclasspath',
                join(os.environ['JAVA_HOME'], 'jre', 'lib', 'rt.jar'),
                '-classpath', join(self.platform_dir, "android.jar"), "-d",
                join('build', 'obj'), join("build", "gen", self.package_dir, "R.java"),
                join("java", self.package_dir, "MainActivity.java")
            ],
            [self.dx,
                 '--dex', '--output=' + join('build','apk','classes.dex'),
                 join('build', 'obj')
            ],
            [self.aapt,
                'package', '-f',
                '-M', 'AndroidManifest.xml',
                '-A', 'assets',
                '-S', 'res' + os.path.sep,
                '-I', join(self.platform_dir, "android.jar"),
                '-F', join("build", self.apk_name + ".unsigned.apk"),
                join('build','apk')
            ],
            [self.zipalign,
                '-f', '-p', '4',
                join("build", self.apk_name + ".unsigned.apk"),
                join("build", self.apk_name + ".aligned.apk")
            ],
            [self.apksigner,
                'sign', '--ks', self.keystore.file,
                '--ks-key-alias', self.keystore.alias,
                '--ks-pass', 'pass:' + self.keystore.passw,
                '--key-pass', 'pass:' + self.keystore.passw,
                '--out', join("build", self.apk_name + ".apk"),
                join("build", self.apk_name + ".aligned.apk")
            ]
        ):
            subprocess.check_call(command)

    def build(self):
        self.makedirs()
        self.elm_make()
        self.build_apk()

    @classmethod
    def _check_adb_on_path(cls):
        try:
            subprocess.check_call(["adb", "--version"])
        except FileNotFoundError:
            quit_error(
                "Couldn't find your `adb` executable."
                " You probably need to add the"
                " .../Sdk/platform-tools/ directory to your PATH."
            )

    def install(self):
        self.__class__._check_adb_on_path()
        subprocess.check_call(["adb",
            "install", "-r", join("build", self.apk_name + ".apk")
        ])

    def run(self):
        self.__class__._check_adb_on_path()
        subprocess.check_call(["adb",
            "shell", "am", "start", "-n", self.package + "/.MainActivity"
        ])

class KeyStore:
    def __init__(self, file, alias, passw):
        self.file = file
        self.alias = alias
        self.passw = passw

    @classmethod
    def create_debug_key(cls):
        if os.path.isfile('debug.keystore'):
            quit_error("A debug.keystore file already exists in the current directory.")
        subprocess.check_call(['keytool',
            '-genkey', '-v', '-keystore', 'debug.keystore', '-storepass',
            'android', '-alias', 'androiddebugkey', '-keypass', 'android',
            '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
            '-dname', 'CN=Android Debug,O=Android,C=US'
        ])
        print("The key was created in the file: debug.keystore")

    @classmethod
    def create_key(cls):
        raise NotImplementedError

    @classmethod
    def from_current_dir_and_env(cls):
        try:
            keystore_file = os.environ['KEYSTORE_FILE']
        except KeyError:
            quit_error(
                "No keystore file was supplied through the KEYSTORE_FILE environment variable.\n"
                "Supply the keystore file through the KEYSTORE_FILE environment variable.\n"
                "For example, if you've generated a debug.keystore file using `manage.py create-debug-keystore`"
                " then use:\n"
                "KEYSTORE_FILE=debug.keystore manage.py ...\n"
                "If you don't have a keystore file yet, you can generate one using:\n"
                "./manage.py create-debug-keystore (for a debug key)\n"
                "or\n"
                "./manage.py create-keystore (for a normal key)"
            )
        else:
            if not os.path.isfile(keystore_file):
                quit_error(
                    "No such file %s" % repr(keystore_file)
                )
        if 'debug' in keystore_file:
            return cls(keystore_file, 'androiddebugkey', 'android')
        else:
            return cls(
                keystore_file,
                os.environ['KEYSTORE_ALIAS'],
                os.environ['KEYSTORE_PASS']
            )


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        quit_error(usage())
    if sys.argv[1] != 'create-key' and len(sys.argv) != 2:
        quit_error(usage())
    elif sys.argv[1] == 'create-debug-key':
        KeyStore.create_debug_key()
    elif sys.argv[1] == 'create-key':
        KeyStore.create_key()
    elif sys.argv[1] == 'build':
        Project.from_current_dir_and_env().build()
    elif sys.argv[1] == 'install':
        Project.from_current_dir_and_env().install()
    elif sys.argv[1] == 'install+run':
        Project.from_current_dir_and_env().install()
        Project.from_current_dir_and_env().run()
    elif sys.argv[1] == 'elm-live':
        subprocess.check_call([
            "elm-live", "src/Main.elm", "-d", "assets", "--", "--output=assets/main.js"
        ])

    else:
        quit_error(usage())
