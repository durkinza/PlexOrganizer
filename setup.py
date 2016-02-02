from setuptools import setup, find_packages
from PlexOrganizer import __version__ as organizer_version
from pip.req import parse_requirements
from pip import download

# Let's get our requirements from requirements.txt
requirements = parse_requirements("requirements.txt", session=download.PipSession())
my_requirements = [str(req.req) for req in requirements]

setup(
    name='PlexOrganizer',
    version = organizer_version,
    description='Python Plex media file manager.',
    author='Zane Durkin',
    author_email='zanedurkin@gmail.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=my_requirements
)
