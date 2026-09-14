#!/usr/bin/env python3
"""Clone llama.cpp and build llama-server for THIS host (issue #78).

Apple Silicon (darwin + arm64/aarch64) → Metal cmake.
NVIDIA (`nvidia-smi` lists a GPU) → CUDA cmake (nvcc required).
Neither → CPU cmake (Metal off, CUDA off). Never Metal-on-NVIDIA, never CUDA-on-Mac.

If llama-server is already resolvable, do nothing.
Never called from --download-top-tier.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

LLAMA_CPP_CLONE_URL = "https://github.com/ggml-org/llama.cpp.git"
LLAMA_CPP_DEFAULT_SRC = os.path.join(
    os.path.expanduser("~"), "repository", "git", "llama.cpp"
)
def find_llama_server():
    """Same lookup as llama_serve.resolve_llama_server, without exiting."""
    env = (os.environ.get("LLAMA_SERVER") or "").strip()
    if env:
        if os.path.isfile(env) and os.access(env, os.X_OK):
            return env
        raise SystemExit(
            f"[ERROR] LLAMA_SERVER={env!r} is not an executable llama-server. "
            "Fix LLAMA_SERVER or unset it. Not compiling over a bad override."
        )
    found = shutil.which("llama-server")
    if found:
        return found
    home_bin = os.path.join(os.path.expanduser("~"), "bin", "llama-server")
    if os.path.isfile(home_bin) and os.access(home_bin, os.X_OK):
        return home_bin
    return None


def detect_gpu(platform=None, machine=None, nvidia_smi=None):
    """Return 'metal', 'cuda', or 'cpu'. Injectables are for tests."""
    plat = sys.platform if platform is None else platform
    mach = os.uname().machine if machine is None else machine
    if plat == "darwin" and mach in ("arm64", "aarch64"):
        return "metal"
    smi = shutil.which("nvidia-smi") if nvidia_smi is None else nvidia_smi
    if smi:
        try:
            proc = subprocess.run(
                [smi, "-L"], capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.TimeoutExpired):
            proc = None
        if proc is not None and proc.returncode == 0 and (
            "GPU" in (proc.stdout or "") or "NVIDIA" in (proc.stdout or "").upper()
        ):
            return "cuda"
        # nvidia-smi -L typically prints "GPU 0: ..."
        if proc is not None and proc.returncode == 0 and (proc.stdout or "").strip():
            return "cuda"
    return "cpu"


def cmake_configure_args(gpu):
    """Exact cmake -D flags for this GPU. No extra backends."""
    if gpu == "metal":
        return [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DGGML_METAL=ON",
            "-DGGML_CUDA=OFF",
        ]
    if gpu == "cuda":
        return [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DGGML_CUDA=ON",
            "-DGGML_METAL=OFF",
        ]
    if gpu == "cpu":
        return [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DGGML_METAL=OFF",
            "-DGGML_CUDA=OFF",
        ]
    raise SystemExit(f"[ERROR] unknown llama.cpp backend {gpu!r}")


def _run(cmd, cwd=None):
    print("==> " + " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=cwd)
    if proc.returncode != 0:
        raise SystemExit(
            f"[ERROR] command failed (rc={proc.returncode}): {' '.join(cmd)}"
        )


def ensure_llama_server(run=None):
    """Return path to llama-server, cloning/building if missing.

    `run` overrides subprocess for tests (callable(cmd, cwd=) -> None or raise).
    """
    existing = find_llama_server()
    if existing:
        return existing

    gpu = detect_gpu()
    if gpu == "cuda" and not shutil.which("nvcc"):
        raise SystemExit(
            "[ERROR] NVIDIA GPU detected but nvcc is not on PATH. "
            "Install the CUDA toolkit, then retry. No Metal/CPU fallback."
        )

    src = (os.environ.get("LLAMA_CPP_SRC") or "").strip() or LLAMA_CPP_DEFAULT_SRC
    runner = run if run is not None else _run
    have_tree = os.path.isdir(os.path.join(src, ".git")) or os.path.isdir(
        os.path.join(src, "ggml")
    )
    if not have_tree:
        parent = os.path.dirname(src)
        os.makedirs(parent, exist_ok=True)
        runner(["git", "clone", "--depth", "1", LLAMA_CPP_CLONE_URL, src], cwd=None)

    print(f"==> building llama-server backend={gpu}", flush=True)
    cmake_cmd = ["cmake", "-B", "build"] + cmake_configure_args(gpu)
    runner(cmake_cmd, cwd=src)
    jobs = str(os.cpu_count() or 1)
    runner(
        [
            "cmake",
            "--build",
            "build",
            "--config",
            "Release",
            "--target",
            "llama-server",
            "-j",
            jobs,
        ],
        cwd=src,
    )
    built = os.path.join(src, "build", "bin", "llama-server")
    if os.name == "nt":
        exe = built + ".exe"
        if os.path.isfile(exe):
            built = exe
    if not os.path.isfile(built):
        raise SystemExit(f"[ERROR] cmake finished but {built} is missing")
    dest_dir = os.path.join(os.path.expanduser("~"), "bin")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "llama-server")
    if os.path.islink(dest) or os.path.exists(dest):
        os.remove(dest)
    os.symlink(built, dest)
    print(f"==> Symlinked {dest} -> {built}", flush=True)
    return dest


def main(argv=None):
    path = ensure_llama_server()
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
