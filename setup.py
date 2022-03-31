from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("bot.common", ["bot/common.py"]),
]
setup(
    name="common",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}, annotate=True),
)
