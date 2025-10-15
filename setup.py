from setuptools import setup

setup(
    name='limitwarden',
    version='0.1.0',
    py_modules=[
        'main',
        'scanner',
        'manifest_patcher',
        'patcher',
        'metrics',
        'heuristics',
        'config',
    ],
    packages=['utils'],
    install_requires=[
        'kubernetes',
        'PyYAML',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'limitwarden=main:main',
        ],
    },
    author='Marie Grin',
    description='LimitWarden: Kubernetes resource hygiene enforcer',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mariedevops/limitwarden',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
