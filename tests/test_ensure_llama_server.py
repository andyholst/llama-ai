"""Hermetic tests for issue #78: clone/build llama-server for Metal vs CUDA."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ensure_llama_server as els  # noqa: E402


def test_detect_metal_on_darwin_arm64():
    assert els.detect_gpu(platform="darwin", machine="arm64", nvidia_smi=None) == "metal"
    assert els.detect_gpu(platform="darwin", machine="aarch64", nvidia_smi=None) == "metal"


def test_detect_cuda_when_nvidia_smi_lists_gpu(tmp_path, monkeypatch):
    smi = tmp_path / "nvidia-smi"
    smi.write_text("#!/bin/sh\necho 'GPU 0: NVIDIA RTX'\n")
    smi.chmod(0o755)
    assert els.detect_gpu(platform="linux", machine="x86_64", nvidia_smi=str(smi)) == "cuda"


def test_detect_cpu_on_linux_without_nvidia(monkeypatch):
    assert els.detect_gpu(platform="linux", machine="x86_64", nvidia_smi=None) == "cpu"


def test_cmake_args_metal_not_cuda():
    args = els.cmake_configure_args("metal")
    assert "-DGGML_METAL=ON" in args
    assert "-DGGML_CUDA=OFF" in args
    assert "-DGGML_CUDA=ON" not in args


def test_cmake_args_cuda_not_metal():
    args = els.cmake_configure_args("cuda")
    assert "-DGGML_CUDA=ON" in args
    assert "-DGGML_METAL=OFF" in args
    assert "-DGGML_METAL=ON" not in args


def test_cmake_args_cpu_disables_gpu_backends():
    args = els.cmake_configure_args("cpu")
    assert "-DGGML_METAL=OFF" in args
    assert "-DGGML_CUDA=OFF" in args
    assert "-DGGML_METAL=ON" not in args
    assert "-DGGML_CUDA=ON" not in args


def test_bad_llama_server_env_does_not_compile(tmp_path, monkeypatch):
    monkeypatch.setenv("LLAMA_SERVER", str(tmp_path / "missing-bin"))
    with pytest.raises(SystemExit) as e:
        els.find_llama_server()
    assert "not an executable" in str(e.value)


def test_ensure_skips_build_when_binary_exists(tmp_path, monkeypatch):
    fake = tmp_path / "llama-server"
    fake.write_bytes(b"x")
    fake.chmod(0o755)
    monkeypatch.setenv("LLAMA_SERVER", str(fake))
    calls = []

    def no_run(cmd, cwd=None):
        calls.append(cmd)
        raise AssertionError("cmake must not run")

    assert els.ensure_llama_server(run=no_run) == str(fake)
    assert calls == []


def test_ensure_metal_clone_cmake_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(els, "find_llama_server", lambda: None)
    monkeypatch.setattr(els, "detect_gpu", lambda **k: "metal")
    home = tmp_path / "home"
    (home / "bin").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    src = tmp_path / "llama.cpp"
    monkeypatch.setenv("LLAMA_CPP_SRC", str(src))
    cmds = []

    def run(cmd, cwd=None):
        cmds.append(list(cmd))
        if cmd[:2] == ["git", "clone"]:
            src.mkdir()
            (src / "ggml").mkdir()
            return
        if cmd[0] == "cmake" and "-B" in cmd:
            (src / "build" / "bin").mkdir(parents=True)
            binp = src / "build" / "bin" / "llama-server"
            binp.write_bytes(b"m")
            binp.chmod(0o755)

    def exp(p):
        return str(home) if p == "~" else p

    monkeypatch.setattr(els.os.path, "expanduser", exp)
    out = els.ensure_llama_server(run=run)
    cmake = [c for c in cmds if c and c[0] == "cmake" and "-B" in c][0]
    assert "-DGGML_METAL=ON" in cmake
    assert "-DGGML_CUDA=OFF" in cmake
    assert any(c[:2] == ["git", "clone"] for c in cmds), cmds
    assert "openrouter" not in out.lower()


def test_ensure_cuda_cmake_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(els, "find_llama_server", lambda: None)
    monkeypatch.setattr(els, "detect_gpu", lambda **k: "cuda")
    monkeypatch.setattr(els.shutil, "which", lambda n: "/usr/bin/nvcc" if n == "nvcc" else None)
    src = tmp_path / "llama.cpp"
    src.mkdir()
    (src / "ggml").mkdir()
    monkeypatch.setenv("LLAMA_CPP_SRC", str(src))
    home = tmp_path / "home"
    (home / "bin").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr(els.os.path, "expanduser",
                        lambda p: str(home) if p in ("~", "~/bin/llama-server") else p)
    cmds = []

    def run(cmd, cwd=None):
        cmds.append(cmd)
        if cmd[0] == "cmake" and "-B" in cmd:
            (src / "build" / "bin").mkdir(parents=True)
            binp = src / "build" / "bin" / "llama-server"
            binp.write_bytes(b"c")
            binp.chmod(0o755)

    # expanduser("~") used for dest symlink
    def exp(p):
        if p == "~":
            return str(home)
        return os.path.expanduser(p)

    monkeypatch.setattr(els.os.path, "expanduser", exp)
    els.ensure_llama_server(run=run)
    cmake = [c for c in cmds if c[0] == "cmake" and "-B" in c][0]
    assert "-DGGML_CUDA=ON" in cmake
    assert "-DGGML_METAL=OFF" in cmake
    assert not any(c[:2] == ["git", "clone"] for c in cmds), "src already present"


def test_ensure_cpu_cmake_when_no_gpu(tmp_path, monkeypatch):
    monkeypatch.setattr(els, "find_llama_server", lambda: None)
    monkeypatch.setattr(els, "detect_gpu", lambda **k: "cpu")
    src = tmp_path / "llama.cpp"
    src.mkdir()
    (src / "ggml").mkdir()
    monkeypatch.setenv("LLAMA_CPP_SRC", str(src))
    home = tmp_path / "home"
    (home / "bin").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))

    def exp(p):
        return str(home) if p == "~" else p

    monkeypatch.setattr(els.os.path, "expanduser", exp)
    cmds = []

    def run(cmd, cwd=None):
        cmds.append(list(cmd))
        if cmd[0] == "cmake" and "-B" in cmd:
            (src / "build" / "bin").mkdir(parents=True)
            binp = src / "build" / "bin" / "llama-server"
            binp.write_bytes(b"cpu")
            binp.chmod(0o755)

    els.ensure_llama_server(run=run)
    cmake = [c for c in cmds if c[0] == "cmake" and "-B" in c][0]
    assert "-DGGML_METAL=OFF" in cmake
    assert "-DGGML_CUDA=OFF" in cmake
    assert "-DGGML_CUDA=ON" not in cmake
    assert "-DGGML_METAL=ON" not in cmake


def test_ensure_cuda_without_nvcc_fails(monkeypatch):
    monkeypatch.setattr(els, "find_llama_server", lambda: None)
    monkeypatch.setattr(els, "detect_gpu", lambda **k: "cuda")
    monkeypatch.setattr(els.shutil, "which", lambda n: None)
    with pytest.raises(SystemExit) as e:
        els.ensure_llama_server(run=lambda *a, **k: (_ for _ in ()).throw(AssertionError("cmake")))
    assert "nvcc" in str(e.value).lower()
