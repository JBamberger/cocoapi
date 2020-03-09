from setuptools import setup, Extension
from distutils.command.build_ext import build_ext
import numpy as np

# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"


flags = {
    'msvc': [],
    'unix': ['-Wno-cpp', '-Wno-unused-function', '-std=c99']
}


class flagselector_build_ext(build_ext):
    def build_extentions(self):
        c = self.compiler.compiler_type
        if c in ['mingw32', 'unix', 'cygwin', 'bcpp']:
            args = flags['unix']
        elif c == 'msvc':
            args = flags['msvc']
        else:
            raise RuntimeError("Could not select compilation flags.")

        for e in self.extensions:
            e.extra_compile_args = args


ext_modules = [
    Extension(
        'pycocotools._mask',
        sources=['../common/maskApi.c', 'pycocotools/_mask.pyx'],
        include_dirs=[np.get_include(), '../common'],
    )
]

setup(
    name='pycocotools',
    packages=['pycocotools'],
    package_dir={'pycocotools': 'pycocotools'},
    install_requires=[
        'setuptools>=18.0',
        'cython>=0.27.3',
        'matplotlib>=2.1.0'
    ],
    version='2.0',
    ext_modules=ext_modules,
    cmdclass={'build_ext': flagselector_build_ext}
)
