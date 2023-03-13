import requests
import hashlib
import subprocess
import os


def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_hash = get_expec_hashval()

    # Download (but don't save) the VLC installer from the VLC website
    software_data = download_software()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_valid(software_data, expected_hash):
        # Save the downloaded VLC installer to disk
        software_path = save_software(software_data)

        # Silently run the VLC installer
        install_software(software_path)

        # Delete the VLC installer from disk
        delete_software(software_path)
    else:
        print('Hash values are different , Installation Failed ')


def get_expec_hashval():
    # Send GET message to download the file
    file_web_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_web_msg = requests.get(file_web_url)
    # Check
    # whether the download was successful
    if resp_web_msg.status_code == requests.codes.ok:
        # Extract text file content from
        # response message
        file_content = resp_web_msg.text
        hash_val = file_content.split(' ')
        return hash_val[0]


def download_software():
    # Send GET message to download the file
    file_web_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_web_msg = requests.get(file_web_url)
    # Check
    # whether the download was successful
    if resp_web_msg.status_code == requests.codes.ok:
        # Extract text file content from
        # response message
        web_content = resp_web_msg.content
        return web_content


def installer_valid(software_data, expected_hash):
    # Calculating hash value
    calc_hash = image_hash = hashlib.sha256(software_data).hexdigest()

    # Validating the Hash value
    if calc_hash == expected_hash:
        return True
    else:
        return False


def save_software(software_data):
    # Save the binary file to disk
    path = r'C:\vlc_installer.exe'
    with open(path, 'wb') as file:
        file.write(software_data)

    return path


def install_software(path):
    # Running the installer file
    subprocess.run([path, '/L=1033', '/S'])


def delete_software(path):
    # Deleting the installer file from disk
    os.remove(path)


# Driver Code
if __name__ == '__main__':
    main()
