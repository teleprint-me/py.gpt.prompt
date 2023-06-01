# pygptprompt/main.py
import argparse

from pygptprompt.session.context import SessionContext


def main(config_path):
    chat = SessionContext(config_path=config_path)
    chat.main_loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to the configuration file")
    args = parser.parse_args()
    main(config_path=args.config)
