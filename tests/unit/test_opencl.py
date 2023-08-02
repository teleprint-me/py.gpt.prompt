"""
tests/unit/test_opencl.py
"""
import pyopencl
import pytest


# NOTE:
# PyOpenCL and Installable Client Driver (ICD) must be compiled to specific hardware.
# Using a virtual environment (e.g. Poetry) masks the system install because it's
# job is to isolate packages from the system libraries. This creates a conflict
# that will eventually need to be addressed. This test is temporarily disabled
# as a result of this issue.
@pytest.mark.skip
def test_opencl():
    # Get all available platforms
    platforms = pyopencl.get_platforms()
    assert platforms, "No OpenCL platforms available"

    for platform in platforms:
        # Get all available devices for each platform
        devices = platform.get_devices()
        assert devices, f"No OpenCL devices available for platform {platform.name}"

        for device in devices:
            # Check if device name is not empty
            assert device.name, "Device name is empty"


if __name__ == "__main__":
    pytest.main([__file__])
