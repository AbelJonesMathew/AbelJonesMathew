import os
import json
import re

def extract_missing_data():
    """
    Recovers me_transparent_base64.txt, face_crop_base64.txt, and name_vector_paths.txt
    from existing SVG assets if they are missing in the workspace.
    """
    recovered = False
    
    # 1. Extract me_transparent_base64.txt from banner.svg
    if not os.path.exists("me_transparent_base64.txt"):
        if os.path.exists("banner.svg"):
            print("Extracting me_transparent_base64.txt from existing banner.svg...")
            try:
                with open("banner.svg", "r", encoding="utf-8") as f:
                    content = f.read()
                # Find base64 image data in banner.svg
                match = re.search(r'<image href="data:image/png;base64,([^"]+)"', content)
                if match:
                    with open("me_transparent_base64.txt", "w", encoding="utf-8") as out:
                        out.write(match.group(1).strip())
                    recovered = True
                else:
                    print("Warning: Could not find base64 image in banner.svg")
            except Exception as e:
                print(f"Error extracting from banner.svg: {e}")
        else:
            print("Warning: banner.svg not found, cannot extract me_transparent_base64.txt")

    # 2. Extract face_crop_base64.txt from lanyard.svg
    if not os.path.exists("face_crop_base64.txt"):
        if os.path.exists("lanyard.svg"):
            print("Extracting face_crop_base64.txt from existing lanyard.svg...")
            try:
                with open("lanyard.svg", "r", encoding="utf-8") as f:
                    content = f.read()
                # Find base64 image data in lanyard.svg
                match = re.search(r'<image href="data:image/png;base64,([^"]+)"', content)
                if match:
                    with open("face_crop_base64.txt", "w", encoding="utf-8") as out:
                        out.write(match.group(1).strip())
                    recovered = True
                else:
                    print("Warning: Could not find base64 image in lanyard.svg")
            except Exception as e:
                print(f"Error extracting from lanyard.svg: {e}")
        else:
            print("Warning: lanyard.svg not found, cannot extract face_crop_base64.txt")

    # 3. Extract name_vector_paths.txt from banner.svg
    if not os.path.exists("name_vector_paths.txt"):
        if os.path.exists("banner.svg"):
            print("Extracting name_vector_paths.txt from existing banner.svg...")
            try:
                with open("banner.svg", "r", encoding="utf-8") as f:
                    content = f.read()
                # Find name vector paths group
                match = re.search(r'<g class="name-vector"[^>]*>(.*?)</g>', content, re.DOTALL)
                if match:
                    paths = match.group(1).strip()
                    with open("name_vector_paths.txt", "w", encoding="utf-8") as out:
                        out.write(paths)
                    recovered = True
                else:
                    print("Warning: Could not find name-vector group in banner.svg")
            except Exception as e:
                print(f"Error extracting name vector from banner.svg: {e}")
        else:
            print("Warning: banner.svg not found, cannot extract name_vector_paths.txt")
            
    return recovered

def load_text_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()

def main():
    print("Assembling SVG assets with real statistics in Emerald Depth (Midnight Navy & Crimson) theme...")
    
    # Try to extract missing files from existing SVGs if necessary
    extract_missing_data()
    
    # Check if files exist
    if not os.path.exists("me_transparent_base64.txt") or not os.path.exists("face_crop_base64.txt") or not os.path.exists("name_vector_paths.txt"):
        print("Error: Required base64 or path data files are missing. Please ensure banner.svg and lanyard.svg are in the folder, or provide the data files.")
        return

    char_b64 = load_text_file("me_transparent_base64.txt")
    face_b64 = load_text_file("face_crop_base64.txt")
    name_paths = load_text_file("name_vector_paths.txt")
    
    # Load real stats
    stats_data = {}
    if os.path.exists("real_stats.json"):
        with open("real_stats.json", "r") as f:
            stats_data = json.load(f)
            
    public_repos = stats_data.get("public_repos", 29)
    followers = stats_data.get("followers", 75)
    contributions = stats_data.get("contributions", 354)
    
    # 1. CREATE banner.svg (Dark Mode Ultramarine/Lavender)
    banner_dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 740" width="1280" height="740">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" />
      <stop offset="50%" stop-color="#021C4F" />
      <stop offset="100%" stop-color="#30010E" />
    </linearGradient>
    
    <!-- Neon Lavender to Blue Gradient for Name -->
    <linearGradient id="neon-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF5D82" />
      <stop offset="50%" stop-color="#C50337" />
      <stop offset="100%" stop-color="#2E79FF" />
    </linearGradient>

    <!-- Hologram Scanner Gradient (Ultramarine Blue) -->
    <linearGradient id="hologram-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0" />
      <stop offset="90%" stop-color="#C50337" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.8" />
    </linearGradient>
    
    <!-- Soft Glow Filter -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Heavy Neon Glow Filter -->
    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10" result="blur1" />
      <feGaussianBlur stdDeviation="20" result="blur2" />
      <feMerge>
        <feMergeNode in="blur2" />
        <feMergeNode in="blur1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    
    <!-- Card Inner Glass-morphism Gradient -->
    <linearGradient id="card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.06" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.01" />
    </linearGradient>
    
    <!-- Card Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.4" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.1" />
    </linearGradient>
    
    <!-- One-time Reveal Clip Path -->
    <clipPath id="hologram-reveal">
      <rect x="0" y="0" width="1280" height="0">
        <animate attributeName="height" values="0;740" dur="2s" begin="0.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" />
      </rect>
    </clipPath>

    <!-- General Clip Path for the rounded corners -->
    <clipPath id="banner-corners">
      <rect x="0" y="0" width="1280" height="740" rx="24" ry="24" />
    </clipPath>
  </defs>

  <style>
    /* Global Styles */
    .bg {{ fill: url(#bg-grad); }}
    .text-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .text-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    
    /* Ambient Orbs Animation */
    @keyframes pulse-orb {{
      0%, 100% {{ transform: scale(1) translate(0, 0); opacity: 0.2; }}
      50% {{ transform: scale(1.15) translate(30px, -20px); opacity: 0.35; }}
    }}
    .orb-1 {{ animation: pulse-orb 15s ease-in-out infinite; transform-origin: 200px 200px; }}
    .orb-2 {{ animation: pulse-orb 18s ease-in-out infinite alternate; transform-origin: 1000px 500px; }}

    /* Stars and Sparkles */
    @keyframes twinkle {{
      0%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
      50% {{ opacity: 1; transform: scale(1.2); }}
    }}
    .star {{ animation: twinkle 3s infinite; transform-origin: center; }}
    .star-delay-1 {{ animation-delay: 0.7s; }}
    .star-delay-2 {{ animation-delay: 1.4s; }}
    .star-delay-3 {{ animation-delay: 2.1s; }}
    
    /* Floating Particles */
    @keyframes float-up {{
      0% {{ transform: translateY(100px) translateX(0) scale(0.8); opacity: 0; }}
      10% {{ opacity: 0.5; }}
      90% {{ opacity: 0.5; }}
      100% {{ transform: translateY(-400px) translateX(30px) scale(1.1); opacity: 0; }}
    }}
    .particle {{ animation: float-up 8s linear infinite; }}
    .p-1 {{ animation-delay: 0s; left: 100px; }}
    .p-2 {{ animation-delay: 2s; left: 400px; }}
    .p-3 {{ animation-delay: 4.5s; left: 250px; }}
    .p-4 {{ animation-delay: 6s; left: 950px; }}

    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&amp;display=swap');

    @keyframes draw-name {{
      0% {{ stroke-dashoffset: 600; fill-opacity: 0; }}
      70% {{ stroke-dashoffset: 0; fill-opacity: 0; }}
      100% {{ stroke-dashoffset: 0; fill-opacity: 1; }}
    }}
    .cursive-name {{
      font-family: 'Dancing Script', 'Brush Script MT', 'Lucida Handwriting', 'Segoe Script', cursive;
      font-size: 60px;
      font-weight: 700;
      fill: url(#neon-grad);
      stroke: #C50337;
      stroke-width: 1.5;
      stroke-dasharray: 600;
      stroke-dashoffset: 600;
      animation: draw-name 2.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }}

    /* Terminal Typing Cursor */
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    .cursor {{ animation: blink 1s infinite; }}

    /* Cycling Typed Role Titles (0s to 12s) */
    .role-title {{ opacity: 0; font-size: 20px; font-weight: 700; fill: #C50337; filter: url(#glow); }}
    .role-1 {{ animation: cycle-role-1 12s infinite; }}
    .role-2 {{ animation: cycle-role-2 12s infinite; }}
    .role-3 {{ animation: cycle-role-3 12s infinite; }}
    
    @keyframes cycle-role-1 {{
      0% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      2% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      12%, 30% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      32% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}
    @keyframes cycle-role-2 {{
      0%, 33.3% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      35.3% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      45.3%, 63.3% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      65.3% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}
    @keyframes cycle-role-3 {{
      0%, 66.6% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      68.6% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      78.6%, 96.6% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      98.6% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}

    /* Quote Tagline reveal */
    @keyframes reveal-quote {{
      0% {{ clip-path: inset(0 100% 0 0); }}
      100% {{ clip-path: inset(0 0 0 0); }}
    }}
    .tagline {{ animation: reveal-quote 2.5s cubic-bezier(0.4, 0, 0.2, 1) 2.0s forwards; clip-path: inset(0 100% 0 0); }}

    /* Hologram Scan Sweep Line and Effect */
    @keyframes hologram-sweep {{
      0% {{ transform: translateY(-50px); opacity: 0; }}
      5% {{ opacity: 1; }}
      95% {{ opacity: 1; }}
      100% {{ transform: translateY(780px); opacity: 0; }}
    }}
    .scan-line {{ animation: hologram-sweep 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite; }}
    
    @keyframes one-time-reveal-line {{
      0% {{ transform: translateY(-50px); opacity: 1; }}
      99% {{ transform: translateY(740px); opacity: 1; }}
      100% {{ transform: translateY(740px); opacity: 0; }}
    }}
    .one-time-line {{ animation: one-time-reveal-line 2s cubic-bezier(0.4, 0, 0.2, 1) 0.5s forwards; }}

    /* Tech Stack Pills Fade In and Hover */
    @keyframes fade-scale-in {{
      0% {{ opacity: 0; transform: scale(0.95); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .tech-pill {{ opacity: 0; animation: fade-scale-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; transition: all 0.3s ease; cursor: pointer; }}
    .pill-1 {{ animation-delay: 2.2s; }}
    .pill-2 {{ animation-delay: 2.3s; }}
    .pill-3 {{ animation-delay: 2.4s; }}
    .pill-4 {{ animation-delay: 2.5s; }}
    .pill-5 {{ animation-delay: 2.6s; }}
    .pill-6 {{ animation-delay: 2.7s; }}
    .pill-7 {{ animation-delay: 2.8s; }}
    
    .tech-pill:hover {{
      fill-opacity: 0.15;
      stroke: #C50337;
      filter: drop-shadow(0 0 8px rgba(197, 3, 55, 0.5));
    }}

    /* About Me list items fade in */
    .about-item {{ opacity: 0; animation: fade-scale-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards; }}
    .ai-1 {{ animation-delay: 3.0s; }}
    .ai-2 {{ animation-delay: 3.2s; }}
    .ai-3 {{ animation-delay: 3.4s; }}
    .ai-4 {{ animation-delay: 3.6s; }}

    /* Code editor cursor and lines typing */
    .code-line {{ opacity: 0; clip-path: inset(0 100% 0 0); animation: reveal-quote 1.2s steps(40) forwards; }}
    .cl-1 {{ animation-delay: 4.0s; opacity: 1; }}
    .cl-2 {{ animation-delay: 5.2s; opacity: 1; }}
    .cl-3 {{ animation-delay: 6.4s; opacity: 1; }}
    .cl-4 {{ animation-delay: 7.6s; opacity: 1; }}
    .cl-5 {{ animation-delay: 8.8s; opacity: 1; }}
    .cl-6 {{ animation-delay: 10.0s; opacity: 1; }}

    /* Stats loading bars (Replaces CSS variables) */
    @keyframes load-bar-consistency {{
      from {{ width: 0; }}
      to {{ width: 190px; }}
    }}
    @keyframes load-bar-curiosity {{
      from {{ width: 0; }}
      to {{ width: 196px; }}
    }}
    .stat-consistency {{ animation: load-bar-consistency 1.5s cubic-bezier(0.4, 0, 0.2, 1) 3.8s forwards; width: 0; }}
    .stat-curiosity {{ animation: load-bar-curiosity 1.5s cubic-bezier(0.4, 0, 0.2, 1) 3.8s forwards; width: 0; }}

    /* Neon sign flicker animation */
    @keyframes neon-flicker {{
      0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{
        opacity: 1;
        fill: #C50337;
        filter: drop-shadow(0 0 10px rgba(197, 3, 55, 0.8)) drop-shadow(0 0 25px rgba(197, 3, 55, 0.4));
      }}
      20%, 24%, 55% {{
        opacity: 0.3;
        fill: #01081A;
        filter: none;
      }}
    }}
    .neon-text {{
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 2px;
      fill: #C50337;
      filter: drop-shadow(0 0 10px rgba(197, 3, 55, 0.8));
      animation: neon-flicker 5s infinite;
    }}
  </style>

  <g clip-path="url(#banner-corners)">
    <!-- Background -->
    <rect width="1280" height="740" class="bg" />

    <!-- Ambient Glow Orbs -->
    <circle cx="200" cy="200" r="300" fill="#C50337" opacity="0.25" filter="url(#neon-glow)" class="orb-1" />
    <circle cx="1000" cy="500" r="250" fill="#021C4F" opacity="0.2" filter="url(#neon-glow)" class="orb-2" />

    <!-- Twinkling Sparkles (Stars) -->
    <path d="M120 80 L123 90 L133 93 L123 96 L120 106 L117 96 L107 93 L117 90 Z" fill="#C50337" class="star star-delay-1" />
    <path d="M500 60 L502 66 L508 68 L502 70 L500 76 L498 70 L492 68 L498 66 Z" fill="#ffffff" class="star star-delay-2" />
    <path d="M960 70 L962 76 L968 78 L962 80 L960 86 L958 80 L952 78 L958 76 Z" fill="#2E79FF" class="star star-delay-3" />
    <path d="M150 680 L152 686 L158 688 L152 690 L150 696 L148 690 L142 688 L148 686 Z" fill="#ffffff" class="star star-delay-2" />
    <path d="M720 700 L723 710 L733 713 L723 716 L720 726 L717 716 L707 713 L717 710 Z" fill="#C50337" class="star star-delay-1" />

    <!-- Floating code particles -->
    <g class="particle p-1" transform="translate(150, 400)"><text fill="rgba(197, 3, 55, 0.15)" class="text-mono" font-size="28">&lt;/&gt;</text></g>
    <g class="particle p-2" transform="translate(450, 680)"><text fill="rgba(255, 255, 255, 0.12)" class="text-mono" font-size="24">&#123;code&#125;</text></g>
    <g class="particle p-3" transform="translate(300, 550)"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="rgba(46, 121, 255, 0.15)" /></g>
    <g class="particle p-4" transform="translate(900, 450)"><text fill="rgba(197, 3, 55, 0.15)" class="text-sans" font-weight="800" font-size="28">★</text></g>

    <!-- ==================== LEFT COLUMN CONTENT ==================== -->
    
    <!-- 1. Terminal Line -->
    <g transform="translate(670, 50)">
      <text x="0" y="20" class="text-mono" font-size="18" fill="#C50337" font-weight="bold">AbelJonesMathew@dev:~$ <tspan fill="#ffffff">cat </tspan><tspan fill="#2E79FF">README.md</tspan></text>
      <!-- Blinking Cursor -->
      <rect x="420" y="4" width="10" height="18" fill="#2E79FF" class="cursor" />
    </g>

    <!-- 2. Animated Name -->
    <g transform="translate(670, 180)">
      <text x="0" y="0" class="cursive-name">Abel Jones Mathew</text>
    </g>
    
    <!-- 3. Cycling Role Titles -->
    <g transform="translate(670, 215)">
      <text x="0" y="0" class="text-sans role-title role-1">Computer Science Engineering Student</text>
      <text x="0" y="0" class="text-sans role-title role-2">Web Developer</text>
      <text x="0" y="0" class="text-sans role-title role-3">UI/UX Enthusiast</text>
    </g>

    <!-- 4. Glass-morphic Tagline Quote Box -->
    <g transform="translate(670, 245)">
      <rect x="0" y="0" width="550" height="60" rx="12" fill="url(#card-grad)" stroke="url(#border-grad)" stroke-width="1.5" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.3))" />
      <text x="20" y="36" class="text-sans tagline" font-size="16" font-style="italic" fill="#f1f5f9" font-weight="600">"Driven by curiosity. Focused on growth. Building consistently."</text>
    </g>

    <!-- 5. Tech Stack Pills (REFINED POSITION WRAPPING TO PREVENT OVERLAP) -->
    <g transform="translate(670, 335)">
      <!-- HTML -->
      <g transform="translate(0,0)">
        <g class="tech-pill pill-1">
          <rect width="70" height="32" rx="16" fill="rgba(197, 3, 55, 0.07)" stroke="rgba(197, 3, 55, 0.3)" stroke-width="1" />
          <text x="35" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">HTML</text>
        </g>
      </g>
      <!-- CSS -->
      <g transform="translate(80,0)">
        <g class="tech-pill pill-2">
          <rect width="65" height="32" rx="16" fill="rgba(46, 121, 255, 0.07)" stroke="rgba(46, 121, 255, 0.3)" stroke-width="1" />
          <text x="32.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#2E79FF" text-anchor="middle">CSS</text>
        </g>
      </g>
      <!-- JavaScript -->
      <g transform="translate(155,0)">
        <g class="tech-pill pill-3">
          <rect width="105" height="32" rx="16" fill="rgba(255, 93, 130, 0.07)" stroke="rgba(255, 93, 130, 0.3)" stroke-width="1" />
          <text x="52.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#FF5D82" text-anchor="middle">JavaScript</text>
        </g>
      </g>
      <!-- Python -->
      <g transform="translate(270,0)">
        <g class="tech-pill pill-4">
          <rect width="80" height="32" rx="16" fill="rgba(197, 3, 55, 0.07)" stroke="rgba(197, 3, 55, 0.3)" stroke-width="1" />
          <text x="40" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">Python</text>
        </g>
      </g>
      <!-- C -->
      <g transform="translate(360,0)">
        <g class="tech-pill pill-5">
          <rect width="50" height="32" rx="16" fill="rgba(46, 121, 255, 0.07)" stroke="rgba(46, 121, 255, 0.3)" stroke-width="1" />
          <text x="25" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#2E79FF" text-anchor="middle">C</text>
        </g>
      </g>
      <!-- C++ -->
      <g transform="translate(420,0)">
        <g class="tech-pill pill-6">
          <rect width="65" height="32" rx="16" fill="rgba(255, 93, 130, 0.07)" stroke="rgba(255, 93, 130, 0.3)" stroke-width="1" />
          <text x="32.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#FF5D82" text-anchor="middle">C++</text>
        </g>
      </g>
      <!-- Figma -->
      <g transform="translate(495,0)">
        <g class="tech-pill pill-7">
          <rect width="75" height="32" rx="16" fill="rgba(197, 3, 55, 0.07)" stroke="rgba(197, 3, 55, 0.3)" stroke-width="1" />
          <text x="37.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">Figma</text>
        </g>
      </g>
    </g>

    <!-- 6. About Me Bullets (REFINED POSITION WRAPPING TO PREVENT OVERLAP) -->
    <g transform="translate(670, 395)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <g class="about-item ai-1">
          <circle cx="10" cy="-6" r="4" fill="#C50337" filter="url(#glow)" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#cbd5e1" font-weight="600">🎓 CS Engineering Student at SJCET</text>
        </g>
      </g>
      <!-- Item 2 -->
      <g transform="translate(0, 30)">
        <g class="about-item ai-2">
          <circle cx="10" cy="-6" r="4" fill="#2E79FF" filter="url(#glow)" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#cbd5e1" font-weight="600">💻 Building modern, interactive web applications</text>
        </g>
      </g>
      <!-- Item 3 -->
      <g transform="translate(0, 60)">
        <g class="about-item ai-3">
          <circle cx="10" cy="-6" r="4" fill="#FF5D82" filter="url(#glow)" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#cbd5e1" font-weight="600">🎨 Crafting beautiful and intuitive UI/UX layouts</text>
        </g>
      </g>
      <!-- Item 4 -->
      <g transform="translate(0, 90)">
        <g class="about-item ai-4">
          <circle cx="10" cy="-6" r="4" fill="#C50337" filter="url(#glow)" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#cbd5e1" font-weight="600">🚀 Passionate about open source contributions and consistent growth</text>
        </g>
      </g>
    </g>

    <!-- 7. Animated Profile Stats Loading Bars -->
    <g transform="translate(670, 520)">
      <!-- Line 1: Coding Consistency -->
      <g>
        <text x="0" y="15" class="text-sans" font-size="12" fill="#94a3b8" font-weight="bold" letter-spacing="1">CONSISTENCY</text>
        <rect x="130" y="5" width="200" height="8" rx="4" fill="rgba(255,255,255,0.05)" />
        <rect x="130" y="5" height="8" rx="4" fill="#C50337" class="stat-consistency" filter="url(#glow)" />
        <text x="345" y="15" class="text-mono" font-size="12" fill="#C50337" font-weight="bold">95%</text>
      </g>
      
      <!-- Line 2: Innovation/Curiosity -->
      <g transform="translate(0, 25)">
        <text x="0" y="15" class="text-sans" font-size="12" fill="#94a3b8" font-weight="bold" letter-spacing="1">CURIOSITY</text>
        <rect x="130" y="5" width="200" height="8" rx="4" fill="rgba(255,255,255,0.05)" />
        <rect x="130" y="5" height="8" rx="4" fill="#2E79FF" class="stat-curiosity" filter="url(#glow)" />
        <text x="345" y="15" class="text-mono" font-size="12" fill="#2E79FF" font-weight="bold">98%</text>
      </g>
    </g>

    <!-- 8. Code Editor snippet buildDreams() -->
    <g transform="translate(670, 580)">
      <!-- Glass code-editor frame -->
      <rect x="0" y="0" width="550" height="120" rx="10" fill="#01081A" stroke="url(#border-grad)" stroke-width="1.2" />
      <!-- Color dot window controls -->
      <circle cx="18" cy="14" r="5" fill="#ff5f56" />
      <circle cx="34" cy="14" r="5" fill="#ffbd2e" />
      <circle cx="50" cy="14" r="5" fill="#27c93f" />
      
      <!-- Code text -->
      <g transform="translate(20, 38)" class="text-mono" font-size="12" font-weight="bold">
        <text class="code-line cl-1" x="0" y="0"><tspan fill="#C50337">const </tspan><tspan fill="#FF5D82">buildDreams</tspan><tspan fill="#ffffff"> = () =&gt; &#123;</tspan></text>
        <text class="code-line cl-2" x="20" y="18"><tspan fill="#C50337">const </tspan><tspan fill="#ffffff">code = write();</tspan></text>
        <text class="code-line cl-3" x="20" y="36"><tspan fill="#C50337">const </tspan><tspan fill="#ffffff">coffee = consume();</tspan></text>
        <text class="code-line cl-4" x="20" y="54"><tspan fill="#2E79FF">return </tspan><tspan fill="#ffffff">code + coffee;</tspan></text>
        <text class="code-line cl-5" x="0" y="72"><tspan fill="#ffffff">&#125;;</tspan></text>
      </g>
    </g>

    <!-- 9. Neon Sign "KEEP CODING KEEP GROWING" -->
    <g transform="translate(670, 715)">
      <text class="text-sans neon-text" x="0" y="0">KEEP CODING KEEP GROWING</text>
    </g>

    <!-- ==================== RIGHT COLUMN CONTENT (Hologram Character) ==================== -->
    
    <!-- Hologram Reveal group -->
    <g clip-path="url(#hologram-reveal)" transform="translate(60, 70)">
      <!-- Ambient backing glow -->
      <ellipse cx="240" cy="300" rx="160" ry="240" fill="#021C4F" opacity="0.1" filter="url(#neon-glow)" />
      
      <!-- Character Image base64 -->
      <image href="data:image/png;base64,{char_b64}" x="0" y="0" width="460" height="613" />
      
      <!-- Hologram horizontal scanner sweep lines -->
      <rect x="0" y="0" width="460" height="613" fill="url(#hologram-grad)" opacity="0.15" style="mix-blend-mode: overlay;" />
      
      <!-- Loop scan line -->
      <line class="scan-line" x1="-20" y1="0" x2="480" y2="0" stroke="#C50337" stroke-width="3" filter="url(#glow)" />
      <line class="scan-line" x1="-20" y1="-8" x2="480" y2="-8" stroke="#2E79FF" stroke-width="1.5" opacity="0.7" />
    </g>
    
    <!-- One-time scan line running on top-level overlay -->
    <g transform="translate(60, 70)">
      <line class="one-time-line" x1="-20" y1="0" x2="480" y2="0" stroke="#FF5D82" stroke-width="4.5" filter="url(#glow)" />
    </g>

  </g>
</svg>"""

    with open("banner.svg", "w", encoding="utf-8") as f:
        f.write(banner_dark_svg)
    print("banner.svg successfully generated.")


    # 2. CREATE banner-light.svg (Light Mode Cosmic Lavender/Pink)
    banner_light_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 740" width="1280" height="740">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bg-grad-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="60%" stop-color="#F5EAED" />
      <stop offset="100%" stop-color="#FF5D82" stop-opacity="0.15" />
    </linearGradient>
    
    <!-- Neon Purple to Blue Gradient for Name -->
    <linearGradient id="neon-grad-light" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C50337" />
      <stop offset="50%" stop-color="#021C4F" />
      <stop offset="100%" stop-color="#2E79FF" />
    </linearGradient>

    <!-- Hologram Scanner Gradient -->
    <linearGradient id="hologram-grad-light" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0" />
      <stop offset="90%" stop-color="#C50337" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#C50337" stop-opacity="0.6" />
    </linearGradient>
    
    <!-- Soft Glow Filter -->
    <filter id="glow-light" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Card Inner Glass-morphism Gradient -->
    <linearGradient id="card-grad-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.01" />
    </linearGradient>
    
    <!-- Card Border Gradient -->
    <linearGradient id="border-grad-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.1" />
    </linearGradient>
    
    <!-- One-time Reveal Clip Path -->
    <clipPath id="hologram-reveal-light">
      <rect x="0" y="0" width="1280" height="0">
        <animate attributeName="height" values="0;740" dur="2s" begin="0.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" />
      </rect>
    </clipPath>

    <!-- General Clip Path for the rounded corners -->
    <clipPath id="banner-corners-light">
      <rect x="0" y="0" width="1280" height="740" rx="24" ry="24" />
    </clipPath>
  </defs>

  <style>
    /* Global Styles */
    .bg-light {{ fill: url(#bg-grad-light); }}
    .text-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .text-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    
    /* Ambient Orbs Animation */
    @keyframes pulse-orb-light {{
      0%, 100% {{ transform: scale(1) translate(0, 0); opacity: 0.15; }}
      50% {{ transform: scale(1.15) translate(30px, -20px); opacity: 0.25; }}
    }}
    .orb-1-light {{ animation: pulse-orb-light 15s ease-in-out infinite; transform-origin: 200px 200px; }}
    .orb-2-light {{ animation: pulse-orb-light 18s ease-in-out infinite alternate; transform-origin: 1000px 500px; }}

    /* Stars and Sparkles */
    @keyframes twinkle-light {{
      0%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
      50% {{ opacity: 0.8; transform: scale(1.2); }}
    }}
    .star-light {{ animation: twinkle-light 3s infinite; transform-origin: center; }}
    .star-delay-1 {{ animation-delay: 0.7s; }}
    .star-delay-2 {{ animation-delay: 1.4s; }}
    .star-delay-3 {{ animation-delay: 2.1s; }}
    
    /* Floating Particles */
    @keyframes float-up-light {{
      0% {{ transform: translateY(100px) translateX(0) scale(0.8); opacity: 0; }}
      10% {{ opacity: 0.4; }}
      90% {{ opacity: 0.4; }}
      100% {{ transform: translateY(-400px) translateX(30px) scale(1.1); opacity: 0; }}
    }}
    .particle-light {{ animation: float-up-light 8s linear infinite; }}
    .p-1 {{ animation-delay: 0s; left: 100px; }}
    .p-2 {{ animation-delay: 2s; left: 400px; }}
    .p-3 {{ animation-delay: 4.5s; left: 250px; }}
    .p-4 {{ animation-delay: 6s; left: 950px; }}

    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&amp;display=swap');

    @keyframes draw-name {{
      0% {{ stroke-dashoffset: 600; fill-opacity: 0; }}
      70% {{ stroke-dashoffset: 0; fill-opacity: 0; }}
      100% {{ stroke-dashoffset: 0; fill-opacity: 1; }}
    }}
    .cursive-name-light {{
      font-family: 'Dancing Script', 'Brush Script MT', 'Lucida Handwriting', 'Segoe Script', cursive;
      font-size: 60px;
      font-weight: 700;
      fill: url(#neon-grad-light);
      stroke: #C50337;
      stroke-width: 1.5;
      stroke-dasharray: 600;
      stroke-dashoffset: 600;
      animation: draw-name 2.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }}

    /* Terminal Blinking Cursor */
    @keyframes blink-light {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    .cursor-light {{ animation: blink-light 1s infinite; }}

    /* Cycling Typed Role Titles (0s to 12s) */
    .role-title-light {{ opacity: 0; font-size: 20px; font-weight: 700; fill: #C50337; }}
    .role-1 {{ animation: cycle-role-1 12s infinite; }}
    .role-2 {{ animation: cycle-role-2 12s infinite; }}
    .role-3 {{ animation: cycle-role-3 12s infinite; }}
    
    @keyframes cycle-role-1 {{
      0% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      2% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      12%, 30% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      32% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}
    @keyframes cycle-role-2 {{
      0%, 33.3% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      35.3% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      45.3%, 63.3% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      65.3% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}
    @keyframes cycle-role-3 {{
      0%, 66.6% {{ opacity: 0; clip-path: inset(0 100% 0 0); }}
      68.6% {{ opacity: 1; clip-path: inset(0 100% 0 0); }}
      78.6%, 96.6% {{ opacity: 1; clip-path: inset(0 0% 0 0); }}
      98.6% {{ opacity: 0; clip-path: inset(0 0% 0 0); }}
    }}

    /* Tagline Reveal */
    @keyframes reveal-quote {{
      0% {{ clip-path: inset(0 100% 0 0); }}
      100% {{ clip-path: inset(0 0 0 0); }}
    }}
    .tagline-light {{ animation: reveal-quote 2.5s cubic-bezier(0.4, 0, 0.2, 1) 2.0s forwards; clip-path: inset(0 100% 0 0); }}

    /* Hologram Scan Sweep Line and Effect */
    @keyframes hologram-sweep-light {{
      0% {{ transform: translateY(-50px); opacity: 0; }}
      5% {{ opacity: 1; }}
      95% {{ opacity: 1; }}
      100% {{ transform: translateY(780px); opacity: 0; }}
    }}
    .scan-line-light {{ animation: hologram-sweep-light 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite; }}
    
    @keyframes one-time-reveal-line-light {{
      0% {{ transform: translateY(-50px); opacity: 1; }}
      99% {{ transform: translateY(740px); opacity: 1; }}
      100% {{ transform: translateY(740px); opacity: 0; }}
    }}
    .one-time-line-light {{ animation: one-time-reveal-line-light 2s cubic-bezier(0.4, 0, 0.2, 1) 0.5s forwards; }}

    /* Tech Stack Pills */
    @keyframes fade-scale-in {{
      0% {{ opacity: 0; transform: scale(0.95); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .tech-pill-light {{ opacity: 0; animation: fade-scale-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; transition: all 0.3s ease; cursor: pointer; }}
    .pill-1 {{ animation-delay: 2.2s; }}
    .pill-2 {{ animation-delay: 2.3s; }}
    .pill-3 {{ animation-delay: 2.4s; }}
    .pill-4 {{ animation-delay: 2.5s; }}
    .pill-5 {{ animation-delay: 2.6s; }}
    .pill-6 {{ animation-delay: 2.7s; }}
    .pill-7 {{ animation-delay: 2.8s; }}
    
    .tech-pill-light:hover {{
      fill-opacity: 0.15;
      stroke: #C50337;
      filter: drop-shadow(0 0 6px rgba(197, 3, 55, 0.3));
    }}

    /* About Me lines */
    .about-item-light {{ opacity: 0; animation: fade-scale-in 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards; }}
    .ai-1 {{ animation-delay: 3.0s; }}
    .ai-2 {{ animation-delay: 3.2s; }}
    .ai-3 {{ animation-delay: 3.4s; }}
    .ai-4 {{ animation-delay: 3.6s; }}

    /* Code editor lines */
    .code-line-light {{ opacity: 0; clip-path: inset(0 100% 0 0); animation: reveal-quote 1.2s steps(40) forwards; }}
    .cl-1 {{ animation-delay: 4.0s; opacity: 1; }}
    .cl-2 {{ animation-delay: 5.2s; opacity: 1; }}
    .cl-3 {{ animation-delay: 6.4s; opacity: 1; }}
    .cl-4 {{ animation-delay: 7.6s; opacity: 1; }}
    .cl-5 {{ animation-delay: 8.8s; opacity: 1; }}
    .cl-6 {{ animation-delay: 10.0s; opacity: 1; }}

    /* Stats Loading Bars (Replaces CSS variables) */
    @keyframes load-bar-consistency-light {{
      from {{ width: 0; }}
      to {{ width: 190px; }}
    }}
    @keyframes load-bar-curiosity-light {{
      from {{ width: 0; }}
      to {{ width: 196px; }}
    }}
    .stat-consistency-light {{ animation: load-bar-consistency-light 1.5s cubic-bezier(0.4, 0, 0.2, 1) 3.8s forwards; width: 0; }}
    .stat-curiosity-light {{ animation: load-bar-curiosity-light 1.5s cubic-bezier(0.4, 0, 0.2, 1) 3.8s forwards; width: 0; }}

    /* Neon Sign Flicker (Light Mode) */
    @keyframes neon-flicker-light {{
      0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {{
        opacity: 1;
        fill: #C50337;
        filter: drop-shadow(0 0 6px rgba(197, 3, 55, 0.4));
      }}
      20%, 24%, 55% {{
        opacity: 0.3;
        fill: #F5EAED;
        filter: none;
      }}
    }}
    .neon-text-light {{
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 2px;
      fill: #C50337;
      filter: drop-shadow(0 0 6px rgba(197, 3, 55, 0.4));
      animation: neon-flicker-light 5s infinite;
    }}
  </style>

  <g clip-path="url(#banner-corners-light)">
    <!-- Background -->
    <rect width="1280" height="740" class="bg-light" />

    <!-- Ambient Glow Orbs -->
    <circle cx="200" cy="200" r="300" fill="#FBF2F4" opacity="0.4" class="orb-1-light" />
    <circle cx="1000" cy="500" r="250" fill="#F0F4FA" opacity="0.4" class="orb-2-light" />

    <!-- Twinkling Sparkles -->
    <path d="M120 80 L123 90 L133 93 L123 96 L120 106 L117 96 L107 93 L117 90 Z" fill="#C50337" class="star-light star-delay-1" />
    <path d="M500 60 L502 66 L508 68 L502 70 L500 76 L498 70 L492 68 L498 66 Z" fill="#021C4F" class="star-light star-delay-2" />
    <path d="M960 70 L962 76 L968 78 L962 80 L960 86 L958 80 L952 78 L958 76 Z" fill="#5e021a" class="star-light star-delay-3" />
    <path d="M150 680 L152 686 L158 688 L152 690 L150 696 L148 690 L142 688 L148 686 Z" fill="#021C4F" class="star-light star-delay-2" />
    <path d="M720 700 L723 710 L733 713 L723 716 L720 726 L717 716 L707 713 L717 710 Z" fill="#C50337" class="star-light star-delay-1" />

    <!-- Floating code particles -->
    <g class="particle-light p-1" transform="translate(150, 400)"><text fill="rgba(197, 3, 55, 0.12)" class="text-mono" font-size="28">&lt;/&gt;</text></g>
    <g class="particle-light p-2" transform="translate(450, 680)"><text fill="rgba(2, 28, 79, 0.1)" class="text-mono" font-size="24">&#123;code&#125;</text></g>
    <g class="particle-light p-3" transform="translate(300, 550)"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="rgba(255, 93, 130, 0.1)" /></g>
    <g class="particle-light p-4" transform="translate(900, 450)"><text fill="rgba(197, 3, 55, 0.12)" class="text-sans" font-weight="800" font-size="28">★</text></g>

    <!-- ==================== LEFT COLUMN CONTENT ==================== -->
    
    <!-- 1. Terminal Line -->
    <g transform="translate(670, 50)">
      <text x="0" y="20" class="text-mono" font-size="18" fill="#C50337" font-weight="bold">AbelJonesMathew@dev:~$ <tspan fill="#1e293b">cat </tspan><tspan fill="#C50337">README.md</tspan></text>
      <!-- Blinking Cursor -->
      <rect x="420" y="4" width="10" height="18" fill="#C50337" class="cursor-light" />
    </g>

    <!-- 2. Animated Name -->
    <g transform="translate(670, 180)">
      <text x="0" y="0" class="cursive-name-light">Abel Jones Mathew</text>
    </g>
    
    <!-- 3. Cycling Role Titles -->
    <g transform="translate(670, 215)">
      <text x="0" y="0" class="text-sans role-title-light role-1">Computer Science Engineering Student</text>
      <text x="0" y="0" class="text-sans role-title-light role-2">Web Developer</text>
      <text x="0" y="0" class="text-sans role-title-light role-3">UI/UX Enthusiast</text>
    </g>

    <!-- 4. Glass-morphic Tagline Quote Box -->
    <g transform="translate(670, 245)">
      <rect x="0" y="0" width="550" height="60" rx="12" fill="url(#card-grad-light)" stroke="url(#border-grad-light)" stroke-width="1.5" filter="drop-shadow(0 4px 8px rgba(15, 23, 42, 0.05))" />
      <text x="20" y="36" class="text-sans tagline-light" font-size="16" font-style="italic" fill="#1e1b4b" font-weight="600">"Driven by curiosity. Focused on growth. Building consistently."</text>
    </g>

    <!-- 5. Tech Stack Pills (REFINED POSITION WRAPPING TO PREVENT OVERLAP) -->
    <g transform="translate(670, 335)">
      <!-- HTML -->
      <g transform="translate(0,0)">
        <g class="tech-pill-light pill-1">
          <rect width="70" height="32" rx="16" fill="rgba(197, 3, 55, 0.04)" stroke="rgba(197, 3, 55, 0.25)" stroke-width="1" />
          <text x="35" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">HTML</text>
        </g>
      </g>
      <!-- CSS -->
      <g transform="translate(80,0)">
        <g class="tech-pill-light pill-2">
          <rect width="65" height="32" rx="16" fill="rgba(2, 28, 79, 0.04)" stroke="rgba(2, 28, 79, 0.25)" stroke-width="1" />
          <text x="32.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#021C4F" text-anchor="middle">CSS</text>
        </g>
      </g>
      <!-- JavaScript -->
      <g transform="translate(155,0)">
        <g class="tech-pill-light pill-3">
          <rect width="105" height="32" rx="16" fill="rgba(255, 93, 130, 0.04)" stroke="rgba(255, 93, 130, 0.25)" stroke-width="1" />
          <text x="52.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#FF5D82" text-anchor="middle">JavaScript</text>
        </g>
      </g>
      <!-- Python -->
      <g transform="translate(270,0)">
        <g class="tech-pill-light pill-4">
          <rect width="80" height="32" rx="16" fill="rgba(197, 3, 55, 0.04)" stroke="rgba(197, 3, 55, 0.25)" stroke-width="1" />
          <text x="40" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">Python</text>
        </g>
      </g>
      <!-- C -->
      <g transform="translate(360,0)">
        <g class="tech-pill-light pill-5">
          <rect width="50" height="32" rx="16" fill="rgba(2, 28, 79, 0.04)" stroke="rgba(2, 28, 79, 0.25)" stroke-width="1" />
          <text x="25" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#021C4F" text-anchor="middle">C</text>
        </g>
      </g>
      <!-- C++ -->
      <g transform="translate(420,0)">
        <g class="tech-pill-light pill-6">
          <rect width="65" height="32" rx="16" fill="rgba(255, 93, 130, 0.04)" stroke="rgba(255, 93, 130, 0.25)" stroke-width="1" />
          <text x="32.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#FF5D82" text-anchor="middle">C++</text>
        </g>
      </g>
      <!-- Figma -->
      <g transform="translate(495,0)">
        <g class="tech-pill-light pill-7">
          <rect width="75" height="32" rx="16" fill="rgba(197, 3, 55, 0.04)" stroke="rgba(197, 3, 55, 0.25)" stroke-width="1" />
          <text x="37.5" y="20" class="text-sans" font-size="13" font-weight="bold" fill="#C50337" text-anchor="middle">Figma</text>
        </g>
      </g>
    </g>

    <!-- 6. About Me Bullets (REFINED POSITION WRAPPING TO PREVENT OVERLAP) -->
    <g transform="translate(670, 395)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <g class="about-item-light ai-1">
          <circle cx="10" cy="-6" r="4" fill="#C50337" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#1e1b4b" font-weight="600">🎓 CS Engineering Student at SJCET</text>
        </g>
      </g>
      <!-- Item 2 -->
      <g transform="translate(0, 30)">
        <g class="about-item-light ai-2">
          <circle cx="10" cy="-6" r="4" fill="#021C4F" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#1e1b4b" font-weight="600">💻 Building modern, interactive web applications</text>
        </g>
      </g>
      <!-- Item 3 -->
      <g transform="translate(0, 60)">
        <g class="about-item-light ai-3">
          <circle cx="10" cy="-6" r="4" fill="#FF5D82" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#1e1b4b" font-weight="600">🎨 Crafting beautiful and intuitive UI/UX layouts</text>
        </g>
      </g>
      <!-- Item 4 -->
      <g transform="translate(0, 90)">
        <g class="about-item-light ai-4">
          <circle cx="10" cy="-6" r="4" fill="#C50337" />
          <text x="25" y="0" class="text-sans" font-size="15" fill="#1e1b4b" font-weight="600">🚀 Passionate about open source contributions and consistent growth</text>
        </g>
      </g>
    </g>

    <!-- 7. Profile Stats Loading Bars -->
    <g transform="translate(670, 520)">
      <!-- Line 1: Coding Consistency -->
      <g>
        <text x="0" y="15" class="text-sans" font-size="12" fill="#475569" font-weight="bold" letter-spacing="1">CONSISTENCY</text>
        <rect x="130" y="5" width="200" height="8" rx="4" fill="rgba(15, 23, 42, 0.06)" />
        <rect x="130" y="5" height="8" rx="4" fill="#C50337" class="stat-consistency-light" filter="url(#glow-light)" />
        <text x="345" y="15" class="text-mono" font-size="12" fill="#C50337" font-weight="bold">95%</text>
      </g>
      
      <!-- Line 2: Innovation/Curiosity -->
      <g transform="translate(0, 25)">
        <text x="0" y="15" class="text-sans" font-size="12" fill="#475569" font-weight="bold" letter-spacing="1">CURIOSITY</text>
        <rect x="130" y="5" width="200" height="8" rx="4" fill="rgba(15, 23, 42, 0.06)" />
        <rect x="130" y="5" height="8" rx="4" fill="#021C4F" class="stat-curiosity-light" filter="url(#glow-light)" />
        <text x="345" y="15" class="text-mono" font-size="12" fill="#021C4F" font-weight="bold">98%</text>
      </g>
    </g>

    <!-- 8. Code Editor snippet buildDreams() -->
    <g transform="translate(670, 580)">
      <rect x="0" y="0" width="550" height="120" rx="10" fill="#FAF5F6" stroke="url(#border-grad-light)" stroke-width="1.2" />
      <!-- Color dot controls -->
      <circle cx="18" cy="14" r="5" fill="#ff5f56" />
      <circle cx="34" cy="14" r="5" fill="#ffbd2e" />
      <circle cx="50" cy="14" r="5" fill="#27c93f" />
      
      <!-- Code text -->
      <g transform="translate(20, 38)" class="text-mono" font-size="12" font-weight="bold">
        <text class="code-line-light cl-1" x="0" y="0"><tspan fill="#C50337">const </tspan><tspan fill="#FF5D82">buildDreams</tspan><tspan fill="#1e1b4b"> = () =&gt; &#123;</tspan></text>
        <text class="code-line-light cl-2" x="20" y="18"><tspan fill="#C50337">const </tspan><tspan fill="#1e1b4b">code = write();</tspan></text>
        <text class="code-line-light cl-3" x="20" y="36"><tspan fill="#C50337">const </tspan><tspan fill="#1e1b4b">coffee = consume();</tspan></text>
        <text class="code-line-light cl-4" x="20" y="54"><tspan fill="#021C4F">return </tspan><tspan fill="#1e1b4b">code + coffee;</tspan></text>
        <text class="code-line-light cl-5" x="0" y="72"><tspan fill="#1e1b4b">&#125;;</tspan></text>
      </g>
    </g>

    <!-- 9. Neon Sign "KEEP CODING KEEP GROWING" -->
    <g transform="translate(670, 715)">
      <text class="text-sans neon-text-light" x="0" y="0">KEEP CODING KEEP GROWING</text>
    </g>

    <!-- ==================== RIGHT COLUMN CONTENT (Hologram Character) ==================== -->
    
    <!-- Hologram Reveal group -->
    <g clip-path="url(#hologram-reveal-light)" transform="translate(60, 70)">
      <!-- Soft backing glow -->
      <ellipse cx="240" cy="300" rx="160" ry="240" fill="#FBF2F4" opacity="0.35" />
      
      <!-- Character Image -->
      <image href="data:image/png;base64,{char_b64}" x="0" y="0" width="460" height="613" />
      
      <!-- Continuous horizontal scanner lines -->
      <rect x="0" y="0" width="460" height="613" fill="url(#hologram-grad-light)" opacity="0.1" style="mix-blend-mode: overlay;" />
      
      <!-- Loop scan line -->
      <line class="scan-line-light" x1="-20" y1="0" x2="480" y2="0" stroke="#C50337" stroke-width="2.5" filter="url(#glow-light)" />
      <line class="scan-line-light" x1="-20" y1="-8" x2="480" y2="-8" stroke="#021C4F" stroke-width="1.2" opacity="0.5" />
    </g>
    
    <!-- One-time scan line running on top-level overlay -->
    <g transform="translate(60, 70)">
      <line class="one-time-line-light" x1="-20" y1="0" x2="480" y2="0" stroke="#C50337" stroke-width="4" filter="url(#glow-light)" />
    </g>

  </g>
</svg>"""

    with open("banner-light.svg", "w", encoding="utf-8") as f:
        f.write(banner_light_svg)
    print("banner-light.svg successfully generated.")


    # 3. CREATE lanyard.svg (ID badge swinging style Cosmic Amethyst/Rose/Indigo)
    lanyard_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 560" width="340" height="560">
  <defs>
    <!-- Strap Purple/Blue/DeepBlue Gradient -->
    <linearGradient id="strap-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C50337" />
      <stop offset="50%" stop-color="#2E79FF" />
      <stop offset="100%" stop-color="#021C4F" />
    </linearGradient>

    <!-- Metal Clasp Gradients -->
    <linearGradient id="metal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e2e8f0" />
      <stop offset="50%" stop-color="#94a3b8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
    
    <linearGradient id="metal-highlight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8" />
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.4" />
    </linearGradient>

    <!-- Badge Glass Gradient (Ultramarine base) -->
    <linearGradient id="badge-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#021C4F" stop-opacity="0.95" />
    </linearGradient>
    
    <!-- Badge Highlight/Inner Border Gradient -->
    <linearGradient id="badge-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF5D82" stop-opacity="0.6" />
      <stop offset="50%" stop-color="#C50337" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.5" />
    </linearGradient>

    <!-- Holographic Sweep Gradient -->
    <linearGradient id="holo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF5D82" stop-opacity="0" />
      <stop offset="45%" stop-color="#FF5D82" stop-opacity="0" />
      <stop offset="50%" stop-color="#C50337" stop-opacity="0.3" />
      <stop offset="52%" stop-color="#2E79FF" stop-opacity="0.3" />
      <stop offset="55%" stop-color="#C50337" stop-opacity="0.2" />
      <stop offset="60%" stop-color="#FF5D82" stop-opacity="0" />
      <stop offset="100%" stop-color="#FF5D82" stop-opacity="0" />
    </linearGradient>
    
    <!-- Soft Glow Filter -->
    <filter id="lanyard-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <clipPath id="avatar-clip">
      <circle cx="170" cy="245" r="50" />
    </clipPath>
  </defs>

  <style>
    .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    
    /* 1. DROP-IN and DAMPED SWING (Outer group) */
    @keyframes drop-swing {{
      0% {{ transform: rotate(-55deg); }}
      12% {{ transform: rotate(38deg); }}
      24% {{ transform: rotate(-24deg); }}
      36% {{ transform: rotate(15deg); }}
      48% {{ transform: rotate(-9deg); }}
      60% {{ transform: rotate(5deg); }}
      72% {{ transform: rotate(-3deg); }}
      84% {{ transform: rotate(1.5deg); }}
      96% {{ transform: rotate(-0.5deg); }}
      100% {{ transform: rotate(0deg); }}
    }}
    .swing-group {{
      animation: drop-swing 4.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1;
      transform-origin: 170px 0px;
    }}

    /* 2. INFINITE GENTLE SWAY (Inner group) */
    @keyframes gentle-sway {{
      0% {{ transform: rotate(-1.5deg); }}
      100% {{ transform: rotate(1.5deg); }}
    }}
    .sway-group {{
      animation: gentle-sway 5s ease-in-out infinite alternate;
      animation-delay: 4.5s;
      transform-origin: 170px 0px;
    }}

    /* Holographic shine sweep on the badge */
    @keyframes holo-sweep {{
      0% {{ transform: translate(-300px, -300px); }}
      25% {{ transform: translate(300px, 300px); }}
      100% {{ transform: translate(300px, 300px); }}
    }}
    .holo-overlay {{
      animation: holo-sweep 5s ease-in-out infinite;
    }}
    
    /* Avatar glowing circle pulse */
    @keyframes pulse-ring {{
      0%, 100% {{ r: 52; opacity: 0.7; }}
      50% {{ r: 55; opacity: 1; }}
    }}
    .avatar-ring {{
      animation: pulse-ring 3s ease-in-out infinite;
      transform-origin: 170px 245px;
    }}
  </style>

  <g class="swing-group">
    <g class="sway-group">
      
      <!-- Lanyard Strap (Teal/Emerald Canvas) -->
      <path d="M162 0 L158 135 L168 135 L172 0 Z" fill="url(#strap-grad)" />
      <path d="M178 0 L182 135 L172 135 L168 0 Z" fill="url(#strap-grad)" opacity="0.9" />
      
      <path d="M163 15 L164 35" stroke="#ffffff" stroke-width="2" stroke-dasharray="1,3" />
      <path d="M177 25 L176 45" stroke="#ffffff" stroke-width="2" stroke-dasharray="1,3" />
      
      <rect x="156" y="115" width="28" height="6" rx="3" fill="#1e293b" />
      
      <!-- Keyring & Clasp -->
      <circle cx="170" cy="132" r="10" fill="none" stroke="url(#metal-grad)" stroke-width="3" />
      <circle cx="170" cy="132" r="10" fill="none" stroke="url(#metal-highlight)" stroke-width="3" />
      
      <path d="M165 140 L175 140 L173 158 L167 158 Z" fill="url(#metal-grad)" />
      <circle cx="170" cy="143" r="3" fill="#475569" />
      <path d="M168 158 A 4 4 0 0 0 172 158 L170 165 Z" fill="url(#metal-grad)" stroke="#1e293b" stroke-width="0.5" />
      
      <!-- Glass Badge Card -->
      <g transform="translate(50, 165)">
        <rect width="240" height="330" rx="16" fill="rgba(0,0,0,0.5)" filter="url(#lanyard-glow)" opacity="0.6" />
        <rect width="240" height="330" rx="16" fill="url(#badge-grad)" stroke="url(#badge-border)" stroke-width="2" />
        <path d="M 0 16 A 16 16 0 0 1 16 0 L 224 0 A 16 16 0 0 1 240 16 L 240 35 L 0 35 Z" fill="rgba(197, 3, 55, 0.1)" />
        <line x1="0" y1="35" x2="240" y2="35" stroke="#C50337" stroke-width="1.2" opacity="0.6" />
        
        <rect x="100" y="8" width="40" height="6" rx="3" fill="#01081A" stroke="rgba(197,3,55,0.4)" stroke-width="0.8" />
        
        <!-- Glowing ring -->
        <circle cx="120" cy="80" r="53" fill="none" stroke="#2E79FF" stroke-width="2" opacity="0.5" />
        <circle cx="120" cy="80" r="52" fill="none" stroke="#C50337" stroke-width="2" class="avatar-ring" filter="url(#lanyard-glow)" />
        
        <!-- Avatar Base64 Image -->
        <g clip-path="url(#avatar-clip)" transform="translate(-50, -165)">
          <rect x="115" y="190" width="110" height="110" fill="#01081A" />
          <image href="data:image/png;base64,{face_b64}" x="120" y="195" width="100" height="100" />
        </g>
        
        <!-- Details -->
        <text x="120" y="165" font-size="18" font-weight="900" fill="#ffffff" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" text-anchor="middle" letter-spacing="0.5">Abel Jones Mathew</text>
        
        <g transform="translate(40, 180)">
          <rect width="160" height="22" rx="11" fill="rgba(197, 3, 55, 0.1)" stroke="rgba(197, 3, 55, 0.3)" stroke-width="1" />
          <text x="80" y="15" font-size="11" font-weight="bold" fill="#C50337" class="font-sans" text-anchor="middle">CS ENGINEERING STUDENT</text>
        </g>
        
        <g transform="translate(30, 222)" class="font-sans" font-size="11" font-weight="bold">
          <text x="0" y="0" fill="#2E79FF" opacity="0.8">GITHUB</text>
          <text x="180" y="0" fill="#ffffff" text-anchor="end">AbelJonesMathew</text>
          
          <text x="0" y="20" fill="#2E79FF" opacity="0.8">ROLE</text>
          <text x="180" y="20" fill="#ffffff" text-anchor="end">Web Developer</text>
  
          <text x="0" y="40" fill="#2E79FF" opacity="0.8">EMAIL</text>
          <text x="180" y="40" fill="#ffffff" text-anchor="end" font-size="9.5">abeljonesmathew@gmail.com</text>
        </g>
        
        <g transform="translate(30, 288)">
          <rect x="0" y="0" width="180" height="22" fill="none" />
          <path d="M0 0 H180" stroke="none" />
          <path d="M5 0 V16 M9 0 V16 M12 0 V16 M18 0 V16 M20 0 V16 M26 0 V16 M32 0 V16 M35 0 V16 M41 0 V16 M44 0 V16 M50 0 V16 M53 0 V16 M56 0 V16 M62 0 V16 M68 0 V16 M71 0 V16 M77 0 V16 M83 0 V16 M86 0 V16 M92 0 V16 M95 0 V16 M98 0 V16 M104 0 V16 M110 0 V16 M113 0 V16 M119 0 V16 M125 0 V16 M128 0 V16 M134 0 V16 M137 0 V16 M140 0 V16 M146 0 V16 M152 0 V16 M155 0 V16 M161 0 V16 M167 0 V16 M170 0 V16 M175 0 V16" stroke="#ffffff" stroke-width="1.5" opacity="0.75" />
          <text x="90" y="26" font-size="8.5" fill="#2E79FF" class="font-mono" text-anchor="middle" letter-spacing="2">73472526-9AA0-4998</text>
        </g>
        
        <g clip-path="url(#badge-clip-inner)">
          <rect width="240" height="330" rx="16" fill="url(#holo-grad)" class="holo-overlay" pointer-events="none" style="mix-blend-mode: color-dodge;" />
        </g>
      </g>
      
      <mask id="badge-mask">
        <rect x="50" y="165" width="240" height="330" rx="16" fill="#ffffff" />
      </mask>
      
    </g>
  </g>
  
  <clipPath id="badge-clip-inner">
    <rect width="240" height="330" rx="16" />
  </clipPath>
</svg>"""

    with open("lanyard.svg", "w", encoding="utf-8") as f:
        f.write(lanyard_svg)
    print("lanyard.svg successfully generated.")


    # 4. CREATE stats.svg (Dynamic Cosmic Obsidian/Amethyst Stats from actual JSON)
    stats_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 200" width="450" height="200">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" />
      <stop offset="100%" stop-color="#021C4F" />
    </linearGradient>
    
    <!-- Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.1" />
    </linearGradient>
    
    <!-- Rank Circle Glow -->
    <radialGradient id="ring-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#C50337" stop-opacity="0" />
    </radialGradient>
    
    <filter id="card-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    
    /* Rank Ring drawing */
    @keyframes draw-ring {{
      from {{ stroke-dashoffset: 283; }}
      to {{ stroke-dashoffset: 42.45; }}
    }}
    .rank-ring {{
      stroke-dasharray: 283;
      stroke-dashoffset: 283;
      animation: draw-ring 1.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
      transform: rotate(-90deg);
      transform-origin: 75px 100px;
    }}
    
    /* Rank text pulse */
    @keyframes pulse-rank {{
      0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 2px rgba(197, 3, 55, 0.6)); }}
      50% {{ transform: scale(1.08); filter: drop-shadow(0 0 12px rgba(197, 3, 55, 0.8)); }}
    }}
    .rank-text {{
      animation: pulse-rank 3s ease-in-out infinite;
      transform-origin: 75px 100px;
    }}
    
    /* Stats list items sliding in */
    @keyframes slide-in {{
      from {{ transform: translateX(40px); opacity: 0; }}
      to {{ transform: translateX(0); opacity: 1; }}
    }}
    .stat-row {{ opacity: 0; animation: slide-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }}
  </style>

  <!-- Card Body -->
  <rect x="1" y="1" width="448" height="198" rx="16" fill="url(#card-bg)" stroke="url(#border-grad)" stroke-width="1.5" />
  
  <!-- Outer glowing rings behind Rank -->
  <circle cx="75" cy="100" r="55" fill="url(#ring-glow)" />
  
  <!-- Rank Ring -->
  <circle cx="75" cy="100" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="6" />
  <circle cx="75" cy="100" r="45" fill="none" stroke="#C50337" stroke-width="6" stroke-linecap="round" class="rank-ring" filter="url(#card-glow)" />
  
  <!-- Rank Badge Text -->
  <g class="rank-text">
    <text x="75" y="108" font-size="28" font-weight="900" fill="#ffffff" class="font-sans" text-anchor="middle" letter-spacing="1">A</text>
  </g>
  <text x="75" y="162" font-size="10" font-weight="bold" fill="#C50337" class="font-sans" text-anchor="middle" letter-spacing="2">PROFILE RANK</text>

  <!-- Divider Line -->
  <line x1="150" y1="30" x2="150" y2="170" stroke="rgba(197, 3, 55, 0.15)" stroke-width="1.2" />

  <!-- Stats Rows -->
  <g transform="translate(175, 0)" class="font-sans">
    <!-- Header -->
    <text x="0" y="32" font-size="14" font-weight="900" fill="#ffffff" letter-spacing="1.5">ABEL'S REAL STATS</text>
    <line x1="0" y1="42" x2="220" y2="42" stroke="#2E79FF" stroke-width="1" opacity="0.3" />
    
    <!-- Total Contributions -->
    <g transform="translate(0, 72)">
      <g class="stat-row" style="animation: slide-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s forwards;">
        <circle cx="5" cy="-5" r="3" fill="#C50337" />
        <text x="18" y="0" font-size="12" fill="#94a3b8" font-weight="bold">Contributions</text>
        <text x="220" y="0" font-size="13" font-weight="bold" fill="#ffffff" class="font-mono" text-anchor="end">{contributions:,}</text>
      </g>
    </g>
    
    <!-- Repos -->
    <g transform="translate(0, 105)">
      <g class="stat-row" style="animation: slide-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s forwards;">
        <circle cx="5" cy="-5" r="3" fill="#2E79FF" />
        <text x="18" y="0" font-size="12" fill="#94a3b8" font-weight="bold">Public Repos</text>
        <text x="220" y="0" font-size="13" font-weight="bold" fill="#ffffff" class="font-mono" text-anchor="end">{public_repos}</text>
      </g>
    </g>
    
    <!-- Followers -->
    <g transform="translate(0, 138)">
      <g class="stat-row" style="animation: slide-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.6s forwards;">
        <circle cx="5" cy="-5" r="3" fill="#FF5D82" />
        <text x="18" y="0" font-size="12" fill="#94a3b8" font-weight="bold">Followers</text>
        <text x="220" y="0" font-size="13" font-weight="bold" fill="#ffffff" class="font-mono" text-anchor="end">{followers}</text>
      </g>
    </g>
  </g>
</svg>"""

    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(stats_svg)
    print("stats.svg successfully generated.")

    # 5. CREATE langs.svg (Real top languages from actual repos)
    languages = stats_data.get("languages", {})
    if not languages:
        languages = {
            "Python": 32.0,
            "HTML": 20.0,
            "CSS": 20.0,
            "C": 12.0,
            "TypeScript": 4.0
        }
    
    # Sort and take top 5
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Map colors matching the dark/neon theme
    color_map = {
        "Python": "#C50337",
        "HTML": "#2E79FF",
        "CSS": "#FF5D82",
        "JavaScript": "#FFBC0A",
        "TypeScript": "#007ACC",
        "C": "#FF5D82",
        "C++": "#F34B7D",
        "Java": "#B07219",
        "Rust": "#DEA584",
        "Go": "#00ADD8"
    }
    theme_colors = ["#2E79FF", "#C50337", "#FF5D82", "#C50337", "#2E79FF"]
    
    keyframes = []
    classes = []
    items_svg = []
    
    for idx, (lang, pct) in enumerate(sorted_langs):
        width_px = round((pct / 100) * 240)
        keyframes.append(f"    @keyframes load-bar-{idx} {{ from {{ width: 0px; }} to {{ width: {width_px}px; }} }}")
        classes.append(f"    .bar-{idx} {{ animation: load-bar-{idx} 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; width: 0; }}")
        
        color = color_map.get(lang, theme_colors[idx % len(theme_colors)])
        y_pos = 68 + idx * 26
        
        items_svg.append(f"""    <!-- {lang} -->
    <g class="lang-item item-{idx+1}" transform="translate(0, {y_pos})">
      <text x="0" y="0" font-size="12" font-weight="bold" fill="#ffffff">{lang}</text>
      <rect x="90" y="-10" width="240" height="8" rx="4" fill="rgba(255,255,255,0.05)" />
      <rect x="90" y="-10" height="8" rx="4" fill="{color}" class="bar-{idx}" filter="url(#lang-glow)" />
      <text x="390" y="0" font-size="12" font-weight="bold" fill="{color}" class="font-mono" text-anchor="end">{pct}%</text>
    </g>""")

    # If we have less than 5 languages, fill the remaining slots with Figma Design or placeholders
    if len(sorted_langs) < 5:
        idx = len(sorted_langs)
        y_pos = 68 + idx * 26
        keyframes.append(f"    @keyframes load-bar-figma {{ from {{ width: 0px; }} to {{ width: 132px; }} }}")
        classes.append(f"    .bar-figma {{ animation: load-bar-figma 1.5s cubic-bezier(0.4, 0, 0.2, 1) forwards; width: 0; }}")
        items_svg.append(f"""    <!-- Figma UI/UX -->
    <g class="lang-item item-5" transform="translate(0, {y_pos})">
      <text x="0" y="0" font-size="12" font-weight="bold" fill="#ffffff">Figma Design</text>
      <rect x="90" y="-10" width="240" height="8" rx="4" fill="rgba(255,255,255,0.05)" />
      <rect x="90" y="-10" height="8" rx="4" fill="#2E79FF" class="bar-figma" filter="url(#lang-glow)" />
      <text x="390" y="0" font-size="12" font-weight="bold" fill="#2E79FF" class="font-mono" text-anchor="end">Design</text>
    </g>""")
        
    keyframes_str = "\n".join(keyframes)
    classes_str = "\n".join(classes)
    items_str = "\n\n".join(items_svg)
    
    langs_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 200" width="450" height="200">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" />
      <stop offset="100%" stop-color="#021C4F" />
    </linearGradient>
    
    <!-- Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.1" />
    </linearGradient>
    
    <!-- Glowing Soft Filter -->
    <filter id="lang-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .font-sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .font-mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    
    /* Loading language progress bars based on actual repo count */
{keyframes_str}

{classes_str}
    
    /* Fading in text delays */
    @keyframes fade-in {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    .lang-item {{ opacity: 0; animation: fade-in 0.5s ease-out forwards; }}
    .item-1 {{ animation-delay: 0.1s; }}
    .item-2 {{ animation-delay: 0.2s; }}
    .item-3 {{ animation-delay: 0.3s; }}
    .item-4 {{ animation-delay: 0.4s; }}
    .item-5 {{ animation-delay: 0.5s; }}
  </style>

  <!-- Card Body -->
  <rect x="1" y="1" width="448" height="198" rx="16" fill="url(#card-bg)" stroke="url(#border-grad)" stroke-width="1.5" />
  
  <g transform="translate(25, 0)" class="font-sans">
    <!-- Header -->
    <text x="0" y="32" font-size="14" font-weight="900" fill="#ffffff" letter-spacing="1.5">REAL TOP LANGUAGES</text>
    <line x1="0" y1="42" x2="390" y2="42" stroke="#2E79FF" stroke-width="1" opacity="0.3" />

{items_str}
  </g>
</svg>"""
    with open("langs.svg", "w", encoding="utf-8") as f:
        f.write(langs_svg)
    print("langs.svg successfully generated.")


    # 6. CREATE trophies.svg (Unified Theme Achievements & Trophies)
    create_trophies()

    # 7. CREATE animated social buttons
    create_social_buttons()

    print("All SVG assets successfully assembled.")

def chr_delays_css(count, start_delay=1.0):
    lines = []
    for i in range(count):
        d_draw = round(start_delay + i * 0.08, 2)
        d_fill = round(start_delay + 0.8 + i * 0.08, 2)
        lines.append(f"    .name-vector path:nth-child({i+1}), .name-vector-light path:nth-child({i+1}) {{ animation-delay: {d_draw}s, {d_fill}s; }}")
    return "\n".join(lines)

def create_trophies():
    trophies_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 200" width="920" height="200">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" />
      <stop offset="100%" stop-color="#021C4F" />
    </linearGradient>
    
    <!-- Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#C50337" stop-opacity="0.5" />
      <stop offset="100%" stop-color="#2E79FF" stop-opacity="0.1" />
    </linearGradient>

    <!-- Cells Highlight Gradient -->
    <linearGradient id="cell-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.01" />
    </linearGradient>
    
    <!-- Diagonal Shine Gradient -->
    <linearGradient id="shine-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.25" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    
    <!-- Glowing Filter -->
    <filter id="trophy-glow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
    .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    
    /* Cells Pop In Animation */
    @keyframes pop-in {
      0% { transform: scale(0.9); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }
    .trophy-cell { opacity: 0; animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }
    
    /* Shine Sweep Animation */
    @keyframes shine-sweep {
      0% { transform: translate(-300px, 0); }
      30%, 100% { transform: translate(300px, 0); }
    }
    .shine-rect {
      animation: shine-sweep 4s ease-in-out infinite;
    }
    .shine-delay-1 { animation-delay: 0.5s; }
    .shine-delay-2 { animation-delay: 1.5s; }
    .shine-delay-3 { animation-delay: 2.5s; }
  </style>

  <!-- Card Body -->
  <rect x="1" y="1" width="918" height="198" rx="16" fill="url(#card-bg)" stroke="url(#border-grad)" stroke-width="1.5" />

  <!-- Main Container -->
  <g transform="translate(25, 0)" class="font-sans">
    <!-- Header -->
    <text x="0" y="32" font-size="14" font-weight="900" fill="#ffffff" letter-spacing="1.5">PROFILE ACHIEVEMENTS &amp; TROPHIES</text>
    <line x1="0" y1="42" x2="868" y2="42" stroke="#2E79FF" stroke-width="1" opacity="0.3" />

    <!-- Trophy Cell 1: Commits Master -->
    <g transform="translate(0, 60)">
      <g class="trophy-cell cell-1" style="animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s forwards;">
        <!-- Card background -->
        <rect width="270" height="110" rx="12" fill="url(#cell-bg)" stroke="rgba(197, 3, 55, 0.25)" stroke-width="1" />
        <!-- Golden/Purple Trophy Icon -->
        <g transform="translate(20, 25)" filter="url(#trophy-glow)">
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V19h3v2H7v-2h3v-2.07A6 6 0 0 1 6 11V6h12v5a6 6 0 0 1-5 5.93zM8 8H7V7h1zm0 2H7V9h1zm0 2H7v-1h1zm8-4h-1V7h1zm0 2h-1V9h1zm0 2h-1v-1h1z" fill="#C50337" />
        </g>
        <!-- Title & Details -->
        <text x="75" y="42" font-size="13" font-weight="bold" fill="#ffffff">Commits Master</text>
        <text x="75" y="62" font-size="10.5" fill="#94a3b8">Rank: Gold (1,000+ Commits)</text>
        <text x="75" y="80" font-size="10.5" fill="#C50337" font-weight="bold">TOP 2.5% CONTRIBUTOR</text>
        
        <!-- Shine layer -->
        <g clip-path="url(#cell-clip-1)">
          <rect width="270" height="110" fill="url(#shine-grad)" class="shine-rect shine-delay-1" pointer-events="none" />
        </g>
        <clipPath id="cell-clip-1"><rect width="270" height="110" rx="12" /></clipPath>
      </g>
    </g>

    <!-- Trophy Cell 2: PR Champion -->
    <g transform="translate(299, 60)">
      <g class="trophy-cell cell-2" style="animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s forwards;">
        <rect width="270" height="110" rx="12" fill="url(#cell-bg)" stroke="rgba(46, 121, 255, 0.25)" stroke-width="1" />
        <!-- Pink/Rose Trophy Icon -->
        <g transform="translate(20, 25)" filter="url(#trophy-glow)">
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V19h3v2H7v-2h3v-2.07A6 6 0 0 1 6 11V6h12v5a6 6 0 0 1-5 5.93zM8 8H7V7h1zm0 2H7V9h1zm0 2H7v-1h1zm8-4h-1V7h1zm0 2h-1V9h1zm0 2h-1v-1h1z" fill="#2E79FF" />
        </g>
        <text x="75" y="42" font-size="13" font-weight="bold" fill="#ffffff">PR Champion</text>
        <text x="75" y="62" font-size="10.5" fill="#94a3b8">Rank: Diamond (150+ PRs)</text>
        <text x="75" y="80" font-size="10.5" fill="#2E79FF" font-weight="bold">TOP 5% COLLABORATOR</text>
        
        <!-- Shine layer -->
        <g clip-path="url(#cell-clip-2)">
          <rect width="270" height="110" fill="url(#shine-grad)" class="shine-rect shine-delay-2" pointer-events="none" />
        </g>
        <clipPath id="cell-clip-2"><rect width="270" height="110" rx="12" /></clipPath>
      </g>
    </g>

    <!-- Trophy Cell 3: Clean Coder -->
    <g transform="translate(598, 60)">
      <g class="trophy-cell cell-3" style="animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.5s forwards;">
        <rect width="270" height="110" rx="12" fill="url(#cell-bg)" stroke="rgba(255, 93, 130, 0.25)" stroke-width="1" />
        <!-- Indigo Trophy Icon -->
        <g transform="translate(20, 25)" filter="url(#trophy-glow)">
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V19h3v2H7v-2h3v-2.07A6 6 0 0 1 6 11V6h12v5a6 6 0 0 1-5 5.93zM8 8H7V7h1zm0 2H7V9h1zm0 2H7v-1h1zm8-4h-1V7h1zm0 2h-1V9h1zm0 2h-1v-1h1z" fill="#FF5D82" />
        </g>
        <text x="75" y="42" font-size="13" font-weight="bold" fill="#ffffff">Clean Coder</text>
        <text x="75" y="62" font-size="10.5" fill="#94a3b8">Rank: Emerald (Consistent Styling)</text>
        <text x="75" y="80" font-size="10.5" fill="#FF5D82" font-weight="bold">99% TEST PASS RATE</text>
        
        <!-- Shine layer -->
        <g clip-path="url(#cell-clip-3)">
          <rect width="270" height="110" fill="url(#shine-grad)" class="shine-rect shine-delay-3" pointer-events="none" />
        </g>
        <clipPath id="cell-clip-3"><rect width="270" height="110" rx="12" /></clipPath>
      </g>
    </g>
  </g>
</svg>"""
    with open("trophies.svg", "w", encoding="utf-8") as f:
        f.write(trophies_svg)
    print("trophies.svg successfully generated.")

def create_social_buttons():
    # Helper to generate button template
    def button_template(filename, label, border_hex, icon_path):
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 50" width="180" height="50">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="btn-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#01081A" />
      <stop offset="100%" stop-color="#021C4F" />
    </linearGradient>

    <!-- Neon Glow Filter -->
    <filter id="btn-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .text-btn {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 13px;
      font-weight: 800;
      fill: #ffffff;
      letter-spacing: 1.5px;
    }}
    
    /* Flowing neon border animation */
    @keyframes border-flow {{
      0% {{ stroke-dashoffset: 0; }}
      100% {{ stroke-dashoffset: -460; }}
    }}
    .flowing-border {{
      stroke-dasharray: 100 360;
      stroke-dashoffset: 0;
      animation: border-flow 3.5s linear infinite;
    }}
    
    /* Subtle hover pulse styling */
    @keyframes pulse-light {{
      0%, 100% {{ opacity: 0.8; filter: drop-shadow(0 0 2px {border_hex}); }}
      50% {{ opacity: 1; filter: drop-shadow(0 0 8px {border_hex}); }}
    }}
    .glow-element {{
      animation: pulse-light 3s ease-in-out infinite;
    }}
  </style>

  <!-- Button Card Backing -->
  <rect x="1" y="1" width="178" height="48" rx="24" fill="url(#btn-bg)" stroke="rgba(255,255,255,0.05)" stroke-width="1.5" />
  
  <!-- Flowing Neon Path -->
  <rect x="1" y="1" width="178" height="48" rx="24" fill="none" stroke="{border_hex}" stroke-width="2.5" class="flowing-border glow-element" filter="url(#btn-glow)" />

  <!-- Center Group -->
  <g transform="translate(25, 0)">
    <!-- Icon -->
    <g transform="translate(0, 15)" fill="{border_hex}" class="glow-element">
      {icon_path}
    </g>
    <!-- Label -->
    <text x="35" y="30" class="text-btn">{label}</text>
  </g>
</svg>"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"{filename} successfully generated.")

    # Icon Paths matching the theme colors
    email_icon = '<path d="M0 3a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3zm2 2v9h14V5l-7 4.5L2 5z" fill="#FF5D82" />'
    linkedin_icon = '<path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.779-1.75-1.75s.784-1.75 1.75-1.75 1.75.779 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" fill="#C50337" />'
    portfolio_icon = '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.53c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.4z" fill="#2E79FF" />'
    github_icon = '<path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" fill="#ffffff" />'

    button_template("btn-email.svg", "EMAIL ME", "#FF5D82", email_icon)
    button_template("btn-linkedin.svg", "LINKEDIN", "#C50337", linkedin_icon)
    button_template("btn-portfolio.svg", "PORTFOLIO", "#2E79FF", portfolio_icon)
    button_template("btn-github.svg", "GITHUB", "#ffffff", github_icon)

if __name__ == "__main__":
    main()
