# `llama-cpp-python` Installation Guide

`llama-cpp-python` is a state-of-the-art library for efficient inference with Meta's LLaMA large language model, optimized for various hardware acceleration technologies. This guide provides detailed instructions for setting up `llama-cpp-python` on systems with Python 3.8 or later, highlighting support for OpenBLAS, Vulkan, CUDA, ROCm, and Metal.

## Prerequisites

Before proceeding, ensure your system meets the following requirements:
- Python version 3.8 or later installed.
- `pip` is updated to the latest version to avoid any compatibility issues.

## Installation from PyPI (Recommended)

Install `llama-cpp-python` directly from PyPI to ensure you get a version built with optimizations specific to your system:

```bash
pip install llama-cpp-python
```

For upgrading or rebuilding with different options:

```bash
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

## Installation with Hardware Acceleration

Follow the corresponding section below based on your preferred or available hardware acceleration backend.

### Installation with OpenBLAS

For enhanced processing with OpenBLAS:

```bash
export CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
pip install llama-cpp-python
```

This configures `llama-cpp-python` to use OpenBLAS, offering faster computation where supported.

### Installation with Vulkan

Vulkan support, useful for systems with unsupported graphics cards:

```bash
export CMAKE_ARGS="-DLLAMA_VULKAN=on"
pip install llama-cpp-python
```

### Installation with CUDA

For NVIDIA GPUs, enabling CUDA acceleration:

```bash
export CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python
```

### Installation with Metal (Apple Silicon)

Apple Silicon users can leverage Metal for acceleration:

```bash
export CMAKE_ARGS="-DLLAMA_METAL=on"
pip install llama-cpp-python
```

Ensure your Python installation supports `arm64` architecture. For Miniforge on Apple Silicon:

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

### Installation with ROCm (AMD GPUs)

For AMD GPU acceleration with ROCm:

```bash
export CMAKE_ARGS="-DLLAMA_HIPBLAS=on"
pip install llama-cpp-python
```

Specify additional ROCm configuration as needed:

```bash
export LLAMA_HIPBLAS=on
export HIP_VISIBLE_DEVICES=0
export HSA_OVERRIDE_GFX_VERSION=10.3.0
export LLAMA_CUDA_DMMV_X=64
export LLAMA_CUDA_MMV_Y=2
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

## Troubleshooting

If you encounter any issues, consider the following solutions:
- Verify that your Python and `pip` versions are up to date, as `llama-cpp-python` supports Python 3.8 or higher.
- Ensure your GPU drivers and any required installations (CUDA/ROCm) are current and correctly set up.
- Check that environment variables are properly configured in your system.

For more detailed troubleshooting, visit:
- [Issues for GPU-related problems](https://github.com/abetlen/llama-cpp-python/issues?q=is%3Aissue+is%3Aopen+gpu)
- [Discussions for GPU-related questions](https://github.com/abetlen/llama-cpp-python/discussions?discussions_q=is%3Aopen+gpu)

## Further Resources

For more information on the specific technologies and configurations mentioned here, please refer to the following resources:
- [OpenBLAS Documentation](https://www.openblas.net/)
- [Vulkan Guide](https://vulkan.lunarg.com/)
- [CUDA Toolkit Documentation](https://developer.nvidia.com/cuda-toolkit)
- [ROCm Installation](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation-Guide.html)
- [Metal for Developers](https://developer.apple.com/metal/)

## Community Support

Your participation and feedback are highly valued in our community. If you have questions, feedback, or require assistance, you're encouraged to join the community forum or file an issue related to `llama.cpp` and `llama-cpp-python` development on GitHub. This collaborative effort not only helps you but also enhances the tool for others.

For `llama.cpp`-specific inquiries or contributions, the `llama.cpp` GitHub repository is the go-to resource. Engaging with the community through forums, discussions, or by contributing directly can offer valuable insights and support for your projects.
