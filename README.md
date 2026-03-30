# Chaos Unveiled: From Order to Chaos in Oscillations


A **Manim-powered visualization journey** through the progression from **linear oscillators → coupled systems → nonlinear pendulums → double pendulum chaos → Lorenz attractor**, showing how simple deterministic equations produce wildly unpredictable behavior.

## 🎬 Scene Breakdown

| Scene | Title | Key Concept | Visual Highlight |
|-------|-------|-------------|------------------|
| **1** | Linear Oscillator | Perfect sine waves | Clean harmonic motion |
| **2** | Coupled Oscillators | Normal modes, beats | Two springs syncing |
| **3** | Nonlinear Pendulum | Period depends on amplitude | Elliptical phase portrait |
| **4** | Period vs Amplitude | \( T \approx 2\pi\sqrt{L/g} (1 + \frac{\theta_0^2}{16}) \) | Live measurement |
| **5** | Taylor Expansion | \(\sin\theta \approx \theta - \frac{\theta^3}{6}\) | Mathematical derivation |
| **6** | Enter Chaos | Recipe: nonlinearity + 2+ DOF | Phase portrait teaser |
| **7** | Double Pendulum | Deterministic chaos | Glowing bobs + smooth tail |
| **8** | Sensitive Dependence | 0.018° → different futures | Two overlaid pendulums diverge |
| **8b** | Lorenz Attractor | Butterfly effect in 3D | 5 cyan→gold trajectories |

## 🚀 Quick Start

```bash
# Clone & install
git clone https://github.com/yourusername/chaos-unveiled.git
cd chaos-unveiled

# Install dependencies
pip install manim[community] scipy numpy

# Render a scene in low quality
manim -pql main.py Scene7DoublePendulum

# Render a scene in high quality
manim -pqh main.py Scene8bLorenzAttractor

# Render a video in 4K
manim -pkh main.py Scene7DoublePendulum
```

## 🛠️ Technical Highlights

### **Smooth Animations**
- **6000+ time steps** with `DOP853` solver (`rtol=1e-10`)
- **Zero-lag tails** via `always_redraw()` with `np.searchsorted()`
- **Arc-length parameterization** for perfect bob-trail sync

### **Visual Polish**
```
Glow effect: 4 layered Circle() → soft halo
Tail gradient: color_gradient(CYAN→GOLD→RED)
3D lighting fix: set_shade_in_3d(False)
Phase portraits: ParametricFunction with live axes
```

### **Physics Accuracy**
```
Double pendulum: full nonlinear Lagrange equations
Nonlinear pendulum: exact period formula derivation
Lorenz: classic σ=10, ρ=28, β=8/3 parameters
Coupled oscillators: analytic normal modes
```


## 🎓 Learning Outcomes

1. **Linear → Nonlinear**: How \(\sin\theta \approx \theta\) breaks down
2. **Coupling**: Normal modes emerge from 2×2 eigenvalue problem  
3. **Chaos Recipe**: Nonlinearity + 2+ DOF + sensitivity = chaos
4. **Butterfly Effect**: 0.018° initial difference → completely different paths
5. **Strange Attractors**: Bounded, deterministic, non-repeating motion

## 📂 File Structure

```
chaos-unveiled/
├── main.py              # All scenes (Scene1Linear → Scene8bLorenz)
├── screenshots/         # Thumbnails for README
├── physics/             # Raw equations & derivations
├── render.sh           # Batch render script
└── README.md           # You're reading it!
```

## 🔮 Future Plans

- [ ] **Feigenbaum bifurcation diagram** (logistic map)
- [ ] **Lyapunov exponents** live calculation  
- [ ] **Poincaré sections** for double pendulum
- [ ] **4K render pipeline** with audio narration
- [ ] **Interactive Jupyter version**

## 🙏 Acknowledgments

- **Manim Community** — v0.18.1 made this possible
- **3Blue1Brown** — inspiration for mathematical beauty
- **Perplexity AI** — co-pilot for debugging Manim edge cases
- **Physics StackExchange** — equation validation

## 📄 License

MIT License — use freely, cite if you find it helpful!

***

**"Order from chaos, or chaos from order? Both are true."**

> Built with ❤️ during late-night physics + coding sessions at BITS Goa, March 2026

***

⭐ **Star if you learned something!** 🚀
