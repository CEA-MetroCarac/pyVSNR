from setuptools import setup, find_packages

setup(
    name="pyVSNR",
    version='1.0.2',
    license='GPLv3',
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
    ],
    packages=find_packages(),

    description="VSNR (Variational Stationary Noise Remover) algorithm in "
                "python",

    url="https://github.com/CEA-MetroCarac/pyVSNR",
    author_email="patrick.quemere@cea.fr",
    author="Patrick Quéméré",
    keywords="VSNR, noise reduction",
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GPL-3.0 license',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Console',
    ],
)
