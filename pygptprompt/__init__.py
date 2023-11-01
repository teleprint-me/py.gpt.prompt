"""
pygptprompt/__init__.py

PyGPTPrompt: A Context Window Management System for Automating Prompting with Chat Models.
Copyright (C) 2023 Austin Berrio

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.

"There is a stubbornness about me that never can bear to be frightened at the will of others. My courage always rises at every attempt to intimidate me."
  - Jane Austen, Pride and Prejudice
"""
import os

__version__ = "0.0.39"
__name__ = "pygptprompt"
__agent__ = f"teleprint-me/{__name__}"
__source__ = f"https://github.com/{__agent__}"
__author__ = "Austin Berrio"
__email__ = "aberrio@teleprint.me"

try:
    CPU_COUNT: int = len(os.sched_getaffinity(0))
except AttributeError:
    CPU_COUNT: int = os.cpu_count() or 2
