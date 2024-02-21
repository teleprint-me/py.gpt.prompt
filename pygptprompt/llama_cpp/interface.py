"""
pygptprompt/llama_cpp/interface.py
"""
from cffi import FFI

# Create an FFI object
ffi = FFI()

# Load the shared library
llama_lib = ffi.dlopen("pygptprompt/llama_cpp/libs/libllama.so")

# Define the C structures and types
ffi.cdef(
    """
    typedef int32_t llama_token;

    typedef struct {
        llama_token id; // token id
        float logit;    // log-odds of the token
        float p;        // probability of the token
    } llama_token_data;
    """
)

# Now you can use llama_lib to access functions from the shared library
