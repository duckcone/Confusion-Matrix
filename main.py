import tkinter.ttk as ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sklearn.metrics import roc_curve, auc
import random
import scipy.stats


fig = plt.Figure(figsize=(10,10), dpi=80)
fig1 = plt.Figure(figsize=(5,5), dpi=70)
fig2 = plt.Figure(figsize=(5,5), dpi=70)
fig3 = plt.Figure(figsize=(5,5), dpi=70)

ax=fig.add_subplot(221)
ax1=fig.add_subplot(222)
ax2=fig.add_subplot(223)
ax3=fig.add_subplot(224)

window = tk.Tk()
window.title("Graph")
window.geometry("1200x800")

data_size = 500

def draw():
    ax.cla()
    ax1.cla()
    ax2.cla()
    ax3.cla()

    np.random.seed(0)
    
    TN = 0
    FP = 0
    FN = 0
    TP = 0
    critical_point = roc_scale.get()

    

    datay=list()
    data=list()
    datax1=list()
    datax2=list()
    datax=list()

    for i in range(data_size):
        datay.append(0)
    
    # print(datay)
    for i in range(data_size):
        datay.append(1)

    mu1 = mu1_scale.get()
    sigma1 = 1
    mu2 = mu2_scale.get()
    sigma2 = 1

    datax1 = list(np.random.normal(mu1, sigma1, data_size))
    datax2 = list(np.random.normal(mu2, sigma2, data_size))
    datax1.sort()
    datax2.sort()
    datax = datax1 + datax2

    for i in range(data_size):
        if(datax2[i] > critical_point):
            TP += 1
        else:
            FN += 1
        
        if(datax1[i] > critical_point):
            FP += 1
        else:
            TN += 1

        sensitivity = TP / (TP + FN)
        specificity = TN / (TN + FP)

    

    _, bins_edge1, _ = ax1.hist(datax1, bins=50, density=True, alpha=0.5)
    _, bins_edge2, _ = ax3.hist(datax2, bins=50, density=True, alpha=0.5)
    ax2.hist(datax1, bins=50, density=True, alpha=0.5)
    ax2.hist(datax2, bins=50, density=True, alpha=0.5)


    normpdf1 = scipy.stats.norm.pdf(bins_edge1, mu1, sigma1)
    normpdf2 = scipy.stats.norm.pdf(bins_edge2, mu2, sigma2)


    fpr,tpr,t =roc_curve(datay,datax)
    roc_auc = auc(fpr,tpr)

    lw = 3
    ax.plot(fpr, tpr, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    ax.plot([0.0, 1.0], [0.0, 1.0], color='navy', lw=lw, linestyle='--')
    ax.plot(1-specificity, sensitivity,  color='red', lw=1, marker='o', label='TPR=%.2f, FPR=%.2f' % (sensitivity,1-specificity))
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver operating characteristic example')
    ax.legend(loc="lower right")

    ax1.plot(bins_edge1,normpdf1, color='blue', lw=lw, label=' µ1=%0.2f, σ1=%0.2f' % (mu1, sigma1))
    ax1.plot([roc_scale.get(), roc_scale.get()], [0.0, 0.7], color='black', linestyle='--')
    ax1.set_xlim([-8, 8])
    ax1.set_ylim([0.0, 0.5])
    ax1.legend(loc="lower right")

    ax2.plot(bins_edge1,normpdf1, color='blue')
    ax2.plot(bins_edge2,normpdf2, color='red')
    ax2.plot([roc_scale.get(), roc_scale.get()], [0.0, 0.7], color='black', linestyle='--')
    ax2.set_xlim([-8, 8])
    ax2.set_ylim([0.0, 0.5])
    # ax2.plot([roc_slide.val, roc_slide.val], [0.0, 0.7], color='black', linestyle='--')

    ax3.plot(bins_edge2,normpdf2, color='red', lw=lw, label=' µ2=%0.2f, σ2=%0.2f' % (mu2, sigma2))
    ax3.plot([roc_scale.get(), roc_scale.get()], [0.0, 0.7], color='black', linestyle='--')
    ax3.set_xlim([-8, 8])
    ax3.set_ylim([0.0, 0.5])
    ax3.legend(loc="lower right")

    canvas.draw()
    window.after(100, draw)


frame_1 = tk.LabelFrame(window,labelanchor="nw",text="圖表",foreground="green")
frame_1.grid(row=0, column=0)

canvas = FigureCanvasTkAgg(fig, master = frame_1)
canvas.get_tk_widget().grid(row=0, column=0)
canvas.draw()

frame_2 = tk.LabelFrame(window,labelanchor="nw",text="參數調整",foreground="green")
frame_2.grid(row=0, column=1, sticky="nwse")

# mu1_var.trace("w",graph)
text_mu1=tk.Label(frame_2,text="µ1 of graph 1:")
text_mu1.grid(row=0,column=0)
mu1_scale =tk.Scale(frame_2,from_=-5,to=5,length=200,resolution = 0.01, orient="h")
mu1_scale.set(0)
mu1_scale.grid(row=1, column=0)

text_mu2=tk.Label(frame_2,text="µ2 of graph 2:")
text_mu2.grid(row=2,column=0)
mu2_scale =tk.Scale(frame_2,from_=-5,to=5,length=200,resolution = 0.01, orient="h")
mu2_scale.set(1)
mu2_scale.grid(row=3, column=0)

text_roc=tk.Label(frame_2,text="Slide to get ROC point:")
text_roc.grid(row=4,column=0)
roc_scale =tk.Scale(frame_2,from_=-8,to=8,length=200,resolution = 0.01,orient="h")
roc_scale.set(0.5)
roc_scale.grid(row=5, column=0)

window.after(100, draw)

window.mainloop()