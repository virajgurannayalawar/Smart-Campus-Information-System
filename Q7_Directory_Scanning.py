import os 

class MissingFileOrFolderError(Exception): 
    """Raised when a required file or folder is missing in the directory.""" 
    pass 

def scan_directory(path): 
    try: 
        if not os.path.exists(path): 
            raise FileNotFoundError(f"Invalid directory path: {path}") 
        print(f"\nScanning directory: {path}\n") 
        
        for root, dirs, files in os.walk(path): 
            level = root.replace(path, "").count(os.sep) 
            indent = " " * 4 * level 
            print(f"{indent}{os.path.basename(root)}/") 
            sub_indent = " " * 4 * (level + 1) 
            for f in files: 
                print(f"{sub_indent}{f}") 
                
            if not files and not dirs: 
                raise MissingFileOrFolderError(f"Empty folder detected: {root}") 
                
    except FileNotFoundError as e: 
        print(f"Error: {e}") 
    except MissingFileOrFolderError as e: 
        print(f"Custom Error: {e}") 
    except Exception as e: 
        print(f"Unexpected Error: {e}") 

if __name__ == "__main__": 
    directory_path = input("Enter the directory path to scan: ") 
    scan_directory(directory_path) 
