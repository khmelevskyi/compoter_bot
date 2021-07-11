from os import getcwd, path


def enviroment_files():
    def check_file(filename):
        print()
        create_path = path.abspath(getcwd())
        create_path = path.join(create_path, filename)
        if not path.exists(create_path):
            print(f"{filename} not found")
            print(f"create_path: {create_path}")
            if filename == ".env":
                with open(create_path, "w") as env:
                    env.write("API_KEY=''\n\n")

                    env.write("host=''\n")
                    env.write("port=''\n\n")

                    env.write("user_email=''\n")
                    env.write("password_email=''\n\n")

                    env.write("from=''\n")
                    env.write("to=''\n\n")
            else:
                f = open(create_path, "x")
                f.close()
            print(f"{filename} need to be completed")
        else:
            print(f"{filename} exist")
        print()
    check_file(".env")