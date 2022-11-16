import matplotlib.pyplot as plt

def plError(input):
    plErrorString = "PLOT(matplotlib): "
    print(plErrorString+input)

def canvasPlot(canvas,picture,aspectRatio,figSize,size,inferno=True):
    if canvas.res > 2000:
        plError(f"WARNING: Canvas resolution is {canvas.res}, this can possibly make plotting slow!")
    plError("Plotting.....")
    plt.figure(figsize=(figSize,figSize*aspectRatio))
    if inferno:
        plt.pcolormesh(canvas.xv,canvas.yv,picture,cmap="inferno")
    else:
        plt.pcolormesh(canvas.xv,canvas.yv,picture)
    plt.xlim(-size,size)
    plt.ylim(-size*aspectRatio,size*aspectRatio)
    plError("Plot done!")
    plt.show()
    plError("Plot closed! Moving on.")