## llama-cpp-python Installation

llama-cpp-python can be installed from PyPI or with different BLAS backends for
faster processing.

### Installation from PyPI (recommended)

Install from PyPI (requires a c compiler):

```bash
pip install llama-cpp-python
```

The above command will attempt to install the package and build `llama.cpp` from
source. This is the recommended installation method as it ensures that
`llama.cpp` is built with the available optimizations for your system.

If you have previously installed `llama-cpp-python` through pip and want to
upgrade your version or rebuild the package with different compiler options,
please add the following flags to ensure that the package is rebuilt correctly:

```bash
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

Note: If you are using Apple Silicon (M1) Mac, make sure you have installed a
version of Python that supports arm64 architecture. For example:

```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

Otherwise, while installing it will build the llama.ccp x86 version which will
be 10x slower on Apple Silicon (M1) Mac.

### Installation with Hardware Acceleration

`llama.cpp` supports multiple BLAS backends for faster processing.

To install with OpenBLAS, set the `LLAMA_BLAS and LLAMA_BLAS_VENDOR` environment
variables before installing:

```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
```

To install with cuBLAS, set the `LLAMA_CUBLAS=1` environment variable before
installing:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

To install with CLBlast, set the `LLAMA_CLBLAST=1` environment variable before
installing:

```bash
CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install llama-cpp-python
```

To install with Metal (MPS), set the `LLAMA_METAL=on` environment variable
before installing:

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

To install with hipBLAS / ROCm support for AMD cards, set the `LLAMA_HIPBLAS=on`
environment variable before installing:

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" pip install llama-cpp-python
```

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with hipBLAS / ROCm support for AMD cards, set the `LLAMA_HIPBLAS=on`
environment variable before installing:

**Building llama.cpp for AMD GPU**

1. Clone the llama.cpp repository:

   ```sh
   git clone <llama.cpp_repository_url>
   ```

2. Navigate to the llama.cpp directory:

   ```sh
   cd llama.cpp
   ```

3. Clean the previous build (optional but recommended):

   ```sh
   make clean
   ```

4. Set the required environment variables (adjust values if necessary):

   ```sh
   export HIP_VISIBLE_DEVICES=0  # If you have more than one GPU
   export HSA_OVERRIDE_GFX_VERSION=10.3.0  # If your GPU is not officially supported
   ```

5. Configure the build using CMake:

   ```sh
   CC=/opt/rocm/llvm/bin/clang CXX=/opt/rocm/llvm/bin/clang++ cmake .. -DLLAMA_HIPBLAS=ON -DLLAMA_CUDA_DMMV_X=64 -DLLAMA_CUDA_MMV_Y=2
   ```

6. Build llama.cpp:
   ```sh
   cmake --build .
   ```

**Building llama-cpp-python for AMD GPU**

1. Make sure you have the llama.cpp repository cloned and built as mentioned
   above.

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install llama-cpp-python with the required environment variables (adjust
   values if necessary):
   ```sh
   LLAMA_HIPBLAS=on HIP_VISIBLE_DEVICES=0 HSA_OVERRIDE_GFX_VERSION=10.3.0 LLAMA_CUDA_DMMV_X=64 LLAMA_CUDA_MMV_Y=2 pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
   ```

These simplified instructions should help both users and repository maintainers
easily set up llama.cpp and llama-cpp-python for AMD GPUs.
