## llama-cpp-python Installation

llama-cpp-python can be installed from PyPI or with different BLAS backends for
faster processing.

### Installation from PyPI (recommended)

Install from PyPI (requires a C compiler):

```bash
pip install llama-cpp-python
```

If you have previously installed llama-cpp-python through pip and want to
upgrade your version or rebuild the package with different compiler options,
please add the following flags to ensure that the package is rebuilt correctly:

```bash
pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
```

Note: If you are using Apple Silicon (M1) Mac, make sure you have installed a
version of Python that supports arm64 architecture.

### Installation with Hardware Acceleration

`llama.cpp` supports multiple BLAS backends for faster processing. Use the
`FORCE_CMAKE=1` environment variable to force the use of `cmake` and install the
pip package for the desired BLAS backend.

To install with OpenBLAS, set the `LLAMA_BLAS and LLAMA_BLAS_VENDOR` environment
variables before installing:

```bash
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with cuBLAS, set the `LLAMA_CUBLAS=1` environment variable before
installing:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with CLBlast, set the `LLAMA_CLBLAST=1` environment variable before
installing:

```bash
CMAKE_ARGS="-DLLAMA_CLBLAST=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with Metal (MPS), set the `LLAMA_METAL=on` environment variable
before installing:

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with hipBLAS / ROCm support for AMD cards, set the `LLAMA_HIPBLAS=on`
environment variable before installing:

```bash
CMAKE_ARGS="-DLLAMA_HIPBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

Detailed MacOS Metal GPU install documentation is available at
[docs/install/macos.md](https://llama-cpp-python.readthedocs.io/en/latest/install/macos/).
