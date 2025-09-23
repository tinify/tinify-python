[![MIT License](http://img.shields.io/badge/license-MIT-green.svg) ](https://github.com/tinify/tinify-python/blob/main/LICENSE)
[![CI](https://github.com/tinify/tinify-python/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/tinify/tinify-python/actions/workflows/ci-cd.yml)
[![PyPI](https://img.shields.io/pypi/v/tinify)](https://pypi.org/project/tinify/#history)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinify)](https://pypi.org/project/tinify/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/tinify)](https://pypi.org/project/tinify/)


# Tinify API client for Python

**Tinify** is the official Python client for the [TinyPNG](https://tinypng.com) and [TinyJPG](https://tinyjpg.com/) image compression API, enabling developers to intelligently compress, resize, convert and optimize PNG, APNG, JPEG, WebP and AVIF images programmatically. Read more at [https://tinify.com](https://tinify.com/developers).


[Go to the full documentation for the Python client](https://tinypng.com/developers/reference/python).

## Features

- Compress and optimize images, reducing file size by 50-80% while preserving visual quality
- Resize and crop images with smart compression
- Convert between PNG, JPEG, WebP and AVIF formats
- Preserve metadata (optional)
- Upload to storage providers like Amazon S3, Google cloud storage.
- Apply visual transformations with the Tinify API
- Comprehensive error handling



## Requirements

- Python 2.7+
- Requests library

## Installation

Install the API client with pip:

```bash
pip install tinify
```

## Quick start


```python
import tinify

# Set your API key (get one for free at https://tinypng.com/developers)
tinify.key = "YOUR_API_KEY"

# Compress an image from a file
tinify.from_file("unoptimized.png").to_file("optimized.png")

# Compress from URL
tinify.from_url("https://example.com/image.jpg").to_file("optimized.jpg")

# Compress from buffer
source_data = b"<image data>"
tinify.from_buffer(source_data).to_file("optimized.jpg")
```

## Advanced Usage

### Resizing

```python
# Scale image to fit within 300x200px while preserving aspect ratio
tinify.from_file("original.jpg").resize(
    method="scale",
    width=300,
    height=200
).to_file("resized.jpg")

# Fit image to exact 300x200px dimensions
tinify.from_file("original.jpg").resize(
    method="fit",
    width=300,
    height=200
).to_file("resized.jpg")

# Cover 300x200px area while preserving aspect ratio
tinify.from_file("original.jpg").resize(
    method="cover",
    width=300,
    height=200
).to_file("resized.jpg")
```

### Format Conversion

```python
# Convert to WebP format
tinify.from_file("image.png").convert(
    type=["image/webp"]
).to_file("image.webp")
```

```python
# Convert to smallest format
converted = tinify.from_file("image.png").convert(
    type=["image/webp", "image/webp"]
)
extension = converted.result().extension
converted.to_file("image." + extension)
```

### Compression Count Monitoring

```python
# Check the number of compressions made this month
compression_count = tinify.compression_count
print(f"You have made {compression_count} compressions this month")
```

## Error Handling

```python
import tinify

tinify.key = "YOUR_API_KEY"

try:
    tinify.from_file("unoptimized.png").to_file("optimized.png")
except tinify.AccountError as e:
    # Verify or update API key
    print(f"Account error: {e.message}")
except tinify.ClientError as e:
    # Handle client errors (e.g., invalid image)
    print(f"Client error: {e.message}")
except tinify.ServerError as e:
    # Handle server errors
    print(f"Server error: {e.message}")
except tinify.ConnectionError as e:
    # Handle network connectivity issues
    print(f"Connection error: {e.message}")
except Exception as e:
    # Handle general errors
    print(f"Error: {str(e)}")
```

## Running tests

```
pip install -r requirements.txt -r test-requirements.txt
py.test
```

To test more runtimes, tox can be used

```
tox
```



### Integration tests

```
pip install -r requirements.txt -r test-requirements.txt
TINIFY_KEY=$YOUR_API_KEY py.test test/integration.py
```

## License

This software is licensed under the MIT License. See [LICENSE](https://github.com/tinify/tinify-python/blob/master/LICENSE) for details.

## Support

For issues and feature requests, please use our [GitHub Issues](https://github.com/tinify/tinify-python/issues) page or contact us at [support@tinify.com](mailto:support@tinify.com)
