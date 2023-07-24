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

### Installation with OpenBLAS / cuBLAS / CLBlast / Metal

llama.cpp supports multiple BLAS backends for faster processing. Use the
`FORCE_CMAKE=1` environment variable to force the use of `cmake` and install the
pip package for the desired BLAS backend.

To install with OpenBLAS:

```bash
CMAKE_ARGS="-DLLAMA_OPENBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with cuBLAS:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

NOTE: Use cuBLAS if you have AMD as `llama.cpp` takes care of this for you under
the hood. It compiles the necessary HIP code using `nvcc`. Reference
[ggerganov/llama.cpp pull request #1087](https://github.com/ggerganov/llama.cpp/pull/1087)
for more information.

To install with CLBlast:

```bash
CMAKE_ARGS="-DLLAMA_CLBLAST=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

To install with Metal (MPS):

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python
```

Detailed MacOS Metal GPU install documentation is available at
[docs/install/macos.md](https://llama-cpp-python.readthedocs.io/en/latest/install/macos/).
