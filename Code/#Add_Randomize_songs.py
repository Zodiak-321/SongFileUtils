import os
import random
import string

def main():
    print("正在为歌曲添加随机字母前缀（格式：字母_歌名）...\n")
    
    # 支持的音频格式
    extensions = {'.mp3', '.flac', '.wma', '.m4a', '.wav', '.aac', '.ogg'}
    
    count = 0
    for filename in os.listdir('.'):
        name, ext = os.path.splitext(filename)
        
        if ext.lower() in extensions:
            # 检查是否已经有字母前缀
            if not (len(name) > 2 and name[1] == '_' and name[0].isalpha()):
                # 生成随机字母
                random_letter = random.choice(string.ascii_uppercase)
                new_name = f"{random_letter}_{filename}"
                
                # 重命名文件
                os.rename(filename, new_name)
                print(f"重命名: {filename} -> {new_name}")
                count += 1
    
    print(f"\n完成！共处理 {count} 个文件。")

if __name__ == "__main__":
    main()
    input("按Enter键退出...")