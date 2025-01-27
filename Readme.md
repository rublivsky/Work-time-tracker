# Time Tracker Bot

## Description

Time Tracker Bot is a Telegram bot designed to help users track their work sessions. It allows users to start and end work sessions, and provides analytics on their work time.

## Features

- User authentication via Telegram
- Start and end work sessions
- View analytics of work sessions

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    ```bash
    cp .env.example .env
    # Edit .env file with your configuration
    ```

## Usage

1. **Run the bot**:
    ```bash
    python bot.py
    ```

2. **Interact with the bot on Telegram**:
    - `/start` to authenticate and start using the bot
    - `/start_session` or "Начало сессии" to start a work session
    - `/end_session` or "Конец сессии" to end a work session
    - `/analysis` or "Аналитика" to view work session analytics

## Database Models

### UsersORM
- `id`: Primary key
- [telegram_id](http://_vscodecontentref_/0): Telegram ID of the user
- `username`: Username of the user
- `contact`: Contact information of the user

### WorkTimesORM
- `id`: Primary key
- [telegram_id](http://_vscodecontentref_/1): Foreign key referencing `UsersORM.telegram_id`
- [session_date](http://_vscodecontentref_/2): Date of the work session
- [start_time](http://_vscodecontentref_/3): Start time of the work session
- [end_time](http://_vscodecontentref_/4): End time of the work session
- `bonuses`: Bonuses earned during the session
- [status](http://_vscodecontentref_/5): Status of the session (active or inactive)

## Functions

### `set_user(session, telegram_id, username)`
Sets a new user in the database or retrieves an existing user.

### `update_user(session, telegram_id, contact)`
Updates the contact information of an existing user.

### `get_user(session, telegram_id)`
Retrieves a user from the database based on their Telegram ID.

### `set_start_time(session, telegram_id, date, time)`
Sets the start time for a work session.

### [set_end_time(session, telegram_id, date, time)](http://_vscodecontentref_/6)
Sets the end time for a work session.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes ([git commit -m 'Add some feature'](http://_vscodecontentref_/7)).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.