#!/usr/bin/env python3
"""
version_manager.py — Prep Version Backup & Rollback

Manages version history for interview prep documents.
Keeps up to 10 versions per prep. Uses timestamped snapshots.

Usage:
    python3 version_manager.py --action backup --slug google-swe --base-dir ./preps
    python3 version_manager.py --action list --slug google-swe --base-dir ./preps
    python3 version_manager.py --action rollback --slug google-swe --version v2 --base-dir ./preps
    python3 version_manager.py --help
"""

import argparse
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

MAX_VERSIONS = 10

def get_version_dir(prep_dir: Path) -> Path:
    """Get or create the versions directory."""
    v_dir = prep_dir / "versions"
    v_dir.mkdir(exist_ok=True)
    return v_dir


def get_current_version(prep_dir: Path) -> str:
    """Read current version from meta.json."""
    meta_path = prep_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return meta.get("version", "v1")
    return "v1"


def backup(slug: str, base_dir: Path) -> dict:
    """Create a backup of the current prep state."""
    prep_dir = base_dir / slug
    if not prep_dir.exists():
        return {"error": "not_found", "message": f"Prep '{slug}' not found"}

    v_dir = get_version_dir(prep_dir)
    current_ver = get_current_version(prep_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{current_ver}_{timestamp}"
    backup_dir = v_dir / backup_name
    backup_dir.mkdir()
    # Copy all files (except versions dir) to backup
    for item in prep_dir.iterdir():
        if item.name == "versions":
            continue
        if item.is_file():
            shutil.copy2(item, backup_dir / item.name)
        elif item.is_dir():
            shutil.copytree(item, backup_dir / item.name)

    # Enforce max versions limit
    existing = sorted(v_dir.iterdir(), key=lambda x: x.stat().st_mtime)
    while len(existing) > MAX_VERSIONS:
        oldest = existing.pop(0)
        shutil.rmtree(oldest)

    return {
        "status": "backed_up",
        "slug": slug,
        "version": current_ver,
        "backup_name": backup_name,
        "backup_path": str(backup_dir),
        "total_versions": len(list(v_dir.iterdir())),
    }


def list_versions(slug: str, base_dir: Path) -> dict:
    """List all available versions for a prep."""
    prep_dir = base_dir / slug
    if not prep_dir.exists():
        return {"error": "not_found", "message": f"Prep '{slug}' not found"}
    v_dir = get_version_dir(prep_dir)
    versions = []
    for d in sorted(v_dir.iterdir()):
        if d.is_dir():
            files = [f.name for f in d.iterdir() if f.is_file()]
            versions.append({
                "name": d.name,
                "files": files,
                "timestamp": datetime.fromtimestamp(d.stat().st_mtime).isoformat(),
            })

    return {
        "slug": slug,
        "current_version": get_current_version(prep_dir),
        "versions": versions,
        "total": len(versions),
    }


def rollback(slug: str, base_dir: Path, version: str) -> dict:
    """Rollback a prep to a specific version."""
    prep_dir = base_dir / slug
    v_dir = get_version_dir(prep_dir)

    # Find matching version
    target = None
    for d in v_dir.iterdir():
        if d.is_dir() and (d.name == version or d.name.startswith(version)):
            target = d
            break
    if not target:
        return {"error": "version_not_found", "message": f"Version '{version}' not found for '{slug}'"}

    # Backup current state first
    backup_result = backup(slug, base_dir)

    # Restore from target version
    for item in target.iterdir():
        dest = prep_dir / item.name
        if item.is_file():
            shutil.copy2(item, dest)
        elif item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)

    return {
        "status": "rolled_back",
        "slug": slug,
        "restored_from": target.name,
        "backup_before_rollback": backup_result.get("backup_name", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Manage prep version history")
    parser.add_argument("--action", required=True,
                       choices=["backup", "list", "rollback"],
                       help="Action to perform")
    parser.add_argument("--slug", required=True, help="Prep identifier")
    parser.add_argument("--version", help="Version to rollback to (for rollback action)")
    parser.add_argument("--base-dir", default="./preps", help="Base directory for preps")
    args = parser.parse_args()

    base = Path(args.base_dir)

    if args.action == "backup":
        result = backup(args.slug, base)
    elif args.action == "list":
        result = list_versions(args.slug, base)
    elif args.action == "rollback":
        if not args.version:
            print(json.dumps({"error": "missing_version", "message": "Provide --version for rollback"}))
            sys.exit(1)
        result = rollback(args.slug, base, args.version)
    else:
        result = {"error": "unknown_action"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()