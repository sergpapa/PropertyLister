import re
import subprocess

def get_package_version(package_name):
    result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith('Version:'):
            return line.split(' ')[1]
    return None

def convert_requirements(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            match = re.match(r'(\S+) @ file:///.+', line)
            if match:
                package = match.group(1)
                version = get_package_version(package)
                if version:
                    outfile.write(f'{package}=={version}\n')
                else:
                    print(f'Could not find version for package: {package}')
            else:
                outfile.write(line)

convert_requirements('requirements.txt', 'requirements_converted.txt')