# antipattern-bird
Simple python Game (Flappy Bird Like)

![Intro](https://github.com/dvdred/antipattern-bird/raw/refs/heads/stable/demo00.png)
![Options](https://github.com/dvdred/antipattern-bird/raw/refs/heads/stable/demo01.png)
![Game](https://github.com/dvdred/antipattern-bird/raw/refs/heads/stable/demo02.png)
![Win](https://github.com/dvdred/antipattern-bird/raw/refs/heads/stable/demo03.png)

An addictive, Python-powered Flappy-style mini-game with rainbow & zebra power-ups, customizable bird, lives system and 4-min speed-run victory.

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

### Character Customization

Before each game, you'll see a **customization menu** where you can choose:

**Shape Selection** (keyboard numbers `1-5` or mouse click)
- `1` - Square
- `2` - Circle  
- `3` - Triangle
- `4` - Diamond
- `5` - Random (changes every game over)

**Color Selection** (keyboard letters or mouse click)
- `Q` - Saffron (yellow-orange)
- `W` - Coral (orange-red)
- `E` - Royal Blue
- `R` - Forest Green
- `Y` - Goldenrod
- `U` - Medium Purple
- `I` - Blood Red
- `T` - Random (changes every Game Over)

**DEBUG Mode** (keyboard letter `D` or mouse click)
- Toggles real-time overlay showing:
  - **Game Time** - elapsed time in mm:ss format
  - **Base Speed** - starting scroll speed
  - **Special Pipes** - Info extra for special pipes 
  - **SPEED** - final combined speed (highlighted in green)
  - **Pipe Gap** - current vertical spacing between pipes

> Useful for understanding the difficulty curve and optimizing your strategy!

**AUDIO Mode** (keyboard letter `A` or mouse click)
- Toggles sound effects ON/OFF
- Visual indicator: 🔊 (ON) or 🔇 (OFF)
- Useful for playing in quiet environments!

Press `SPACE` to confirm and start the game with your chosen appearance!

> **Note**: Your selection is remembered during the current session. After a Game Over, press `O` to return to this menu and change your bird. After winning, you'll automatically return here with increased difficulty.

### In-Game Controls

| Key | Action |
|-----|--------|
| `SPACE` (tap or hold) | Jump / Flap |
| `P` | Pause / Resume |
| `O` (after Game Over) | Return to customization menu |
| `Q` or `ESC` | Quit to desktop |

The game window is **resizable** - drag the corners to adjust the size while maintaining the correct aspect ratio.

### Game Interface

```
Score: 42      ❤ ❤ ❤      Level 1
```
- **Score** - total points collected  
- **❤** - remaining lives (max 6)  
- **Level** - auto-scaling difficulty (1→2→3 based on elapsed time)

**Earning points** (all values are multiplied by the current Level)
* **1 pt** - pass a normal pipe (with AntiPattern names)
* **2 pt** - pass the black-&-white **ZEBRA** pipe  
* **3 pt** - pass the **RAINBOW** pipe

**Bonus points** (awarded at Game Over or Victory)
* **15 pt** - Reached Level 2
* **30 pt** - Reached Level 3
* **50 pt** - Won the game (survived 4 minutes)
* **+100 pt** - Won with maximum lives (6❤)

### Special Pipes

**🌈 RAINBOW** (vertical colored stripes)  
- Triggers a white flash and cheerful "bling" sound
- Points **3 pts** × level multiplier
- Spawn: Very Common (20-45 seconds)

**🦓 ZEBRA** (black/white vertical stripes)  
- Activates **ZEBRA-SPEED mode** for 8 seconds:
  - Everything scrolls **1.5× faster**
  - All POINTS earned are **DOUBLED** (×2)
  - A countdown timer appears at the top
- Points **2 pts** × level multiplier
- Spawn: once per minute

**🧊 ICE** (white/blue pipe)  
- Activates **ICE-SLOW mode** for 8 seconds:
  - Everything scrolls **0.5× slower**
  - A countdown timer appears at the top
- Spawn: Common-Medium (30-60 seconds)

**🗿 LEGACY** (dark brown pipe)  
- Grants instant **4 pts** × level multiplier
- Smaller vertical gap size (-15px)
- Spawn: Medium (65-80 seconds)

**🪨​ DEBT** (dark gray pipe with ⚓ anchor icon)
- Activates **TECH-DEBT mode** for 8 seconds:
  - Gravity malus **20% heavier**
  - A anchor appears over the bird
- Points **5 pts** × level multiplier  
- Spawn: Medium (50-70 seconds)

**🍝 Spaghetti** (animated red/yellow pipe)
- Effect: Reverses controls and gravity for **6 seconds** (Jump descends instead of ascends, and gravity is reversed for that time)
- Visual: Two-tone yellow and red wavy/intertwined stripes similar to those on barber poles
- Points **7 pts** × level multiplier 
- Spawn: Medium-Rare (75-100 seconds)

**👻 GHOST** (semi-transparent light blue pipe)
- **Memory test challenge:**
  - Appears semi-transparent (30% opacity) for **2 seconds**
  - Then becomes **completely invisible** but still solid for scoring
  - You can **pass through it without damage** (walls don't hurt)
  - But you **must pass through the gap** to collect points
- Points **3 pts** × level multiplier
- Spawn: Common (40-45 seconds)

**💩​ MUD** (brown/yellow pipe) [BOSS]
- Big size Pipe
- **Aim Challenge**
  - Stay low and hope in 
- Points **15 pts** × level multiplier  
- Spawn: at the end of 2° and 3° lvl

**🪙 GOLDEN** (gold pipe)
- +1 Life (or **+10 pts × level** if already at 6 lives)
- Spawn: One (180-210 seconds)

### Extra Lives

Every triangular-number score target awards **+1 life** (up to maximum 6):
- 5, 15, 30, 50, 75, 105, 140, 180, 225...

When you collect a life, you'll hear a happy "power-up" sound! 🎵

**Life Overflow Bonus** ⭐  
When you already have **6 lives** (maximum), extra lives are converted to **bonus points**:
- Formula: **+10 pts × current level**
- Example: At Level 3, you get **+30 pts** instead of a life
- A popup with ⭐ emoji shows the bonus for 2 seconds

### Level Progression

The game automatically increases difficulty based on time survived:

| Time | Level | Speed | Points | Pipe Gap |
|------|-------|-------|--------|----------|
| 0-90s | Level 1 | 1.0× | 1.0× | 180px (easy) |
| 90-150s | Level 2 | 1.5× | 1.5× | 165px (medium) |
| 150-240s | Level 3 | 2.0× | 2.0× | 150px (hard) |
| **240s** | **VICTORY!** | — | — | **Win screen + bonus** |

> **Note**: As you progress, not only does speed increase, but the vertical gap between pipes **gets narrower**, making navigation more challenging!

### Game Over & Continue

When you lose all lives:
- **Best Score** is displayed (highest score in current session)
- **Bonus points** are added based on level reached
- Press `SPACE` to **restart** with the same bird customization
- Press `O` to **return to customization menu** and change your bird
- Press `Q` to quit

> **Tip**: After a tough run, press `O` to try a different shape or color!

### Victory & Progressive Difficulty

When you reach the **4-minute mark**:
1. You see the **WIN screen** with your score and bonuses
2. Press `SPACE` to return to the **customization menu**
3. The next game will have **+0.5 base speed** (stacks up to 6.0×)
4. This creates an endless challenge for skilled players!

## Visual Features

- **Animated clouds** - Two layers of procedurally-generated clouds drift across the sky at different speeds
- **Colored particles** - Your bird leaves a trail of particles matching its color when jumping
- **Dynamic backgrounds** - Randomized pastel skies and ground colors for each game
- **Invulnerability flash** - After losing a life, your bird blinks for 2 seconds
- **Smooth scaling** - Resize the window freely without distortion
- **A Finish Line** - Endline and final autofly effect to victory!

## Tips & Tricks

1. **Save zebra pipes for hard moments** - The speed boost is challenging but doubles your points!
2. **Plan ahead** - Rainbow pipes are worth 3× your level multiplier (9 pts at Level 3!)
3. **Learn the rhythm** - Each level has a consistent scroll speed - find your timing
4. **Don't panic after hits** - You have 2 seconds of invulnerability to reposition
5. **Mix it up** - Try different bird shapes - they have slightly different visual hitboxes!

## Sound Effects (from https://freesound.org )

- 🐦 Flap/Jump ( https://freesound.org/people/cabled_mess/sounds/350898/ )
- ⭐ Point scored ( https://freesound.org/people/LittleRobotSoundFactory/sounds/270302/ )  
- 🌈 Rainbow/Zebra collected ( https://freesound.org/people/1bob/sounds/717770/ )
- ❤️ Life gained ( https://freesound.org/people/LilMati/sounds/523650/ )
- 💔 Life lost ( https://freesound.org/people/GameAudio/sounds/220174/ )
- 🪙​ Golden Pipe ( https://freesound.org/people/Eschwabe3/sounds/460132/ )
- 🧊 Ice Pipe ( https://freesound.org/people/JarredGibb/sounds/263915/ )
- 🗿​ LegacyCode Pipe ( https://freesound.org/people/qubodup/sounds/743248/ )
- 🪨 Tech Debt Pipe ( https://freesound.org/people/joseegn/sounds/752434/ )
- 🍝 Spaghetti Pipe ( https://freesound.org/people/plagasRZ/sounds/326349/ )
- 👻​ Ghost Pipe ( https://freesound.org/people/Beast_Toil/sounds/249413/ )
- 💩 BBall of Mud Pipe ( https://freesound.org/people/Breviceps/sounds/445117/ )
- 🏆​ Victory! ( https://freesound.org/people/Victor_Natas/sounds/741118/ )

> Sounds play at 60% volume by default. Make sure your system volume is comfortable!

## Technical Features

- Built with **Pygame** (Python)
- **60 FPS** game loop
- Runs on Windows, Linux, and macOS (no binary)
- Standalone executables available (PyInstaller)
- Fully resizable window with letterboxing
- Pause functionality maintains game state
- Debug Overlay

## Contributing

We welcome contributions! 🎉

### Ways to Contribute

- 🐛 **Report bugs** - Use our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ **Suggest features** - Use our [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- 💻 **Submit code** - Follow our [Contributing Guidelines](CONTRIBUTING.md)
- 📝 **Improve docs** - Documentation PRs are always welcome

### Quick Links

- [Contributing Guidelines](CONTRIBUTING.md) - Development setup, coding standards, PR process
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards and expectations
- [Pull Request Template](.github/pull_request_template.md) - Template for submitting PRs
- [Issue Templates](.github/ISSUE_TEMPLATE/) - Report bugs or request features

### Development Setup

```bash
git clone https://github.com/dvdred/antipattern-bird.git
cd antipattern-bird
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
### Running Tests
```
python -m unittest test_app.py
```

See CONTRIBUTING.md for detailed guidelines on adding new features, pipe types, and more.

## Credits

- **Made with 💜 by** dvdred@gmail.com  
- **License**: GPL3  
- **Font**: DejaVu Sans Mono and NotoColorEmoji (for emoji support)
- **AntiPattern names** inspired by software engineering anti-patterns

---

Good luck, customize your bird, and keep flapping! 🐦✨