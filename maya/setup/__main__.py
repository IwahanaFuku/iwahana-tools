import sys


def main(maya_version: str):
    from .envmanager import EnvManager
    EnvManager.write_env_script_path("2025")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <maya_version>")
        sys.exit(1)
    maya_version = sys.argv[1]
    main(maya_version)
