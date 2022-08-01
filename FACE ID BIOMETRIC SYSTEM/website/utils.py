from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt 

from PIL import Image, ImageEnhance
from flask import flash

import matplotlib.pyplot as plt
import cv2

import math

from mtcnn.mtcnn import MTCNN
import mediapipe as mp
import numpy as np
from scipy.spatial import distance

from scipy.spatial.distance import cosine

from website.models import Person

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# Face mesh landmarks constants
FACE_LEFT = 234
FACE_RIGHT = 454
FACE_UP = 10
FACE_DOWN = 152

EYE_LEFT_LEFT = 33
EYE_LEFT_RIGHT = 133
EYE_RIGHT_LEFT = 362
EYE_RIGHT_RIGHT = 263

NOSE_LEFT = 192
NOSE_RIGHT = 456

MOUTH_LEFT = 57
MOUTH_RIGHT = 287
MOUTH_MIDDLE = 14

EYE_LINE = 6
NOSE_LINE = 1
MOUTH_LINE = 13

MATCH_THRESHOLD = 0.005



### START PREPROCESSING

def perform_complex_preprocessing(img_path):
	"""Performs complex preprocessing.

	Args:
		img_path (str): The path to the file that is to be preprocessed.
	"""
	img = prepare_img(img_path)
	try:
		left_eye, right_eye = get_key_points(img_path)
		img = align_face(img, img_path, left_eye, right_eye)
	except:
		flash('Invalid photo. Please upload a photo that meets the requirements.', 'danger')

	img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

	img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)

	img = Image.fromarray(img)
	img.save(img_path)


def align_face(img, img_path, left_eye, right_eye,):
	"""Aligns the face detected in the image based on left and right eye coordinates.


	Args:
		img (Image): The image to be aligned
		img_path (str): The path for saving the aligned face image.
		left_eye (tuple): The left eye coordinates
		right_eye (tuple): The right eye coordinates.

	Returns:
		Results in aligned image.
	"""
	left_eye_x, left_eye_y = left_eye
	right_eye_x, right_eye_y = right_eye
	
	# find rotation direction
	
	if left_eye_y > right_eye_y:
		point_3rd = (right_eye_x, left_eye_y)
		direction = -1 # rotate same direction to clock
	else:
		point_3rd = (left_eye_x, right_eye_y)
		direction = 1 # rotate inverse direction of clock
	
	# find length of triangle edges
	
	a = distance.euclidean(np.array(left_eye), np.array(point_3rd))
	b = distance.euclidean(np.array(right_eye), np.array(point_3rd))
	c = distance.euclidean(np.array(right_eye), np.array(left_eye))
	
	if b != 0 and c != 0: 
	
		cos_a = (b * b + c * c - a * a)/(2 * b * c)
		angle = np.arccos(cos_a) # angle in radian
		angle = (angle * 180) / math.pi # radian to degree
	
		# rotate base image
		if direction == -1:
			angle = 90 - angle
	
		img = Image.fromarray(img)
		img = img.rotate(direction * angle)

		img.save(img_path)
		return img

def enhance_image_contrast(img, img_path, factor):
	"""Enhances image contrast according to the factor value specified.

	Args:
		img (Image): The image to be enhanced.
		img_path (str): The path for saving the image.
		factor (float): The enhancement contrast factor value.
	"""
	enhancer = ImageEnhance.Contrast(img)
	img = enhancer.enhance(factor)
	img.save(img_path)

def enhance_image_sharpness(img, img_path, factor):
	"""Enhances image sharpness according to the factor value specified.

	Args:
		img (Image): The image to be enhanced.
		img_path (str): A path for saving the image
		factor (float): The enhancement factor value.
	"""
	enhancer = ImageEnhance.Sharpness(img)
	img = enhancer.enhance(factor)
	img.save(img_path)

def resize_img(img, img_path, basewidth):
	"""Resizes and saves image.

	Args:
		img (Image): The image to be resized.
		img_path (str): The path for saving the image.
		basewidth (int): The specified base width of resized image.

	Returns:
		tuple: The tuple (basewidth, hsize) describing the final shape of the resized image.

	"""
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)

	img.save(img_path)

	return (basewidth, hsize)

def prepare_img(img_path):
	"""Prepares the image by extracting the face.

	Args:
		img_path (str): The path to the image to be prepared.

	Returns:
		The cropped image that includes the face only + required padding.
	"""
	try:
		img = cv2.imread(img_path)
		data=detect_faces(img)
		biggest = 0
		if data != []:
			for faces in data:
				box = faces['box']            
				area = box[3]  * box[2]
				if area > biggest:
					biggest = area
					bbox=  box 
			bbox[0]= 0 if bbox[0]<0 else bbox[0]
			bbox[1]= 0 if bbox[1]<0 else bbox[1]
			img=img[bbox[1]: bbox[1]+bbox[3],bbox[0]: bbox[0]+ bbox[2]]   
		cv2.imwrite(img_path, img)
		return img
	except:
		return cv2.imread(img_path)

def get_key_points(path):
	"""Gets the key points for image preprocessing - face alignment.

	Args:
		path (str): The path to the image.

	Returns:
		tuple: The left eye and right eye keypoints.
	"""
	image = plt.imread(path)
	detector = MTCNN()
	faces = detector.detect_faces(image)
	if len(faces) == 0 or len(faces) > 1:
		raise Exception('Invalid photo')
	else:
		face = faces[0]
		score = face["confidence"]
		if score > 0.90:
			keypoints = face["keypoints"]
			left_eye = keypoints["left_eye"]
			right_eye = keypoints["right_eye"]
			return (left_eye, right_eye)

### END PREPROCESSING


### START BIOMETRIC VECTOR VERIFICATION
def check_biometric_vector(biometric_vector):
	"""Checks the biometric vector against the exisitng reference vector in the database.

	Args:
		biometric_vector (list): The biometric vector to be verified.

	Returns:
		list: The list of matched biometric vectors.
	"""
	match_list = []
	person_list = Person.query.all()

	for person in person_list:
		candidate_vector = [person.w1, person.w2, person.w3, person.w4, person.w5, person.w6, person.w7]
		if is_match(biometric_vector, candidate_vector, threshold=MATCH_THRESHOLD):
			print("Could be", person.nickname)
			match_list.append(person.nickname)
	return match_list

def is_match(known_vector, candidate_vector, threshold):
	"""Checks if specified vectors match.

	Args:
		known_vector (list): The known biometric vector.
		candidate_vector (list): The candidate biometric vector.
		threshold (float): The threshold value for comparison.

	Returns:
		bool: True if the cosine metric value is within a given threshold value, false otherwise.
	"""
	score = cosine(known_vector, candidate_vector)
	if score <= threshold:
		print(known_vector, candidate_vector)
		print('face is a match (%.5f <= %.5f)' % (score, threshold))
		return True
	else:
		print('face is NOT a match (%.5f > %.5f)' % (score, threshold))
		return False

### END BIOMETRIC VECTOR VERIFICATION


### START BIOMETRIC VECTOR AND FACE MESH GENERATION

def get_biometrics_vector(file_path):
	"""Constructs the biometric vector.

	Args:
		file_path (str): The path to the image from which biometric vector is to be constructed.

	Returns:
		biometric_vector (list): Biometric vector compontents stored in a list
	"""
	with mp_face_mesh.FaceMesh(
		static_image_mode=True,
		max_num_faces=1,
		refine_landmarks=True,
		min_detection_confidence=0.5) as face_mesh:
		
		image = cv2.imread(file_path)

		# Convert the BGR image to RGB before processing.
		results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

		# Get landmark for one face
		landmarks = results.multi_face_landmarks[0].landmark

		biometric_vector = [-1, -1, -1, -1, -1, -1, -1]

		x1 = landmarks[EYE_RIGHT_LEFT].x - landmarks[EYE_LEFT_RIGHT].x
		x2 = landmarks[NOSE_RIGHT].x - landmarks[NOSE_LEFT].x
		x3 = landmarks[MOUTH_MIDDLE].y - landmarks[NOSE_LINE].y
		x4 = landmarks[FACE_RIGHT].x - landmarks[FACE_LEFT].x
		x5 = landmarks[NOSE_LINE].y - landmarks[EYE_LINE].y
		x6 = landmarks[MOUTH_LINE].y - landmarks[EYE_LINE].y
		x7 = landmarks[FACE_DOWN].y - landmarks[EYE_LINE].y

		biometric_vector[0] = x1/x2
		biometric_vector[1] = x1/x3
		biometric_vector[2] = x2/x3
		biometric_vector[3] = x1/x4
		biometric_vector[4] = x1/x5
		biometric_vector[5] = x1/x6
		biometric_vector[6] = x2/x7

		generate_face_mesh(results, image, file_path)

		return biometric_vector

def generate_face_mesh(results, img, file_path):
	"""Generates face mesh on the image.
	"""
	annotated_image = img.copy()
	for face_landmarks in results.multi_face_landmarks:
		mp_drawing.draw_landmarks(
			image=annotated_image,
			landmark_list=face_landmarks,
			connections=mp_face_mesh.FACEMESH_TESSELATION,
			landmark_drawing_spec=None,
			connection_drawing_spec=mp_drawing_styles
			.get_default_face_mesh_tesselation_style())
		mp_drawing.draw_landmarks(
			image=annotated_image,
			landmark_list=face_landmarks,
			connections=mp_face_mesh.FACEMESH_CONTOURS,
			landmark_drawing_spec=None,
			connection_drawing_spec=mp_drawing_styles
			.get_default_face_mesh_contours_style())
		mp_drawing.draw_landmarks(
			image=annotated_image,
			landmark_list=face_landmarks,
			connections=mp_face_mesh.FACEMESH_IRISES,
			landmark_drawing_spec=None,
			connection_drawing_spec=mp_drawing_styles
			.get_default_face_mesh_iris_connections_style())
	cv2.imwrite(file_path + '_annotated_image' + '.png', annotated_image)

### END BIOMETRIC VECTOR AND FACE MESH GENERATION


### CHECK IMAGE FILE VALIDITY

def allowed_file(filename):
	"""Check if the file has allowed extension.

	Args:
		filename (str): The name of the file.

	Returns:
		bool: True if the file is supported, false otherwise.
	"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_one_face(img_path):
	"""Checks if only one face is visible on the uploaded photo.

	Args:
		img_path (str): The path to the image uploaded that is to be checked.

	Returns:
		bool: True if the image contains only one face, False otherwise
	"""
	faces = detect_faces(img_path)
	if len(faces) > 1 or len(faces) == 0:
		flash("Invalid photo uploaded. Please upload image with one face only.", 'danger')
		return False
	return True

def check_valid_emotion(img_path):
	"""Checks if the face on the photo exibits a neutral expression.

	Args:
		img_path (str): The path to the image.

	Returns:
		bool: True if the detected emotion is valid, false otherwise.
	"""
	obj = deepface_analyze(img_path)
	emotion = obj["dominant_emotion"]
	gender = obj["gender"]
	print('[EMOTION]', emotion, obj)
	if emotion == 'happy' or emotion == 'angry':
		message = "Invalid photo uploaded. This " + gender + " seems to be " + emotion + ". Please upload image with natural face expression."
		flash(message, 'danger')
		return False
	return True

def detect_faces(path):
	"""Detects faces from passed image.

	Args:
		path (str): The path to the saved image.

	Returns:
		list: The list of faces detected using MTCNN model.
	"""
	image = plt.imread(path)
	detector = MTCNN()
	faces = detector.detect_faces(image)
	return faces

### END CHECK IMAGE FILE VALIDITY


#### DEEPFACE ANALYSIS

def deepface_analyze(img_path):
	"""Performs DeepFace emotion recognition analysis.

	Args:
		img_path (str): The path to the image.
	"""
	model_name = "VGG-Face"
	model = DeepFace.build_model(model_name) 

	obj = DeepFace.analyze(img_path)
	return(obj)