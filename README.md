[<img src="https://travis-ci.org/tinify/tinify-python.svg?branch=master" alt="Build Status">](https://travis-ci.org/tinify/tinify-python)

# Tinify API client for Python

## Installation

Install the API client:

```
pip install tinify
```

## Usage

```python
import tinify
tinify.set_key('YOUR_API_KEY')

tinify.from_file('unoptimized.png').to_file('optimized.png')
```

## Running tests

```
pip install -r requirements.txt -r test-requirements.txt
nosetests
```

## License

This software is licensed under the MIT License. [View the license](LICENSE).
