"""Rebuild the vector figures shared by Chapter 8 and the Beamer deck."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy.special import expit

OUT = Path(__file__).resolve().parents[1] / "figures" / "ch8"
OUT.mkdir(exist_ok=True)
BLUE, TEAL, ORANGE, INK = "#205987", "#007C78", "#AD5015", "#16324F"
plt.rcParams.update({
    "font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12,
    "legend.fontsize": 11, "legend.frameon": False,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#8A99A5", "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "pdf.fonttype": 42,
})

inputs = np.array([1., 2.])
targets = np.array([.8, .6])

def individual_gradients(a):
    return inputs * (expit(a * inputs) - targets)

def loss(a):
    logits = np.asarray(a)[..., None] * inputs
    return np.mean(np.logaddexp(0, logits) - targets * logits, axis=-1)

optimum = brentq(lambda a: individual_gradients(a).mean(), 0, 1)
start = np.log(4.)

def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight", pad_inches=.05)
    plt.close(fig)

def distillation():
    fig, ax = plt.subplots(figsize=(8.8, 3.05), layout="constrained")
    grid = np.linspace(.02, 1.53, 300)
    ax.plot(grid, loss(grid), color=BLUE, lw=2)
    steps = [start]
    for _ in range(5):
        steps.append(steps[-1] - individual_gradients(steps[-1]).mean())
    ax.scatter(steps, loss(steps), s=40, color=ORANGE, zorder=3)
    for k, offset in [(0,(-28,8)), (1,(-2,11)), (2,(-3,11))]:
        ax.annotate(f"step {k}", (steps[k],loss(steps[k])), xytext=offset,
                    textcoords="offset points", ha="center", color=ORANGE)
    ax.scatter(optimum,loss(optimum),marker="D",s=36,color=TEAL,zorder=4)
    ax.annotate("minimum", (optimum,loss(optimum)), xytext=(-55,16),
                textcoords="offset points", color=TEAL,
                arrowprops={"arrowstyle":"-", "color":TEAL})
    ax.set(xlabel="Student parameter  $a$", ylabel="Mean cross-entropy (nats)",
           xlim=(0,1.58), ylim=(.625,.925))
    save(fig, "student-descent")

def parabola():
    fig, axes = plt.subplots(1,2,figsize=(9.2,3.15),layout="constrained")
    k=np.arange(9)
    for eta, color, shape, style in [(.5,BLUE,'o','-'),(1.5,ORANGE,'x','--')]:
        w=4*(1-eta)**k
        axes[0].plot(k,w,style,marker=shape,color=color,label=fr"$\eta={eta}$")
    axes[0].axhline(0, lw=.6, color=INK)
    axes[0].set(ylabel="Parameter  $w_k$",title="Two parameter paths")
    axes[0].legend()
    w=4*.5**k
    axes[1].plot(k,w**2/2,'o-',color=TEAL)
    axes[1].set(yscale="log", ylabel="Loss (log scale)",title="Both paths have the same loss")
    for ax in axes:
        ax.set(xlabel="Update  $k$", xticks=range(0,9,2))
    save(fig,"parabola")

def valley_path(eta,beta,steps=24):
    w=np.array([4.,1.])
    m=np.zeros(2)
    path=[w.copy()]
    for _ in range(steps):
        m=beta*m+(1-beta)*np.array([w[0],20*w[1]])
        w=w-eta*m
        path.append(w.copy())
    return np.array(path)

def contours(ax, height=1.25, levels=(.08,.3,.8,2,4,7,11,17,24)):
    us=np.linspace(-1.25,4.7,180); vs=np.linspace(-height,height,180)
    u,v=np.meshgrid(us,vs)
    ax.contour(u,v,(u**2+20*v**2)/2,
               levels=levels,colors="#AFBFC9",linewidths=.8)
    ax.scatter(0,0,color=TEAL,marker="*",s=110,zorder=4)
    ax.set(xlim=(us[0],us[-1]),ylim=(vs[0],vs[-1]),xlabel="Parameter  $u$",
           ylabel="Parameter  $v$",yticks=[-1,0,1] if height<2 else [-5,0,5])

def valleys():
    fig, axes=plt.subplots(1,2,figsize=(9.3,3.05),layout="constrained")
    for ax, eta, color, title in zip(
        axes, [.09, .11], [BLUE, ORANGE],
        [r"Stable step  $\eta=0.09$", r"Unstable step  $\eta=0.11$"],
    ):
        if eta == .09:
            contours(ax)
        else:
            contours(ax, height=5.6, levels=[.8,4,11,24,60,130,230])
        path = valley_path(eta, 0, 9)
        ax.plot(*path.T, "o-", color=color, ms=4)
        ax.set_title(title)
    save(fig,"valley-steps")
    fig, axes=plt.subplots(1,2,figsize=(9.3,3.05),layout="constrained",sharey=True)
    for ax,eta,beta,color,title in zip(axes,[.09,.16],[0.,.5],[BLUE,ORANGE],
                                       ["Gradient descent","Momentum"]):
        contours(ax)
        p=valley_path(eta,beta,12)
        ax.plot(*p.T,"o-",color=color,ms=4,lw=1.6)
        ax.scatter(*p[-1],color=color,edgecolor=INK,s=56,zorder=4)
        ax.set_title(title)
    axes[1].set_ylabel("")
    save(fig,"momentum")

def batches():
    fig,ax=plt.subplots(figsize=(8.8,3.2),layout="constrained")
    indices=np.random.default_rng(28).integers(0,2,size=(65,16))
    for batch, color, title in [(1,ORANGE,"One example"),(16,BLUE,"Batch of 16")]:
        a=optimum; path=[a]
        for row in indices:
            a-=.35*individual_gradients(a)[row[:batch]].mean()
            path.append(a)
        ax.plot(path,color=color,lw=1.8,label=title)
    ax.axhline(optimum,color=TEAL,lw=1.8,ls="--",label="Full gradient")
    ax.legend(loc="upper left",ncols=3,bbox_to_anchor=(0,1.2))
    ax.set(xlabel="Update",ylabel="Student parameter  $a$",xlim=(0,len(indices)))
    save(fig,"batch-paths")

if __name__=="__main__":
    distillation()
    parabola()
    valleys()
    batches()
