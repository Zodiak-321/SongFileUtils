import os
import sys

def restore_original_names():
    """
    恢复歌曲的原始文件名（移除"字母_"前缀）
    格式：将"X_歌曲名.mp3"恢复为"歌曲名.mp3"
    """
    print("正在恢复歌曲的原始文件名...\n")
    
    # 支持的音频格式
    audio_extensions = {'.mp3', '.flac', '.wma', '.m4a', '.wav', '.aac', '.ogg'}
    restored_count = 0
    skipped_count = 0
    
    # 获取当前目录下的所有文件
    for filename in os.listdir('.'):
        # 检查是否是文件（不是文件夹）
        if not os.path.isfile(filename):
            continue
            
        # 获取文件扩展名
        name_part, ext = os.path.splitext(filename)
        
        # 检查是否是音频文件
        if ext.lower() in audio_extensions:
            # 检查文件名是否符合"字母_歌曲名"的格式
            # 条件：文件名长度至少3个字符，第二个字符是下划线，第一个字符是字母
            if (len(name_part) >= 2 and 
                name_part[1] == '_' and 
                name_part[0].isalpha()):
                
                # 提取原始文件名（移除前两个字符：字母+下划线）
                original_name = name_part[2:] + ext
                
                # 检查目标文件名是否已存在（避免冲突）
                if not os.path.exists(original_name):
                    # 重命名文件
                    os.rename(filename, original_name)
                    print(f"✓ 恢复: {filename} -> {original_name}")
                    restored_count += 1
                else:
                    print(f"⚠ 跳过（文件已存在）: {filename} -> {original_name}")
                    skipped_count += 1
            else:
                print(f"  跳过（无前缀）: {filename}")
    
    print(f"\n{'='*50}")
    print(f"恢复完成！")
    print(f"已恢复: {restored_count} 个文件")
    if skipped_count > 0:
        print(f"跳  过: {skipped_count} 个文件（文件名冲突）")
    print(f"{'='*50}")
    
    return restored_count

def main():
    """主函数"""
    # 显示提示信息
    print("歌曲文件名恢复工具")
    print("功能：移除音频文件的'字母_'前缀（例如：A_歌曲名.mp3 -> 歌曲名.mp3）")
    print("-" * 50)
    
    # 询问用户是否继续
    response = input("是否继续恢复原始文件名？(y/n): ").lower()
    if response != 'y' and response != 'yes':
        print("操作已取消。")
        return
    
    # 执行恢复操作
    try:
        restored = restore_original_names()
        
        if restored > 0:
            print("\n提示：")
            print("1. 如果部分文件未能恢复，可能是因为目标文件名已存在")
            print("2. 你可以手动重命名这些文件")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("请检查是否有文件正在被其他程序使用。")
    
    # 等待用户按Enter键退出
    input("\n按Enter键退出...")

if __name__ == "__main__":
    main()