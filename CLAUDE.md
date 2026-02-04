# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a Born2beRoot guide - a comprehensive tutorial for setting up a Debian Linux virtual machine with advanced partitioning (LVM + LUKS encryption). The content is primarily an HTML guide with supporting images.

### Repository Structure

```
Born2beRoot/
├── born2beroot.html          # Main HTML guide (opens in browser)
├── download_all_images.py    # Script to download all 65 screenshots from web.archive.org
└── images/                   # Directory containing 65 PNG screenshots for the guide
```

## Commands

### Download Images
To download or refresh the guide screenshots (65 images total):
```bash
python3 download_all_images.py
```

The script includes:
- Retry logic (max 3 attempts per image)
- Skip detection for existing files
- Random delays between downloads (0.5-1.5s)
- Progress tracking and summary

### View the Guide
Open the HTML file in a browser:
```bash
# Linux
xdg-open born2beroot.html

# macOS
open born2beroot.html
```

## Architecture

### Image Download Script (`download_all_images.py`)

The `IMAGES` list contains an ordered array of 65 screenshot objects, each with:
- `src`: web.archive.org URL
- `name`: output filename (numbered 01-65 for ordering)
- `alt`: descriptive text for the image

The download function implements:
- Session-based HTTP requests with custom User-Agent
- Streaming download with 8KB chunks
- File size validation (rejects 0-byte files)
- Exponential backoff retry logic

### HTML Guide (`born2beroot.html`)

A self-contained, styled HTML document with:
- Embedded CSS using CSS custom properties for theming
- Responsive layout with sticky sidebar navigation (desktop)
- 65 embedded image references pointing to `images/` directory
- Sections covering: VM creation, Debian installation, partitioning, LVM, LUKS encryption, GRUB setup

## Notes

- Images are sourced from web.archive.org (Wayback Machine) snapshots from codequoi.com
- The guide covers the full Born2beRoot project setup including dual-boot partitioning with LVM and encryption
- All images use descriptive filenames numbered 01-65 to maintain proper order in the guide
