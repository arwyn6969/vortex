"""
Alias 'src' package for code under vortex/src and vortex-next/src.
"""

import os

# Directory containing this alias package
package_dir = os.path.dirname(__file__)

# Include main project code under vortex/src
vortex_src = os.path.normpath(os.path.join(package_dir, '..', 'vortex', 'src'))
if os.path.isdir(vortex_src):
    __path__.append(vortex_src)

# Include next project code under vortex-next/src
vortex_next_src = os.path.normpath(os.path.join(package_dir, '..', 'vortex-next', 'src'))
if os.path.isdir(vortex_next_src):
    __path__.append(vortex_next_src) 