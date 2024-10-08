import os
import replicate
import aiohttp
import asyncio
import logging
import time
from tqdm import tqdm
from pathlib import Path

# Setup logging
logging.basicConfig(filename='image_generation.log', level=logging.DEBUG)

async def get_api_token():
    token_file = Path.home() / '.replicate_token'
    if token_file.exists():
        return token_file.read_text().strip()
    token = input("Please enter your REPLICATE_API_TOKEN: ")
    token_file.write_text(token)
    return token

def get_aspect_ratio():
    aspect_ratios = ["1:1", "16:9", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"]
    print("Available aspect ratios:")
    for i, ratio in enumerate(aspect_ratios, 1):
        print(f"{i}. {ratio}")
    while True:
        choice = input(f"Select an aspect ratio (1-{len(aspect_ratios)}) [default: 1:1]: ")
        if choice == "":
            return "1:1"
        if choice.isdigit() and 1 <= int(choice) <= len(aspect_ratios):
            return aspect_ratios[int(choice) - 1]
        print("Invalid choice. Please try again.")

def get_numeric_input(prompt, default, min_value, max_value):
    while True:
        value = input(f"{prompt} [{default}]: ")
        if value == "":
            return default
        try:
            value_float = float(value)
            if min_value <= value_float <= max_value:
                return value_float
            else:
                print(f"Value must be between {min_value} and {max_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

async def save_image(session, url, filename):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            with open(filename, 'wb') as f:
                f.write(content)
        print(f"\nImage saved as {filename}")
    except aiohttp.ClientError as e:
        print(f"\nFailed to download image: {e}")
        logging.error("Failed to download image", exc_info=True)

def save_prompt_as_md(prompt, filename):
    try:
        with open(filename, 'w') as f:
            f.write(f"# Image Generation Prompt\n\n{prompt}\n")
        print(f"Prompt saved as {filename}")
    except Exception as e:
        print(f"Failed to save prompt: {e}")
        logging.error("Failed to save prompt", exc_info=True)

def format_filename(prompt_number, model, seed, aspect_ratio, safety_tolerance, steps, interval, suffix):
    ar_map = {"1:1": "ar11", "16:9": "ar169", "21:9": "ar219", "2:3": "ar23", "3:2": "ar32", "4:5": "ar45", "5:4": "ar54", "9:16": "ar916", "9:21": "ar921"}
    ar_formatted = ar_map.get(aspect_ratio, "ar11")
    model_short = "fp" if model == "flux-pro" else "fs"
    safety_formatted = f"{safety_tolerance}" if safety_tolerance is not None else ""
    steps_formatted = f"{steps}" if steps is not None else ""
    interval_formatted = f"{interval}" if interval is not None else ""
    return f"{prompt_number}-{model_short}-{seed}-{ar_formatted}-{safety_formatted}-{steps_formatted}-{interval_formatted}_{suffix:03}"

def get_save_directory():
    default_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    user_dir = input(f"Enter the directory to save images [default: {default_dir}]: ")
    if user_dir == "":
        return default_dir
    if os.path.isdir(user_dir):
        return user_dir
    else:
        print(f"Directory {user_dir} does not exist. Using default directory.")
        return default_dir

def select_model():
    models = [
        ("Flux Pro", "black-forest-labs/flux-pro"),
        ("Flux Schnell", "black-forest-labs/flux-schnell")
    ]
    print("Available models:")
    for i, (name, _) in enumerate(models, 1):
        print(f"{i}. {name}")
    while True:
        choice = input(f"Select a model (1-{len(models)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        print("Invalid choice. Please try again.")

async def generate_image(model_id, input_data):
    with tqdm(total=100, desc="Generating image", bar_format='{l_bar}{bar}') as pbar:
        output = await asyncio.to_thread(replicate.run, model_id, input=input_data)
        pbar.update(100)
    return output

async def main():
    REPLICATE_API_TOKEN = await get_api_token()
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
    save_dir = get_save_directory()
    image_count = 1
    prompt_number = input("Enter a prompt number (e.g., 001): ")

    async with aiohttp.ClientSession() as session:
        while True:
            model_name, model_id = select_model()
            prompt = input("Please enter your image generation prompt: ")
            input_data = {"prompt": prompt}

            if "flux-pro" in model_id:
                seed = get_numeric_input("Enter seed (integer)", 12, 0, 2**32-1)
                guidance = get_numeric_input("Enter guidance value", 3.5, 2, 5)
                aspect_ratio = get_aspect_ratio()
                safety_tolerance = get_numeric_input("Enter safety tolerance", 5, 1, 5)
                steps = get_numeric_input("Enter number of steps", 30, 1, 50)
                interval = get_numeric_input("Enter interval", 2, 1, 4)
                input_data.update({
                    "seed": int(seed),
                    "guidance": guidance,
                    "aspect_ratio": aspect_ratio,
                    "safety_tolerance": int(safety_tolerance),
                    "steps": int(steps),
                    "interval": interval
                })
            else:  # Flux Schnell
                seed = get_numeric_input("Enter seed (integer)", 12, 0, 2**32-1)
                aspect_ratio = get_aspect_ratio()
                num_outputs = get_numeric_input("Enter number of outputs", 1, 1, 4)
                output_format = input("Enter output format (webp/jpg/png) [default: webp]: ").lower() or "webp"
                output_quality = get_numeric_input("Enter output quality", 80, 0, 100)
                input_data.update({
                    "seed": int(seed),
                    "aspect_ratio": aspect_ratio,
                    "num_outputs": int(num_outputs),
                    "output_format": output_format,
                    "output_quality": int(output_quality),
                    "disable_safety_checker": True  # Set to True by default
                })

            try:
                output = await generate_image(model_id, input_data)

                if isinstance(output, list):  # Flux Schnell returns a list of URLs
                    tasks = []
                    for i, url in enumerate(output):
                        if isinstance(url, str) and url.startswith('http'):
                            filename_base = format_filename(prompt_number,
                                                            "flux-schnell",
                                                            input_data.get('seed', 0),
                                                            input_data.get('aspect_ratio', '1:1'),
                                                            None,  # safety_tolerance not applicable
                                                            None,  # steps not applicable
                                                            None,  # interval not applicable
                                                            image_count + i)
                            image_filename = os.path.join(save_dir, f"{filename_base}.{input_data['output_format']}")
                            tasks.append(save_image(session, url, image_filename))
                    await asyncio.gather(*tasks)
                    image_count += len(output)
                    md_filename = os.path.join(save_dir, f"{prompt_number}_{image_count:03}.md")
                    save_prompt_as_md(prompt, md_filename)
                elif isinstance(output, str) and output.startswith('http'):  # Flux Pro returns a single URL
                    filename_base = format_filename(prompt_number,
                                                    "flux-pro",
                                                    input_data.get('seed', 0),
                                                    input_data.get('aspect_ratio', '1:1'),
                                                    input_data.get('safety_tolerance', 0),
                                                    input_data.get('steps', 0),
                                                    input_data.get('interval', 0),
                                                    image_count)
                    image_filename = os.path.join(save_dir, f"{filename_base}.png")
                    md_filename = os.path.join(save_dir, f"{prompt_number}_{image_count:03}.md")
                    await save_image(session, output, image_filename)
                    save_prompt_as_md(prompt, md_filename)
                    image_count += 1
                else:
                    print("\nNo valid output was generated.")
                    print(f"Received output: {output}")
                    logging.error("No valid output was generated", exc_info=True)

                print(f"Total images generated: {image_count - 1}")
            except Exception as e:
                print(f"\nAn error occurred while generating the image: {str(e)}")
                logging.error("An error occurred while generating the image", exc_info=True)

            cont = input("Do you want to generate another image? (y/n): ").strip().lower()
            if cont != 'y':
                break

if __name__ == "__main__":
    asyncio.run(main())
