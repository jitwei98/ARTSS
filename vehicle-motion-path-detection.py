import cv2 as cv
import numpy as np

def region_of_interest(img, vertices):
	mask = np.zeros_like(img)
	#channel_count = img.shape[2]
	match_mask_color = 255
	cv.fillPoly(mask, vertices, match_mask_color)
	masked_image = cv.bitwise_and(img, mask)
	return masked_image

def mask_frame(gray_image):
	height = gray_image.shape[0]
	width = gray_image.shape[1]
	# For test_video_1.mp4
	# region_of_interest_vertices = [
	#     (0, height/2),
	#     (0, height),
	#     (width/2, height),
	#     (width/2, height/4),
	#     (width/4, height/4)
	# ]
	# For test_video_3.mp4
	region_of_interest_vertices = [
		(width/2, height/3),
		(0, height/3),
		(0, height),
		(width/2, height),
	]
	canny_image = cv.Canny(gray_image, 100, 120)
	frame = region_of_interest(gray_image, 
				np.array([region_of_interest_vertices], np.int32))

	# cv.imshow("processed frame", frame)
	return frame

def draw_road_line(roadImg, p1x, p1y, p2x, p2y):
	cv.line(img=roadImg, pt1=(int(p1x), int(p1y)), pt2=(int(p2x), int(p2y)), color=(0, 0, 255), thickness=1, lineType=8, shift=0)

# Parameters for Shi-Tomasi corner detection
# feature_params = dict(maxCorners = 1000, qualityLevel = 0.2, minDistance = 2, blockSize = 7)
feature_params = dict(maxCorners = 1000, qualityLevel = 0.2, minDistance = 50, blockSize = 7)
# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize = (15,15), maxLevel = 5, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
# The video feed is read in as a VideoCapture object
# cap = cv.VideoCapture("shibuya.mp4")
cap = cv.VideoCapture("test_video_4.mp4")
# Variable for color to draw optical flow track
color = (0, 255, 0)
# ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence
ret, first_frame = cap.read()
# Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
# Finds the strongest corners in the first frame by Shi-Tomasi method - we will track the optical flow for these corners
# https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
# Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
mask = np.zeros_like(first_frame)

counter = 0

height = first_frame.shape[0]
width = first_frame.shape[1]

"""
# first lane
#zoneA = [(0, height), (0 , 5*height/6 + 12),(width/2 - 80,height/3 + 30),(width/2 - 60,  height/3 + 30), (48, height)]
zoneAx = [0, width/2 - 80, width/2 - 60, 48]
zoneAy = [height, 5*height/6 + 12, height/3 + 30, height]
# second lane
#zoneB = [(48, height),(width/2 - 60,  height/3 + 30),(width/2 - 40,  height/3 + 30), (width/5 + 3, height)]
zoneBx = [48,width/2 - 60,width/2 - 40,width/5 + 3]
zoneBy = [height/3 + 30, height]
# third lane
# zoneC = [(width/5 + 3, height),(width/2 - 40,  height/3 + 30),( width/2 - 16,  height/3 + 30), (2*width/5 - 18, height)]
zoneCx = [width/5 + 3, width/2 - 40, width/2 - 16, 2*width/5 - 18]
zoneCy = [height,  height/3 + 30]
"""

while(cap.isOpened()):
	# ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
	ret, frame = cap.read()
	# Converts each frame to grayscale - we previously only converted the first frame to grayscale
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	draw_road_line(frame, 0, 5*height/6 + 12 , width/2 - 80,  height/3 + 30)
	draw_road_line(frame, 48, height, width/2 - 60,  height/3 + 30)
	draw_road_line(frame, width/5 + 3, height, width/2 - 40,  height/3 + 30)
	draw_road_line(frame, 2*width/5 - 18, height, width/2 - 16,  height/3 + 30)
	#draw_road_line(frame, width/2, 6*height/7 +10, width/2 -15,  2*height/7)
	#draw_road_line(frame, width/3 - 20, 6*height/7 +10, width/2 -26,  2*height/7)
	#draw_road_line(frame, width/8 - 8, 6*height/7 +10, width/2 -44,  2*height/7)
	#draw_road_line(frame, 0, 3*height/4 + 15, width/2 - 55,  2*height/7)
	#draw_road_line(frame, 0, 2*height/3 - 11, width/2 - 68,  2*height/7)

	if counter % 25 == 0:
		masked_prev_gray = mask_frame(prev_gray)
		prev = cv.goodFeaturesToTrack(masked_prev_gray, mask = None, **feature_params)
		# prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
	if counter % 50 == 0:
		mask = np.zeros_like(frame)
	counter += 1

	# Calculates sparse optical flow by Lucas-Kanade method
	# https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
	next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)
	# Selects good feature points for previous position
	good_old = prev[status == 1]
	# Selects good feature points for next position
	good_new = next[status == 1]
	# Draws the optical flow tracks

	for i, (new, old) in enumerate(zip(good_new, good_old)):
		# Returns a contiguous flattened array as (x, y) coordinates for new point
		a, b = new.ravel()
		# Returns a contiguous flattened array as (x, y) coordinates for old point
		c, d = old.ravel()		

		if b > 2*height/5:
			# Draws line between new and old position with green color and 2 thickness
			mask = cv.line(mask, (a, b), (c, d), color, 2)
			# Draws filled circle (thickness of -1) at new position with green color and radius of 3
			frame = cv.circle(frame, (a, b), 3, color, -1)

	# Overlays the optical flow tracks on the original frame
	output = cv.add(frame, mask)
	# Updates previous frame
	prev_gray = gray.copy()
	# Updates previous good feature points
	prev = good_new.reshape(-1, 1, 2)
	# Opens a new window and displays the output frame
	cv.imshow("BKE Camera 0614", output)
	# Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
	if cv.waitKey(10) & 0xFF == ord('q'):
		break
# The following frees up resources and closes all windows
cap.release()
cv.destroyAllWindows()