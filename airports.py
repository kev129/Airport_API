import json
from datetime import datetime

import requests
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

console = Console(record=True)

