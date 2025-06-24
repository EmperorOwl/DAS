# Bot

This is the Bot component of the Discord Algebra System (DAS). 
It is a Discord bot.

## Running the Bot

## Dependencies
- Python 3.8 or higher
- Python environment with required packages (see requirements.txt)

### Local Development

1. Make sure you're in the `bot` directory
    ```
    cd bot
    ```

2. Create virtual environment
    ```
    python -m venv .venv
    ```

3. Activate virtual environment
    ```
    .\.venv\Scripts\activate
    ```

4. Install dependencies
    ```
    pip install -r requirements.txt
    ```

5. Start the bot
    ```
    python -m src.main
    ```

6. Format code
    ```
    pip install autopep8
    autopep8 . --in-place --recursive --exclude .venv
    ```
