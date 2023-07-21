from streamlit.web import cli
import sys


if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "main.py"]
    sys.exit(cli.main())
