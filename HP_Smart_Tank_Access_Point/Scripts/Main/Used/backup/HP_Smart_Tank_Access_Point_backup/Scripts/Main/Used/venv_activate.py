import os
import sys

# Check if the script is running inside a virtual environment
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    # Activate the virtual environment on Windows
    if sys.platform == "win32":
        activate_script = os.path.join(sys.prefix, 'Scripts', 'activate')
    else:
        # Activate the virtual environment on non-Windows
        activate_script = os.path.join(sys.prefix, 'bin', 'activate')

    # Run the activation script
    with open(activate_script, 'r') as f:
        exec(f.read(), {'__file__': activate_script})
