Getting Started with VORTEX
========================

This guide will help you get up and running with VORTEX.

Installation
-----------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/vortex.git
      cd vortex

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt
      pip install -r requirements-dev.txt  # For development

Basic Usage
----------

Running the Game
~~~~~~~~~~~~~~

To start VORTEX, run:

.. code-block:: bash

   python run_game.py

First-Time Setup
~~~~~~~~~~~~~~

1. When you first start the game, you'll be prompted to create a player profile
2. Follow the guide's instructions to set up your character
3. Explore the world and interact with the AI guides

Development Setup
---------------

For developers, we recommend:

1. Install development dependencies:

   .. code-block:: bash

      pip install -r requirements-dev.txt

2. Set up pre-commit hooks:

   .. code-block:: bash

      pre-commit install

3. Run tests:

   .. code-block:: bash

      ./run_tests.sh

Configuration
------------

VORTEX uses environment variables for configuration. Copy the example environment file:

.. code-block:: bash

   cp .env.example .env

Then edit `.env` with your settings:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DEBUG`: Set to True for development
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

Next Steps
---------

- Read the :doc:`architecture/index` to understand the system design
- Check out the :doc:`guides/index` for detailed tutorials
- Review the :doc:`api/index` for API documentation
