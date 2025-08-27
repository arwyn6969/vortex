import sys
import os

# Automatically add code directories to sys.path for tests
# Add vortex/src to sys.path so tests can import modules under 'src'
root_dir = os.path.dirname(__file__)
vortex_src = os.path.join(root_dir, 'vortex', 'src')
if os.path.isdir(vortex_src):
    sys.path.insert(0, vortex_src)

# Add vortex-next/src to sys.path so tests can import modules under 'src'
vortex_next_src = os.path.join(root_dir, 'vortex-next', 'src')
if os.path.isdir(vortex_next_src):
    sys.path.insert(0, vortex_next_src) 