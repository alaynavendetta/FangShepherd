#!/usr/bin/python3

'''
FangShepherd by Alayna Ferdarko
Written on 13 March, 2025
'''

import re
import pyfiglet

FangShepherdArt = pyfiglet.figlet_format("Fang Shepherd")

def defang(text):
    text = re.sub(r"http", "hxxp", text, flags=re.IGNORECASE)
    text = text.replace(".", "[.]")
    text = text.replace("@", "[@]")
    return text

def refang(text):
    text = re.sub(r"hxxp", "http", text, flags=re.IGNORECASE)
    text = text.replace("[.]", ".")
    text = text.replace("[@]", "@")
    return text

# Expanded IOC extraction with hash support
def extract_iocs(text_blob):
    urls = re.findall(r'https?://[^\s"\'<>]+', text_blob)
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text_blob)
    emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text_blob)
    md5_hashes = re.findall(r'\b[a-fA-F0-9]{32}\b', text_blob)
    sha1_hashes = re.findall(r'\b[a-fA-F0-9]{40}\b', text_blob)
    sha256_hashes = re.findall(r'\b[a-fA-F0-9]{64}\b', text_blob)

    iocs = urls + ips + emails + md5_hashes + sha1_hashes + sha256_hashes
    return iocs

def read_from_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def save_to_file(results, output_file):
    with open(output_file, "w") as f:
        for item in results:
            f.write(item + "\n")
    print(f"\nResults saved to {output_file}")

def main():
    print(FangShepherdArt)
    print("FangShepherd Version 1.0 by Alayna Ferdarko")
    print ("")
    action = input("Choose action:\n1. Extract IOCs + Defang\n2. Extract IOCs + Refang\n3. Just Defang\n4. Just Refang\n> ").strip()

    if action not in ("1", "2", "3", "4"):
        print("Invalid choice. Exiting.")
        return

    source_choice = input("Input method:\n1. Paste text\n2. Read from file\n> ")

    if source_choice.strip() == "1":
        print("Paste your input text. Type 'DONE' when finished:")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "DONE":
                break
            lines.append(line)
        input_text = "\n".join(lines)
    elif source_choice.strip() == "2":
        file_path = input("Enter file path: ").strip().strip('"')
        try:
            input_text = read_from_file(file_path)
        except FileNotFoundError:
            print("File not found. Exiting.")
            return
    else:
        print("Invalid input method. Exiting.")
        return

    if action in ("1", "2"):
        extracted = extract_iocs(input_text)
        if not extracted:
            print("No IOCs found.")
            return
        print(f"\nExtracted {len(extracted)} IOCs:")
        for item in extracted:
            print(item)
        processed = [defang(ioc) if action == "1" else refang(ioc) for ioc in extracted]
    else:
        # Just defang/refang everything line by line
        lines = input_text.splitlines()
        processed = [defang(line.strip()) if action == "3" else refang(line.strip()) for line in lines if line.strip()]

    print("\n=== Processed Results ===")
    for res in processed:
        print(res)

    save_option = input("\nSave results to a file? (y/n): ").strip().lower()
    if save_option == "y":
        output_file = input("Enter output file name (e.g., output.txt): ").strip()
        save_to_file(processed, output_file)

if __name__ == "__main__":
    main()
