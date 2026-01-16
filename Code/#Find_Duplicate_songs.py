import os
import shutil
from pathlib import Path
import unicodedata
import re
from collections import defaultdict
import sys

def normalize_text(text):
    """标准化文本：移除特殊字符、转换为小写、统一Unicode字符"""
    if not text:
        return ""
    
    # 转换为NFKC规范化形式（统一字符表示）
    text = unicodedata.normalize('NFKC', text)
    
    # 转换为小写
    text = text.lower()
    
    # 移除常见的干扰字符和符号
    # 保留字母、数字、空格、连字符、下划线、点
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    
    # 替换多个空格为单个空格
    text = re.sub(r'\s+', ' ', text)
    
    # 移除开头结尾的空格
    text = text.strip()
    
    return text

def extract_song_info(filename):
    """
    从文件名中提取歌曲信息
    格式通常为：歌名 - 歌手.扩展名 或 歌名 - 歌手_后缀.扩展名
    """
    # 移除扩展名
    name_without_ext = os.path.splitext(filename)[0]
    
    # 分割歌手和可能的品质后缀
    parts = name_without_ext.split(' - ', 1)
    
    if len(parts) == 2:
        song_name = parts[0].strip()
        artist_and_suffix = parts[1].strip()
        
        # 分离歌手和品质后缀
        artist = artist_and_suffix
        quality = ""
        
        # 常见的品质/版本后缀
        quality_suffixes = [
            '_eg', '_hq', '_320k', '_flac', '_mp3', '_aac', '_lossless',
            '_explicit', '_clean', '_remastered', '_remix', '_live',
            '_acoustic', '_instrumental', '_demo', '_version', '_edit'
        ]
        
        for suffix in quality_suffixes:
            if artist_and_suffix.lower().endswith(suffix):
                artist = artist_and_suffix[:-len(suffix)]
                quality = suffix
                break
        
        # 如果没有匹配到已知后缀，尝试按最后一个下划线分割
        if not quality and '_' in artist_and_suffix:
            last_underscore = artist_and_suffix.rfind('_')
            if last_underscore > 0:
                possible_artist = artist_and_suffix[:last_underscore]
                possible_suffix = artist_and_suffix[last_underscore:]
                
                # 如果后缀看起来像是品质标记
                if (len(possible_suffix) <= 8 and 
                    any(c.isdigit() for c in possible_suffix)):
                    artist = possible_artist
                    quality = possible_suffix
        
        return {
            'filename': filename,
            'full_path': os.path.abspath(filename),
            'song_name': song_name,
            'artist': artist.strip(),
            'quality_suffix': quality,
            'normalized_song': normalize_text(song_name),
            'normalized_artist': normalize_text(artist.strip()),
            'extension': os.path.splitext(filename)[1].lower(),
            'size': os.path.getsize(filename) if os.path.exists(filename) else 0
        }
    else:
        # 不符合标准格式的文件
        return {
            'filename': filename,
            'full_path': os.path.abspath(filename),
            'song_name': name_without_ext,
            'artist': '',
            'quality_suffix': '',
            'normalized_song': normalize_text(name_without_ext),
            'normalized_artist': '',
            'extension': os.path.splitext(filename)[1].lower(),
            'size': os.path.getsize(filename) if os.path.exists(filename) else 0
        }

def find_identical_songs(directory="."):
    """
    查找歌手和歌名完全相同的歌曲
    返回字典：键为(标准化歌名, 标准化歌手)，值为歌曲列表
    """
    print("正在扫描歌曲文件...")
    
    # 支持的音频格式
    audio_extensions = {'.mp3', '.flac', '.wma', '.m4a', '.wav', '.aac', '.ogg'}
    
    # 收集所有歌曲文件信息
    songs_by_key = defaultdict(list)
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            if ext in audio_extensions:
                song_info = extract_song_info(filename)
                
                # 使用标准化歌名和歌手作为键
                key = (song_info['normalized_song'], song_info['normalized_artist'])
                songs_by_key[key].append(song_info)
    
    print(f"共找到 {sum(len(songs) for songs in songs_by_key.values())} 个音频文件")
    
    # 只保留有重复的组（至少2首相同的歌曲）
    duplicates = {key: songs for key, songs in songs_by_key.items() 
                  if len(songs) > 1 and key[0]}  # key[0]是歌名，不能为空
    
    return duplicates

def analyze_duplicates(duplicates):
    """
    分析重复歌曲，确定应该保留哪个文件
    策略：
    1. 优先保留有品质标记的文件（如_EG）
    2. 其次保留文件大小较大的文件（通常音质更好）
    3. 保留FLAC格式（如果存在）
    4. 保留MP3格式（如果没有其他高品质格式）
    """
    decisions = []
    
    for (song_name, artist_name), songs in duplicates.items():
        # 按优先级排序：
        # 1. 有品质标记的优先
        # 2. 文件大小大的优先
        # 3. 特定格式优先（FLAC > WAV > M4A > MP3 > 其他）
        format_priority = {
            '.flac': 5,
            '.wav': 4,
            '.m4a': 3,
            '.mp3': 2
        }
        
        def song_priority(song):
            # 有品质标记的得分更高
            quality_score = 10 if song['quality_suffix'] else 0
            
            # 格式优先级
            format_score = format_priority.get(song['extension'], 1)
            
            # 文件大小（MB）
            size_score = song['size'] / (1024 * 1024)  # 转换为MB
            
            # 综合得分：品质标记权重最高，然后是格式，最后是大小
            return (quality_score * 10000) + (format_score * 1000) + size_score
        
        # 按优先级排序，得分最高的第一个
        sorted_songs = sorted(songs, key=song_priority, reverse=True)
        
        # 要保留的歌曲（优先级最高的）
        keep_song = sorted_songs[0]
        
        # 要删除的歌曲（其他所有）
        delete_songs = sorted_songs[1:]
        
        decisions.append({
            'song_key': (song_name, artist_name),
            'keep': keep_song,
            'delete': delete_songs,
            'total_count': len(songs)
        })
    
    return decisions

def create_backup_folder():
    """创建备份文件夹"""
    backup_base = "Deleted_Songs_Backup"
    backup_num = 1
    backup_folder = f"{backup_base}_{backup_num}"
    
    # 查找可用的备份文件夹名
    while os.path.exists(backup_folder):
        backup_num += 1
        backup_folder = f"{backup_base}_{backup_num}"
    
    os.makedirs(backup_folder, exist_ok=True)
    return backup_folder

def safe_delete_songs(decisions, backup_mode=True, dry_run=False):
    """
    安全删除重复歌曲
    backup_mode: True=移动到备份文件夹，False=直接删除
    dry_run: True=模拟运行（不实际删除），False=实际执行
    """
    if not decisions:
        print("没有需要删除的重复歌曲。")
        return {"deleted": 0, "backed_up": 0, "skipped": 0, "errors": 0}
    
    backup_folder = None
    if backup_mode and not dry_run:
        backup_folder = create_backup_folder()
        print(f"创建备份文件夹: {backup_folder}")
    
    stats = {"deleted": 0, "backed_up": 0, "skipped": 0, "errors": 0}
    
    for decision in decisions:
        song_name, artist_name = decision['song_key']
        keep_song = decision['keep']
        delete_songs = decision['delete']
        
        print(f"\n处理歌曲: {song_name} - {artist_name}")
        print(f"  保留: {keep_song['filename']} ({keep_song['size']/1024/1024:.2f} MB)")
        
        for song in delete_songs:
            try:
                if dry_run:
                    print(f"  模拟删除: {song['filename']}")
                    stats["deleted"] += 1
                elif backup_mode:
                    # 移动到备份文件夹
                    backup_path = os.path.join(backup_folder, song['filename'])
                    shutil.move(song['full_path'], backup_path)
                    print(f"  移动到备份: {song['filename']}")
                    stats["backed_up"] += 1
                else:
                    # 直接删除
                    os.remove(song['full_path'])
                    print(f"  直接删除: {song['filename']}")
                    stats["deleted"] += 1
            except Exception as e:
                print(f"  错误: 无法删除 {song['filename']} - {str(e)}")
                stats["errors"] += 1
    
    return stats

def display_summary(decisions, stats):
    """显示处理摘要"""
    if not decisions:
        print("\n🎉 没有找到需要处理的重复歌曲。")
        return
    
    total_duplicates = sum(decision['total_count'] for decision in decisions)
    total_to_delete = sum(len(decision['delete']) for decision in decisions)
    total_to_keep = len(decisions)  # 每组保留一个
    
    print(f"\n{'='*80}")
    print("处理摘要:")
    print(f"{'='*80}")
    print(f"找到的重复歌曲组数: {len(decisions)}")
    print(f"涉及歌曲总数: {total_duplicates}")
    print(f"将要保留的歌曲数: {total_to_keep}")
    print(f"将要删除/备份的歌曲数: {total_to_delete}")
    
    if stats:
        print(f"\n处理结果:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    # 显示每组的具体决定
    print(f"\n详细处理决定:")
    print(f"{'-'*80}")
    
    for i, decision in enumerate(decisions, 1):
        song_name, artist_name = decision['song_key']
        keep_song = decision['keep']
        delete_songs = decision['delete']
        
        print(f"\n{i}. {song_name} - {artist_name}")
        print(f"   保留: {keep_song['filename']}")
        
        if delete_songs:
            print(f"   删除:")
            for song in delete_songs:
                print(f"     - {song['filename']}")
        else:
            print(f"   删除: 无")

def main():
    """主函数"""
    print("🎵 智能重复歌曲删除工具")
    print("=" * 80)
    print("功能：自动识别并删除歌手和歌名完全相同的重复歌曲")
    print("注意：只删除完全相同的歌曲（标准化后歌名和歌手相同）")
    print("-" * 80)
    
    # 选择目录
    directory = input("请输入要扫描的目录（直接回车使用当前目录）: ").strip()
    if not directory:
        directory = "."
    
    if not os.path.isdir(directory):
        print(f"❌ 错误：目录 '{directory}' 不存在！")
        return
    
    print(f"\n正在扫描目录: {os.path.abspath(directory)}")
    
    # 查找重复歌曲
    duplicates = find_identical_songs(directory)
    
    if not duplicates:
        print("\n🎉 没有找到歌手和歌名完全相同的重复歌曲。")
        return
    
    print(f"\n🔍 找到 {len(duplicates)} 组重复歌曲:")
    print("-" * 80)
    
    for i, ((song_name, artist_name), songs) in enumerate(duplicates.items(), 1):
        print(f"\n第 {i} 组: {song_name} - {artist_name}")
        for j, song in enumerate(songs, 1):
            quality_mark = f" [{song['quality_suffix']}]" if song['quality_suffix'] else ""
            size_mb = song['size'] / (1024 * 1024)
            print(f"  {j:2d}. {song['filename']} ({size_mb:.2f} MB{quality_mark})")
    
    # 分析重复并决定保留哪个
    decisions = analyze_duplicates(duplicates)
    
    # 显示将要执行的操作
    print(f"\n{'='*80}")
    print("将要执行的操作:")
    print("=" * 80)
    
    total_to_delete = sum(len(decision['delete']) for decision in decisions)
    total_size_mb = sum(song['size'] for decision in decisions 
                       for song in decision['delete']) / (1024 * 1024)
    
    print(f"总删除/备份文件数: {total_to_delete}")
    print(f"总大小: {total_size_mb:.2f} MB")
    
    # 选择操作模式
    print(f"\n请选择操作模式:")
    print("1. 模拟运行（只显示将要执行的操作，不实际删除）")
    print("2. 安全模式（将重复文件移动到备份文件夹）")
    print("3. 直接删除（谨慎！无法恢复）")
    print("4. 取消操作")
    
    try:
        choice = int(input("\n请选择 (1-4): "))
    except ValueError:
        print("❌ 请输入有效数字！")
        return
    
    if choice == 4:
        print("操作已取消。")
        return
    
    # 执行操作
    stats = None
    if choice == 1:
        print("\n开始模拟运行...")
        stats = safe_delete_songs(decisions, backup_mode=False, dry_run=True)
    elif choice == 2:
        print("\n开始安全模式（移动到备份文件夹）...")
        stats = safe_delete_songs(decisions, backup_mode=True, dry_run=False)
    elif choice == 3:
        confirm = input("\n⚠️  警告：此操作将直接删除文件，无法恢复！\n是否确认？(输入'YES'继续): ")
        if confirm == 'YES':
            print("\n开始直接删除...")
            stats = safe_delete_songs(decisions, backup_mode=False, dry_run=False)
        else:
            print("操作已取消。")
            return
    else:
        print("❌ 选择无效！")
        return
    
    # 显示摘要
    display_summary(decisions, stats)
    
    # 保存日志
    save_log = input("\n是否保存处理日志？(y/n): ").lower()
    if save_log in ['y', 'yes']:
        save_operation_log(decisions, stats, directory)
    
    print("\n操作完成！")

def save_operation_log(decisions, stats, directory):
    """保存操作日志"""
    import json
    from datetime import datetime
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'directory': os.path.abspath(directory),
        'stats': stats,
        'decisions': []
    }
    
    for decision in decisions:
        song_name, artist_name = decision['song_key']
        
        decision_entry = {
            'song_name': song_name,
            'artist_name': artist_name,
            'keep': {
                'filename': decision['keep']['filename'],
                'size': decision['keep']['size'],
                'quality_suffix': decision['keep']['quality_suffix']
            },
            'delete': [
                {
                    'filename': song['filename'],
                    'size': song['size'],
                    'quality_suffix': song['quality_suffix']
                }
                for song in decision['delete']
            ]
        }
        log_data['decisions'].append(decision_entry)
    
    # 生成日志文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"song_cleanup_log_{timestamp}.json"
    
    with open(log_filename, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"日志已保存到: {log_filename}")
    
    # 同时保存为文本格式
    txt_log_filename = f"song_cleanup_log_{timestamp}.txt"
    with open(txt_log_filename, 'w', encoding='utf-8') as f:
        f.write("重复歌曲清理日志\n")
        f.write("=" * 80 + "\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"目录: {os.path.abspath(directory)}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("统计信息:\n")
        for key, value in stats.items():
            f.write(f"  {key}: {value}\n")
        
        f.write("\n\n处理详情:\n")
        f.write("=" * 80 + "\n")
        
        for i, decision in enumerate(decisions, 1):
            song_name, artist_name = decision['song_key']
            keep_song = decision['keep']
            
            f.write(f"\n{i}. {song_name} - {artist_name}\n")
            f.write(f"   保留: {keep_song['filename']}\n")
            
            if decision['delete']:
                f.write(f"   删除:\n")
                for song in decision['delete']:
                    f.write(f"     - {song['filename']}\n")
    
    print(f"文本日志已保存到: {txt_log_filename}")

if __name__ == "__main__":
    main()