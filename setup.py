from setuptools import setup

setup(
    name="necntp",
    version="0.1.0",
    description="NTP syncronizer based on the NTPD's shared memory interface",
    author="r-yamada1998",
    author_email="yamadier@icloud.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">3.7,<4.0",
    install_requires=[
        "ntplib>=0.4.0,<0.5.0",
        "sysv-ipc>=1.1.0,<2.0.0"
    ],
)
