from distutils.core import setup

setup(
    name='nocc',
    version='0.1.0',
    license='GPL-3.0',
    packages=['nocc', 'nocc.utils'],
    scripts=['bin/nocc'],
    description='Remove Deaf & Hard of Hearing content in str subtitles',
    install_requires=[
        "python-magic",
        "click",
        "pysrt",
        "cchardet"
    ],
)
