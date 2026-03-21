#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path


# ==========================================================
# Utilities
# ==========================================================

def run(cmd: str) -> None:
    """Execute a shell command."""
    print(f"\n>>> {cmd}")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"\nERROR: Command failed -> {cmd}")
        exit(1)


def install_pacman(packages: list[str], needed: bool = False) -> None:
    """Install packages using pacman."""
    flag = "--needed" if needed else ""
    pkg = " ".join(packages)

    run(f"sudo pacman -S {flag} --noconfirm {pkg}")


def install_yay(packages: list[str]) -> None:
    """Install packages using yay."""
    pkg = " ".join(packages)

    run(f"yay -S --noconfirm --removemake {pkg}")


# ==========================================================
# Input Method (Fcitx5)
# ==========================================================

def install_fcitx5() -> None:
    print("\n=== Installing Fcitx5 + UniKey ===")

    install_pacman([
        "fcitx5",
        "fcitx5-qt",
        "fcitx5-gtk",
        "fcitx5-unikey",
        "fcitx5-configtool"
    ])

    env_content = """GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
"""

    tmp_file = "/tmp/fcitx_env"

    with open(tmp_file, "w") as f:
        f.write(env_content)

    run(f"sudo cp {tmp_file} /etc/environment")
    os.remove(tmp_file)


# ==========================================================
# AMD GPU Driver
# ==========================================================

def install_amd_driver() -> None:
    print("\n=== Installing AMD Vulkan Driver ===")

    install_pacman([
        "lib32-mesa",
        "vulkan-radeon",
        "lib32-vulkan-radeon",
        "vulkan-icd-loader",
        "lib32-vulkan-icd-loader"
    ], needed=True)


# ==========================================================
# XFCE Panel Configuration
# ==========================================================

def setup_xfce_panel() -> None:
    print("\n=== Configuring XFCE Panel ===")

    repo = "https://github.com/tofu2220/my-dotfile.git"
    repo_dir = Path("my-dotfile")

    if not repo_dir.exists():
        run(f"git clone {repo}")

    panel_file = repo_dir / "xfce4-panel.xml"

    if not panel_file.exists():
        print("Panel configuration file not found.")
        return

    config_dir = Path.home() / ".config/xfce4/xfconf/xfce-perchannel-xml"
    config_dir.mkdir(parents=True, exist_ok=True)

    run("xfce4-panel --quit")
    run("pkill xfconfd")

    run(f"cp {panel_file} {config_dir}")

    run("xfce4-panel &")


# ==========================================================
# Basic Applications
# ==========================================================

def install_basic_apps() -> None:
    print("\n=== Installing Basic Applications ===")

    install_pacman([
        "mpv",
        "steam",
        "gnome-keyring",
    ])


# ==========================================================
# Programming Environment
# ==========================================================

def install_programming_tools() -> None:
    print("\n=== Installing Programming Tools ===")

    install_pacman([
        "clang",
        "go",
        "rustup",
    ])

    run("rustup install stable")
    run("rustup default stable")

    install_yay([
        "vscodium-bin",
        "github-desktop-bin"
    ])


# ==========================================================
# CPU Power Management
# ==========================================================

def install_auto_cpufreq() -> None:
    print("\n=== Installing auto-cpufreq ===")

    install_yay(["auto-cpufreq"])

    run("sudo systemctl mask power-profiles-daemon.service")
    run("sudo systemctl enable auto-cpufreq.service")


# ==========================================================
# Main
# ==========================================================

def main() -> None:

    print("""
====================================
 Arch Linux Development Setup
====================================
""")

    install_fcitx5()

    install_amd_driver()

    install_basic_apps()

    install_programming_tools()

    install_auto_cpufreq()

    setup_xfce_panel()

    print("\nSetup completed successfully.")
    print("Reboot recommended.")

if __name__ == "__main__":
    main()
