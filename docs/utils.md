#


### perform_complex_preprocessing
```python
.perform_complex_preprocessing(
   img_path
)
```

---
Performs complex preprocessing.


**Args**

* **img_path** (str) : The path to the file that is to be preprocessed.


----


### align_face
```python
.align_face(
   img, img_path, left_eye, right_eye
)
```

---
Aligns the face detected in the image based on left and right eye coordinates.



**Args**

* **img** (Image) : The image to be aligned
* **img_path** (str) : The path for saving the aligned face image.
* **left_eye** (tuple) : The left eye coordinates
* **right_eye** (tuple) : The right eye coordinates.


**Returns**

Results in aligned image.

----


### enhance_image_contrast
```python
.enhance_image_contrast(
   img, img_path, factor
)
```

---
Enhances image contrast according to the factor value specified.


**Args**

* **img** (Image) : The image to be enhanced.
* **img_path** (str) : The path for saving the image.
* **factor** (float) : The enhancement contrast factor value.


----


### enhance_image_sharpness
```python
.enhance_image_sharpness(
   img, img_path, factor
)
```

---
Enhances image sharpness according to the factor value specified.


**Args**

* **img** (Image) : The image to be enhanced.
* **img_path** (str) : A path for saving the image
* **factor** (float) : The enhancement factor value.


----


### resize_img
```python
.resize_img(
   img, img_path, basewidth
)
```

---
Resizes and saves image.


**Args**

* **img** (Image) : The image to be resized.
* **img_path** (str) : The path for saving the image.
* **basewidth** (int) : The specified base width of resized image.


**Returns**

* **tuple**  : The tuple (basewidth, hsize) describing the final shape of the resized image.


----


### prepare_img
```python
.prepare_img(
   img_path
)
```

---
Prepares the image by extracting the face.


**Args**

* **img_path** (str) : The path to the image to be prepared.


**Returns**

The cropped image that includes the face only + required padding.

----


### get_key_points
```python
.get_key_points(
   path
)
```

---
Gets the key points for image preprocessing - face alignment.


**Args**

* **path** (str) : The path to the image.


**Returns**

* **tuple**  : The left eye and right eye keypoints.


----


### check_biometric_vector
```python
.check_biometric_vector(
   biometric_vector
)
```

---
Checks the biometric vector against the exisitng reference vector in the database.


**Args**

* **biometric_vector** (list) : The biometric vector to be verified.


**Returns**

* **list**  : The list of matched biometric vectors.


----


### is_match
```python
.is_match(
   known_vector, candidate_vector, threshold
)
```

---
Checks if specified vectors match.


**Args**

* **known_vector** (list) : The known biometric vector.
* **candidate_vector** (list) : The candidate biometric vector.
* **threshold** (float) : The threshold value for comparison.


**Returns**

* **bool**  : True if the cosine metric value is within a given threshold value, false otherwise.


----


### get_biometrics_vector
```python
.get_biometrics_vector(
   file_path
)
```

---
Constructs the biometric vector.


**Args**

* **file_path** (str) : The path to the image from which biometric vector is to be constructed.


**Returns**

* **biometric_vector** (list) : Biometric vector compontents stored in a list


----


### generate_face_mesh
```python
.generate_face_mesh(
   results, img, file_path
)
```

---
Generates face mesh on the image.


----


### allowed_file
```python
.allowed_file(
   filename
)
```

---
Check if the file has allowed extension.


**Args**

* **filename** (str) : The name of the file.


**Returns**

* **bool**  : True if the file is supported, false otherwise.


----


### check_valid_emotion
```python
.check_valid_emotion(
   img_path
)
```

---
Checks if the face on the photo exibits a neutral expression.


**Args**

* **img_path** (str) : The path to the image.


**Returns**

* **bool**  : True if the detected emotion is valid, false otherwise.


----


### detect_faces
```python
.detect_faces(
   path
)
```

---
Detects faces from passed image.


**Args**

* **path** (str) : The path to the saved image.


**Returns**

* **list**  : The list of faces detected using MTCNN model.


----


### deepface_analyze
```python
.deepface_analyze(
   img_path
)
```

---
Performs DeepFace emotion recognition analysis.


**Args**

* **img_path** (str) : The path to the image.

