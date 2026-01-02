import maya.cmds as cmds
import math

root = 'Root'
fps = 30.0

# Ensure scene is 30 fps
cmds.currentUnit(time='ntsc')

# Add Speed attribute if it doesn't exist
if not cmds.attributeQuery('Speed', node=root, exists=True):
    cmds.addAttr(root, ln='Speed', at='double', k=True)
    cmds.setAttr(f'{root}.Speed', e=True, k=True)
    
# Frame range
start = int(cmds.playbackOptions(q=True, min=True))
end   = int(cmds.playbackOptions(q=True, max=True))

def distance(p1, p2):
    return math.sqrt(
        (p2[0]-p1[0])**2 +
        (p2[1]-p1[1])**2 +
        (p2[2]-p1[2])**2
    )

# Calculate and key speed
for f in range(start, end):
    cmds.currentTime(f)
    p1 = cmds.xform(root, q=True, ws=True, t=True)

    cmds.currentTime(f + 1)
    p2 = cmds.xform(root, q=True, ws=True, t=True)

    dist_per_frame = distance(p1, p2)          # cm/frame
    speed = dist_per_frame * fps                # cm/sec

    cmds.setKeyframe(
        root,
        attribute='Speed',
        time=f,
        value=speed
    )

print("Speed attribute keyed successfully.")
