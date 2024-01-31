# llama-cpp-python Installation Guide

llama-cpp-python is a versatile library for efficient inference of Meta's LLaMA large language model. This installation guide will help you set up llama-cpp-python with different hardware backends to optimize performance. Whether you prefer OpenBLAS, Vulkan, CUDA, or ROCm, we've got you covered.

## Installation from PyPI (Recommended)

The recommended way to install llama-cpp-python is from PyPI. This method ensures that llama.cpp is built with optimizations tailored to your system.

```bash
pip install llama-cpp-python
```

If you need to upgrade or rebuild the package with different compiler options, use the following command:

```bash
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

## Installation with Hardware Acceleration

llama.cpp supports various BLAS backends and hardware acceleration options for enhanced performance.

### Installation with OpenBLAS

To install llama-cpp-python with OpenBLAS, set the `LLAMA_BLAS` and `LLAMA_BLAS_VENDOR` environment variables before installing:

```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
```

This command installs llama-cpp-python with OpenBLAS as the backend for faster processing.

### Installation with Vulkan

To install llama-cpp-python with Vulkan, follow these steps:

1. Set the `LLAMA_VULKAN` environment variable before installing:

   ```bash
   CMAKE_ARGS="-DLLAMA_VULKAN=on" pip install llama-cpp-python
   ```

2. This command installs llama-cpp-python with Vulkan support. Vulkan is particularly useful for unsupported graphics cards, providing an alternative to CUDA or ROCm.

### Installation with CUDA

For CUDA support, set the `LLAMA_CUBLAS` environment variable before installing:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

This command installs llama-cpp-python with CUDA acceleration.

### Installation with Metal

To install with Metal (MPS), set the `LLAMA_METAL=on` environment variable
before installing:

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

#### Note for Apple Silicon (M1) Mac Users

If you are using an Apple Silicon (M1) Mac, ensure you have a Python version that supports arm64 architecture. Follow these steps:

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

### Installation with ROCm

To install llama-cpp-python with ROCm support for AMD cards, set the `LLAMA_HIPBLAS` environment variable before installing:

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python
```

You can also specify additional environment variables for ROCm configuration:

```bash
LLAMA_HIPBLAS=on HIP_VISIBLE_DEVICES=0 HSA_OVERRIDE_GFX_VERSION=10.3.0 LLAMA_CUDA_DMMV_X=64 LLAMA_CUDA_MMV_Y=2 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

These instructions cover installation with OpenBLAS, Vulkan, CUDA, and ROCm to cater to various hardware configurations.
