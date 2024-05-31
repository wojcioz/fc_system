import os

class Pipe:
    def __init__(self, pipe_name):
        self.pipe_name = pipe_name

    def create_pipe(self):
        try:
            os.mkfifo(self.pipe_name)
            print(f"Pipe '{self.pipe_name}' created successfully.")
        except OSError as e:
            print(f"Failed to create pipe '{self.pipe_name}': {e}")

    def read_from_pipe(self):
        try:
            with open(self.pipe_name, 'r') as pipe:
                data = pipe.read()
                print(f"Read from pipe '{self.pipe_name}': {data}")
        except FileNotFoundError:
            print(f"Pipe '{self.pipe_name}' does not exist.")
        except Exception as e:
            print(f"Failed to read from pipe '{self.pipe_name}': {e}")

    def write_to_pipe(self, data):
        try:
            with open(self.pipe_name, 'w') as pipe:
                pipe.write(data)
                print(f"Data written to pipe '{self.pipe_name}': {data}")
        except FileNotFoundError:
            print(f"Pipe '{self.pipe_name}' does not exist.")
        except Exception as e:
            print(f"Failed to write to pipe '{self.pipe_name}': {e}")