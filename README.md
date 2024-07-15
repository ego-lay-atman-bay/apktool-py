# apktool-py

ApktoolPy is a python wrapper for [Apktool](https://apktool.org/). It is mainly a python api, but can also be ran from the command line.

This project is in no way affiliated with apktool, and will most likely not receive updates immediately. The package version is also not a reflection of the apktool version.

# Installation

The only installation requirements are the same ones as apktool, which can be found here: https://apktool.org/docs/install (you do not need to download a wrapper script, or the apktool jar, that's what this package is).

You can just install this from pypi with

```
pip install apktool-py
```

# Python api

Usage

```python
import apktool

apktool.decode('app.apk', 'app')
apktool.build('app', 'app-build.apk')

# Get apktool version
apktool.version()
```

I don't feel like showing the entire api here, so just use your IDE to figure it out. Hint, it's very similar to the apktool arguments. You can also just look in the source files.

# Running from the command line

You can also run apktool from the command line with

```
apktool --help
```

or

```
python -m apktool --help
```

Note: this just passes the arguments directly into apktool, they are different from the python api.

# Credits
- [Apktool](https://apktool.org/)
  - brut.all
  - iBotPeaches
  - JesusFreke
