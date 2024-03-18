import argparse
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
from PIL import Image
from transformers import AutoTokenizer


def evaluate_path(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def initialize_pipeline(
    model_file_path: str, config: dict
) -> StableDiffusionXLImg2ImgPipeline:
    if config.get("use_single_file", False):
        pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(
            model_file_path,
            **config,
        )
    else:
        for key in ["use_single_file", "load_safety_checker"]:
            config.pop(key, None)
        pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
            model_file_path,
            **config,
        )
    pipe.to(device=config.get("device", "cpu"))
    return pipe


def initialize_lora(
    pipe: StableDiffusionXLImg2ImgPipeline,
    model_path: str,
    adapter_name: Optional[str] = None,
    **kwargs: Any,
) -> StableDiffusionXLImg2ImgPipeline:
    """
    Load LoRA weights into the StableDiffusionXLImg2ImgPipeline.

    This function loads LoRA weights specified in `model_path` into the pipeline.
    It enhances the pipeline's capabilities for text-to-image generation.

    Parameters:
        pipe (StableDiffusionXLImg2ImgPipeline): The image generation pipeline to enhance with LoRA weights.
        pretrained_model_name_or_path_or_dict (Union[str, os.PathLike, Dict[str, Any]]):
            Path to the LoRA weights file or a dictionary containing the weights.
        adapter_name (str, optional):
            Adapter name to be used for referencing the loaded adapter model. If not specified, it will use
            a default name based on the total number of adapters being loaded.
        **kwargs (Any, optional):
            Additional keyword arguments to customize the loading process.

    Returns:
        StableDiffusionXLImg2ImgPipeline: The enhanced pipeline with LoRA weights loaded.

    Note:
        - You should have a StableDiffusionXLImg2ImgPipeline instance created before calling this function.
        - The `pretrained_model_name_or_path_or_dict` parameter should point to the location of LoRA weights
          or a dictionary containing the weights.
        - If you want to reference the loaded adapter model with a specific name, you can specify it using
          the `adapter_name` parameter.
        - Additional keyword arguments can be passed via `kwargs` to further customize the loading process,
          such as specifying the exact components of LoRA to load.
    """
    # Check if the provided path is valid and load the LoRA weights
    pipe.load_lora_weights(model_path, adapter_name=adapter_name, **kwargs)
    # Return the modified pipe
    return pipe


def initialize_image(
    image_path: str,
    dimensions: Tuple[int, int] = None,
) -> Image:
    """
    Initialize and preprocess the input image.

    Args:
        image_path (str): Path to the initial image.
        dimensions (Tuple[int, int], optional): Desired image dimensions (width, height).
            If None, default dimensions (768x512) are used.

    Returns:
        Image: Preprocessed image.
    """
    init_image = Image.open(evaluate_path(image_path)).convert("RGB")

    if dimensions is None:
        init_image = init_image.resize((768, 512))
    else:
        init_image = init_image.resize(dimensions)

    return init_image


def handle_pipeline_result(result: StableDiffusionPipelineOutput) -> List[Image]:
    """
    Handle the result from the diffusion pipeline and convert it into a list of PIL Images.

    Args:
        result (StableDiffusionPipelineOutput): Result from the diffusion pipeline.

    Returns:
        List[Image]: List of generated images.
    """
    if isinstance(result.images, list):
        images = result.images
    elif isinstance(result.images, np.ndarray):
        images = [Image.fromarray(img) for img in result.images]
    else:
        raise ValueError("Unsupported image format")

    return images


def write_images(
    images: List[Image],
    output_directory: str = "images",
    delay: float = 1 / 30,
) -> List[Tuple[Image, str]]:
    """
    Write the generated images to the specified output directory.

    Args:
        images (List[Image]): List of generated images.
        output_directory (str, optional): Directory to save generated images.
        delay (float, optional): Delay between image generation.

    Returns:
        List[Tuple[Image, str]]: List of tuples containing generated images and their paths.
    """
    dataset = []

    for image in images:
        image_path = f"{output_directory}/{datetime.now()}.png"
        image.save(image_path)
        dataset.append((image, image_path))
        print(f"Created: {image_path}")
        time.sleep(delay)  # NOTE: Prevent overwrites

    return dataset


def get_estimated_steps(strength: float, num_inference_steps: int) -> int:
    """
    Estimate the number of inference steps based on the strength parameter.

    This function simulates the calculation performed internally by the StableDiffusionXLImg2ImgPipeline in the
    diffusers library when processing image-to-image tasks. It determines the effective number of inference
    steps that will be used by the pipeline, considering the influence of the strength parameter.

    Parameters:
    - strength (float): The amount of noise to add to the image, typically between 0 and 1.
    - num_inference_steps (int): The initially desired number of inference steps.

    Returns:
    - int: The estimated number of inference steps after considering the strength parameter.

    Note:
    - In the context of the StableDiffusionXLImg2ImgPipeline, the strength parameter affects the starting point of the
      denoising process. A lower strength value reduces the number of effective inference steps. This function mimics
      that behavior by scaling down the number of steps based on the strength value.

    Example:
    >>> get_estimated_steps(0.5, 50)
    25
    >>> get_estimated_steps(1.0, 50)
    50
    """
    return min(int(num_inference_steps * strength), num_inference_steps)


def adjust_inference_steps(
    strength: float, num_inference_steps: int, allow_low_strength=False
) -> int:
    """
    Adjust the number of inference steps for the StableDiffusionXLImg2ImgPipeline based on the strength parameter.

    The function scales the number of inference steps to compensate for the reduction caused by lower strength values.
    It ensures that the effective number of inference steps remains close to the desired amount, despite the strength parameter's influence.

    Parameters:
    - strength (float): The amount of noise to add to the image, typically between 0 and 1.
    - num_inference_steps (int): The desired number of inference steps.
    - allow_low_strength (bool): If set to True, allows strength values below 10%. Defaults to False.

    Returns:
    - int: The adjusted number of inference steps.

    Raises:
    - ValueError: If strength is below 10% and allow_low_strength is False. Lower strength values significantly alter the number of inference steps, leading to unpredictable results. This behavior can be bypassed by specifying a denoising start value.

    Note:
    - This function normalizes the strength value to a percentage for easier comparison and decision-making.
    - It's tailored to the behavior of the StableDiffusionXLImg2ImgPipeline in the diffusers library, where the strength parameter influences the starting point of the denoising process.

    Example:
    >>> adjust_inference_steps(0.5, 50)
    50
    >>> adjust_inference_steps(0.05, 50)
    ValueError: Strength must be at least 10% unless a denoising start value is specified.
    """
    estimated_strength = strength * 100  # normalize the float value
    if estimated_strength < 10 and not allow_low_strength:
        raise ValueError(
            "Strength must be at least 10% unless a denoising start value is specified."
        )

    # Calculate the original estimated inference steps
    original_estimated_steps = get_estimated_steps(strength, num_inference_steps)

    # Determine the adjustment factor
    adjustment_factor = num_inference_steps / max(original_estimated_steps, 1)

    # Apply the adjustment
    return int(num_inference_steps * adjustment_factor)


def generate_images(
    pipe: StableDiffusionXLImg2ImgPipeline,
    image_path: str,
    prompt: str,
    negative_prompt: Optional[str] = None,
    strength=0.75,
    num_inference_steps: int = 50,
    guidance_scale=7.5,
    num_images_per_prompt: int = 2,
    output_directory: str = "images",
    delay: float = 1 / 30,
    dimensions: Optional[Tuple[int, int]] = None,
) -> Tuple[List[Tuple[Image, str]], float]:
    try:
        start_time = datetime.now()
        init_image = initialize_image(image_path, dimensions)

        adjusted_inference_steps = adjust_inference_steps(strength, num_inference_steps)

        result = pipe(
            prompt=prompt,
            image=init_image,
            strength=strength,
            num_inference_steps=adjusted_inference_steps,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images_per_prompt,
        )

        images = handle_pipeline_result(result)
        dataset = write_images(images, output_directory, delay)

        end_time = datetime.now()
        elapsed_time = end_time - start_time

        return dataset, elapsed_time

    except KeyboardInterrupt:
        # Gracefully interrupt image generation
        print("KeyboardInterrupt: Exiting now.")
        exit(1)


def assert_prompt_length(
    tokenizer_path: str,
    prompt: str,
    negative_prompt: Optional[str] = None,
) -> None:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    prompt_tokens = len(tokenizer.encode(prompt))
    negative_prompt_tokens = len(
        tokenizer.encode(negative_prompt) if negative_prompt else []
    )
    model_max_length = tokenizer.model_max_length
    if prompt_tokens > model_max_length:
        raise ValueError(
            f"Prompt is {prompt_tokens} out of {model_max_length} tokens. Shorten your prompts."
        )
    print(f"Prompt is okay: Using {prompt_tokens} tokens.\n")
    if negative_prompt_tokens > tokenizer.model_max_length:
        raise ValueError(
            f"Negative prompt is {negative_prompt_tokens} out of {model_max_length} tokens. Shorten your prompts."
        )
    print(f"Negative prompt is okay: Using {negative_prompt_tokens} tokens.\n")


def initialize_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate images using diffusion-based models."
    )
    parser.add_argument("model", help="Path to the diffusion model or model ID")
    parser.add_argument("image", help="Path to the initial image")
    parser.add_argument("prompt", help="Prompt for image generation")
    parser.add_argument(
        "--use_single_file", action="store_true", help="Use a fine-tuned model"
    )
    parser.add_argument(
        "--negative_prompt", help="Negative prompt for image generation"
    )
    parser.add_argument(
        "--output_dir", default="images", help="Directory to save generated images"
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=0.75,
        help="The amount of noise added to the image. Values must be between 0 and 1.",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=7.5,
        help="Guidance scale for image generation",
    )
    parser.add_argument(
        "--num_images", type=int, default=2, help="Number of images to generate"
    )
    parser.add_argument(
        "--num_steps", type=int, default=50, help="Number of inference steps"
    )
    parser.add_argument(
        "--lora",
        action="store_true",
        help="Use LoRA for fine-tuning the model",
    )
    parser.add_argument(
        "--lora_path",
        help="Path to LoRA weights",
    )
    parser.add_argument(
        "--adapter_name",
        help="Name of the LoRA adapter",
    )
    parser.add_argument(
        "--delay", type=float, default=1 / 30, help="Delay between image generation"
    )
    parser.add_argument(
        "--device", default="cpu", help="The device to use. Defaults to 'cpu'"
    )
    parser.add_argument(
        "--tokenizer", default=None, help="Path to the models tokenizer"
    )

    return parser


def main():
    parser = initialize_arg_parser()
    args = parser.parse_args()

    if args.tokenizer is not None:
        assert_prompt_length(args.tokenizer, args.prompt, args.negative_prompt)

    config = {
        "use_single_file": args.use_single_file,  # You can customize other model-specific parameters here
        "device": args.device,  # Change to "cuda" if using GPU
        "variant": "fp16",
        "torch_dtype": torch.bfloat16,
        "use_safetensors": True,
        "load_safety_checker": False,
        "add_watermarker": False,
    }

    pipe = initialize_pipeline(args.model, config)

    if args.lora is True:
        initialize_lora(pipe, args.lora_path, args.adapter_name)

    images, elapsed_time = generate_images(
        pipe,
        args.image,
        args.prompt,
        negative_prompt=args.negative_prompt,
        strength=args.strength,
        num_inference_steps=args.num_steps,
        guidance_scale=args.guidance_scale,
        num_images_per_prompt=args.num_images,
        output_directory=args.output_dir,
        delay=args.delay,
    )

    print(f"Elapsed time: {elapsed_time}")


if __name__ == "__main__":
    main()
