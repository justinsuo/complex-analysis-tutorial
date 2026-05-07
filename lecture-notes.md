# Complex Analysis — Complete Lecture Notes

UC Berkeley — Brown & Churchill *Complex Variables and Applications*, 9th ed.

Compiled from the 37 lecture transcripts. Every definition, theorem, proof, and example in order. Formulas in LaTeX-style notation throughout.

---

## Lecture 1 — Course Intro & Complex Numbers

### Syllabus essentials
- Textbook: Brown & Churchill, *Complex Variables and Applications*, 9th ed.
- HW posted Friday, due Sunday 9 days later (≥1 week).
- Midterm: in class. Final: 7–10 PM. Grading: 25% HW + 25% midterm + 50% final, with the final allowed to replace the midterm if higher.

### Course preview — four big topics
1. **Complex numbers**: $z = x + iy$ with $i^2 = -1$. Identify $\mathbb{C} \leftrightarrow \mathbb{R}^2$ as sets, but $\mathbb{C}$ has **extra product structure**.
2. **Analytic (= complex-differentiable) functions** $f:\mathbb{C}\to\mathbb{C}$: defined via the same limit
$$f'(z_0)=\lim_{\Delta z\to 0}\frac{f(z_0+\Delta z)-f(z_0)}{\Delta z}$$
but with $\Delta z$ approaching from any direction in $\mathbb{C}$.
3. **Theorems unique to complex analysis** — three flagship results:
   - **Cauchy's theorem**: $\oint_\gamma f\,dz = 0$ for analytic $f$ along any reasonable closed path.
   - **Regularity**: analytic ⟹ $f'$ exists ⟹ $f''$ exists ⟹ infinitely differentiable.
   - **Analytic continuation**: two analytic functions agreeing on a small disk agree everywhere.
   None of these hold in real analysis.
4. **Singular points** and **residues**, e.g.
$$\oint_C \frac{dz}{z} = 2\pi i$$
for any counterclockwise closed contour $C$ around $0$.

### Where complex numbers come from
The quadratic $ax^2 + bx + c = 0$ has solutions $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$. When $b^2-4ac<0$ no real solution exists. **Define** $i$ with $i^2=-1$; then $\sqrt{-K^2}=Ki$ and the formula always produces two roots in $\mathbb{C}$.

### Definition (complex numbers)
A **complex number** is $z = x+iy$ where $x,y\in\mathbb{R}$, $i^2=-1$.
- $\operatorname{Re}(z) = x$ (real part)
- $\operatorname{Im}(z) = y$ (imaginary part — note: just $y$, not $iy$)
- $\mathbb{R}$ is the subset of $\mathbb{C}$ with $\operatorname{Im}(z)=0$.
- $z$ is **purely imaginary** if $\operatorname{Re}(z)=0$.

### Algebra
- **Sum**: $(x_1+iy_1)+(x_2+iy_2)=(x_1+x_2)+i(y_1+y_2)$.
- **Product** (via distributing and $i^2=-1$):
$$(x_1+iy_1)(x_2+iy_2)=(x_1x_2-y_1y_2)+i(x_1y_2+x_2y_1).$$
Sums and products are commutative, associative, distributive — all standard real-number algebra survives.

### Inverses
- $0+z=z$, $1\cdot z = z$.
- $-(x+iy)=-x-iy$.
- For $z\neq 0$: $z^{-1}=\dfrac{x}{x^2+y^2} - i\dfrac{y}{x^2+y^2}$. Derived by writing $z^{-1}=u+iv$, multiplying $z\cdot z^{-1}=1$, equating real/imag parts, solving the linear system.

### Why $\mathbb{C}\neq\mathbb{R}^2$ as a structure
Inner product on $\mathbb{R}^2$ is real-valued; complex multiplication is complex-valued. The product depends on the rule $i^2=-1$; coordinates $x,y$ are interlocked through $i$, while in $\mathbb{R}^2$ they're independent.

---

## Lecture 2 — Modulus, Conjugate, Metric, Sequences

### Subtraction & division
- $z_1-z_2 = (x_1-x_2)+i(y_1-y_2)$.
- $\dfrac{z_1}{z_2} = z_1\cdot z_2^{-1}$ for $z_2\neq 0$.
- **Computation trick**: multiply numerator and denominator by $\bar z_2$. Example
$$\frac{4+i}{2-3i}\cdot\frac{2+3i}{2+3i}=\frac{5+14i}{13}.$$

### Modulus
$$|z|=\sqrt{x^2+y^2}\quad(\text{= length of vector }(x,y)).$$
- Two complex numbers cannot be ordered (unless real); but $|z_1|\le|z_2|$ makes sense.
- $|\operatorname{Re}(z)|\le|z|$ and $|\operatorname{Im}(z)|\le|z|$.

### Distance & metric
$$d(z_1,z_2)=|z_1-z_2|.$$
This is the standard $\mathbb{R}^2$ Euclidean metric. So $\mathbb{C}$ is a metric space:
- $d(z_1,z_2)\ge 0$ with equality iff $z_1=z_2$.
- $d(z_1,z_2)=d(z_2,z_1)$.
- **Triangle inequality**: $|z_1+z_2|\le|z_1|+|z_2|$. **Reverse**: $\big||z_1|-|z_2|\big|\le|z_1-z_2|$.
- $|z_1z_2|=|z_1||z_2|$ and $|z_1/z_2|=|z_1|/|z_2|$.

### Conjugate
$\bar z = x - iy$ (reflection across real axis).
- $\bar{\bar z}=z$, $|\bar z|=|z|$.
- $\operatorname{Re}(z)=\frac{z+\bar z}{2}$, $\operatorname{Im}(z)=\frac{z-\bar z}{2i}$.
- $z$ real $\iff z=\bar z$; purely imaginary $\iff z=-\bar z$.
- $\overline{z_1\pm z_2}=\bar z_1\pm\bar z_2$, $\overline{z_1z_2}=\bar z_1\bar z_2$, $\overline{z_1/z_2}=\bar z_1/\bar z_2$.

### Master identity
$$z\bar z = x^2+y^2 = |z|^2,\qquad \frac{1}{z}=\frac{\bar z}{|z|^2}\ (z\ne 0).$$

### Sequences
$z_n\to z_0$ means $|z_n-z_0|\to 0$. Equivalently $\operatorname{Re}(z_n)\to\operatorname{Re}(z_0)$ AND $\operatorname{Im}(z_n)\to\operatorname{Im}(z_0)$. $\mathbb{C}$ is **complete** (Cauchy ⟹ convergent), and the **Bolzano–Weierstrass** theorem holds: every bounded sequence has a convergent subsequence.

---

## Lecture 3 — Euler's Formula, Polar Form, Geometry of Multiplication

### Euler's formula and exponential of imaginary
Goal: define $e^{iy}$ so that $e^z = \sum z^n/n!$ extends consistently. Substituting $z=iy$ and separating real/imag terms gives
$$\boxed{e^{iy} = \cos y + i\sin y}.$$
**Definition for general** $z=x+iy$: $e^z = e^x(\cos y + i\sin y)$.

### Polar form
For nonzero $z$, write $x=r\cos\theta$, $y=r\sin\theta$, so
$$z = r(\cos\theta + i\sin\theta) = r\,e^{i\theta},$$
with $r=|z|>0$ and $\theta = \arg(z)$. The argument is multivalued: $\arg(z) = \theta_0 + 2n\pi$ for any integer $n$. The **principal value** $\operatorname{Arg}(z)\in(-\pi,\pi]$ is unique.

Examples:
- $\arg(-1) = \pi + 2n\pi$, $\operatorname{Arg}(-1)=\pi$.
- $\arg(-1-i) = -3\pi/4 + 2n\pi$, $\operatorname{Arg}(-1-i)=-3\pi/4$. Hence $-1-i = \sqrt 2\,e^{i\,3\pi/4}=\sqrt 2\,e^{-i\,3\pi/4}$.

### Conjugate in polar
$\overline{re^{i\theta}} = r\,e^{-i\theta}$.

### Circle equations
- $z(\theta) = R\,e^{i\theta}$, $\theta\in[0,2\pi)$ ⟹ circle of radius $R$ centered at origin.
- $z(\theta) = z_0 + R\,e^{i\theta}$ ⟹ circle of radius $R$ centered at $z_0$.

### Multiplication is rotation + scaling
$$z_1z_2 = r_1r_2\,e^{i(\theta_1+\theta_2)}.$$
**Proof** uses $\cos(\theta_1+\theta_2)$ and $\sin(\theta_1+\theta_2)$ angle-sum formulas after distributing.

**Division**: $z_1/z_2 = (r_1/r_2)e^{i(\theta_1-\theta_2)}$ (proof: write $1/z_2 = \bar z_2/|z_2|^2$ and apply the product formula).

**De Moivre**: $z^n = r^n e^{in\theta}$ for any integer $n$.

**Boxed identity**: $(\cos\theta+i\sin\theta)^n = \cos n\theta + i\sin n\theta$.

### Computational example
$(-1+i)^7$: write $-1+i=\sqrt 2\,e^{i\,3\pi/4}$, so the seventh power is $(\sqrt 2)^7 e^{i\,21\pi/4}=8\sqrt 2\,e^{i\,5\pi/4}=-8-8i$.

### Big-picture remark
We use the symbol $z$ for clean theorem statements but resort to $x,y$ (or $r,\theta$) when computing — Cauchy–Riemann equations later live in $(x,y)$-coordinates. Proofs are anchored in real analysis; results are dramatically stronger.

---

## Lecture 4 — Roots, Power Function, Topology

### Roots / power function
Define for nonzero $z=re^{i\theta}$ and real $T$:
$$z^{T} = r^{T}\,e^{i(\theta+2n\pi)T},\quad n\in\mathbb{Z}.$$
Generally **multivalued**.

**Number of values** of $z^T$:
- $T\in\mathbb{Z}$: 1 value.
- $T=p/q$ (lowest terms): $q$ values.
- $T$ irrational/complex: infinitely many values.

**Lemma**: $e^{i(\theta+2n_1\pi)T}=e^{i(\theta+2n_2\pi)T}\iff (n_1-n_2)T\in\mathbb{Z}$.

### $k$-th roots ($k\in\mathbb{Z}_{>0}$)
$$z^{1/k}=r^{1/k}\,e^{i(\theta+2n\pi)/k},\quad n=0,1,\dots,k-1.$$
Equally spaced around a circle of radius $r^{1/k}$.

Example: $\sqrt[4]{-16} = \sqrt[4]{16}\,e^{i(\pi+2n\pi)/4} = 2\,e^{i\pi/4}, 2\,e^{i\,3\pi/4}, 2\,e^{i\,5\pi/4}, 2\,e^{i\,7\pi/4}$, i.e., $\pm\sqrt 2\pm i\sqrt 2$.

### Topology of $\mathbb{C}$ — same as $\mathbb{R}^2$
- $r$-**neighborhood** of $z_0$: $B_r(z_0)=\{z:|z-z_0|<r\}$.
- Deleted nbhd: $0<|z-z_0|<r$.
- $z_0$ is **interior** to $S$ if some $B_r(z_0)\subseteq S$.
- $S$ is **open** if every point is interior; **closed** if its complement is open.
- **Closure**: limits of sequences in $S$. **Boundary**: $\bar S\setminus\text{int}\,S$.
- $S$ is **path-connected** if any two points are joined by a continuous path in $S$.
- A **domain** $D$ is open + connected.

We will mainly use *path-connected*. For open sets in $\mathbb{C}$, connected $\iff$ path-connected.

---

## Lecture 5 — Complex Functions, Limits, Continuity

### Complex functions
$f:\text{dom}(f)\subseteq\mathbb{C}\to\mathbb{C}$, $f(z)=u(x,y)+iv(x,y)$. Equivalently, $f$ is a pair $(u,v):\mathbb{R}^2\to\mathbb{R}^2$.

Examples:
- $f(z)=1/z$: $u=\frac{x}{x^2+y^2}$, $v=\frac{-y}{x^2+y^2}$.
- $f(z)=z^2$: $u=x^2-y^2$, $v=2xy$.
- $f(z)=|z|^2$ is real-valued ($v\equiv 0$).

### Limit
Sequential definition: for **every** sequence $z_n\to z_0$ ($z_n\neq z_0$), $f(z_n)\to w_0$. Equivalent $\varepsilon$-$\delta$:
$$\forall\varepsilon>0\ \exists\delta>0:\ 0<|z-z_0|<\delta\Rightarrow|f(z)-w_0|<\varepsilon.$$

**Limit splits into parts**: $\lim f = u_0+iv_0\iff\lim u=u_0$ AND $\lim v=v_0$.

### Continuity
$f$ continuous at $z_0$: $\lim_{z\to z_0} f(z)=f(z_0)$. Sums/products/quotients/compositions of continuous functions are continuous.

### Limits at infinity
There is **one** $\infty$ in $\mathbb{C}$:
- $\lim_{z\to z_0}f(z)=\infty\iff\lim_{z\to z_0}1/f(z)=0$.
- $\lim_{z\to\infty}f(z)=w_0\iff\lim_{z\to 0}f(1/z)=w_0$.
- $\lim_{z\to\infty}f(z)=\infty\iff\lim_{z\to 0}1/f(1/z)=0$.

Compactness lemma: continuous $f$ on a closed bounded set attains its maximum modulus (and is bounded).

---

## Lecture 6 — Differentiability (Real Background) & Complex Derivative

### Real differentiability — refresher
1-D: $g'(x_0)=\lim_{\Delta x\to 0}\frac{g(x_0+\Delta x)-g(x_0)}{\Delta x}$.

In dimension 2: a function $u:\mathbb{R}^2\to\mathbb{R}$ is **differentiable at $(x_0,y_0)$** if there's a linear map $T:\mathbb{R}^2\to\mathbb{R}$ such that
$$u(x_0+\Delta x,y_0+\Delta y)=u(x_0,y_0)+T(\Delta x,\Delta y)+o(\sqrt{\Delta x^2+\Delta y^2}).$$
$T$ is the **differential**, and $T(a,b)=u_x a + u_y b$.

Subtlety: partial derivatives existing $\not\Rightarrow$ differentiable, $\not\Rightarrow$ continuous. **Sufficient condition**: $u_x,u_y$ continuous on a neighborhood ⟹ $u$ differentiable.

Mixed partials: in general $u_{xy}\neq u_{yx}$, but they're **equal if continuous**.

### Complex derivative
$$f'(z_0)=\lim_{\Delta z\to 0}\frac{f(z_0+\Delta z)-f(z_0)}{\Delta z}$$
with $\Delta z\in\mathbb{C}$ — the limit must exist independently of approach direction.

**Theorem**: complex-differentiable at $z_0$ ⟹ both $u,v$ are real-differentiable at $(x_0,y_0)$. Proof writes $\Delta z = \Delta r\,e^{i\theta}$, sets $f'(z_0)=u_0+iv_0$, and shows the difference $u(x_0+\Delta x,y_0+\Delta y)-u(x_0,y_0)-(u_0\Delta x-v_0\Delta y)$ is $o(\Delta r)$.

### Quick examples
- $f(z)=1/z$ ($z\neq 0$): direct computation gives $f'(z) = -1/z^2$.
- $f(z) = \bar z$: limit ratio is $\overline{\Delta z}/\Delta z$, which is $1$ along real axis and $-1$ along imaginary axis. Hence $\bar z$ is **nowhere** differentiable (as a complex function), although $u=x$, $v=-y$ are real-differentiable.
- $f(z)=|z|^2 = z\bar z$: differentiable only at $z=0$, where $f'(0)=0$. Not analytic anywhere.

---

## Lecture 7 — Cauchy–Riemann Equations

### Theorem (Cauchy–Riemann)
$f=u+iv$ is complex-differentiable at $z_0=x_0+iy_0$ **iff** both
1. $u,v$ are real-differentiable at $(x_0,y_0)$, and
2. The Cauchy–Riemann equations hold there:
$$\boxed{u_x=v_y,\qquad u_y=-v_x.}$$

If both hold, $f'(z_0) = u_x + i v_x = v_y - i u_y$.

### Proof sketch
- (⟹) Take $\Delta z=\Delta x$ (real direction): the limit equals $u_x + i v_x$.
  Take $\Delta z = i\Delta y$: the limit equals $\frac1i(u_y+iv_y)=v_y-iu_y$. Equate to get CR.
- (⟸) Use real differentiability of $u,v$ to write $f(z_0+\Delta z)-f(z_0)$ as the linear part plus $o(|\Delta z|)$, then use CR to factor out a single complex multiplier.

### Practical sufficient condition
If $u_x,u_y,v_x,v_y$ are **continuous** on a neighborhood and CR holds, $f$ is differentiable there.

### Rules of differentiation
All real rules carry over identically:
- $(c)' = 0$, $(z)' = 1$, $(z^n)' = n z^{n-1}$.
- $(cf)' = c f'$, $(f+g)' = f'+g'$, $(fg)' = f'g+fg'$, $(f/g)' = (f'g-fg')/g^2$, $(g\circ f)' = g'(f)\,f'$.

---

## Lecture 8 — CR Examples, $\partial/\partial \bar z$, $e^z$

### Detection examples
- $f(z)=\bar z$: $u_x=1,v_y=-1$; CR fails everywhere.
- $f(z)=|z|^2$: CR holds **only at $(0,0)$**; differentiable only at $z=0$.
- A real-valued function that satisfies CR in any open set must be constant (since $u_x=u_y=0$).

### $z, \bar z$ as independent variables
Inverting $z=x+iy$, $\bar z=x-iy$:
$$x=\tfrac12(z+\bar z),\qquad y=\tfrac{1}{2i}(z-\bar z).$$
By the chain rule (formal),
$$\frac{\partial}{\partial z}=\tfrac12(\partial_x - i\partial_y),\qquad \frac{\partial}{\partial\bar z}=\tfrac12(\partial_x+i\partial_y).$$

### CR ⟺ no $\bar z$ dependence
**Theorem**: $f$ satisfies CR at a point iff $\partial f/\partial\bar z=0$ there. Moreover when differentiable, $f' = \partial f/\partial z$.

Quick checks:
- $f(z)=\bar z$: $\partial f/\partial\bar z=1$ — never differentiable.
- $f(z)=|z|^2 = z\bar z$: $\partial f/\partial\bar z=z$, zero only at $z=0$.

### Complex exponential
$$e^z = e^{x+iy} = e^x(\cos y + i\sin y),\quad u=e^x\cos y,\ v=e^x\sin y.$$
$u_x=e^x\cos y=v_y$, $u_y=-e^x\sin y=-v_x$. CR holds, partials continuous ⟹ $e^z$ is **entire** with $(e^z)'=u_x+iv_x=e^z$.

---

## Lecture 9 — CR in Polar, Branches Foreshadowed

### CR in polar coordinates
With $x=r\cos\theta,\ y=r\sin\theta$, the chain rule gives
$$u_r = u_x\cos\theta + u_y\sin\theta,\qquad u_\theta = -u_x r\sin\theta + u_y r\cos\theta,$$
and the same for $v$. Translating CR equations:
$$\boxed{r u_r = v_\theta,\qquad u_\theta = -r v_r.}$$
Then
$$f'(z) = e^{-i\theta}(u_r + i v_r).$$
Derivation: solve the linear system above for $u_x, v_x$ in terms of $u_r, v_r, \theta$, plug into $f'=u_x+iv_x$, simplify.

### Application: $\sqrt{z}$ branch
Let $f(z)=\sqrt r\,e^{i\theta/2}$ on $r>0$, $0<\theta<2\pi$. Compute $u=\sqrt r\cos(\theta/2)$, $v=\sqrt r\sin(\theta/2)$. Verify polar CR holds, partials continuous ⟹ $f$ analytic on this slit plane, and
$$f'(z)=\frac{1}{2f(z)}.$$

### Definition: analytic
$f$ is **analytic at $z_0$** if it's differentiable on some open neighborhood of $z_0$. Analytic on a domain $D$: differentiable everywhere on $D$. **Entire**: analytic on $\mathbb{C}$.

Key distinction: $|z|^2$ is differentiable at $z=0$ only — **not analytic** anywhere because no neighborhood of differentiability.

### Theorem (constancy)
If $f'\equiv 0$ on a domain $D$, then $f$ is constant on $D$. Proof reduces (via CR) to the real analogue: $\nabla u\equiv 0$ on connected $D$ ⟹ $u$ constant.

Corollary chain:
- $f$ and $\bar f$ both analytic on $D$ ⟹ $f$ constant.
- $|f|$ constant on $D$ ⟹ $f$ constant.
- $f$ real-valued and analytic on $D$ ⟹ $f$ constant.

---

## Lecture 10 — Analytic Functions, Harmonic, Möbius Preview

### Harmonic functions
$u:\mathbb{R}^2\to\mathbb{R}$ is **harmonic** if $u_{xx}+u_{yy}=0$ (Laplace's equation) with continuous second partials.

### Theorem (analytic ⟹ harmonic parts)
If $f=u+iv$ analytic on $D$, both $u$ and $v$ are harmonic on $D$.
Proof: differentiate the CR equations again. From $u_x=v_y$, $u_{xx}=v_{yx}$; from $u_y=-v_x$, $u_{yy}=-v_{xy}$. Add: $u_{xx}+u_{yy}=v_{yx}-v_{xy}=0$ (mixed partials equal). Same for $v$.

### Theorem (harmonic conjugate, simply connected case)
If $D$ is **simply connected** and $u$ is harmonic on $D$, there exists $v$ such that $f=u+iv$ is analytic on $D$. Without simply connected, this can fail.

**Counterexample**: $u=\ln|z|$ is harmonic on $\mathbb{C}\setminus\{0\}$. The natural conjugate would be $\theta=\arg z$, but $\arg$ is multi-valued there — no global single-valued $v$ exists.

### Simply connected (working definition)
Domain $D\subseteq\mathbb{C}$ is simply connected iff every closed curve in $D$ contracts to a point inside $D$. Equivalent in $\mathbb{C}$: every simple closed curve $C\subset D$ has its interior also $\subset D$ (no holes).

---

## Lecture 11 — Möbius Transformations

### Definition
$$f(z)=\frac{az+b}{cz+d},\quad ad-bc\neq 0.$$
Domain is $\mathbb{C}\cup\{\infty\}$ via $f(-d/c)=\infty,\ f(\infty)=a/c$.

### Properties
- $f'(z)=\dfrac{ad-bc}{(cz+d)^2}\neq 0$.
- Invertible: $f^{-1}(w)=\dfrac{-dw+b}{cw-a}$ (also Möbius).
- Form a **group** under composition.

### Generators
Every Möbius is a composition of:
1. Translation $z\mapsto z+b$.
2. Dilation $z\mapsto rz$, $r>0$.
3. Rotation $z\mapsto e^{i\theta}z$.
4. Inversion $z\mapsto 1/z$.

For $c\neq 0$ specifically:
$$\frac{az+b}{cz+d}=\frac{bc-ad}{c^2}\cdot\frac{1}{z+d/c}+\frac{a}{c}.$$

### Geometry: circles ↔ circles
**Theorem**: every Möbius transformation maps generalized circles (= circles + lines) to generalized circles. Proof reduces to the case $f(z)=1/z$.

**Detailed example**: image of $\{x=1\}$ under $1/z$. Let $z=1+iy$, then $w=u+iv = (1-iy)/(1+y^2)$, so $u=\frac{1}{1+y^2}$, $v=\frac{-y}{1+y^2}$. Then $u^2+v^2 = u$, i.e., $(u-1/2)^2+v^2 = 1/4$ — circle of radius $1/2$ centered at $1/2$ (passing through origin).

**Algebraic reason**: any generalized circle has equation
$$A(x^2+y^2)+Bx+Cy=D,\quad (A,B,C)\neq 0.$$
Substituting $x=u/(u^2+v^2)$, $y=-v/(u^2+v^2)$ yields an equation of the same form, so circles map to circles.

---

## Lecture 12 — Exponential & Logarithm

### Recap on $e^z$
$e^z = e^x(\cos y + i\sin y)$. Entire, $(e^z)'=e^z$, $|e^{iy}|=1$.

### Image, multiplication, periodicity
- $w_0\in\text{Image}(e^z)\iff w_0\neq 0$. Proof: write $w_0=re^{i\theta}$ ($r>0$), then $z=\ln r + i\theta$ gives $e^z=w_0$.
- $e^{z_1}e^{z_2}=e^{z_1+z_2}$.
- **Periodic**: $e^{z_1}=e^{z_2}\iff z_1-z_2=2n\pi i$, $n\in\mathbb{Z}$. Proof uses moduli + $\arg$ comparison.
- $|e^{-\pi i}|=1$, $e^{-\pi i}=-1$. So $e$ to a complex number can be negative — never zero.

### Logarithm
For $z=re^{i\theta}\neq 0$:
$$\log z=\ln r + i(\theta+2n\pi),\quad n\in\mathbb{Z}.$$
Multivalued. Examples:
- $\log(-1-\sqrt 3 i)$: $r=2$, $\arg = -2\pi/3$, so $\log = \ln 2 + i(-2\pi/3 + 2n\pi)$.
- $\log(1) = 2n\pi i$.
- $\log(-1) = (2n+1)\pi i$.
- $\log(i) = (1/2 + 2n)\pi i$.

### Principal log
$$\operatorname{Log}(z)=\ln r + i\Theta,\ \Theta\in(-\pi,\pi].$$

### Theorem (left/right inverse)
- $e^{\log z} = z$ for any value of $\log z$.
- $\log e^z = z + 2n\pi i$ — multivalued on the right.

### Discontinuity of principal log on negative real axis
Let $a_n = e^{i(\pi - 1/n)}\to -1$ from the upper half. Let $b_n = e^{i(-\pi+1/n)}\to -1$ from below. Then $\operatorname{Log}(a_n)\to\pi i$ but $\operatorname{Log}(b_n)\to -\pi i$. Different limits ⟹ $\operatorname{Log}$ not continuous at $-1$ (or any point on the negative real axis).

### Theorem (analytic on slit plane)
On $D=\{re^{i\theta}: r>0,\ -\pi<\theta<\pi\}$, $\operatorname{Log}(z)$ is analytic with derivative $1/z$. Use polar CR: $u=\ln r$, $v=\theta$, $u_r=1/r$, $u_\theta=0$, $v_r=0$, $v_\theta=1$. Both equations and continuity hold.

---

## Lecture 13 — Branches of Log, Power Function

### Branches
A **branch** of $\log z$ on a domain $D$ is a single-valued analytic function $f$ on $D$ with $f(z)\in\log z$.

For any $\alpha\in\mathbb{R}$, let $D_\alpha=\{re^{i\theta}: r>0,\ \alpha<\theta<\alpha+2\pi\}$. Then $f(z)=\ln r + i\theta$ is a branch on $D_\alpha$, with branch cut $\theta=\alpha$ and derivative $1/z$.

### Why $1/z$ has no antiderivative on $\mathbb{C}\setminus\{0\}$
We will see $\oint_{|z|=1} dz/z = 2\pi i\neq 0$. Equivalently, no single-valued analytic primitive on the punctured plane (it would be a global single-valued log, which doesn't exist).

### Counterexample: $u=\ln|z|$
Harmonic on $\mathbb{C}\setminus\{0\}$ but admits no global analytic $f=u+iv$ (because $v$ would be a global $\arg$). On any slit plane, however, it does — that's $\operatorname{Log}(z)$.

### Power function $z^c$
$$z^c = e^{c\log z}.$$
Multivalued in general. Number of distinct values:
- $c\in\mathbb{Z}$: 1.
- $c=p/q\in\mathbb{Q}$: $q$.
- $c\notin\mathbb{Q}$: $\infty$.

**Branch**: pick any branch of $\log z$ on $D$, then $z^c = e^{c\cdot\text{branch}(\log z)}$ is analytic on $D$ with $(z^c)' = c z^{c-1}$ (using the same branch of $\log$ implicitly).

### Computational examples
- $i^i = e^{i\log i} = e^{i\cdot i(\pi/2 + 2n\pi)} = e^{-\pi/2 - 2n\pi}$ — all real numbers!
- Principal value of $z^i$: $e^{i\operatorname{Log}(z)}=e^{i(\ln r + i\theta)}=e^{-\theta}(\cos(\ln r)+i\sin(\ln r))$. The principal value sends $r$ into the **angle** of the result, and $\theta$ into the modulus — geometric inversion of usual roles.

---

## Lecture 14 — Power vs. Exponential Functions

### Power function $z^c$ properties (collected)
- Defined for $z\neq 0$: $z^c=e^{c\log z}$.
- Multivalued except for $c\in\mathbb{Z}$.
- Branch cuts inherited from $\log$.
- Derivative $c z^{c-1}$ (with consistent branch).

### Exponential with general base
$$c^z=e^{z\log c},\quad c\neq 0.$$
- For each fixed value of $\log c$, this is **entire** (variable $z$ appears outside the log).
- Derivative: $\dfrac{d}{dz}c^z = c^z\cdot\log c$.

If $c=e$ specifically, the canonical choice $\log c=1$ gives the usual $e^z$. Other values of $\log e = 1+2n\pi i$ produce $e^z\cdot e^{2n\pi i z}$ — still entire but distinct.

### Worked example
All branches of $i^z$. $\log i = i(\pi/2+2n\pi)$. Then $i^z = e^{i z(\pi/2 + 2n\pi)}$ — for each $n$ a different entire function.

---

## Lecture 15 — Trig & Hyperbolic Functions, Zeros

### Definitions (complex sin, cos)
$$\sin z = \frac{e^{iz}-e^{-iz}}{2i},\quad \cos z = \frac{e^{iz}+e^{-iz}}{2}.$$
Motivation: matches Euler's formula and Taylor series of real sin/cos.

### Properties
- $(\sin z)'=\cos z$, $(\cos z)'=-\sin z$.
- $\cos(-z)=\cos z$, $\sin(-z)=-\sin z$.
- $e^{iz}=\cos z + i\sin z$.
- $\sin^2 z + \cos^2 z = 1$.
- Addition formulas for $\sin(z_1+z_2)$, $\cos(z_1+z_2)$.

### Unboundedness
$\sin(iy)=i\sinh y$ and $\cos(iy)=\cosh y$, both grow without bound. So **complex sin/cos are NOT bounded** — sharp difference from the real case.

### Zeros are real
- $\sin z = 0\iff e^{iz}=e^{-iz}\iff e^{2iz}=1\iff 2iz = 2n\pi i\iff z = n\pi$.
- $\cos z = 0\iff e^{iz}=-e^{-iz}=e^{iz}e^{i\pi}/e^{2iz}$... cleanly: $\cos z=0\iff z=(n+\tfrac12)\pi$.

So $\tan z=\sin z/\cos z$ is well-defined except at $z=(n+1/2)\pi$, and $\cot z$ except at $z=n\pi$.

### Singular points / zeros — terminology
- $z_0$ is a **zero** of $f$ if $f(z_0)=0$.
- $z_0$ is a **singular point** if $f$ is analytic in a deleted nbhd of $z_0$ but $f$ fails to be analytic at $z_0$ (or is undefined there).
- Example: $f(z)=(z+1)/(z-1)$. Zero at $-1$, singular at $1$.

---

## Lecture 16 — Hyperbolic, Inverse Trig

### Hyperbolic
$$\sinh z=\frac{e^z-e^{-z}}{2},\quad \cosh z=\frac{e^z+e^{-z}}{2}.$$
Same identities as real, plus the connectors:
- $\sinh(iz) = i\sin z$, $\cosh(iz)=\cos z$.
- $\sin(iz) = i\sinh z$, $\cos(iz) = \cosh z$.
- $\cosh^2 z - \sinh^2 z = 1$.
- Zeros: $\sinh z=0\iff z=n\pi i$; $\cosh z=0\iff z=(n+\tfrac12)\pi i$.

Defined: $\tanh z = \sinh z/\cosh z$ (avoid $z=(n+\tfrac12)\pi i$), $\coth z=\cosh z/\sinh z$ (avoid $z=n\pi i$).

### Inverse trig
$\sin^{-1}z$ solves $\sin w = z$. Set $t=e^{iw}$; then $z=(t-1/t)/(2i)$, i.e. $t^2-2izt-1=0$:
$$t = iz + \sqrt{1-z^2}\ (\text{either branch of root}).$$
Hence
$$\sin^{-1}z = -i\log\!\big(iz + (1-z^2)^{1/2}\big).$$
Multivalued (log + square root). On a chosen branch, $(\sin^{-1}z)' = 1/\sqrt{1-z^2}$.

Similarly
$$\cos^{-1}z = -i\log\!\big(z + i(1-z^2)^{1/2}\big).$$

### Looking ahead
Section 40 begins integration. We define the integral of a function $w:[a,b]\to\mathbb{C}$ first, then integrals along contours. Real analysis intuition transfers, but for $f:\mathbb{C}\to\mathbb{C}$ we will only use **one-dimensional** integrals along curves — never area integrals — because the natural object $f(z)\,dz$ has $dz=dx+i\,dy$ (linear in $dx,dy$), unlike a 2-form $dx\wedge dy$.

---

## Lecture 17 — Integrals: $w(t)$, Contours, Definition

### Integral of $w:[a,b]\to\mathbb{C}$
Write $w(t)=u(t)+iv(t)$. Define
$$\int_a^b w(t)\,dt = \int_a^b u\,dt + i\int_a^b v\,dt.$$
Both real integrals must exist.

**Properties** (mirroring real):
- Linearity: $\int(c_1w_1+c_2w_2) = c_1\int w_1 + c_2\int w_2$ for any $c_i\in\mathbb{C}$.
- $\int_a^b = \int_a^c + \int_c^b$.
- **FTC**: if $W:[a,b]\to\mathbb{C}$ has continuous derivative, $\int_a^b W'(t)\,dt = W(b)-W(a)$.

### Modulus inequality
$$\left|\int_a^b w(t)\,dt\right|\le\int_a^b|w(t)|\,dt.$$
**Proof**: if LHS = $r_0 e^{i\theta_0}$, multiply by $e^{-i\theta_0}$ to get $r_0 = \operatorname{Re}\int e^{-i\theta_0}w(t)\,dt = \int\operatorname{Re}(e^{-i\theta_0}w)\,dt$. Then $\operatorname{Re}(e^{-i\theta_0}w)\le|e^{-i\theta_0}w|=|w|$. Done.

### Contours
- $z(t):[a,b]\to\mathbb{C}$ continuous, piecewise differentiable with $z'(t)\neq 0$ except at finitely many corners.
- **Simple**: $z$ injective on $(a,b)$.
- **Closed**: $z(a)=z(b)$.

### Contour integral
$$\int_C f(z)\,dz = \int_a^b f(z(t))\,z'(t)\,dt.$$
Independent of orientation-preserving reparametrization. Reversing orientation flips sign.

### Length
$L(C) = \int_a^b |z'(t)|\,dt$ — derived as the sum of tangent-line segment lengths.

---

## Lecture 19 — Inequalities, Antiderivative Theorem

### ML inequality
If $|f|\le M$ on a contour $C$ of length $L$,
$$\left|\int_C f\,dz\right|\le ML.$$
Proof: $\int_C f\,dz = \int_a^b f(z(t))z'(t)\,dt$, and $|f(z(t))z'(t)|\le M|z'(t)|$.

### Application: $\int_{C_R}\frac{z+1}{(z^2+4)(z^2+9)}\,dz\to 0$
On the upper semicircle $C_R$ ($|z|=R$), $|z+1|\le R+1$ and $|z^2+4||z^2+9|\ge(R^2-4)(R^2-9)$. ML bound:
$$\left|\int_{C_R}\right|\le\pi R\cdot\frac{R+1}{(R^2-4)(R^2-9)}\to 0.$$

### Antiderivative theorem (★ key)
For $f$ continuous on a domain $D$, the following are equivalent:
- (A) $f$ has an antiderivative $F$ on $D$ ($F'=f$).
- (B) $\int_C f\,dz$ depends only on endpoints of $C\subset D$.
- (C) $\oint_C f\,dz = 0$ for every closed contour $C\subset D$.

Under any of these, $\int_{z_1}^{z_2}f\,dz = F(z_2)-F(z_1)$ — the FTC.

### Examples
- $f(z)=e^{iz}$: antiderivative $-ie^{iz}$. So $\int_0^\pi e^{iz}\,dz = -ie^{i\pi}+ie^0 = i+i = 2i$.
- $f(z)=1/z$: **no** antiderivative on $\mathbb{C}\setminus\{0\}$ because $\oint_{|z|=1}dz/z=2\pi i\neq 0$.
- $f(z)=1/z^2$: antiderivative $-1/z$. $\int_{-i}^i dz/z^2 = -1/i + 1/(-i) = 2i$.

### Ahead
On a slit plane (where $\log$ has a branch), $1/z$ does have antiderivative $\operatorname{Log}(z)$.

---

## Lecture 20 — Antiderivative Proof, Cauchy–Goursat (Easy Version)

### Proof of antiderivative theorem
**(A)⟹(B)**: by parametrizing $C$ via $z(t)$, $\int_C f\,dz = \int W'(t)\,dt = W(b)-W(a) = F(z_2)-F(z_1)$.

**(B)⟹(C)**: closed loop has $z_1=z_2$ ⟹ integral zero.

**(C)⟹(A)**: fix $z_0\in D$, define $F(z)=\int_{z_0}^z f\,ds$ (well-defined under (C)). Then for small $\Delta z$,
$$\frac{F(z+\Delta z)-F(z)}{\Delta z}-f(z) = \frac{1}{\Delta z}\int_C(f(s)-f(z))\,ds$$
along a line from $z$ to $z+\Delta z$. By continuity of $f$, $|f(s)-f(z)|<\varepsilon$ for $s$ close. ML bound gives $|\cdot|\le\varepsilon$. So $F'(z)=f(z)$.

### Theorem (Cauchy–Goursat, smooth version)
If $f$ analytic on a region $R$ bounded by a simple closed contour $C$, **and** $f'$ is continuous, then $\oint_C f\,dz=0$.

**Proof via Green's theorem**: $f=u+iv$,
$$\oint_C f\,dz = \oint_C(u\,dx-v\,dy) + i\oint_C(v\,dx+u\,dy).$$
Apply Green's:
$$= \iint_R(-v_x-u_y)\,dA + i\iint_R(u_x-v_y)\,dA.$$
Both integrands vanish by CR.

**Goursat's contribution**: the conclusion holds without assuming $f'$ continuous — analyticity alone suffices.

### Differences to $\mathbb{R}$
- $\mathbb{R}^n$ is always simply connected for $n=1$ (intervals); domains of $\mathbb{C}$ may have holes.
- Continuous $g:\mathbb{R}\to\mathbb{R}$ always has an antiderivative; continuous $f:\mathbb{C}\to\mathbb{C}$ does **not**, in general (we need analyticity + simply connected).
- A differentiable $G:\mathbb{R}\to\mathbb{R}$ may have a non-differentiable derivative; an analytic $f:\mathbb{C}\to\mathbb{C}$ has a derivative that is itself analytic (proved later).

---

## Lecture 21 — Cauchy–Goursat Applications

### Theorem (Cauchy–Goursat)
$f$ analytic on a region bounded by a simple closed contour $C$ ⟹ $\oint_C f\,dz=0$. (Goursat: no assumption of $f'$ continuous needed.)

### Case work for non-simple curves
- Simple closed: direct application.
- Closed with finitely many self-intersections: split into simple closed loops, each contributes $0$, sum is $0$.
- With infinitely many self-intersections: indent slightly to remove the bad part; in the limit, contributions cancel.

### Key corollary: simply connected domains
If $D$ simply connected and $f$ analytic on $D$:
- $\oint_C f\,dz=0$ for every closed $C\subset D$.
- Hence $f$ has an antiderivative on $D$.

### Example
$f(z)=z e^{z^2}$ is entire ⟹ $\oint_C z e^{z^2}\,dz=0$ for any closed $C$.

### Multiply connected: deformation
**Theorem**: If $C_1$ inside $C_2$ are simple closed counterclockwise contours, $f$ analytic on the annular region between them, then
$$\oint_{C_1}f\,dz = \oint_{C_2}f\,dz.$$

**Proof**: cut the annular region with two crosscut segments to make it simply connected with boundary $C_2 - C_1 + (\text{crosscuts cancel})$. Apply Cauchy–Goursat.

### Big example
$\oint_C dz/z = 2\pi i$ for *any* simple closed counterclockwise $C$ around $0$. (Shrink to unit circle, parametrize $z=e^{i\theta}$, integrate $\int_0^{2\pi}i\,d\theta$.)

### General multiply connected version
If $C$ encloses simple closed $C_1,\dots,C_n$ all counterclockwise, $f$ analytic in the region inside $C$ and outside the $C_k$, then
$$\oint_C f\,dz=\sum_k\oint_{C_k}f\,dz.$$

---

## Lecture 22 — Deformation, Onto Cauchy Integral Formula

### Deformation logic recap
The crucial geometric fact: if $f$ is analytic in the region between two simple closed loops, the loops give equal integrals. So we can replace any loop around an isolated singularity by a small standard one (e.g., circle).

### Cauchy Integral Formula (CIF) — statement
Let $C$ be a simple closed counterclockwise contour, $f$ analytic on and inside $C$, $z_0$ in the interior. Then
$$\boxed{f(z_0)=\frac{1}{2\pi i}\oint_C\frac{f(z)}{z-z_0}\,dz.}$$

### Proof
$g(z)=f(z)/(z-z_0)$ has the only singularity at $z_0$. By deformation,
$$\oint_C g\,dz = \oint_{C_\rho} g\,dz$$
where $C_\rho$ is the circle $z=z_0+\rho e^{i\theta}$. Compute
$$\oint_{C_\rho}\frac{f(z)}{z-z_0}\,dz = \int_0^{2\pi}\frac{f(z_0+\rho e^{i\theta})}{\rho e^{i\theta}}\,i\rho e^{i\theta}\,d\theta = i\int_0^{2\pi}f(z_0+\rho e^{i\theta})\,d\theta.$$

By continuity of $f$ at $z_0$, given $\varepsilon>0$ choose $\rho$ small so $|f(z_0+\rho e^{i\theta})-f(z_0)|<\varepsilon$. Then
$$\left|i\int_0^{2\pi}f(z_0+\rho e^{i\theta})\,d\theta - 2\pi i f(z_0)\right|\le 2\pi\varepsilon.$$
Letting $\varepsilon\to 0$, $\oint_C f(z)/(z-z_0)\,dz = 2\pi i f(z_0)$.

### Example
$\oint_{|z|=2}\dfrac{e^z}{z-1}\,dz = 2\pi i\cdot e^1 = 2\pi i e$ (the singularity $z=1$ is inside).

---

## Lecture 23 — Goursat's Proof (No $f'$ Continuity)

### Strategy
Subdivide the closed region $R$ enclosed by $C$ into many small **squares** (and partial squares near the boundary). On each tiny square $\sigma$, pick $z_j\in\sigma$ and write
$$f(z) = f(z_j) + f'(z_j)(z-z_j) + \delta_j(z)(z-z_j),\quad \delta_j(z)\to 0\text{ as }z\to z_j.$$
The first two terms have antiderivatives ($f(z_j)z$ and $f'(z_j)(z-z_j)^2/2$), so their integrals around $\partial\sigma$ vanish. Only the error term contributes:
$$\oint_{\partial\sigma} f\,dz = \oint_{\partial\sigma}\delta_j(z)(z-z_j)\,dz.$$

### Bounding the error
Given $\varepsilon>0$, by analyticity each square can be made small enough that $|\delta_j(z)|<\varepsilon$ throughout. (A careful nested-square / compactness argument is required to show the partition can be chosen uniformly.)

ML estimate: $|\oint_{\partial\sigma}\delta_j(z)(z-z_j)\,dz|\le \varepsilon\cdot(\text{diag}\sigma)\cdot 4(\text{side}\sigma) = 4\sqrt 2\,\varepsilon\,(\text{side}\sigma)^2$.

Summing over squares — interior edges cancel, only $C$ remains — total area times $\varepsilon$ constant:
$$\left|\oint_C f\,dz\right|\le 4\sqrt 2\,\varepsilon\,(M^2 + ML)$$
where $M$ bounds the bounding box, $L$ is length of $C$. Taking $\varepsilon\to 0$ gives $0$.

### Lemma (Bolzano–Weierstrass for nested squares)
If $R_1\supset R_2\supset\cdots$ are nested closed squares with side $\to 0$, the intersection is a single point. Used inside the partition argument.

---

## Lecture 24 — CIF Examples & Generalized CIF

### Two cases for $\oint_C f(z)/(z-z_0)\,dz$
- $z_0$ outside $C$: integrand analytic inside $C$, integral $= 0$.
- $z_0$ inside $C$: integral $= 2\pi i f(z_0)$.

### Generalized CIF (higher derivatives)
For $f$ analytic on and inside a simple closed counterclockwise $C$, $z_0$ inside:
$$\boxed{f^{(n)}(z_0) = \frac{n!}{2\pi i}\oint_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz,\quad n=0,1,2,\dots}$$

### Earth-shattering corollary
**Analytic at $z_0$ ⟹ $f^{(n)}$ exists at $z_0$ for every $n$**. Because: take any small disk where $f$ is analytic; the formula expresses every derivative as an integral along the disk's boundary, which exists.

In particular, the derivative of an analytic function is itself analytic (and hence continuous, repeatedly differentiable, etc.). This is **wildly stronger than real analysis**.

### More corollaries
- If $f$ has an antiderivative $F$ on $D$ (so $F'=f$), then $F$ analytic ⟹ $f=F'$ analytic.
- Continuous $\not\Rightarrow$ has antiderivative, in $\mathbb{C}$. Example: $f(z)=\bar z$ continuous everywhere but has no antiderivative anywhere (it's not analytic anywhere, so no $F$ with $F'=f$ exists).

### Worked CIF example
$\oint_{|z|=1}\dfrac{e^{2z}}{z^4}\,dz$: take $f(z)=e^{2z}$, $z_0=0$, $n=3$. Then $f^{(3)}(0)=8e^0=8$. Integral $=\frac{2\pi i}{3!}\cdot 8 = \frac{8\pi i}{3}$.

---

## Lecture 25 — Generalized CIF Proof, Liouville, FTA

### Proof of generalized CIF
Induction on $n$. Base $n=0$: standard CIF. Inductive step: differentiate with respect to $z_0$ inside the integral. Need to show the limit
$$\frac{f^{(n)}(z_0+\Delta z)-f^{(n)}(z_0)}{\Delta z}\to f^{(n+1)}(z_0)$$
where $f^{(n+1)}(z_0)$ is the formula with $n+1$. Differentiating $g(z)=1/(z-z_0)^{n+1}$ formally: $g'(z)=(n+1)/(z-z_0)^{n+2}$ — exactly what's needed. Detailed estimate uses ML.

### Theorem (Liouville)
If $f$ is **bounded entire**, $f$ is constant.

**Proof**: bounded $|f|\le M$. Apply generalized CIF with $n=1$ on circle $|z|=R$:
$$|f'(z_0)|\le\frac{1!}{2\pi}\cdot 2\pi R\cdot\frac{M}{R^2} = \frac{M}{R}.$$
Letting $R\to\infty$: $f'(z_0)=0$. Since $z_0$ arbitrary, $f$ constant.

### Theorem (Fundamental Theorem of Algebra)
Every non-constant complex polynomial $P(z) = a_0+\cdots+a_n z^n$ ($a_n\neq 0$, $n\ge 1$) has at least one root in $\mathbb{C}$.

**Proof (Liouville)**: assume no root. Then $1/P(z)$ is entire. Show bounded:
- For $|z|$ large, the leading term dominates: $|P(z)|\ge\tfrac12|a_n||z|^n$, so $|1/P|$ small.
- On the closed disk where this fails, $1/P$ continuous on a compact set ⟹ bounded.
Hence $1/P$ entire and bounded ⟹ constant ⟹ $P$ constant. Contradiction.

**Strong form**: $P(z) = a_n(z-z_1)(z-z_2)\cdots(z-z_n)$. By induction: factor out $(z-z_1)$ via polynomial division, apply FTA again to the quotient.

---

## Lecture 26 — Maximum Modulus Principle

### Local lemma
If $f$ analytic on $|z-z_0|<R$ and $|f(z)|\le|f(z_0)|$ for all $z$ in this disk, then $f$ is constant on the disk.

**Proof**: by CIF on circle $|z-z_0|=r<R$,
$$f(z_0)=\frac{1}{2\pi}\int_0^{2\pi}f(z_0+re^{i\theta})\,d\theta\quad(\text{mean value property}).$$
Take absolute values and use $|f(z_0+re^{i\theta})|\le|f(z_0)|$:
$$|f(z_0)|\le\frac{1}{2\pi}\int_0^{2\pi}|f(z_0+re^{i\theta})|\,d\theta\le|f(z_0)|.$$
Equality forces $|f|\equiv|f(z_0)|$ on the circle. This for all $r$ ⟹ $|f|$ constant in the disk. Earlier corollary: $|f|$ const ⟹ $f$ const.

### Maximum modulus principle (global)
If $f$ analytic on a domain $D$ and $|f|$ attains a maximum at some interior $z_0\in D$, $f$ is constant on $D$.

**Proof**: chain disks. Cover any path from $z_0$ to another point $z_1$ by overlapping disks; apply local lemma to propagate "$|f|=|f(z_0)|$" along the chain.

### Corollary
A non-constant analytic function on a closed bounded region attains its max modulus on the **boundary** only.

### Application
$\max_{|z|\le 1}|z^2+1|$: on $|z|=1$, $|e^{2i\theta}+1|$, max when $e^{2i\theta}=1$ giving $|1+1|=2$. So max is $2$.

### Lookahead
Up next: power series, Taylor's theorem (every analytic $=$ its Taylor series in any disk of analyticity), then Laurent series at singular points.

---

## Lecture 27 — Sequences and Series Recap

### Convergent sequences in $\mathbb{C}$
$z_n\to z_0\iff\operatorname{Re}(z_n)\to\operatorname{Re}(z_0)$ AND $\operatorname{Im}(z_n)\to\operatorname{Im}(z_0)$. Convergent ⟹ bounded.

### Convergent series
$\sum z_n$ converges to $S$ if partial sums $S_N=\sum_{n=1}^N z_n$ converge to $S$. Equivalent: real and imaginary parts both converge.

### Necessary condition
$\sum z_n$ converges ⟹ $z_n\to 0$. Contrapositive gives easy divergence tests, e.g. $\sum i^n$ diverges since $|i^n|=1$.

### Absolute convergence
$\sum z_n$ **absolutely converges** if $\sum|z_n|$ converges (a non-negative real series). Absolute ⟹ convergent (transfers from real case via $\operatorname{Re}/\operatorname{Im}$ split).

---

## Lecture 28 — Power Series, Radius of Convergence

### Power series
$$\sum_{n=0}^\infty a_n(z-z_0)^n.$$
With $L=\limsup|a_n|^{1/n}$, define **radius of convergence**
$$R = 1/L\ \in[0,\infty].$$

### Theorem
- If $|z-z_0|<R$, the series converges absolutely.
- If $|z-z_0|>R$, the series diverges.
- For any $r<R$, the series converges **uniformly** on the closed disk $|z-z_0|\le r$.
- Behavior on $|z-z_0|=R$: case by case.

### Examples
- $\sum z^n$: $R=1$. Converges to $1/(1-z)$ for $|z|<1$. On boundary: at $z=1$ diverges, at $z=-1$ diverges, at $z=i$ diverges (oscillates). All boundary points fail.
- $\sum z^n/n$: $R=1$. By Dirichlet's test, converges on $|z|=1$ except at $z=1$.

### Pointwise vs. uniform convergence
$f_n\to f$ **pointwise** on $D$: $\forall z\in D$, $f_n(z)\to f(z)$.
**Uniform**: $\sup_{z\in D}|f_n(z)-f(z)|\to 0$. Uniform preserves continuity.

Example: $\sum z^n$ converges pointwise to $1/(1-z)$ on $|z|<1$ but **not** uniformly (the boundary spoils it). Restricted to $|z|\le r<1$: uniform.

---

## Lecture 29 — Power Series Are Analytic

### Theorem (continuity)
A power series defines a continuous function inside its disk of convergence. Proof uses uniform convergence + continuity of polynomials (the partial sums) + a $3\varepsilon$ triangle-inequality argument.

### Theorem (term-by-term integration)
If $\sum a_n(z-z_0)^n$ has radius $R$, $C$ is any contour in the disk, $g$ continuous on $C$,
$$\int_C g(z)\sum a_n(z-z_0)^n\,dz = \sum a_n\int_C g(z)(z-z_0)^n\,dz.$$
Proof: uniform convergence on $C$ + ML estimate of the tail.

### Theorem (analytic + termwise differentiation)
A power series $f(z)=\sum a_n(z-z_0)^n$ is **analytic** on $|z-z_0|<R$, and
$$f'(z) = \sum_{n=1}^\infty n a_n(z-z_0)^{n-1}.$$
Same radius of convergence.

**Proof uses CIF**: $f$ analytic because $\oint f\,dz=0$ on any closed contour in the disk (term-by-term integration + each $z\mapsto z^n$ analytic). For $f'$, apply CIF derivative:
$$f'(z) = \frac{1}{2\pi i}\oint\frac{f(s)}{(s-z)^2}\,ds = \frac{1}{2\pi i}\sum a_n\oint\frac{(s-z_0)^n}{(s-z)^2}\,ds = \sum n a_n(z-z_0)^{n-1}$$
again by termwise integration.

---

## Lecture 30 — Taylor & Laurent Series

### Taylor's theorem
$f$ analytic on $|z-z_0|<R$ ⟹
$$f(z)=\sum_{n=0}^\infty\frac{f^{(n)}(z_0)}{n!}(z-z_0)^n,\quad |z-z_0|<R.$$
Series converges to $f$ throughout the disk of analyticity.

**Proof**: in $|z-z_0|<R$, take a circle $C_R'$ ($r<R'<R$) around $z_0$. For $|z-z_0|<r$, geometric series:
$$\frac{1}{s-z}=\frac{1}{(s-z_0)-(z-z_0)}=\sum_{n=0}^\infty\frac{(z-z_0)^n}{(s-z_0)^{n+1}}$$
(valid since $|z-z_0|<|s-z_0|$). Substitute into CIF and use generalized CIF for the coefficients.

### Coefficient uniqueness
If $f(z) = \sum a_n(z-z_0)^n$ on a disk, then necessarily $a_n = f^{(n)}(z_0)/n!$.

### Standard Taylor expansions at $z_0=0$
- $1/(1-z)=\sum z^n$, $|z|<1$.
- $e^z=\sum z^n/n!$, all $z$.
- $\sin z=\sum(-1)^n z^{2n+1}/(2n+1)!$, $\cos z=\sum(-1)^n z^{2n}/(2n)!$.
- $\sinh z, \cosh z$ similarly.
- $\log(1+z) = \sum(-1)^{n+1}z^n/n$, $|z|<1$ (principal branch).

### Laurent's theorem
$f$ analytic on annulus $R_1<|z-z_0|<R_2$ ⟹ unique expansion
$$f(z)=\sum_{n=-\infty}^\infty c_n(z-z_0)^n$$
where
$$c_n = \frac{1}{2\pi i}\oint_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz$$
($C$ any positively oriented simple closed contour in the annulus around $z_0$). Splits as **regular part** ($n\ge 0$) + **principal part** ($n<0$).

### Examples
- $f(z)=1/(z(z+1))$: partial fractions $=1/z - 1/(z+1)$. On $0<|z|<1$: expand $1/(z+1)=\sum(-z)^n$, so $f = 1/z - 1 + z - z^2 + \cdots$. Pole of order 1 at $0$.
- $f(z)=\sin z/z^2$: Taylor of $\sin z$ divided by $z^2$ gives $1/z - z/3! + z^3/5! - \cdots$. Pole of order 1 at $0$.
- $f(z)=e^{1/z}$: substitute $1/z$ into $e^w$: $\sum 1/(n!z^n)$. Infinitely many negative powers — essential singularity at $0$.

---

## Lecture 31 — More on Series, Laurent Conventions

### Series operations
On the common region of convergence:
- Term-by-term sum, product (Cauchy product for two series).
- Differentiation: in Taylor case (no neg powers), the series stays the same form, radius preserved. For Laurent, also term-by-term diff.
- Integration along contours: term-by-term as long as contour lies in the region of convergence.

### Practical computation of Laurent
Tricks:
- Partial fractions to isolate simple factors.
- Geometric series substitution: depending on which of $|w|<1$ or $|w|>1$ you need, expand $1/(1-w)$ or $1/(1-w) = -(1/w)\cdot 1/(1-1/w)$.

Example region matters:
- $1/((z-1)(z-2))$ at $z_0=0$:
  - $|z|<1$: $1/(z-1)=-\sum z^n$, $1/(z-2)=-(1/2)\sum(z/2)^n$ ⟹ Taylor.
  - $1<|z|<2$: $1/(z-1) = 1/z\cdot 1/(1-1/z) = \sum z^{-(n+1)}$, $1/(z-2)$ Taylor as before ⟹ Laurent.
  - $|z|>2$: both expand in $1/z$. ⟹ pure Laurent in $1/z$.

### Identity (analytic continuation)
If $f,g$ analytic on a domain $D$ and equal on a set with a limit point in $D$ (e.g., a small disk, an arc, even a sequence converging in $D$), then $f\equiv g$ on $D$. Consequence: power series uniquely determines $f$ on its disk; the function it extends is unique on any larger domain in which it's analytic.

---

## Lecture 32 — Convergence Properties (Cauchy, Uniform, Termwise)

### Continuity of power-series limits
Already used: power series are continuous on their disk of convergence. Restated formally with $\varepsilon$-$\delta$.

### Theorem (uniform-convergence transfer)
If $\sum f_n$ converges uniformly to $f$ on a contour $C$ and each $f_n$ is continuous on $C$:
- $\int_C f\,dz = \sum\int_C f_n\,dz$.
- $f$ is continuous on $C$.

### Termwise differentiation revisited
If $\sum f_n(z)$ converges to $f(z)$ on a domain $D$, $\sum f_n'(z)$ converges uniformly on compact subsets ⟹ $f'(z) = \sum f_n'(z)$.

For analytic series, this just says **inside the radius**, all the operations are legal.

### Uniform on closed sub-disks
Power series are uniformly convergent on any closed disk strictly inside the disk of convergence. Crucial for term-by-term analysis.

---

## Lecture 33 — Residues and the Residue Theorem

### Definition of residue
For $f$ analytic in a deleted neighborhood $0<|z-z_0|<r$ (so $z_0$ is an isolated singular point), the Laurent expansion has a coefficient $b_1$ on $(z-z_0)^{-1}$. Define
$$\operatorname{Res}_{z=z_0} f := b_1.$$

Equivalently, $\operatorname{Res}_{z=z_0}f = \frac{1}{2\pi i}\oint_C f(z)\,dz$ for any small simple closed counterclockwise $C$ around $z_0$ inside the deleted nbhd.

### Cauchy's residue theorem
Let $C$ be simple closed counterclockwise, $f$ analytic on and inside $C$ except at finitely many isolated singular points $z_1,\dots,z_n$ inside. Then
$$\oint_C f(z)\,dz = 2\pi i\sum_{k=1}^n \operatorname{Res}_{z=z_k} f.$$

**Proof**: surround each $z_k$ with a small disjoint circle $C_k$ inside $C$. $f$ analytic in the multiply-connected region between $C$ and the $C_k$. By the multiply-connected theorem,
$$\oint_C f\,dz = \sum_k \oint_{C_k}f\,dz = 2\pi i\sum_k b_1^{(k)}.$$

### Residue at $\infty$
For $f$ analytic on $|z|>R_0$, set
$$\operatorname{Res}_{z=\infty}f = -\operatorname{Res}_{w=0}\frac{1}{w^2}f(1/w).$$
And: $\oint_C f\,dz = -2\pi i \operatorname{Res}_{z=\infty}f$ for any $C$ enclosing all finite singularities.

Useful when $f$ has many finite singularities but a clean expansion in $1/z$ around $\infty$.

---

## Lecture 34 — Behavior Near Singularities, Computing Residues

### Three types of isolated singularities
By Laurent at $z_0$:
- **Removable**: principal part $=0$. $f$ extends analytically (Riemann's removable-singularity theorem: bounded near $z_0$ ⟹ removable).
- **Pole of order $m\ge 1$**: principal part has finitely many terms, with $b_m\neq 0$ the largest negative power. Equivalent: $\lim_{z\to z_0}|f(z)|=\infty$, and $(z-z_0)^m f(z)$ has a removable singularity at $z_0$ with non-zero limit.
- **Essential**: infinitely many non-zero $b_n$. **Casorati–Weierstrass**: the image of any deleted neighborhood is dense in $\mathbb{C}$ (and Picard: it omits at most one value).

### Zeros / poles relationship
- $f$ has zero of order $m$ at $z_0$ iff $f(z) = (z-z_0)^m g(z)$, $g$ analytic with $g(z_0)\neq 0$.
- Zeros of an analytic non-zero function are **isolated**.
- If $f_1(z_0)\neq 0$ and $f_2$ has zero of order $m$ at $z_0$, then $f_1/f_2$ has pole of order $m$.

### Computing residues — toolkit

**Simple pole** ($m=1$):
$$\operatorname{Res}_{z=z_0}f = \lim_{z\to z_0}(z-z_0)f(z).$$

**Quotient at simple pole**: $f=p/q$ with $p(z_0)\neq 0$, $q(z_0)=0$, $q'(z_0)\neq 0$:
$$\operatorname{Res}_{z=z_0}\frac{p}{q} = \frac{p(z_0)}{q'(z_0)}.$$
Derivation: $q(z) = q'(z_0)(z-z_0)+\cdots$, so $(z-z_0)f\to p(z_0)/q'(z_0)$.

**Pole of order $m$**: let $\varphi(z)=(z-z_0)^m f(z)$ (analytic at $z_0$, $\varphi(z_0)\neq 0$):
$$\operatorname{Res}_{z=z_0}f = \frac{\varphi^{(m-1)}(z_0)}{(m-1)!}.$$

**Caution**: if you guess the wrong order, the formula fails. E.g., $(1-\cos z)/z^3$ at $z=0$ — looks order 3 but $1-\cos z = z^2/2 - z^4/24+\cdots$ so it's actually a pole of order 1 with residue $1/2$.

### Quick examples
- $f(z)=(z+4)/(z^2+1)$ at $z=i$: $q(z)=z^2+1$, $q'(i)=2i$, $p(i)=i+4$, residue $=(i+4)/(2i) = 1/2 - 2i$.
- $f(z) = z^3/(z-i)^3$ at $z=i$: $\varphi(z)=z^3$, $\varphi''(z)=6z$, residue $=6i/2 = 3i$.

---

## Lecture 35 — Real Integrals via Residues (Rational)

### Improper integrals in $\mathbb{R}$
$\int_0^\infty f\,dx = \lim_{R\to\infty}\int_0^R f\,dx$. Symmetric / Cauchy principal value:
$$\operatorname{PV}\int_{-\infty}^\infty f\,dx = \lim_{R\to\infty}\int_{-R}^R f\,dx.$$
If the integral exists in the usual sense, PV equals it. PV may exist when integral doesn't (e.g., $\int_{-\infty}^\infty x\,dx$ has PV $=0$). For **even** $f$: existence of PV equals existence of integral (and equals $2\int_0^\infty f$).

### Strategy for rational $f=P/Q$ with $\deg Q\ge\deg P+2$, no poles on $\mathbb{R}$
1. Extend to $f(z)$ in $\mathbb{C}$.
2. Contour: real segment $[-R,R]$ + upper semicircle $C_R$.
3. Residue theorem: $\oint = 2\pi i\sum_{\text{UHP poles}}\operatorname{Res}$.
4. ML on $C_R$: $|f|\le M/R^2$, length $\pi R$ ⟹ $\int_{C_R}\to 0$.
5. So $\operatorname{PV}\int_{-\infty}^\infty f\,dx = 2\pi i\sum\operatorname{Res}$.
6. If $f$ even, divide by 2 to get $\int_0^\infty$.

### Worked example
$\int_0^\infty\frac{dx}{x^6+1}$. Poles of $1/(z^6+1)$: $z_k=e^{i(2k+1)\pi/6}$, $k=0,\dots,5$. UHP poles: $z_0=e^{i\pi/6}$, $z_1=e^{i\pi/2}=i$, $z_2=e^{i\,5\pi/6}$. Each is a simple pole; using $q'=6z^5$:
$$\operatorname{Res}_{z_k}=\frac{1}{6z_k^5}=-\frac{z_k}{6}\quad(\text{since }z_k^6=-1\Rightarrow z_k^5=-1/z_k).$$
Sum: $z_0+z_1+z_2 = (\tfrac{\sqrt 3}{2}+\tfrac i2)+i+(-\tfrac{\sqrt 3}{2}+\tfrac i2)=2i$. So sum of residues $=-2i/6=-i/3$, and
$$2\pi i\cdot(-i/3)=2\pi/3 \Rightarrow \int_{-\infty}^\infty = 2\pi/3 \Rightarrow \int_0^\infty = \pi/3.$$

---

## Lecture 36 — Trig Integrals & Jordan's Lemma

### Idea
For real integrands containing $\cos ax,\sin ax$, use $e^{iaz}$ in the complex extension because $|e^{iaz}|=e^{-ay}\le 1$ on the upper half-plane (for $a>0$). Then take real/imag part.

### Worked example (ML works)
$\int_{-\infty}^\infty\dfrac{\cos 2x}{(x^2+4)^2}\,dx$. Extend to $f(z)=e^{2iz}/(z^2+4)^2$. Pole of order 2 at $z=2i$ in UHP. With $\varphi(z)=e^{2iz}/(z+2i)^2$:
$$\varphi'(z) = e^{2iz}\frac{2i(z+2i)-2}{(z+2i)^3}.$$
At $z=2i$: $\varphi'(2i) = e^{-4}\cdot\dfrac{2i\cdot 4i-2}{(4i)^3}=\frac{-10\,e^{-4}}{-64i}=\frac{5e^{-4}}{32i}$.
Hence residue $=5e^{-4}/(32i)$, $2\pi i\cdot\text{Res}=5\pi/(16e^4)$. ML on $C_R$ gives $\int_{C_R}\to 0$. Take real part: $\int_{-\infty}^\infty=5\pi/(16e^4)$. By evenness $\int_0^\infty\frac{\cos 2x}{(x^2+4)^2}dx = 5\pi/(32e^4)$.

### When ML isn't enough — Jordan's lemma
**Setup**: integrand $g(z)e^{iaz}$ where $g$ decays slowly (e.g., degree gap = 1).

**Jordan's inequality**: $\sin\theta\ge 2\theta/\pi$ for $\theta\in[0,\pi/2]$.

**Lemma (Jordan)**: $g$ analytic on UHP outside some disk, $\max_{|z|=R}|g(z)|=M_R\to 0$. For $a>0$:
$$\int_{C_R}g(z)e^{iaz}\,dz\to 0\ (R\to\infty).$$
Proof bound:
$$\left|\int_{C_R}\right|\le M_R\cdot R\int_0^\pi e^{-aR\sin\theta}\,d\theta\le M_R\cdot R\cdot 2\int_0^{\pi/2}e^{-2aR\theta/\pi}\,d\theta = M_R\cdot\frac\pi a(1-e^{-aR})\le \frac{\pi M_R}{a}\to 0.$$

### Worked example needing Jordan
$\int_{-\infty}^\infty\dfrac{x\sin 2x}{x^2+3}\,dx$. Use $f(z) = ze^{2iz}/(z^2+3)$. Pole at $z=i\sqrt 3$. Residue (simple pole, use $p/q'$): $i\sqrt 3\,e^{2i\cdot i\sqrt 3}/(2i\sqrt 3) = e^{-2\sqrt 3}/2$.
$2\pi i\cdot\text{Res} = i\pi e^{-2\sqrt 3}$. Big arc: $|g(z)|=|z|/|z^2+3|\sim 1/R\to 0$, so Jordan kills it. Take imaginary part: $\int_{-\infty}^\infty = \pi e^{-2\sqrt 3}$, halve for $[0,\infty)$: $\int_0^\infty x\sin 2x/(x^2+3)\,dx = \frac\pi2 e^{-2\sqrt 3}$.

---

## Lecture 37 — Indented Paths, Branch Cut Contours

### Pole on real axis: indent contour
**Lemma**: $f$ has a simple pole at $x_0\in\mathbb{R}$ with residue $b_1$. Let $C_\rho$ be the small clockwise upper semicircle $z=x_0+\rho e^{-i\theta}$, $\theta\in[-\pi,0]$. Then
$$\lim_{\rho\to 0^+}\int_{C_\rho}f(z)\,dz = -i\pi b_1.$$
(Counterclockwise upper indent gives $+i\pi b_1$; pi instead of 2pi because we traverse only half.)

**Proof**: $f(z) = b_1/(z-x_0)+g(z)$ with $g$ analytic at $x_0$. The integral of $g$ vanishes as $\rho\to 0$. Direct computation gives $\int_{C_\rho}b_1/(z-x_0)\,dz = b_1\cdot(-i\pi)$.

### Dirichlet integral (classical)
$\int_0^\infty\frac{\sin x}{x}\,dx = \pi/2$.

**Method**: $f(z) = e^{iz}/z$ has simple pole on real axis at $0$. Contour: $-R\to-\rho$ on real axis, indent $C_\rho$ above $0$ (clockwise small semicircle), $\rho\to R$ on real axis, big semicircle $C_R$ back. No poles inside ⟹ $\oint = 0$. As $R\to\infty$, $\int_{C_R}\to 0$ by Jordan. As $\rho\to 0$, $\int_{C_\rho}\to-i\pi\operatorname{Res}_{z=0}=-i\pi$. So
$$\operatorname{PV}\int_{-\infty}^\infty\frac{e^{ix}}{x}\,dx = i\pi.$$
Imag part: $\operatorname{PV}\int_{-\infty}^\infty\sin x/x\,dx = \pi$. By evenness, $\int_0^\infty = \pi/2$.

### Branch-cut "keyhole" contours
For $\int_0^\infty\dfrac{x^{-a}}{x+1}\,dx$, $0<a<1$:
- $f(z) = z^{-a}/(z+1)$ with branch of $z^{-a}$ defined for $0<\arg z<2\pi$ (cut along positive real axis).
- Contour: just above cut ($\rho\to R$), big circle $C_R$ counterclockwise, just below cut ($R\to\rho$), small circle $C_\rho$ clockwise around $0$.
- One pole inside: $z=-1=e^{i\pi}$. $\operatorname{Res}_{z=-1}=e^{-i\pi a}$.
- $\int_{C_R}\to 0$, $\int_{C_\rho}\to 0$ (need $0<a<1$).
- Above cut: $z^{-a}=x^{-a}$. Below cut: $z^{-a}=x^{-a}e^{-2\pi i a}$ — and the segment is reversed.
- $\oint = (1-e^{-2\pi i a})\int_0^\infty\frac{x^{-a}}{x+1}\,dx = 2\pi i\,e^{-i\pi a}$.
- Solve: $\int_0^\infty\frac{x^{-a}}{x+1}\,dx = \dfrac{2\pi i\,e^{-i\pi a}}{1-e^{-2\pi i a}} = \dfrac{2\pi i}{e^{i\pi a}-e^{-i\pi a}} = \dfrac{\pi}{\sin\pi a}.$

This is the **reflection formula** for $\Gamma$ in disguise.

### Master toolkit (last words)
You now have four contour patterns covering most exam problems:
1. Real line + UHP semicircle, ML kills the arc — **rational with degree gap ≥ 2**.
2. Same, $e^{iaz}$ swap, ML or Jordan — **trig × rational**.
3. Indented contour around real pole — adds $-i\pi\operatorname{Res}$ — **principal-value integrals like $\sin x/x$**.
4. Keyhole around branch cut — exploits multivaluedness — **$x^a$ × rational**.

Plus the foundational ideas: Cauchy–Goursat, Cauchy integral formula and its derivative form, residue theorem, Liouville, FTA, max modulus, Taylor and Laurent expansions, branch cuts for log and powers — all sitting on top of the single observation that complex differentiability is direction-independent and forces the Cauchy–Riemann equations.

---

*End of notes — 37 lectures.*
