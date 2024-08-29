# Flux Image Generator

## Description

This script, `run-flux.py`, is an image generation tool that utilizes the Flux Pro and Flux Schnell models via the Replicate API. It allows users to generate images based on text prompts, with various customizable parameters.

## Features

- Supports both Flux Pro and Flux Schnell models
- Customizable image generation parameters (e.g., seed, guidance, aspect ratio)
- Automatic file naming and saving
- Prompt saving in Markdown format
- Asynchronous operations for improved performance
- Progress bar for visual feedback during image generation
- API token caching to avoid repeated input
- Optimized image saving process
- Improved error handling and logging

## Requirements

- Python 3.7+
- `replicate` library
- `aiohttp` library
- `tqdm` library

## Installation

1. Clone this repository or download the `run-flux.py` file.

2. Install the required libraries:

```
pip install replicate aiohttp tqdm
```

3. Ensure you have a Replicate API token. You can obtain one from [Replicate](https://replicate.com/).

## Usage

1. Run the script:

```
python run-flux.py
```

2. Follow the prompts to:
   - Enter your Replicate API token (only required on first run)
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

## Recent Improvements

1. **Asynchronous Operations**: The script now uses `asyncio` and `aiohttp` for asynchronous operations, significantly improving performance when generating and downloading multiple images.

2. **Progress Bar**: A progress bar using the `tqdm` library has been added to provide visual feedback during image generation.

3. **API Token Caching**: The script now caches the API token in a file, eliminating the need to enter it every time the script is run.

4. **Optimized Image Saving**: The image saving process is now asynchronous, allowing for concurrent image downloads when multiple images are generated.

5. **Enhanced Error Handling**: Error handling and logging have been improved for better troubleshooting and stability.

6. **Code Refactoring**: The code has been restructured to be more modular and easier to maintain.

## Note

This script is intended for educational and personal use. While efforts have been made to improve its performance and reliability, it is not recommended for production environments without further development and testing.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Replicate](https://replicate.com/) for providing the API access to Flux models
- Black Forest Labs for creating the Flux Pro and Flux Schnell models

## Contributing

While this project is primarily for personal use, suggestions and feedback are welcome. Please open an issue to discuss any proposed changes or improvements.

