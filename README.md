# Flux Image Generator

## Description

This script, `run-flux.py`, is an image generation tool that utilizes the Flux Pro and Flux Schnell models via the Replicate API. It allows users to generate images based on text prompts, with various customizable parameters.

## Features

- Supports both Flux Pro and Flux Schnell models
- Customizable image generation parameters (e.g., seed, guidance, aspect ratio)
- Automatic file naming and saving
- Prompt saving in Markdown format
- Loading animation during image generation
- Error logging for troubleshooting

## Requirements

- Python 3.6+
- `replicate` library
- `requests` library

## Installation

1. Clone this repository or download the `run-flux.py` file.
2. Install the required libraries:

   ```
   pip install replicate requests
   ```

3. Ensure you have a Replicate API token. You can obtain one from [Replicate](https://replicate.com/).

## Usage

1. Run the script:

   ```
   python run-flux.py
   ```

2. Follow the prompts to:
   - Enter your Replicate API token
   - Choose the model (Flux Pro or Flux Schnell)
   - Enter the image generation parameters
   - Specify the save directory for generated images

3. The script will generate the image(s) and save them along with the prompts used.

## Note

This script is intended for educational and personal use. It is not recommended for production environments without further development and error handling.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Replicate](https://replicate.com/) for providing the API access to Flux models
- Black Forest Labs for creating the Flux Pro and Flux Schnell models

## Contributing

While this project is primarily for personal use, suggestions and feedback are welcome. Please open an issue to discuss any proposed changes or improvements.
