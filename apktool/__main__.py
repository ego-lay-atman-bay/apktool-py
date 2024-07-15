from .apktool import run_command

def main():
    import sys
    args = sys.argv[1::]

    run_command(*args, check = False)

if __name__ == "__main__":
    main()
