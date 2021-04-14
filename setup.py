from setuptools import setup

setup(
    name='sh_bucket_gen',
    version='0.1',
    py_modules=['sh_bucket_gen'],
    install_requires=[
        'Click',
        'boto3',
        'python-decouple',
    ],
    entry_points='''
        [console_scripts]
        sh_bucket_gen=sh_bucket_gen:main
    ''',
)