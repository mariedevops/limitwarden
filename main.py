#!/usr/bin/env python3

import argparse
from scanner import find_unbounded_workloads
from metrics import get_usage_for_container
from heuristics import suggest_resources
from patcher import patch_workload
from manifest_patcher import scan_and_patch_manifests
from utils.utils import log

def run_cluster_patch():
    log("🚀 Starting LimitWarden (cluster mode)...")
    workloads = find_unbounded_workloads()

    for workload in workloads:
        usage = get_usage_for_container(workload)
        resources = suggest_resources(usage)
        patch_workload(workload, resources)

    log("✅ LimitWarden completed (cluster mode).")

def run_manifest_patch(path, write=False, dry_run=True):
    log("📁 Scanning manifests at: " + path)
    scan_and_patch_manifests(path=path, write=write, dry_run=dry_run)

def main():
    parser = argparse.ArgumentParser(prog="limitwarden", description="LimitWarden CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: scan
    scan_parser = subparsers.add_parser("scan", help="Scan and optionally patch manifests")
    scan_parser.add_argument("path", help="Path to directory containing YAML files")
    scan_parser.add_argument("--patch", action="store_true", help="Enable patching")
    scan_parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    scan_parser.add_argument("--write", action="store_true", help="Write changes to disk")

    # Subcommand: patch
    patch_parser = subparsers.add_parser("patch", help="Patch manifests directly")
    patch_parser.add_argument("path", help="Path to directory containing YAML files")

    # Default: allow path-only usage
    parser.add_argument("default_path", nargs="?", help="Path to patch if no subcommand is given")

    args = parser.parse_args()

    if args.command == "scan":
        run_manifest_patch(
            path=args.path,
            write=args.write,
            dry_run=args.dry_run or not args.write
        )
    elif args.command == "patch":
        run_manifest_patch(
            path=args.path,
            write=True,
            dry_run=False
        )
    elif args.default_path:
        run_manifest_patch(
            path=args.default_path,
            write=True,
            dry_run=False
        )
    else:
        run_cluster_patch()

if __name__ == "__main__":
    main()
