set -e

# remove old build files
rm -rf build dist *.egg-info

# build distribution
python setup.py bdist

# upload to pypi
twine upload dist/*