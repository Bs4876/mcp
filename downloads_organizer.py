#!/usr/bin/env python3
"""Downloads Organizer MCP"""

import asyncio
import logging
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import zipfile
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('organizer.log', mode='a')])

mcp = FastMCP("downloads-organizer")

FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'Code': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.json', '.xml', '.sql'],
    'Programs': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.apk'],
    'Other': []
}

def get_downloads_path(path: str = None) -> Path:
    return Path(path) if path else Path.home() / "Downloads"

def get_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Other'

def get_file_hash(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def organize_by_type_sync(downloads_path: str = None, dry_run: bool = False) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    moved_files = defaultdict(list)
    errors = []
    
    for item in path.rglob('*'):
        if item.is_file():
            category = get_category(item)
            target_dir = path / category
            
            if item.parent == target_dir:
                continue
            
            if not dry_run:
                target_dir.mkdir(exist_ok=True)
                try:
                    target_path = target_dir / item.name
                    counter = 1
                    while target_path.exists():
                        target_path = target_dir / f"{item.stem}_{counter}{item.suffix}"
                        counter += 1
                    shutil.move(str(item), str(target_path))
                    moved_files[category].append(item.name)
                except Exception as e:
                    errors.append(f"{item.name}: {str(e)}")
            else:
                moved_files[category].append(item.name)
    
    return {"ok": True, "data": {"moved_files": dict(moved_files), "total_files": sum(len(files) for files in moved_files.values()), "categories": len(moved_files), "errors": errors, "dry_run": dry_run}}

def find_duplicates_sync(downloads_path: str = None, delete_duplicates: bool = False) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    file_hashes = defaultdict(list)
    duplicates = []
    space_saved = 0
    
    for item in path.rglob('*'):
        if item.is_file():
            try:
                file_hash = get_file_hash(item)
                file_hashes[file_hash].append(item)
            except Exception:
                continue
    
    for file_hash, files in file_hashes.items():
        if len(files) > 1:
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            keep_file = files[0]
            duplicate_files = files[1:]
            
            for dup in duplicate_files:
                size = dup.stat().st_size
                duplicates.append({"file": str(dup.relative_to(path)), "size": size, "original": str(keep_file.relative_to(path))})
                space_saved += size
                
                if delete_duplicates:
                    try:
                        dup.unlink()
                    except Exception:
                        pass
    
    return {"ok": True, "data": {"duplicates": duplicates, "count": len(duplicates), "space_saved_mb": round(space_saved / (1024 * 1024), 2), "deleted": delete_duplicates}}

def clean_old_files_sync(downloads_path: str = None, days_old: int = 90, delete: bool = False) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    old_files = []
    total_size = 0
    
    for item in path.rglob('*'):
        if item.is_file():
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff_date:
                size = item.stat().st_size
                old_files.append({"file": str(item.relative_to(path)), "age_days": (datetime.now() - mtime).days, "size": size})
                total_size += size
                
                if delete:
                    try:
                        item.unlink()
                    except Exception:
                        pass
    
    return {"ok": True, "data": {"old_files": old_files, "count": len(old_files), "total_size_mb": round(total_size / (1024 * 1024), 2), "deleted": delete, "days_threshold": days_old}}

def get_stats_sync(downloads_path: str = None) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    stats = {"total_files": 0, "total_size": 0, "by_category": defaultdict(lambda: {"count": 0, "size": 0}), "largest_files": []}
    all_files = []
    
    for item in path.rglob('*'):
        if item.is_file():
            size = item.stat().st_size
            category = get_category(item)
            stats["total_files"] += 1
            stats["total_size"] += size
            stats["by_category"][category]["count"] += 1
            stats["by_category"][category]["size"] += size
            all_files.append((item, size))
    
    all_files.sort(key=lambda x: x[1], reverse=True)
    stats["largest_files"] = [{"file": str(f.relative_to(path)), "size_mb": round(s / (1024 * 1024), 2)} for f, s in all_files[:10]]
    
    return {"ok": True, "data": {"total_files": stats["total_files"], "total_size_mb": round(stats["total_size"] / (1024 * 1024), 2), "by_category": {cat: {"count": info["count"], "size_mb": round(info["size"] / (1024 * 1024), 2)} for cat, info in stats["by_category"].items()}, "largest_files": stats["largest_files"]}}

def organize_by_date_sync(downloads_path: str = None, dry_run: bool = False) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    moved_files = defaultdict(list)
    errors = []
    
    for item in path.rglob('*'):
        if item.is_file():
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            date_folder = mtime.strftime("%Y/%m-%B")
            target_dir = path / date_folder
            
            if item.parent == target_dir:
                continue
            
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                try:
                    target_path = target_dir / item.name
                    counter = 1
                    while target_path.exists():
                        target_path = target_dir / f"{item.stem}_{counter}{item.suffix}"
                        counter += 1
                    shutil.move(str(item), str(target_path))
                    moved_files[date_folder].append(item.name)
                except Exception as e:
                    errors.append(f"{item.name}: {str(e)}")
            else:
                moved_files[date_folder].append(item.name)
    
    return {"ok": True, "data": {"moved_files": dict(moved_files), "total_files": sum(len(files) for files in moved_files.values()), "date_folders": len(moved_files), "errors": errors, "dry_run": dry_run}}

def archive_files_sync(downloads_path: str = None, days_old: int = 180, archive_name: str = None) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    if not archive_name:
        archive_name = f"archive_{datetime.now().strftime('%Y-%m-%d')}.zip"
    
    archive_path = path / archive_name
    cutoff_date = datetime.now() - timedelta(days=days_old)
    archived_files = []
    total_size = 0
    
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in path.rglob('*'):
            if item.is_file() and item != archive_path:
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff_date:
                    try:
                        arcname = str(item.relative_to(path))
                        zipf.write(item, arcname)
                        size = item.stat().st_size
                        archived_files.append(arcname)
                        total_size += size
                        item.unlink()
                    except Exception:
                        pass
    
    archive_size = archive_path.stat().st_size if archive_path.exists() else 0
    return {"ok": True, "data": {"archive_name": archive_name, "archived_files": len(archived_files), "original_size_mb": round(total_size / (1024 * 1024), 2), "archive_size_mb": round(archive_size / (1024 * 1024), 2), "compression_ratio": round((1 - archive_size / total_size) * 100, 1) if total_size > 0 else 0, "files": archived_files[:20]}}

def extract_archives_sync(downloads_path: str = None, delete_after: bool = False) -> dict:
    path = get_downloads_path(downloads_path)
    if not path.exists():
        return {"ok": False, "error": f"Path {path} does not exist"}
    
    extracted = []
    errors = []
    
    for item in path.rglob('*'):
        if item.is_file() and item.suffix.lower() == '.zip':
            extract_dir = item.parent / item.stem
            try:
                with zipfile.ZipFile(item, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                extracted.append({"archive": str(item.relative_to(path)), "extracted_to": str(extract_dir.relative_to(path))})
                if delete_after:
                    item.unlink()
            except Exception as e:
                errors.append(f"{item.name}: {str(e)}")
    
    return {"ok": True, "data": {"extracted": extracted, "count": len(extracted), "errors": errors, "deleted_archives": delete_after}}

@mcp.tool()
async def organize_downloads(downloads_path: Optional[str] = None, dry_run: bool = False) -> dict[str, Any]:
    """Organize files in Downloads folder by type (Images, Documents, Videos, etc)"""
    return await asyncio.to_thread(organize_by_type_sync, downloads_path, dry_run)

@mcp.tool()
async def find_duplicates(downloads_path: Optional[str] = None, delete_duplicates: bool = False) -> dict[str, Any]:
    """Find duplicate files by content hash. Optionally delete duplicates keeping newest"""
    return await asyncio.to_thread(find_duplicates_sync, downloads_path, delete_duplicates)

@mcp.tool()
async def clean_old_files(downloads_path: Optional[str] = None, days_old: int = 90, delete: bool = False) -> dict[str, Any]:
    """Find and optionally delete files older than specified days"""
    return await asyncio.to_thread(clean_old_files_sync, downloads_path, days_old, delete)

@mcp.tool()
async def get_folder_stats(downloads_path: Optional[str] = None) -> dict[str, Any]:
    """Get statistics about Downloads folder: file count, size, breakdown by category"""
    return await asyncio.to_thread(get_stats_sync, downloads_path)

@mcp.tool()
async def move_by_date(downloads_path: Optional[str] = None, dry_run: bool = False) -> dict[str, Any]:
    """Organize files into folders by date (Year/Month)"""
    return await asyncio.to_thread(organize_by_date_sync, downloads_path, dry_run)

@mcp.tool()
async def archive_old_files(downloads_path: Optional[str] = None, days_old: int = 180, archive_name: Optional[str] = None) -> dict[str, Any]:
    """Archive old files to ZIP and delete originals"""
    return await asyncio.to_thread(archive_files_sync, downloads_path, days_old, archive_name)

@mcp.tool()
async def extract_archives(downloads_path: Optional[str] = None, delete_after: bool = False) -> dict[str, Any]:
    """Extract all ZIP archives found in Downloads folder. Optionally delete archives after extraction"""
    return await asyncio.to_thread(extract_archives_sync, downloads_path, delete_after)

if __name__ == "__main__":
    mcp.run()
