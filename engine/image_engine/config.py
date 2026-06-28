"""
===========================================
ShowBiz Image Engine
config.py
Version 1.0
===========================================

Central configuration for Image Engine 2.0.

Nothing in production uses this yet.

This file exists so every Image Engine
module shares the same settings.
"""

# ============================================
# Image Providers
# ============================================

IMAGE_PROVIDERS = [

    "wikimedia",

]

# ============================================
# Search Settings
# ============================================

MAX_RESULTS = 10

# ============================================
# Minimum Acceptable Image Size
# ============================================

MIN_WIDTH = 1200

MIN_HEIGHT = 800

# ============================================
# Preferred Download Size
# ============================================

TARGET_WIDTH = 1600

TARGET_HEIGHT = 900

# ============================================
# Image Quality
# ============================================

MIN_SCORE = 80

# ============================================
# Local Folders
# ============================================

TEST_IMAGE_FOLDER = "engine/image_engine/test_images"

CACHE_FOLDER = "engine/image_engine/cache"

# ============================================
# Future API Keys
# ============================================

WIKIMEDIA_API = ""

PEXELS_API_KEY = ""

UNSPLASH_ACCESS_KEY = ""

GETTY_API_KEY = ""

SHUTTERSTOCK_API_KEY = ""

# ============================================
# Logging
# ============================================

VERBOSE = True