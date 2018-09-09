# gaia

![Python Version Support](https://img.shields.io/badge/python-3.4%203.5%203.6%203.6--dev%203.7--dev-brightgreen.svg)
[![Build Status](https://travis-ci.org/deadlylaid/gaia.svg?branch=develop)](https://travis-ci.org/deadlylaid/gaia)
[![GitHub license](https://img.shields.io/github/license/deadlylaid/gaia.svg)](https://github.com/deadlylaid/gaia/blob/develop/LICENSE)
[![codecov](https://codecov.io/gh/deadlylaid/gaia/branch/develop/graph/badge.svg)](https://codecov.io/gh/deadlylaid/gaia)
[![Documentation Status](https://readthedocs.org/projects/gaia-aws-logfinder/badge/?version=latest)](https://gaia-aws-logfinder.readthedocs.io/en/latest/?badge=latest)



Gaia can help you find AWS logs easily



### Contribute

If someone wants to contribute to Gaia, follow this process

```
python -m venv boot
source boot/bin/activate
pip install --upgrade setuptools pip
pip install -e .[test,doc]
cd docs; make html; open _build/html/index.html
```

