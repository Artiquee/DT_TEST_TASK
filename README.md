git clone git@github.com:Artiquee/DT_TEST_TASK.git
cd DT_TEST_TASK
python3 -m venv .venv
- rename .example.env and config .env file
pip install -r requirements.txt
alembic upgrade head
python3 main.py
