import os

ENV_FILE = '.env'

def toggle_debug():
    with open(ENV_FILE, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith('DEBUG='):
            current_value = line.strip().split('=')[1].lower()
            new_value = 'False' if current_value == 'true' else 'True'
            new_lines.append(f'DEBUG={new_value}\n')
            print(f"DEBUG switched to {new_value}")
        else:
            new_lines.append(line)

    with open(ENV_FILE, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    toggle_debug()

# to run in terminal
# python toggle_debug.py