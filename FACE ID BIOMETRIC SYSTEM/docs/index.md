# FACE ID BIOMETRIC SYSTEM
*The application for generating a biometric vector based on the input face image. The system consists of registration, verification and identification module.*
### Table of contents

- [1. Overview](#1-overview) <!-- omit in toc -->
  - [1.1. About the project](#11-about-the-project)
   - [1.2. Biometrics key information](#12-biometrics-key-information)
  - [1.3. Face ID](#13-face-id)
  - [1.4. Developed system key features](#14-developed-system-key-features)
  - [1.5. Technologies-and-modules](#15-technologies-and-modules)
  - [1.6. Project summary information](#16-project-summary-information)
- [2. Application](#2-application)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Run the application](#22-run-the-application)
  - [2.3. Biometric vector faces repository](#23-biometric-vector-faces-repository)
  - [2.4. System evaluation](#24-system-evaluation)
- [3. Documentation](#3-documentation)

### 1. Overview
#### 1.1. About the project

<p>This project is an application that implements artifcial intelligence to perform registration, verification and identification based on the generated biometric vector built according to the input face image.</p>

<p>Using biometric technologies to measure and analyse the unique peron's characteristics. In this project a biometric based on physical characteristics is used (physiological biometrics). This type of biometric is generally used for identification as well as verification purposes.</p>

#### 1.2. Biometrics key information

* biometric, biometric characteristic, biometric modality - measurable biological or behavioral feature, which measurement delivers information that enables to distinguish certain individuals, e.g. iris, fingerprint, gait.
* biometric instance - the specific representation of defined biometric characteristic, e.g. left hand index fingerprint, iris left eye.
* biometrics - automatic recognition of individuals on the basis of their physiological or behavioral characteristics.
* biometric sample - the result of a specific measurement of certain individual biometric instance, obtained with the use of biometric scaner.
* biometric template - the reference biometric sample stored in the system for the purpose of identifying the owner of the certain pattern.
* comparison sample - the sample obtained from the individual subjected to automatic recognition with the use of biometry.
* biometric system - system which uses biometry.
* unimodal biometric system - system which uses only one biometric/biometric characteristic/biometric modality
* match result - numerical rating the similarities of two biometric samples of the same type.
* biometric matching - operation of the matching using a certain algorithm and biometric instance resulting in a numerical result.
* accept threshold - sample comparison threshold, above which samples are found to be compliant.
* reject threshold - sample comparison threshold, below which samples are found to be non-compliant.
* biometric session - the period of user interaction with the system during which a specific number of biometric samples are entered into the system.
<br>

* verification - comparison 1:1: - the check if a sample of the biometric charateritics is similar (for the established threshold) as the individual's pattern stored in database.

* identification - comparison 1:N - taking a sample of anonymous person biometric features and searching the database to find a pattern matching that is similar to the obtained sample, in this way determining the identifity of the person can be accomplished.

More formal definitions and information related to biometry can be found in ISO/IEC JTC1 documents.


Parameters for the ideal biometric modality:

* versality
* unambiguity
* permanence
* stability
* collectability
* accuracy
* speed
* resources
* acceptability
* fraud resistance

Face as a biometric modality is rated accordingly:

| | |
| --- | --- |
| versality | high |
| unambiguity | low |
| permanance | medium |
| stability | medium |
| accuracy | low |
| acceptability | high |
| fraud resistance | low |

> Jain, A.K., A. Ross, and S. Prabhakar. An introduction to
biometric recognition. Biometrics 14, 2004, 14, pp. 4-20 * 
In summary, the face biometric is easy to obtain as it is generally accepted. However, it is hard to clearly establish the identity based on this feature. The accuracy of this biometric is generally not high and it is easy to fraud the system which is solely based on the face image biometric.

#### 1.3. Face ID

The technology of face measurements is based on the detection and establishment of the key points (local features) on the face. The distance between the detected key points is measured and appropriate ratios are formulated. The ratios are the constituents of the output biometric vector.
In this system biometric vector has the following components:

W = [x1/x2, x1/x3, x2/x3, x1/x4, x1/x5, x1/x6, x2/x7]

 - x1 - the distance between outer corners of eyes
 - x2 - nose width
 - x3 - the distance between the mouth line and the nose line
 - x4 - face width
 - x5 - the distance between the eye line and the nose line
 - x6 - the distance between the eye line and the mouth line
 - x7 - the distance between the eye line and the end of the face

 The main issues that with face identification:
 - distance from the camera
 - varied lighting, outdoor/indoor, light effects, illuminance effects, shadows
 - camera positioning
 - pose
 - changes in the outer appearance
 - visibility - some part of faces can be occluded by e.g. glasses
 - face expression
 - individual factors

The vector matching is performed based on <b>cosine similarity metric</b>.
It is expected that a face of the same person should be more similar than the face of different persons.


#### 1.4. Developed system key features

|  | |
| :--- | --- |
| Image preprocessing | performing complex system preprocessing, including face alignment, face cropping, input image normalization, sharpness and contrast enhancement |
| Detection based on MTCNN model | face and key points detection |
| DeepFace analysis | face emotion analysis for neutral expression verification using "VGG-Face" model|
| Registration | adding new user and the associated biometric vector to the system |
| Verification | checking whether the subject is who it claims to be |
| Identification | checking who the subject of identification is |

During registration, verification and identification feature extraction is perfomed.

* Registration - the acquired sample is saved as a reference and registration is successful, provided that the pattern meets the quality requirements.
* Verification - the system compares the sample with the saved concrete user pattern and decides if the identity is correct.
* Identification - the system perform comparison with all users pattern, this results in a list of potential sample owners, which makes it possible to determine who the subject of identification is.

#### 1.5. Technologies and modules

Python version: 3.8.6 

|  |  |
| --- | --- |
| Python | Server-side role for processing the application data. |
| Flask | Web microframework - handling routes, requests and responses. |
| Jinja2 | Template engine for dynamic content loading. |
| HTML5 | Client-side role for web pages construction. |
| CSS, Bootstrap | Styling and designing repsonsive web pages. |

|  |  |
| --- | --- |
| MTCNN | Allows to perform MTCNN Detection -> a) Detection of faces (with the confidence probability) b) Detection of keypoints (left eye, right eye, nose, mouth_left, mouth_right) |
| MediaPipe | MediaPipe Solutions Python API. |
| DeepFace | Performs DeepFace emotion recognition analysis. |
| Matplotlib.pyplot | Reading images. |
| OpenCV | Operations on images, e.g. normalization. |
| Scipy | Distance computations, e.g. euclidean distance. |
| Numpy | Fast mathematical operations on images represanted as an array. |
| Pillow | Operations on images. |

#### 1.6. Project summary information

##### Main Languages
| LANGUAGE | FILES | CODE LINES | COMMENT LINES | BLANK LINES | TOTAL LINES |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Python, Flask | 5 | 364 | 176 | 151 | 691 |
| HTML5, Jinja2, Bootstrap  | 5 | 273 | 0 | 4 | 277 |
| CSS | 1 | 39 | 0 | 7 | 46 |

##### Directories
|  | FILES | CODE LINES | COMMENT LINES | BLANK LINES | TOTAL LINES |
| :--- | ---: | ---: | ---: | ---: | ---: |
| website | 11 | 676 | 176 | 162 | 1,014 |
| static | 1 | 39 | 0 | 7 | 46 |
| static\css | 1 | 39 | 0 | 7 | 46 |
| templates | 5 | 273 | 0 | 4 | 277 |

### 2. Application
#### 2.1. Requirements

All the requirements are included in this project in the following files: requirements.txt, Pipfile, Pipfile.lock.

#### 2.2. Run the application

In the main project directory, in the command line, run the following commands:

`pipenv shell`<br>

`flask run`

Navigate to the http://127.0.0.1:5000 in the browser.

Recommended browsers: Opera, Chrome.

Alternatively, the application can be run from the FACE ID BIOMETRIC/app.py file.

#### 2.3. Biometric vector faces repository

This system used the following faces dataset:

* The IMM Frontal Face Database (http://www2.imm.dtu.dk/pubdb/pubs/3943-full.html) 
* Utrecht ECVP (pics.psych.stir.ac.uk)

The dataset have been manual divided into separate registration and validation repositories due to enabling the accuracy score measurements.

This system so far has gathered 81 records.

#### 2.3. System evaluation

The system can be evaluated according to the following accuracy measurements:

* FRR, FNMR (False Reject Rate, False Non-Match Rate) - measures the rate at which true samples are rejected - estimated as false
* FAR, FMR (False Accept Rate, False Match Rate) - measures the rate at which the false samples are accepted - estimated as true
* FTC (Failure To Capture) - measures how often the process of obtaining the sample, with required for processing quality, is unsuccessful
* FTE (Failure To Enroll) - measures how often the registration process of a new user is unsuccessful
* HTER (Half Total Error Rate) - the total error measurement which takes into account the security and user comfort

Calculations:

* FAR = Total False Acceptence / Total False Attempts
* FRR = Total False Rejections / Total True Attempts
* Equal Error Rate can be obtained where FAR = FRR
* Ability to verify: ATV = 1-(1-FTE)(1-FRR)


### 3. Documentation

In order to get access to the prepared project documentation where all the functions included in this project are properly explained,
navigate to the project's root directory (\FACE ID BIOMETRIC SYSTEM) and in the command line run:

`pipenv shell`

`pipenv run mkdocs serve`

Navigate to the http://127.0.0.1:8000 in the browser.
