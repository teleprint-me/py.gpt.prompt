import pyopencl
import pytest


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
