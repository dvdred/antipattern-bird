# antipattern-bird
Simple python Game (Flappy Bird Like)
![Intro](https://github.com/dvdred/antipattern-bird/raw/refs/heads/main/demo0.png)
![Game](https://github.com/dvdred/antipattern-bird/raw/refs/heads/main/demo1.png)

An addictive, Python-powered Flappy-style mini-game with rainbow & zebra power-ups, lives system and 4-min speed-run victory.

## Quick Start

### Play without installing anything
1. Go to the latest release page
2. Download the file that matches your OS:

| OS | Download & Run |
|----|----------------|
| Windows | `antipattern-bird.exe` |
| Linux | `antipattern-bird` *(single-file binary)* |

Double-click (or run inside a terminal) and enjoy.

### Launch with Python
> Works on any platform that has Python 3.8+

```bash
# 1) clone or download the source
git clone https://github.com/dvdred/antipattern-bird.git
cd antipattern-bird

# 2) optional virtual-env
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

# 3) install dependencies
pip install -r requirements.txt

# 4) play
python app.py
```

Controls are the same whichever way you start it - see next section.

## How to Play

**Objective**  
Survive and score as many points as you can until you either:
- run out of lives ❤, or
- pass the 4-minute mark to unlock the WIN screen

**Controls** (keyboard)
| Key | Action |
|-----|--------|
| `SPACE` (hold to flap) | Jump up |
| `P` | Pause / Resume |
| `Q` or `ESC` inside menus or pause | Quit to desktop |

**What you see**
```
Score: 42      ❤ ❤ ❤      Level 1
```
- **Score** - total points collected  
- **❤** - remaining lives (max 6)  
- **Level** - auto-scaling difficulty (1→2→3 based on elapsed time)

**Earning points** (all values are multiplied by the current Level)
* 1 pt - pass a normal pipe  
* 2 pt - pass the black-&-white ZEBRA pipe  
* 3 pt - pass the RAINBOW pipe

**Extra points** (Loosing or Winning the game)
* 15 pt - Ending at lvl 2
* 30 pt - Ending at lvl 3
* 50 pt - Winning the Game
* 100 pt - Winning the Game with all Lives  

**Special pipes**
RAINBOW (coloured stripes)  
- grants instant 3 pts  
- shows a white flash and a happy "bling" sound

ZEBRA (black/white halves)  
- grants 2 pts  
- starts ZEBRA-SPEED mode: everything scrolls 1.5× faster for 8 s  
- during those 8 s every pipe you pass is worth double (×2)

**Extra life**  
Every triangular-number target (5 - 15 - 30 - 50 - 75 ...) awards +1 life (up to 6).

**Time milestones**
| Time | Effect |
|------|--------|
| 90 s | Level 2 - scroll speed ↑ |
| 150 s | Level 3 - scroll speed ↑↑ |
| 240 s | YOU WIN! |

Good luck, and keep flapping!