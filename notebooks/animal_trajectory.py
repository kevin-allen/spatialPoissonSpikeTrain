import numpy as np
import matplotlib.pyplot as plt

def pickRandomAngle():
    # pick a random number between -np.pi to np.pi
    return np.random.uniform(low=-np.pi, high=np.pi, size=1)[0]

def nextStepPosition(current_Xpos,current_Ypos,current_hd,stepSizeRatio):
    """
    Go from current position to the next position.
    """
    x = current_Xpos + np.cos(current_hd)*stepSizeRatio
    y = current_Ypos + np.sin(current_hd)*stepSizeRatio
    return x,y
    
def isInBox(x,y,boxSize=80):
    """
    Test if x and y are in the box
    """
    if x > 0 and x < boxSize and y > 0 and y < boxSize:
        return True
    else:
        return False
def addHdNoise(hd,noiseLevel=0.1):
    """
    Add some noise to the head direction of the animal. Used to have more natural path (not straight line but also not random)
    """
    x = hd + np.random.uniform(low=-0.2, high=0.2, size=1)[0]
    
    # restrict to -np.pi and np.pi, using arctan2
    return np.arctan2(np.sin(x), np.cos(x))

def walk(samples,boxSize,stepSizeRatio=0.5):
    """
    Generate the animal path. The head direction is the same as heading.
    
    Arguments
    samples: how many data points
    boxSize: size of the square box
    stepSizeRatio: by default the steps are 1 unit, this ratio is used to change this.
    
    Returns
    Xpos: 1D numpy array with x position
    Ypos: 1D numpy array with y position
    hd: 1D numpy array with head direction
    """
    Xpos = np.empty(samples)
    Ypos = np.empty(samples)
    hd = np.empty(samples)
    current_Xpos= boxSize/2
    current_Ypos= boxSize/2
    current_hd = pickRandomAngle()
    
    for i in range(samples):
    
        # add a bit of noise to the head direction
        current_hd = addHdNoise(current_hd)
        # possible new position
        x,y = nextStepPosition(current_Xpos,current_Ypos,current_hd,stepSizeRatio)
        # if out of the box, find a new head direction
        while(not isInBox(x,y)): 
            current_hd = pickRandomAngle()
            x,y = nextStepPosition(current_Xpos,current_Ypos,current_hd,stepSizeRatio)
        # assigned the new position for next iteration
        current_Xpos=x
        current_Ypos=y
        # save the results
        Xpos[i]=current_Xpos
        Ypos[i]=current_Ypos
        hd[i] = current_hd
    
    return Xpos,Ypos,hd

def plotPath(Xpos,Ypos,hd):
    fig,ax =plt.subplots(1,4,figsize=(20,5))
    ax[0].plot(Xpos,Ypos)
    ax[0].set_xlabel("xPos")
    ax[0].set_ylabel("xPos")
    ax[1].hist(Xpos,bins=20)
    ax[1].set_xlabel("xPos")
    ax[1].set_ylabel("Count")
    ax[2].hist(Ypos,bins=20)
    ax[2].set_xlabel("yPos")
    ax[2].set_ylabel("Count")
    ax[3].hist(hd,bins=20)
    ax[3].set_xlabel("hd")
    ax[3].set_ylabel("Count")
    plt.show()
