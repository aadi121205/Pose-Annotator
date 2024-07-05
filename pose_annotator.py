import cv2
import os
import json
from matplotlib import pyplot as plt

# Function to update keypoints interactively
def update_keypoints_interactively(img, keypoints, keypoints_path):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    circles = []

    # Draw initial keypoints
    for point in keypoints:
        if point != [0, 0]:
            cv2.putText(img, str(keypoints.index(point)), tuple(point), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            circle = plt.Circle((point[0], point[1]), 5, color='red', picker=True)
            circles.append(circle)
            ax.add_patch(circle)

    selected_circle = None

    def on_pick(event):
        nonlocal selected_circle
        selected_circle = event.artist

    def on_motion(event):
        if selected_circle is not None:
            x, y = event.xdata, event.ydata
            selected_circle.center = (x, y)
            fig.canvas.draw()

    def on_release(event):
        nonlocal selected_circle
        if selected_circle is not None:
            x, y = selected_circle.center
            index = circles.index(selected_circle)
            keypoints[index] = [int(x), int(y)]
            selected_circle = None

    def save_keypoints():
        keypoints_path_new = keypoints_path.split(".")[0] + "_new." + keypoints_path.split(".")[1]
        with open(keypoints_path_new, 'w') as f:
            json.dump(keypoints, f)

    # Connect the event handlers
    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_release_event', on_release)

    plt.show()

    # Save the updated keypoints to the JSON file after closing the plot
    save_keypoints()

# Process each image and its corresponding keypoints
for file in os.listdir("IMG"):
    img_pth = os.path.join("IMG", file)
    data_pth = os.path.join("Keypoints", file.split(".")[0] + "." + file.split(".")[1] + ".json")
    
    img = cv2.imread(img_pth, 0)
    with open(data_pth, 'r') as f:
        keypoints = json.load(f)
    
    # Update keypoints interactively
    update_keypoints_interactively(img, keypoints, data_pth)

    # Draw updated keypoints on the image
    for point in keypoints:
        if point != [0, 0]:
            cv2.circle(img, tuple(point), 5, (255, 0, 0), -1)
    
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
