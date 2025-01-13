# Food Order System
1. Order Backend System
2. Transaction System
3. E-mail System
4. Analytics System

## Setup
- Kafka Server:
    ```sh
    docker compose up -d

    ```
- Python:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

- Services:
    1. Order Backend System
        ```sh
        python3 order_backend.py
        ```
    2. Transaction System
        ```sh
        python3 transaction.py
        ```

    3. E-mail System
        ```sh
        python3 email_service.py
        ```

    4. Analytics System
        ```sh
        python3 analytics.py
        ```