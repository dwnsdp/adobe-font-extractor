import os
import glob
import re
from fontTools.ttLib import TTFont

def sanitize_filename(name):
    # Remove invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '', name).strip(' .')

def get_font_name(font_path):
    try:
        # Ignore warning logs from fontTools
        import logging
        logging.getLogger("fontTools.ttLib").setLevel(logging.ERROR)
        
        font = TTFont(font_path)
        name_record = font['name']
        
        font_name = None
        # Preferred order: 4 (Full name), 6 (PostScript name), 1 (Family name)
        for nameID in [4, 6, 1]:
            for record in name_record.names:
                if record.nameID == nameID:
                    font_name = record.toUnicode()
                    # Prefer english names if multiple records exist for the same nameID
                    if record.platEncID == 1 and record.langID == 0: 
                        break
            if font_name:
                break
                
        return font_name
    except Exception as e:
        print(f"Error reading {os.path.basename(font_path)}: {e}")
        return None

def main():
    directory = r"d:\Documents\Fonts"
    
    print("Step 1: Adding .otf extension...")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Only process files without extension
        if os.path.isdir(file_path) or '.' in filename:
            continue
            
        otf_path = file_path + ".otf"
        try:
            os.rename(file_path, otf_path)
            print(f"  {filename} -> {filename}.otf")
        except Exception as e:
            print(f"  Failed: {filename}: {e}")

    print("\nStep 2: Renaming files to font names...")
    for otf_file in glob.glob(os.path.join(directory, "*.otf")):
        font_name = get_font_name(otf_file)
        if font_name:
            clean_name = sanitize_filename(font_name)
            if not clean_name:
                print(f"  Could not sanitize name '{font_name}' for {os.path.basename(otf_file)}")
                continue
                
            new_path = os.path.join(directory, clean_name + ".otf")
            
            # Avoid renaming if the name is already correct
            if os.path.abspath(new_path).lower() == os.path.abspath(otf_file).lower():
                continue
                
            # Handle name collisions
            counter = 1
            original_clean_name = clean_name
            while os.path.exists(new_path) and os.path.abspath(new_path).lower() != os.path.abspath(otf_file).lower():
                clean_name = f"{original_clean_name} ({counter})"
                new_path = os.path.join(directory, clean_name + ".otf")
                counter += 1
                
            try:
                os.rename(otf_file, new_path)
                print(f"  {os.path.basename(otf_file)} -> {clean_name}.otf")
            except Exception as e:
                print(f"  Failed to rename {os.path.basename(otf_file)}: {e}")
        else:
            print(f"  Could not extract font name from {os.path.basename(otf_file)}")

if __name__ == "__main__":
    main()
