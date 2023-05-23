import argparse

from pygptprompt.chat.context import ChatContext


def main(config_path):
    chat = ChatContext(config_path=config_path)
    chat.loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to the configuration file")
    args = parser.parse_args()
    main(config_path=args.config)
