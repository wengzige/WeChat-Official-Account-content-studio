#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath


REPO_ROOT = None

BLOCKED_ROOT_FILES = {
    "config.yaml",
    "style.yaml",
    "history.yaml",
    "playbook.md",
    "writing-config.yaml",
    ".env",
}

BLOCKED_TOP_LEVEL_DIRS = {
    "corpus",
    "lessons",
    "clients",
}

ALLOWED_SKILL2_CHILDREN = {
    ".agents",
    ".config",
    ".local",
    "README.md",
    "scripts",
    "templates",
}

BLOCKED_EXTENSIONS = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".crt",
    ".cer",
}

PLACEHOLDER_MARKERS = (
    "your_",
    "example",
    "placeholder",
    "changeme",
    "replace_me",
    "dummy",
    "sample",
    "test",
    "mock",
    "${",
    "%(",
    "xxxx",
    "todo",
)

SECRET_PATTERNS = [
    ("wechat_appid", re.compile(r'(?i)\b(?:appid|app_id)\b\s*[:=]\s*["\']?(wx[a-zA-Z0-9]{14,20})["\']?')),
    ("wechat_secret", re.compile(r'(?i)\b(?:secret|appsecret|client_secret)\b\s*[:=]\s*["\']?([A-Za-z0-9_-]{16,})["\']?')),
    ("api_key", re.compile(r'(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token)\b\s*[:=]\s*["\']?([A-Za-z0-9._\-]{16,})["\']?')),
    ("openai_key", re.compile(r'\bsk-[A-Za-z0-9_-]{16,}\b')),
    ("github_pat", re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b')),
]

TEXT_EXTENSIONS = {
    ".py",
    ".ps1",
    ".sh",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".env",
    ".gitignore",
}


def run_git(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def is_binary(data: bytes) -> bool:
    return b"\x00" in data


def looks_like_placeholder(value: str) -> bool:
    lowered = value.strip().lower()
    if not lowered:
        return True
    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def is_blocked_path(path: str) -> str | None:
    pure = PurePosixPath(path)
    name = pure.name

    if path in BLOCKED_ROOT_FILES:
        return f"blocked sensitive root file: {path}"

    if name in {".env"} or name.startswith(".env."):
        return f"blocked environment file: {path}"

    if pure.suffix.lower() in BLOCKED_EXTENSIONS:
        return f"blocked certificate or private-key file: {path}"

    if pure.parts and pure.parts[0] in BLOCKED_TOP_LEVEL_DIRS:
        return f"blocked personal data directory: {path}"

    if pure.parts and pure.parts[0] == "output" and path != "output/.gitkeep":
        return f"blocked generated output path: {path}"

    if pure.parts and pure.parts[0] == "skill2 paibanyouhua" and len(pure.parts) >= 2:
        child = pure.parts[1]
        if child == ".config" and name == "config.yaml":
            return f"blocked skill config file: {path}"
        if child not in ALLOWED_SKILL2_CHILDREN:
            return f"blocked article worktree path under skill2 paibanyouhua: {path}"

    return None


def should_scan_text(path: str) -> bool:
    pure = PurePosixPath(path)
    if pure.suffix.lower() in TEXT_EXTENSIONS:
        return True
    return pure.name in {".gitignore", ".env"}


def load_blob(commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or f"failed to read {path} from {commit}")
    return result.stdout


def find_secret_matches(path: str, text: str) -> list[str]:
    findings: list[str] = []
    for label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            value = match.group(1) if match.groups() else match.group(0)
            if looks_like_placeholder(value):
                continue
            findings.append(f"{label} in {path}: {value[:12]}...")
    return findings


def commits_from_pre_push_stdin(stdin: str) -> list[str]:
    commits: list[str] = []
    for line in stdin.splitlines():
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        _, local_sha, _, remote_sha = parts
        if local_sha == "0" * 40:
            continue
        if remote_sha == "0" * 40:
            result = run_git("rev-list", local_sha)
        else:
            result = run_git("rev-list", f"{remote_sha}..{local_sha}")
        if result.returncode != 0:
            commits.append(local_sha)
            continue
        commits.extend(item.strip() for item in result.stdout.splitlines() if item.strip())
    return sorted(set(commits))


def list_commit_files(commit: str) -> list[str]:
    result = run_git("ls-tree", "-r", "--name-only", commit)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to list files for {commit}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def scan_commit(commit: str) -> dict:
    findings: list[dict] = []
    for path in list_commit_files(commit):
        blocked_reason = is_blocked_path(path)
        if blocked_reason:
            findings.append({"type": "blocked_path", "path": path, "detail": blocked_reason})
            continue

        if not should_scan_text(path):
            continue

        data = load_blob(commit, path)
        if is_binary(data):
            continue

        text = data.decode("utf-8", errors="replace")
        for finding in find_secret_matches(path, text):
            findings.append({"type": "secret_pattern", "path": path, "detail": finding})

    return {
        "commit": commit,
        "findings": findings,
    }


def main() -> int:
    global REPO_ROOT
    parser = argparse.ArgumentParser(description="Block pushing secrets or private work files.")
    parser.add_argument("--pre-push", action="store_true", help="Read pushed refs from stdin like a git pre-push hook.")
    parser.add_argument("--commit", action="append", default=[], help="Commit SHA to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    repo_result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if repo_result.returncode != 0:
        print("Not inside a git repository.", file=sys.stderr)
        return 2
    REPO_ROOT = repo_result.stdout.strip()

    commits = list(args.commit)
    if args.pre_push:
        commits.extend(commits_from_pre_push_stdin(sys.stdin.read()))
    if not commits:
        head = run_git("rev-parse", "HEAD")
        if head.returncode != 0:
            print("Could not resolve HEAD.", file=sys.stderr)
            return 2
        commits = [head.stdout.strip()]

    reports = [scan_commit(commit) for commit in sorted(set(commits))]
    findings = [item for report in reports for item in report["findings"]]
    result = {
        "ok": len(findings) == 0,
        "reports": reports,
        "finding_count": len(findings),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if findings:
            print("Push blocked: detected private files or secret-like content.")
            for item in findings:
                print(f"- {item['detail']}")
        else:
            print("Privacy guard passed: no blocked files or secret-like content detected.")

    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
