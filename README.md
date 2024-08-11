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

## File Naming Convention

The generated images are saved with a specific naming convention:

```
[prompt number]-[model]-[seed]-[aspect ratio]-[safety tolerance]-[steps]-[interval]_[suffix]
```

- `[prompt number]`: User-defined prompt number (e.g., 001)
- `[model]`: 'fp' for Flux Pro, 'fs' for Flux Schnell
- `[seed]`: Seed value used for generation
- `[aspect ratio]`: Formatted aspect ratio (e.g., ar169 for 16:9)
- `[safety tolerance]`: Safety tolerance value (Flux Pro only)
- `[steps]`: Number of steps (Flux Pro only)
- `[interval]`: Interval value (Flux Pro only)
- `[suffix]`: A three-digit number indicating the image count

Example: `008-fp-12-ar169-5-30-2_004.png`

Note: For Flux Schnell, the safety tolerance, steps, and interval fields will be omitted.

## Note

This script is intended for educational and personal use. It is not recommended for production environments without further development and error handling.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Replicate](https://replicate.com/) for providing the API access to Flux models
- Black Forest Labs for creating the Flux Pro and Flux Schnell models

## Contributing

While this project is primarily for personal use, suggestions and feedback are welcome. Please open an issue to discuss any proposed changes or improvements.
